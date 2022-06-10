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

    def test_list_pr(self):
        g = Github("token", "pingcap", "tidb")
        g.list_pr(31609)

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

        sqls = Github.parse_reproduce_step("""```
use test;
drop table if exists NT_28395;
CREATE TABLE `NT_28395` (
  `COL1` bit(28) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
insert into NT_28395 values(0x00DE25BE);
select col1 from NT_28395 t1 where (select count(*) from NT_28395 t2 where t2.col1 in (t1.col1, 0x30)) > 1;```""")
        self.assertEqual(sqls, ['use test;',
                                'drop table if exists NT_28395;',
                                'CREATE TABLE `NT_28395` ( `COL1` bit(28) DEFAULT NULL ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;',
                                'insert into NT_28395 values(0x00DE25BE);',
                                'select col1 from NT_28395 t1 where (select count(*) from NT_28395 t2 where t2.col1 in (t1.col1, 0x30)) > 1;'])

        sqls = Github.parse_reproduce_step("""```
drop table if exists t;
CREATE TABLE `t` (
  `a` int(11) DEFAULT NULL,
  `b` int(11) GENERATED ALWAYS AS (`a`) STORED NOT NULL,
  PRIMARY KEY (`b`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
insert into t(a) values(102);
prepare stmt from "select * from t where b in (?, ?, ?)";
set @a=102, @b=102, @c=102;
execute stmt using @a,@b,@c;
set @a=-97, @b=-97, @c=-97;
execute stmt using @a,@b,@c;```""")
        self.assertEqual(sqls, ['drop table if exists t;',
                                'CREATE TABLE `t` ( `a` int(11) DEFAULT NULL, `b` int(11) GENERATED ALWAYS AS (`a`) STORED NOT NULL, PRIMARY KEY (`b`) /*T![clustered_index] CLUSTERED */ ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;',
                                'insert into t(a) values(102);',
                                'prepare stmt from "select * from t where b in (?, ?, ?)";',
                                'set @a=102, @b=102, @c=102;',
                                'execute stmt using @a,@b,@c;',
                                'set @a=-97, @b=-97, @c=-97;',
                                'execute stmt using @a,@b,@c;'])

        sqls = Github.parse_reproduce_step("""```
        mysql> create table t1(id int, key(id));
Query OK, 0 rows affected (0.09 sec)

mysql> create table t2(id int, key(id));
Query OK, 0 rows affected (0.09 sec)

mysql> explain select  /*+ merge_join(b) */ * from (select * from t1) a join (select id, count(1) from t2 group by t2.id) b on a.id=b.id;
+--------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------+
| id                             | estRows | task      | access object          | operator info                                                                         |
+--------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------+
| Projection_10                  | 9990.00 | root      |                        | test.t1.id, test.t2.id, Column#5                                                      |
| └─HashJoin_23                  | 9990.00 | root      |                        | inner join, equal:[eq(test.t1.id, test.t2.id)]                                        |
|   ├─HashAgg_36(Build)          | 7992.00 | root      |                        | group by:test.t2.id, funcs:count(1)->Column#5, funcs:firstrow(test.t2.id)->test.t2.id |
|   │ └─IndexReader_43           | 9990.00 | root      |                        | index:IndexFullScan_42                                                                |
|   │   └─IndexFullScan_42       | 9990.00 | cop[tikv] | table:t2, index:id(id) | keep order:false, stats:pseudo                                                        |
|   └─IndexReader_47(Probe)      | 9990.00 | root      |                        | index:IndexFullScan_46                                                                |
|     └─IndexFullScan_46         | 9990.00 | cop[tikv] | table:t1, index:id(id) | keep order:false, stats:pseudo                                                        |
+--------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------+
7 rows in set, 1 warning (0.00 sec)

mysql> show warnings;
+---------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                        |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1815 | There are no matching table names for (b) in optimizer hint /*+ MERGE_JOIN(b) */ or /*+ TIDB_SMJ(b) */. Maybe you can use the table alias name |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)```""")
        self.assertEqual(sqls, ['create table t1(id int, key(id));', 'create table t2(id int, key(id));', 'explain select  /*+ merge_join(b) */ * from (select * from t1) a join (select id, count(1) from t2 group by t2.id) b on a.id=b.id;', 'show warnings;'])


if __name__ == "__main__":
    unittest.main()
