import requests


class Github(object):
    """
    user interface to Github
    """
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo

    def issue_labels(self, issue_number):
        """
        :param issue_number:
        :return: the labels of issue
        """
        res = requests.get("https://api.github.com/repos/{}/{}/issues/{}/labels".format(self.owner, self.repo, issue_number),
                           headers={"Authorization": "token {}".format(self.token)})
        if res.status_code != 200:
            raise Exception("unknown", res.status_code)

        ls = []
        for item in res.json():
            ls.append(item["name"])
        return ls

    def affect_labels(self, issue_number):
        ls = []
        for item in self.issue_labels(issue_number):
            if item.startswith("affects"):
                ls.append(item)
        return ls

    def add_labels(self, issue_number, labels):
        """
        :param issue_number: the unique identification of the issue
        :param labels: the labels will add to issue_number
        :return: None
        """
        res = requests.post("https://api.github.com/repos/{}/{}/issues/{}/labels".format(self.owner, self.repo, issue_number),
                            json={"labels": labels}, headers={"Authorization": "token {}".format(self.token)})

        if res.status_code != 200:
            raise Exception("unknown", res.status_code)

    def delete_all_labels(self, issue_number):
        """
        delete all labels in owner/repo/issues/issue_number
        :param issue_number: the unique identification of the issue
        :return:
        """
        res = requests.delete("https://api.github.com/repos/{}/{}/issues/{}/labels".format(self.owner, self.repo, issue_number),
                              headers={"Authorization": "token {}".format(self.token)})

        if res.status_code != 200 and res.status_code != 204:
            raise Exception("unknown", res.status_code)

    def add_comment(self, issue_number, message):
        """
        add a comment to issue_number
        :param issue_number: the unique identification of the issue
        :param message: the comment content
        :return:
        """
        res = requests.post("https://api.github.com/repos/{}/{}/issues/{}/comments".format(self.owner, self.repo, issue_number),
                            json={"body": message}, headers={"Authorization": "token {}".format(self.token)})

        if res.status_code != 200 and res.status_code != 201:
            raise Exception("unknown", res.status_code)

    def link(self, issue_number):
        return "https://github.com/{}/{}/issues/{}".format(self.owner, self.repo, issue_number)

    def get_release_tag(self):
        res = requests.get(
            "https://api.github.com/repos/{}/{}/releases".format(self.owner, self.repo),
            headers={"Authorization": "token {}".format(self.token)})
        if res.status_code != 200:
            raise Exception("unknown", res.status_code)

        vs = []
        for item in res.json():
            tag_name = item["tag_name"]
            if tag_name.count("-") != 0 or tag_name.count(".") != 2 or not tag_name.startswith("v"):
                continue
            vs.append(tag_name)
        return vs
