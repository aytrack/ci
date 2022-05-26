from source.tibug import TiBug
import sqlparse
import subprocess

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
        self.exist_affects_versions = []
        self.new_affects_versions = []
        self.exist_fix_versions = []
        self.new_fix_versions = []

    def issue_number(self):
        if self.issue_link is None:
            return self.issue_link
        if self.issue_link == "empty":
            return None
        return self.issue_link.split("/")[-1]

    def tibug_add_affects_labels(self):
        ls = []
        for item in self.new_affects_versions:
            if item not in self.exist_affects_versions:
                ls.append(item)
        ls.sort()
        return ls

    def tibug_delete_affects_labels(self):
        ls = []
        for item in self.exist_affects_versions:
            if item not in self.new_affects_versions:
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

    def is_tibug(self):
        return self.case_name.startswith("TIBUG-")

    def affect_branch_message(self, status):
        if self.is_tibug():
            if not TiBug.github_issues_is_valid(self.issue_link):
                return "[{}]({}) github issue field is invalid".format(self.case_name, self.tibug_link)
            
            if self.issue_link == "empty":
                return "[{}]({}) github issue field is empty".format(self.case_name, self.tibug_link)
            
            if status == "todo":
                return "[{}]({}) issue {} exists {} will add labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.exist_labels, self.add_labels)
            if status == "done":
                return "[{}]({}) issue {} exists {} added labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.exist_labels, self.add_labels)

        if status == "todo":
            return "{} exists {} will add labels {}".format(self.case_name, self.exist_labels, self.add_labels)
        if status == "done":
            return "{} exists {} added labels {}".format(self.case_name, self.exist_labels, self.add_labels)

    def affect_branch_rich_message(self, status):
        if self.is_tibug():
            if not TiBug.github_issues_is_valid(self.issue_link):
                return "[{}]({}) github issue field is invalid".format(self.case_name, self.tibug_link)
            
            if self.issue_link == "empty":
                return "[{}]({}) github issue field is empty".format(self.case_name, self.tibug_link)
            
            if status == "todo":
                return "[{}]({}) issue [{}]({}) exists {} will add labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.issue_link, self.exist_labels, self.add_labels)
            if status == "done":
                return "[{}]({}) issue [{}]({}) exists {} added labels {}".format(self.case_name, self.tibug_link, self.issue_number(), self.issue_link, self.exist_labels, self.add_labels)

        if status == "todo":
            return "[{}]({}) exists {} will add labels {}".format(self.case_name, self.issue_link, self.exist_labels, self.add_labels)
        if status == "done":
            return "[{}]({}) exists {} added labels {}".format(self.case_name, self.issue_link, self.exist_labels, self.add_labels)

    def affect_version_message(self, status):
        m = "[{}]({}) ".format(self.case_name, self.tibug_link)
        if len(self.tibug_add_affects_labels()) == 0 and len(self.tibug_delete_affects_labels()) == 0 and \
                len(self.tibug_add_fix_labels()) == 0 and len(self.tibug_delete_fix_labels()) == 0:
            return m + " do nothing"

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

        return m

    @staticmethod
    def gen_execute_lines(case_id, summary, dsn, sqls):
        emails = subprocess.run(["git", "config", "--get", "user.email"], capture_output=True, text=True).stdout.split(
            "\n")
        email = emails[0]
        case_class = case_id.replace("_", "")
        case_class = case_class.replace("-", "")

        dbclient = None
        if dsn is not None and len(dsn) != 0:
            from util.db import DBClient
            dbclient = DBClient(dsn)
            dbclient.execute_sql("drop database if exists case_gen;")
            dbclient.execute_sql("create database case_gen")
            dbclient.execute_sql("use case_gen")

        es = []
        packs = ["from cases.utils.simple import SimpleCase",
                 "from cases.utils.meta import ClusterType, CaseMeta",
                 "from cases.utils.asserts import assert_ordered_msg"]
        funcs = {}
        for item in sqls:
            if item.count('"'):
                sql = "self.execute_sql('{}')".format(item)
            else:
                sql = 'self.execute_sql("{}")'.format(item)
            if dbclient is not None:
                res = dbclient.execute_sql(item)
                if item.lower().count("select") != 0 or item.lower().count("execute") != 0:
                    sql = "res = " + sql
                es.append(sql)
                if item.lower().count("select") != 0 or item.lower().count("execute") != 0:
                    es.append("assert_ordered_msg(res, {})".format(res))
            else:
                es.append(sql)

            ss = sqlparse.parse(item)[0]
            none_whitespace_tokens = []
            none_white_str = ""
            for t in ss.tokens:
                if t.is_whitespace:
                    continue
                none_white_str = none_white_str + t.value
                none_whitespace_tokens.append(t)

            none_white_str = none_white_str.lower()
            # alter table t set tiflash replica 1
            if len(none_whitespace_tokens) >= 6 and none_white_str.startswith("altertable") and none_white_str.count("settiflash replica") == 1:
                if funcs.get("sync_tiflash") is None:
                    funcs["sync_tiflash"] ="""def sync_tiflash(self, number, table_name):
        for i in range(60):
            time.sleep(5)
            res = self.execute_sql("select count(*) from INFORMATION_SCHEMA.TIFLASH_REPLICA where AVAILABLE = {} and TABLE_NAME='{}' and TABLE_SCHEMA='{}';".format(number, table_name, self.db))
            if res == ((1,),):
                break
            if i == 59:
                raise Exception("sync to tiflash failed")"""
                es.append("self.sync_tiflash({}, '{}')".format(none_whitespace_tokens[5].value, none_whitespace_tokens[2].value))
                if "import time" not in packs:
                    packs.append("import time")

        funcs_slice = []
        for k in funcs:
            funcs_slice.append(funcs[k])
        content = """{}


class {}(SimpleCase):
    name = "{}"
    case_meta = CaseMeta(cluster=ClusterType.Default, designer="{}", supported_versions=[">=4.0.0"],
                         summary="{}")

    def run(self):
        {}
    
    {}""".format("\n".join(packs), case_class, case_id, email, summary, "\n        ".join(es), "\n\n        ".join(funcs_slice))

        return content