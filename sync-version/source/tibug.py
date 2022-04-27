from jira import JIRA


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
            issue.update(fields={"versions": failed_version})
        except Exception as err:
            print("update {} affect version fail {}".format(case_name, err))
        else:
            print("update {} affect version success".format(case_name))
            update_count = update_count + 1

        try:
            issue.update(fields={Config.fix_version_field: fix_version})
        except Exception as err:
            print("update {} fix version fail {}".format(case_name, err))
        else:
            print("update {} fix version success".format(case_name))
            update_count = update_count + 1

        return update_count == 2

    def github_issues(self, case_name):
        """
        :param case_name: the unique identification in jira
        :return: the value of github issue's filed
        """
        issue = self.tibug_jira.issue(case_name)
        # customfield_12825 is github issue field
        return issue.fields.customfield_12825

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
