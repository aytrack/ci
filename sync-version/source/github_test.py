import unittest

from github import Github


class TestGithub(unittest.TestCase):
    def test_label(self):
        g = Github("token", "ChenPeng2013", "awesome")
        g.delete_all_labels(1)
        self.assertEqual(g.issue_labels(1), [])

        g.add_labels(1, ["affect-5.0"])
        self.assertEqual(g.issue_labels(1), ["affect-5.0"])

        g.add_labels(1, ["affect-5.1", "affect-5.2"])
        self.assertEqual(g.issue_labels(1), ["affect-5.0", "affect-5.1", "affect-5.2"])

        g.delete_all_labels(1)
        self.assertEqual(g.issue_labels(1), [])

    def test_comment(self):
        g = Github("token", "ChenPeng2013", "awesome")
        g.add_comment(1, "test add label")

    def test_get_release_tag(self):
        g = Github("token", "pingcap", "tidb")
        g.get_release_tag()

    def test_list_issue_timeline(self):
        g = Github("token", "pingcap", "tidb")
        g.list_last_update_issues(1)

    def test_get_issue(self):
        g = Github("token", "pingcap", "tidb")
        g.get_issue(33912)

    def test_parse_reproduce_step(self):
        sqls = Github.parse_reproduce_step("""
        ```drop table if exists t;
create table t(a char(20), b binary(20), c binary(20));
insert into t value('-1', 0x2D31, 0x67);
insert into t value('-1', 0x2D31, 0x73);
select a from t where a between b and c;

MySQL [test]> select a from t where a between b and c;
Empty set (12 min 27.892 sec)

MySQL [test]> insert into mysql.expr_pushdown_blacklist values('cast', 'tikv','');
Query OK, 1 row affected (0.001 sec)

MySQL [test]> admin reload expr_pushdown_blacklist;
Query OK, 0 rows affected (0.001 sec)

MySQL [test]> select a from t where a between b and c;
+------+
| a    |
+------+
| -1   |
| -1   |
+------+
2 rows in set (0.001 sec)```""")
        self.assertEqual(sqls, ['drop table if exists t;', 'create table t(a char(20), b binary(20), c binary(20));', "insert into t value('-1', 0x2D31, 0x67);", "insert into t value('-1', 0x2D31, 0x73);", 'select a from t where a between b and c;', 'select a from t where a between b and c;', "insert into mysql.expr_pushdown_blacklist values('cast', 'tikv','');", 'admin reload expr_pushdown_blacklist;', 'select a from t where a between b and c;'])

if __name__ == "__main__":
    unittest.main()
