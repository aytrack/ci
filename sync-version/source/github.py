import datetime
import requests

tidb_key_words = [
    "A",
    "ACCOUNT",
    "ACTION",
    "ADD",
    "ADMIN",
    "ADVISE",
    "AFTER",
    "AGAINST",
    "AGO",
    "ALGORITHM",
    "ALL",
    "ALTER",
    "ALWAYS",
    "ANALYZE",
    "AND",
    "ANY",
    "AS",
    "ASC",
    "ASCII",
    "AUTO_ID_CACHE",
    "AUTO_INCREMENT",
    "AUTO_RANDOM",
    "AUTO_RANDOM_BASE",
    "AVG",
    "AVG_ROW_LENGTH",
    "B",
    "BACKEND",
    "BACKUP",
    "BACKUPS",
    "BEGIN",
    "BETWEEN",
    "BIGINT",
    "BINARY",
    "BINDING",
    "BINDINGS",
    "BINLOG",
    "BIT",
    "BLOB",
    "BLOCK",
    "BOOL",
    "BOOLEAN",
    "BOTH",
    "BTREE",
    "BUCKETS",
    "BUILTINS",
    "BY",
    "BYTE",
    "C",
    "CACHE",
    "CANCEL",
    "CAPTURE",
    "CASCADE",
    "CASCADED",
    "CASE",
    "CHAIN",
    "CHANGE",
    "CHAR",
    "CHARACTER",
    "CHARSET",
    "CHECK",
    "CHECKPOINT",
    "CHECKSUM",
    "CIPHER",
    "CLEANUP",
    "CLIENT",
    "CMSKETCH",
    "COALESCE",
    "COLLATE",
    "COLLATION",
    "COLUMN",
    "COLUMNS",
    "COLUMN_FORMAT",
    "COMMENT",
    "COMMIT",
    "COMMITTED",
    "COMPACT",
    "COMPRESSED",
    "COMPRESSION",
    "CONCURRENCY",
    "CONFIG",
    "CONNECTION",
    "CONSISTENT",
    "CONSTRAINT",
    "CONTEXT",
    "CONVERT",
    "CPU",
    "CREATE",
    "CROSS",
    "CSV_BACKSLASH_ESCAPE",
    "CSV_DELIMITER",
    "CSV_HEADER",
    "CSV_NOT_NULL",
    "CSV_NULL",
    "CSV_SEPARATOR",
    "CSV_TRIM_LAST_SEPARATORS",
    "CUME_DIST",
    "CURRENT",
    "CURRENT_DATE",
    "CURRENT_ROLE",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "CURRENT_USER",
    "CYCLE",
    "D",
    "DATA",
    "DATABASE",
    "DATABASES",
    "DATE",
    "DATETIME",
    "DAY",
    "DAY_HOUR",
    "DAY_MICROSECOND",
    "DAY_MINUTE",
    "DAY_SECOND",
    "DDL",
    "DEALLOCATE",
    "DECIMAL",
    "DEFAULT",
    "DEFINER",
    "DELAYED",
    "DELAY_KEY_WRITE",
    "DELETE",
    "DENSE_RANK",
    "DEPTH",
    "DESC",
    "DESCRIBE",
    "DIRECTORY",
    "DISABLE",
    "DISCARD",
    "DISK",
    "DISTINCT",
    "DISTINCTROW",
    "DIV",
    "DO",
    "DOUBLE",
    "DRAINER",
    "DROP",
    "DUAL",
    "DUPLICATE",
    "DYNAMIC",
    # duplicate with Empty set
    # "E",
    "ELSE",
    "ENABLE",
    "ENCLOSED",
    "ENCRYPTION",
    "END",
    "ENFORCED",
    "ENGINE",
    "ENGINES",
    "ENUM",
    "ERROR",
    "ERRORS",
    "ESCAPE",
    "ESCAPED",
    "EVENT",
    "EVENTS",
    "EVOLVE",
    "EXCEPT",
    "EXCHANGE",
    "EXCLUSIVE",
    "EXECUTE",
    "EXISTS",
    "EXPANSION",
    "EXPIRE",
    "EXPLAIN",
    "EXTENDED",
    "F",
    "FALSE",
    "FAULTS",
    "FIELDS",
    "FILE",
    "FIRST",
    "FIRST_VALUE",
    "FIXED",
    "FLOAT",
    "FLUSH",
    "FOLLOWING",
    "FOR",
    "FORCE",
    "FOREIGN",
    "FORMAT",
    "FROM",
    "FULL",
    "FULLTEXT",
    "FUNCTION",
    "G",
    "GENERAL",
    "GENERATED",
    "GLOBAL",
    "GRANT",
    "GRANTS",
    "GROUP",
    "GROUPS",
    "H",
    "HASH",
    "HAVING",
    "HIGH_PRIORITY",
    "HISTORY",
    "HOSTS",
    "HOUR",
    "HOUR_MICROSECOND",
    "HOUR_MINUTE",
    "HOUR_SECOND",
    "I",
    "IDENTIFIED",
    "IF",
    "IGNORE",
    "IMPORT",
    "IMPORTS",
    "IN",
    "INCREMENT",
    "INCREMENTAL",
    "INDEX",
    "INDEXES",
    "INFILE",
    "INNER",
    "INSERT",
    "INSERT_METHOD",
    "INSTANCE",
    "INT",
    "INT1",
    "INT2",
    "INT3",
    "INT4",
    "INT8",
    "INTEGER",
    "INTERVAL",
    "INTO",
    "INVISIBLE",
    "INVOKER",
    "IO",
    "IPC",
    "IS",
    "ISOLATION",
    "ISSUER",
    "J",
    "JOB",
    "JOBS",
    "JOIN",
    "JSON",
    "K",
    "KEY",
    "KEYS",
    "KEY_BLOCK_SIZE",
    "KILL",
    "L",
    "LABELS",
    "LAG",
    "LANGUAGE",
    "LAST",
    "LASTVAL",
    "LAST_BACKUP",
    "LAST_VALUE",
    "LEAD",
    "LEADING",
    "LEFT",
    "LESS",
    "LEVEL",
    "LIKE",
    "LIMIT",
    "LINEAR",
    "LINES",
    "LIST",
    "LOAD",
    "LOCAL",
    "LOCALTIME",
    "LOCALTIMESTAMP",
    "LOCATION",
    "LOCK",
    "LOGS",
    "LONG",
    "LONGBLOB",
    "LONGTEXT",
    "LOW_PRIORITY",
    "M",
    "MASTER",
    "MATCH",
    "MAXVALUE",
    "MAX_CONNECTIONS_PER_HOUR",
    "MAX_IDXNUM",
    "MAX_MINUTES",
    "MAX_QUERIES_PER_HOUR",
    "MAX_ROWS",
    "MAX_UPDATES_PER_HOUR",
    "MAX_USER_CONNECTIONS",
    "MB",
    "MEDIUMBLOB",
    "MEDIUMINT",
    "MEDIUMTEXT",
    "MEMORY",
    "MERGE",
    "MICROSECOND",
    "MINUTE",
    "MINUTE_MICROSECOND",
    "MINUTE_SECOND",
    "MINVALUE",
    "MIN_ROWS",
    "MOD",
    "MODE",
    "MODIFY",
    "MONTH",
    "N",
    "NAMES",
    "NATIONAL",
    "NATURAL",
    "NCHAR",
    "NEVER",
    "NEXT",
    "NEXTVAL",
    "NO",
    "NOCACHE",
    "NOCYCLE",
    "NODEGROUP",
    "NODE_ID",
    "NODE_STATE",
    "NOMAXVALUE",
    "NOMINVALUE",
    "NONE",
    "NOT",
    "NOWAIT",
    "NO_WRITE_TO_BINLOG",
    "NTH_VALUE",
    "NTILE",
    "NULL",
    "NULLS",
    "NUMERIC",
    "NVARCHAR",
    "O",
    "OFFSET",
    "ON",
    "ONLINE",
    "ONLY",
    "ON_DUPLICATE",
    "OPEN",
    "OPTIMISTIC",
    "OPTIMIZE",
    "OPTION",
    "OPTIONALLY",
    "OR",
    "ORDER",
    "OUTER",
    "OUTFILE",
    "OVER",
    "P",
    "PACK_KEYS",
    "PAGE",
    "PARSER",
    "PARTIAL",
    "PARTITION",
    "PARTITIONING",
    "PARTITIONS",
    "PASSWORD",
    "PERCENT_RANK",
    "PER_DB",
    "PER_TABLE",
    "PESSIMISTIC",
    "PLUGINS",
    "PRECEDING",
    "PRECISION",
    "PREPARE",
    "PRE_SPLIT_REGIONS",
    "PRIMARY",
    "PRIVILEGES",
    "PROCEDURE",
    "PROCESS",
    "PROCESSLIST",
    "PROFILE",
    "PROFILES",
    "PUMP",
    # duplicate with Query Ok
    # "Q",
    "QUARTER",
    "QUERIES",
    # duplicate with Query Ok
    # "QUERY",
    "QUICK",
    "R",
    "RANGE",
    "RANK",
    "RATE_LIMIT",
    "READ",
    "REAL",
    "REBUILD",
    "RECOVER",
    "REDUNDANT",
    "REFERENCES",
    "REGEXP",
    "REGION",
    "REGIONS",
    "RELEASE",
    "RELOAD",
    "REMOVE",
    "RENAME",
    "REORGANIZE",
    "REPAIR",
    "REPEAT",
    "REPEATABLE",
    "REPLACE",
    "REPLICA",
    "REPLICATION",
    "REQUIRE",
    "RESPECT",
    "RESTORE",
    "RESTORES",
    "RESTRICT",
    "REVERSE",
    "REVOKE",
    "RIGHT",
    "RLIKE",
    "ROLE",
    "ROLLBACK",
    "ROUTINE",
    "ROW",
    "ROWS",
    "ROW_COUNT",
    "ROW_FORMAT",
    "ROW_NUMBER",
    "RTREE",
    "S",
    "SAMPLES",
    "SECOND",
    "SECONDARY_ENGINE",
    "SECONDARY_LOAD",
    "SECONDARY_UNLOAD",
    "SECOND_MICROSECOND",
    "SECURITY",
    "SELECT",
    "SEND_CREDENTIALS_TO_TIKV",
    "SEPARATOR",
    "SEQUENCE",
    "SERIAL",
    "SERIALIZABLE",
    "SESSION",
    "SET",
    "SETVAL",
    "SHARD_ROW_ID_BITS",
    "SHARE",
    "SHARED",
    "SHOW",
    "SHUTDOWN",
    "SIGNED",
    "SIMPLE",
    "SKIP_SCHEMA_FILES",
    "SLAVE",
    "SLOW",
    "SMALLINT",
    "SNAPSHOT",
    "SOME",
    "SOURCE",
    "SPATIAL",
    "SPLIT",
    "SQL",
    "SQL_BIG_RESULT",
    "SQL_BUFFER_RESULT",
    "SQL_CACHE",
    "SQL_CALC_FOUND_ROWS",
    "SQL_NO_CACHE",
    "SQL_SMALL_RESULT",
    "SQL_TSI_DAY",
    "SQL_TSI_HOUR",
    "SQL_TSI_MINUTE",
    "SQL_TSI_MONTH",
    "SQL_TSI_QUARTER",
    "SQL_TSI_SECOND",
    "SQL_TSI_WEEK",
    "SQL_TSI_YEAR",
    "SSL",
    "START",
    "STARTING",
    "STATS",
    "STATS_AUTO_RECALC",
    "STATS_BUCKETS",
    "STATS_HEALTHY",
    "STATS_HISTOGRAMS",
    "STATS_META",
    "STATS_PERSISTENT",
    "STATS_SAMPLE_PAGES",
    "STATUS",
    "STORAGE",
    "STORED",
    "STRAIGHT_JOIN",
    "STRICT_FORMAT",
    "SUBJECT",
    "SUBPARTITION",
    "SUBPARTITIONS",
    "SUPER",
    "SWAPS",
    "SWITCHES",
    "SYSTEM_TIME",
    "T",
    "TABLE",
    "TABLES",
    "TABLESPACE",
    "TABLE_CHECKSUM",
    "TEMPORARY",
    "TEMPTABLE",
    "TERMINATED",
    "TEXT",
    "THAN",
    "THEN",
    "TIDB",
    "TIFLASH",
    "TIKV_IMPORTER",
    "TIME",
    "TIMESTAMP",
    "TINYBLOB",
    "TINYINT",
    "TINYTEXT",
    "TO",
    "TOPN",
    "TRACE",
    "TRADITIONAL",
    "TRAILING",
    "TRANSACTION",
    "TRIGGER",
    "TRIGGERS",
    "TRUE",
    "TRUNCATE",
    "TYPE",
    "U",
    "UNBOUNDED",
    "UNCOMMITTED",
    "UNDEFINED",
    "UNICODE",
    "UNION",
    "UNIQUE",
    "UNKNOWN",
    "UNLOCK",
    "UNSIGNED",
    "UPDATE",
    "USAGE",
    "USE",
    "USER",
    "USING",
    "UTC_DATE",
    "UTC_TIME",
    "UTC_TIMESTAMP",
    "V",
    "VALIDATION",
    "VALUE",
    "VALUES",
    "VARBINARY",
    "VARCHAR",
    "VARCHARACTER",
    "VARIABLES",
    "VARYING",
    "VIEW",
    "VIRTUAL",
    "VISIBLE",
    "W",
    "WARNINGS",
    "WEEK",
    "WEIGHT_STRING",
    "WHEN",
    "WHERE",
    "WIDTH",
    "WINDOW",
    "WITH",
    "WITHOUT",
    "WRITE",
    "X",
    "X509",
    "XOR",
    "Y",
    "YEAR",
    "YEAR_MONTH",
    "Z",
    "ZEROFILL",
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

    def get_issue(self, issue_number):
        res = requests.get("https://api.github.com/repos/{}/{}/issues/{}".format(self.owner, self.repo, issue_number),
                           headers={"Authorization": "token {}".format(self.token)})

        if res.status_code != 200 and res.status_code != 201:
            raise Exception("unknown", res.status_code)

        # title
        # body
        return res.json()

    @staticmethod
    def parse_reproduce_step(body):
        begin = body.find("```")
        if begin == -1:
            return None
        body = body[begin + 3:]
        end = body.find("```")
        if end == -1:
            return None
        body = body[:end]
        if body.startswith("sql"):
            body = body[3:]

        if body.lower().count("select") == 0 and body.lower().count("create") == 0 and body.lower().count("execute") == 0:
            return None

        body = body.replace("\r", " ")

        sqls = []
        global tidb_key_words
        for item in body.split("\n"):
            item = item.lstrip(" ")
            item = item.rstrip(" ")
            if item.startswith("MySQL [test]>"):
                item = item[len("MySQL [test]>"):]
            item = item.lstrip(" ")
            key_word_prefix = False
            for key_word in tidb_key_words:
                if item.upper().startswith(key_word):
                    key_word_prefix = True
                    break
            if not key_word_prefix:
                continue

            if len(item) == 0:
                continue
            sqls.append(item)

        if len(sqls) == 0:
            return None

        return sqls
