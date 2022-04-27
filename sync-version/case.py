
class Case(object):
    def __int__(self, case_name=None, tibug_link=None, issue_link=None, exist_labels=None, add_labels=None):
        if exist_labels is None:
            exist_labels = []
        if add_labels is None:
            add_labels = []

        self.case_name = None
        self.tibug_link = None
        self.issue_link = None
        self.exist_labels = exist_labels
        self.add_labels = add_labels

    def issue_number(self):
        if self.issue_link is None:
            return self.issue_link

        return self.issue_link.split("/")[-1]

