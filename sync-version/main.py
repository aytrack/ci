from config import Config
from source.tibug import TiBug
from util.version import Version
from source.tcms import Tcms
from source.github import Github
from case import Case
from message.lark import Lark
import click
import yaml


g_trigger_id = ""
g_trigger_type = ""


@click.group()
def main():
    pass


@main.group("sync", help="sync tcms results")
@click.option("--trigger-id", help="tcms trigger id")
@click.option("--trigger-type", help="branch or version")
def sync(**params):
    global g_trigger_id
    global g_trigger_type
    g_trigger_id = params.get("trigger_id")
    g_trigger_type = params.get("trigger_type")


def sort(versions):
    # sort versions slice
    for i in range(len(versions)):
        for j in range(i + 1, len(versions)):
            v = Version(versions[i]["version"])
            if not v.less(Version(versions[j]["version"])):
                versions[i], versions[j] = versions[j], versions[i]


def sync_branch_cases(trigger_id):
    tidb_github = Github(Config.github_token, "pingcap", "tidb")
    tibug = TiBug(Config.user, Config.pwd)

    cases = []
    for item in Tcms().case_versions(trigger_id):
        case_name = item["name"]
        case_versions = item["versions"]
        print(case_name)
        if not case_name.startswith("TIBUG-") and not case_name.startswith("GH-TIDB-"):
            print("{} don't support affect-branch".format(case_name))
            continue

        affect_labels = []
        for k in case_versions:
            # filter invalid version
            if k["version"] == "main":
                continue
            if k["status"].lower() == "failure":
                v = Version(k["version"])
                b = v.branch()
                affect_labels.append("affects-{}".format(b))

        c = Case()
        c.case_name = case_name
        if case_name.startswith("TIBUG-"):
            c.tibug_link = tibug.link(case_name)
            link = tibug.github_issues(case_name)
            c.issue_link = link
            if not tibug.github_issues_is_valid(link) or link == "empty":
                cases.append(c)
                continue

            issue_number = link.split("/")[-1]
        else:
            # case_name.startswith("GH-TIDB-")
            issue_number = case_name[len("GH-TIDB-"):]

        exist_labels = tidb_github.affect_labels(issue_number)
        add_labels = []
        for label in affect_labels:
            if label in exist_labels:
                continue
            add_labels.append(label)

        c.exist_labels = exist_labels
        c.add_labels = add_labels
        c.issue_link = tidb_github.link(issue_number)
        c.add_labels.sort()
        c.exist_labels.sort()
        cases.append(c)

    return cases


@sync.command("github", help="sync tcms results to github")
def sync_to_github(**params):
    tidb_github = Github(Config.github_token, "pingcap", "tidb")

    cases = sync_branch_cases(g_trigger_id)
    message = []
    for c in cases:
        if len(c.add_labels) == 0:
            continue

        if c.issue_number():
            # add labels to tidb issue
            tidb_github.add_labels(c.issue_number(), c.add_labels)
            message.append(c.affect_branch_rich_message("done"))

    if len(message) == 0:
        return

    Lark.send("issue affect branch", message)


@sync.command("tibug", help="sync tcms results to tibug")
def sync_to_tibug(**params):
    cases = sync_version_cases(g_trigger_id)
    message = []
    tibug = TiBug(Config.user, Config.pwd)
    for c in cases:
        if len(c.tibug_add_affects_labels()) == 0 and len(c.tibug_delete_affects_labels()) == 0 and \
                len(c.tibug_add_fix_labels()) == 0 and len(c.tibug_delete_fix_labels()) == 0:
            continue

        if tibug.update_tibug_values(c.case_name, c.new_affects_labels, c.new_fix_versions):
            message.append(c.affect_version_message("done"))
        else:
            message.append(c.affect_version_message("done") + ", update failed")

    if len(message) == 0:
        return

    Lark.send("tibug affect version", message)


