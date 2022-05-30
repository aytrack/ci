from jira import JIRA
import datetime


class TiBug(object):
    def __init__(self, user, pwd):
        self.tibug_jira = JIRA("https://internal.pingcap.net/jira/", basic_auth=(user, pwd))

    def update_tibug_values(self, case_name, failed_version, fix_version):
        """
        update tibug affect version fields and fix version fields
        :param case_name: the unique identification in jira
        :param failed_version: a string slice containing version info
        :param fix_version: a string slice containing version info
        :return: true or false
        """
        print("case_name: {}, affect_version: {}, fix_version: {}".format(case_name, failed_version, fix_version))
        issue = self.tibug_jira.issue(case_name)
        update_count = 0
        try:
            fv = []
            for item in failed_version:
                fv.append({"name": item})
            issue.update(fields={"versions": fv})
        except Exception as err:
            print("update {} affect version fail {}".format(case_name, err))
        else:
            print("update {} affect version success".format(case_name))
            update_count = update_count + 1

        try:
            fv = []
            for item in fix_version:
                fv.append({"name": item})
            issue.update(fields={"fixVersions": fv})
        except Exception as err:
            print("update {} fix version fail {}".format(case_name, err))
        else:
            print("update {} fix version success".format(case_name))
            update_count = update_count + 1

        return update_count == 2

    def get(self, case_name):
        """
        :param case_name: the unique identification in jira
        :return: the value of github issue's filed
        """
        data = {}
        issue = self.tibug_jira.issue(case_name)
        # customfield_12825 is github issue field
        data["github_issues"] = issue.fields.customfield_12825
        # customfield_12208 is TEST_CASE_ID
        data["test_case_id"] = issue.fields.customfield_12208
        # customfield_12210 is issue link
        data["issue_link"] = issue.fields.customfield_12210
        data["priority"] = issue.fields.priority.name
        return data

    def update_test_case_id(self, case_name, test_case_id):
        issue = self.tibug_jira.issue(case_name)
        issue.update(fields={"customfield_12208": test_case_id})

    def update_priority(self, case_name, prt):
        issue = self.tibug_jira.issue(case_name)
        issue.update(fields={"priority": {"name": prt}})

    def list(self, days):
        t = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        issues = self.tibug_jira.search_issues('project = TIBUG AND issuetype = "Issue analysis" AND "Issue module" = TiDB AND status = "New Request" AND assignee = "wanghuichang@pingcap.com" AND created >= "{}" ORDER BY created DESC'.
                                               format(t.strftime("%Y-%m-%d %H:%M")))
        names = []
        for item in issues:
            names.append(item.key)
        return names

    @staticmethod
    def github_issues_is_valid(v):
        if v is None:
            return False

        v = v.lstrip()
        v = v.rstrip()
        if v == "empty":
            return True
        if v.startswith("https://github.com/pingcap/tidb/issues/"):
            return True
        return False

    @staticmethod
    def link(case_name):
        return "https://internal.pingcap.net/jira/browse/" + case_name

    def fix_version(self, case_name):
        issue = self.tibug_jira.issue(case_name)
        ls = []
        if issue.fields.fixVersions is None:
            return ls
        for item in issue.fields.fixVersions:
            ls.append(item.name)
        return ls

    def affect_version(self, case_name):
        issue = self.tibug_jira.issue(case_name)
        ls = []
        if issue.fields.versions is None:
            return ls
        for item in issue.fields.versions:
            ls.append(item.name)
        return ls
