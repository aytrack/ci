import unittest
from lark import Lark


class TestLark(unittest.TestCase):

    def test_send(self):
        ms = ['''[TIBUG-604](https://internal.pingcap.net/jira/browse/TIBUG-604) issue [27350](https://github.com/pingcap/tidb/issues/27350) exists [] added labels ['affects-4.0', 'affects-5.0', 'affects-5.1']''',
              '''[GH-TIDB-34362](https://github.com/pingcap/tidb/issues/34362) exists [] added labels ['affects-4.0', 'affects-5.0', 'affects-5.1', 'affects-5.2', 'affects-5.3', 'affects-5.4', 'affects-6.0']''']
        Lark().send("issue affect branch", ms)


if __name__ == "__main__":
    unittest.main()
