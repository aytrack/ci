import unittest

from case import Case


class TestCase(unittest.TestCase):
    def test_gen_case(self):
        res_tibug_2211 = """from cases.utils.simple import SimpleCase
from cases.utils.meta import ClusterType, CaseMeta
from cases.utils.asserts import assert_ordered_msg
import time


class TIBUG2211(SimpleCase):
    name = "TIBUG-2211"
    case_meta = CaseMeta(cluster=ClusterType.Default, designer="chenpeng@pingcap.com", supported_versions=[">=4.0.0"],
                         summary="Planner generates wrong 2 phase aggregate plan for TiFlash")

    def run(self):
        self.execute_sql("create table customer2(c_id bigint primary key);")
        self.execute_sql("create table orders2(o_id bigint primary key, c_id bigint);")
        self.execute_sql("insert into customer2 values(1),(2),(3),(4),(5);")
        self.execute_sql("insert into orders2 values(1,1),(2,1),(3,2),(4,2),(5,2);")
        self.execute_sql("alter table customer2 set tiflash replica 1;")
        self.sync_tiflash(1, 'customer2')
        self.execute_sql("alter table orders2 set tiflash replica 1;")
        self.sync_tiflash(1, 'orders2')
        self.execute_sql("set @@tidb_enforce_mpp=1;")
        self.execute_sql("set @@tidb_opt_agg_push_down=1;")
        self.execute_sql("select count(*) from customer2 c, orders2 o where c.c_id=o.c_id;")
    
    def sync_tiflash(self, number, table_name):
        for i in range(60):
            time.sleep(5)
            res = self.execute_sql("select count(*) from INFORMATION_SCHEMA.TIFLASH_REPLICA where AVAILABLE = {} and TABLE_NAME='{}' and TABLE_SCHEMA='{}';".format(number, table_name, self.db))
            if res == ((1,),):
                break
            if i == 59:
                raise Exception("sync to tiflash failed")"""

        self.assertEqual(Case.gen_execute_lines("TIBUG-2211", "Planner generates wrong 2 phase aggregate plan for TiFlash", None,
                                                ['create table customer2(c_id bigint primary key);',
                                                 'create table orders2(o_id bigint primary key, c_id bigint);',
                                                 "insert into customer2 values(1),(2),(3),(4),(5);",
                                                 'insert into orders2 values(1,1),(2,1),(3,2),(4,2),(5,2);',
                                                 "alter table customer2 set tiflash replica 1;",
                                                 'alter table orders2 set tiflash replica 1;',
                                                 'set @@tidb_enforce_mpp=1;', 'set @@tidb_opt_agg_push_down=1;',
                                                 'select count(*) from customer2 c, orders2 o where c.c_id=o.c_id;']), res_tibug_2211)

        res_tibug_2208 = """from cases.utils.simple import SimpleCase
from cases.utils.meta import ClusterType, CaseMeta
from cases.utils.asserts import assert_ordered_msg


class TIBUG2208(SimpleCase):
    name = "TIBUG-2208"
    case_meta = CaseMeta(cluster=ClusterType.Default, designer="chenpeng@pingcap.com", supported_versions=[">=4.0.0"],
                         summary="Results are different for cast when it's pushed down")

    def run(self):
        self.execute_sql("drop table if exists t;")
        self.execute_sql("create table t(a char(20), b binary(20), c binary(20));")
        self.execute_sql("insert into t value('-1', 0x2D31, 0x67);")
        self.execute_sql("insert into t value('-1', 0x2D31, 0x73);")
        self.execute_sql("select a from t where a between b and c;")
        self.execute_sql("select a from t where a between b and c;")
        self.execute_sql("insert into mysql.expr_pushdown_blacklist values('cast', 'tikv','');")
        self.execute_sql("admin reload expr_pushdown_blacklist;")
        self.execute_sql("select a from t where a between b and c;")
    
    """
        self.assertEqual(Case.gen_execute_lines("TIBUG-2208", "Results are different for cast when it's pushed down", None,
                                                ['drop table if exists t;', 'create table t(a char(20), b binary(20), c binary(20));',
                                                 "insert into t value('-1', 0x2D31, 0x67);", "insert into t value('-1', 0x2D31, 0x73);",
                                                 'select a from t where a between b and c;', 'select a from t where a between b and c;',
                                                 "insert into mysql.expr_pushdown_blacklist values('cast', 'tikv','');",
                                                 'admin reload expr_pushdown_blacklist;', 'select a from t where a between b and c;']), res_tibug_2208)


if __name__ == "__main__":
    unittest.main()
