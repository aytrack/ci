import datetime
import requests

tidb_stmt_prefix = [
    "SELECT",
    "CREATE",
    "DELETE",
    "DROP",
    "ALTER",
    "PREPARE",
    "SET",
    "INSERT",
    "USE",
    "EXECUTE",
    "UPDATE",
    "ADMIN",
    "ANALYZE",
    "SHOW",
    "DESC",
    "EXPLAIN",
    "WITH",
]

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

    def is_bug(self, issue_number):
        for item in self.issue_labels(issue_number):
            if item.startswith("type"):
                return item == "type/bug"
        return False

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

    def list_last_update_issues(self, days):
        issue_ids = []
        page = 1
        t = datetime.datetime.utcnow() - datetime.timedelta(days=int(days))
        while True:
            url = "https://api.github.com/repos/{}/{}/issues?page={}&state=all&per_page=30&labels=type/bug&since={}".\
                format(self.owner, self.repo, page, t.strftime("%Y-%m-%dT%H:%M:%SZ"))
            print(url)
            res = requests.get(url, headers={"Authorization": "token {}".format(self.token)})
            if res.status_code != 200:
                raise Exception("unknown", res.status_code)
            for item in res.json():
                issue_ids.append(item["number"])

            if len(res.json()) < 30:
                break

            page = page + 1

        m = []
        for issue_id in issue_ids:
            add_labels = []
            delete_labels = []
            page = 1
            while True:
                url = "https://api.github.com/repos/{}/{}/issues/{}/timeline?page={}&per_page=30".format(self.owner, self.repo, issue_id, page)
                print(url)
                res = requests.get(url, headers={"Authorization": "token {}".format(self.token)})
                if res.status_code != 200:
                    raise Exception("unknown", res.status_code)

                for item in res.json():
                    if datetime.datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ") < t:
                        continue
                    if item["event"] not in ["unlabeled", "labeled"]:
                        continue
                    if not item["label"]["name"].startswith("affects"):
                        continue
                    if item["actor"]["login"] == "ChenPeng2013":
                        continue
                    if item["event"] == "unlabeled":
                        delete_labels.append(item["label"]["name"])
                    if item["event"] == "labeled":
                        add_labels.append(item["label"]["name"])
                if len(res.json()) < 30:
                    break
                page = page + 1

            if len(add_labels) != 0 or len(delete_labels) != 0:
                m.append({"issue_number": issue_id, "add_labels": add_labels, "delete_labels": delete_labels})

        return m

    def list_pr(self, issue_number):
        print(issue_number)
        data = []
        page = 1
        while True:
            url = "https://api.github.com/repos/{}/{}/issues/{}/timeline?page={}&per_page=30".format(self.owner,
                                                                                                     self.repo,
                                                                                                     issue_number, page)
            print(url)
            res = requests.get(url, headers={"Authorization": "token {}".format(self.token)})
            if res.status_code != 200:
                raise Exception("unknown", res.status_code)

            for item in res.json():
                if item["event"] not in ["cross-referenced"]:
                    continue
                if item["source"]["issue"].get("pull_request") is None:
                    continue
                pr_url = item["source"]["issue"]["pull_request"]["url"]
                print(pr_url)
                pr_res = requests.get(pr_url, headers={"Authorization": "token {}".format(self.token)})
                if pr_res.status_code != 200:
                    raise Exception("unknown", pr_res.status_code)
                merged = True
                if pr_res.json()["merged_at"] is None or len(pr_res.json()["merged_at"]) == 0:
                    merged = False
                ref = pr_res.json()["base"]["ref"]
                data.append({"url": pr_url, "merged": merged, "ref": ref})
            if len(res.json()) < 30:
                break
            page = page + 1

        return data

    def get_issue(self, issue_number):
        res = requests.get("https://api.github.com/repos/{}/{}/issues/{}".format(self.owner, self.repo, issue_number),
                           headers={"Authorization": "token {}".format(self.token)})

        if res.status_code != 200 and res.status_code != 201:
            raise Exception("unknown", res.status_code)

        # title
        # body
        return res.json()

    def search(self, txt):
        page = 1
        data = []
        while True:
            # https://api.github.com/search/issues?q=repo:pingcap/tidb+is:issue+created:2022-05-10..2022-06-09+label:severity/major,severity/critical
            res = requests.get("https://api.github.com/search/issues?q=repo:{}/{}+{}&page={}&per_page=30".format(self.owner, self.repo, txt, page),
                               headers={"Authorization": "token {}".format(self.token)})
            if res.status_code != 200:
                raise Exception("unknown", res.status_code)
            for item in res.json()["items"]:
                label = []
                for l in item["labels"]:
                    if l["name"].startswith("sig") or l["name"].startswith("component") or l["name"].startswith("severity"):
                        label.append(l["name"])
                data.append({"html_url": item["html_url"], "title": item["title"], "label": " ".join(label), "created_at": item["created_at"]})
            if len(res.json()["items"]) < 30:
                break
            page = page + 1
        return data

    @staticmethod
    def parse_reproduce_step(body):
        begin = body.find("### 1. Minimal reproduce step (Required)")
        if begin == -1:
            return None
        body = body[begin + len("### 1. Minimal reproduce step (Required)"):]
        end = body.find("### 2. What did you expect to see? (Required)")
        if end == -1:
            return None
        body = body[:end]
        body = body.replace("```", "")
        if body.startswith("sql"):
            body = body[3:]

        if body.lower().count("select") == 0 and body.lower().count("create") == 0 and body.lower().count("execute") == 0:
            return None

        body = body.replace("\r", " ")

        global tidb_stmt_prefix
        pre_sql_prefix = False
        sqls = []
        for item in body.split("\n"):
            item = item.lstrip(" ")
            item = item.rstrip(" ")
            if item.startswith("MySQL [test]>"):
                item = item[len("MySQL [test]>"):]
            if item.startswith("mysql> "):
                item = item[len("mysql> "):]
            item = item.lstrip(" ")
            if len(item) == 0:
                continue

            key_word_prefix = False
            for key_word in tidb_stmt_prefix:
                if item.upper().startswith(key_word):
                    key_word_prefix = True
                    break

            if key_word_prefix:
                sqls.append(item)
                pre_sql_prefix = True
            else:
                # !key_word_prefix
                if pre_sql_prefix:
                    sqls[len(sqls)-1] += " " + item

            end_sql = (item.count(";") != 0)
            if end_sql:
                pre_sql_prefix = False

            # ignore unknown sql
            continue

        if len(sqls) == 0:
            return None

        # multi statement
        new_sqls = []
        for item in sqls:
            if item.count(";") != 0:
                for each in item.split(";"):
                    if len(each) == 0:
                        continue

                    key_word_prefix = False
                    for key_word in tidb_stmt_prefix:
                        each = each.lstrip(" ")
                        each = each.rstrip(" ")
                        if each.upper().startswith(key_word):
                            key_word_prefix = True
                            break
                    if key_word_prefix:
                        new_sqls.append(each + ";")
            else:
                new_sqls.append(item)

        return new_sqls
