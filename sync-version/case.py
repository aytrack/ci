from source.tibug import TiBug


class Case(object):
    def __int__(self, case_name=None, tibug_link=None, issue_link=None, exist_labels=None, add_labels=None):
        if exist_labels is None:
            exist_labels = []
        if add_labels is None:
            add_labels = []

        self.case_name = None
        self.tibug_link = None

        # issue affect version
        self.issue_link = None
        self.exist_labels = exist_labels
        self.add_labels = add_labels

        # tibug affect version
        self.exist_affects_labels = []
        self.new_affects_labels = []
        self.exist_fix_versions = []
        self.new_fix_versions = []

    def issue_number(self):
        if self.issue_link is None:
            return self.issue_link

        return self.issue_link.split("/")[-1]

    def tibug_add_affects_labels(self):
        ls = []
        for item in self.new_affects_labels:
            if item not in self.exist_affects_labels:
                ls.append(item)
        ls.sort()
        return ls

    def tibug_delete_affects_labels(self):
        ls = []
        for item in self.exist_affects_labels:
            if item not in self.new_affects_labels:
                ls.append(item)
        ls.sort()
        return ls

    def tibug_add_fix_labels(self):
        ls = []
        for item in self.new_fix_versions:
            if item not in self.exist_fix_versions:
                ls.append(item)
        ls.sort()
        return ls

    def tibug_delete_fix_labels(self):
        ls = []
        for item in self.exist_fix_versions:
            if item not in self.new_fix_versions:
                ls.append(item)
        ls.sort()
        return ls

    def affect_branch_message(self, status):
        if not TiBug.github_issues_is_valid(self.issue_link):
            return "[{}]({}) github issue field is invalid".format(self.case_name, self.tibug_link)

        if self.issue_link == "empty":
            return "[{}]({}) github issue field is empty".format(self.case_name, self.tibug_link)

        if status == "todo":
            return "[{}]({}) issue {} exists {} will add labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.exist_labels, self.add_labels)
        if status == "done":
            return "[{}]({}) issue {} exists {} added labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.exist_labels, self.add_labels)
        raise Exception(status)

    def affect_branch_rich_message(self, status):
        if not TiBug.github_issues_is_valid(self.issue_link):
            return "[{}]({}) github issue field is invalid".format(self.case_name, self.tibug_link)

        if self.issue_link == "empty":
            return "[{}]({}) github issue field is empty".format(self.case_name, self.tibug_link)

        if status == "todo":
            return "[{}]({}) issue [{}]({}) exists {} will add labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.issue_link, self.exist_labels, self.add_labels)
        if status == "done":
            return "[{}]({}) issue [{}]({}) exists {} added labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.issue_link, self.exist_labels, self.add_labels)
        raise Exception(status)

    def affect_version_message(self, status):
        m = "[{}]({}) ".format(self.case_name, self.tibug_link)

        todo = "will"
        add_name = "add"
        delete_name = "delete"
        if status == "done":
            todo = ""
            add_name = "added"
            delete_name = "deleted"
        add_affect_version = False
        if len(self.tibug_add_affects_labels()) != 0:
            m += "affect-version {} {} {} ".format(todo, add_name, self.tibug_add_affects_labels())
            add_affect_version = True
        if len(self.tibug_delete_affects_labels()) != 0:
            if not add_affect_version:
                m += "affect-version {} ".format(todo)
            else:
                m += " and "
            m += "{} {} ".format(delete_name, self.tibug_delete_affects_labels())

        add_fix_version = False
        if len(self.tibug_add_fix_labels()) != 0:
            m += ", fix-version {} {} {} ".format(todo, add_name, self.tibug_add_fix_labels())
            add_fix_version = True
        if len(self.tibug_delete_fix_labels()) != 0:
            if not add_fix_version:
                m += ", fix-version {} ".format(todo)
            else:
                m += " and "
            m += "{} {} ".format(delete_name, self.tibug_delete_fix_labels())