def sync_version_cases(trigger_id):
    tibug = TiBug(Config.user, Config.pwd)
    cases = []
    for item in Tcms().case_versions(trigger_id):
        case_name = item["name"]
        if not case_name.startswith("TIBUG-"):
            print("{} don't support affect-version".format(case_name))
            continue

        case_versions = item["versions"]
        new_version = []
        for k in case_versions:
            # filter invalid version
            if k["version"] == "main":
                continue
            new_version.append(k)
        sort(new_version)

        fix_version = []
        failed_version = []
        i = -1
        pre_failed_version = None
        for k in new_version:
            cv = Version(k["version"])

            i = i + 1
            if i > 0:
                lv = Version(new_version[i - 1]["version"])
                if cv.is_branch_adjacent(lv) and pre_failed_version is not None:
                    pv = Version(pre_failed_version)
                    if lv.is_branch_adjacent(pv):
                        # the failed version behind the current two version, reset pre_failed_version
                        pre_failed_version = None

            # all failed case's version is affect-version
            if k["status"].lower() == "failure":
                pre_failed_version = k["version"]
                failed_version.append({"name": k["version"]})
                continue

            if k["status"].lower() == "success":
                if pre_failed_version is None:
                    continue
                # case passed in the version and case failed in previous branch
                if cv.is_adjacent(Version(pre_failed_version)):
                    fix_version.append({"name": k["version"]})
                    continue

                # case passed in new branch and case failed in previous branch
                if cv.is_branch():
                    fix_version.append({"name": k["version"]})
                    continue
        c = Case()
        c.case_name = case_name
        c.tibug_link = tibug.link(case_name)
        c.exist_fix_versions = tibug.fix_version(case_name)
        c.exist_affects_labels = tibug.affect_version(case_name)
        c.new_fix_versions = fix_version
        c.new_affects_labels = failed_version
        cases.append(c)

    return cases


@sync.command("pr", help="add comment to pr")
@click.option("--pr-id", help="utf pr id")
def pr_comment(**params):
    pr_id = params.get("pr_id")

    utf_github = Github(Config.github_token, "pingcap", "automated-tests")
    if g_trigger_type == "branch":
        cases = sync_branch_cases(g_trigger_id)

        message = []
        for c in cases:
            message.append(c.affect_branch_message("todo"))
        if len(message) == 0:
            return
        utf_github.add_comment(pr_id, "\n".join(message))
        return

    # g_trigger_type == "version"
    cases = sync_version_cases(g_trigger_id)
    message = []
    for c in cases:
        message.append(c.affect_version_message("todo"))
    if len(message) == 0:
        return
    utf_github.add_comment(pr_id, "\n".join(message))
    return


@sync.command("lark", help="sync tcms results to pr and add comment")
def lark_message(**params):
    if g_trigger_type == "branch":
        cases = sync_branch_cases(g_trigger_id)

        message = []
        for c in cases:
            if len(c.add_labels) == 0:
                continue
            message.append(c.affect_branch_rich_message("todo"))
        if len(message) == 0:
            return
        Lark.send("issue affect branch", message)
        return

    # g_tigger_type == "version"
    cases = sync_version_cases(g_trigger_id)
    message = []
    for c in cases:
        if len(c.tibug_add_affects_labels()) == 0 and len(c.tibug_delete_affects_labels()) == 0 and \
                len(c.tibug_add_fix_labels()) == 0 and len(c.tibug_delete_fix_labels()) == 0:
            continue
        message.append(c.affect_version_message("todo"))

    if len(message) == 0:
        return
    Lark.send("tibug affect version", message)


@main.group("check", help="check fields")
def check(**params):
    pass


@check.command("tibug", help="check tibug in yaml")
@click.option("--yaml-file", help="yaml file")
def tibug(**params):
    f = open(params.get("yaml_file"))
    data = yaml.safe_load(f)
    f.close()

    case_names = []
    for item in data.get("pipeline", []):
        case_names.append(item["caseName"])
    for item in data.get("steps", []):
        case_names.append(item["caseName"])

    tibug = TiBug(Config.user, Config.pwd)
    messages = []
    for name in case_names:
        if not name.startswith("TIBUG-"):
            print("{} is not a TIBUG".format(name))
            continue
        link = tibug.github_issues(name)
        if tibug.github_issues_is_valid(link):
            print("{} github issue is valid".format(name))
            continue
        messages.append("[%s](%s)".format(name, TiBug.link(name)))

    if len(messages) == 0:
        print("all tibug check passed")
        exit(0)

    Lark.send("github issue field is invalid", messages)


if __name__ == '__main__':
    main()








