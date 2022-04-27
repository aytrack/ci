import unittest

from version import Version


class TestVersion(unittest.TestCase):

    def test_branch(self):
        v = Version("v5.0.1")
        self.assertEqual(v.branch(), "5.0")

        v = Version("v5.1.0")
        self.assertEqual(v.branch(), "5.1")

    def test_less(self):
        s = [("v5.0.1", "v5.0.0", False),
             ("v5.0.0", "v4.0.16", False),
             ("v5.0.1", "v5.0.5", True),
             ("v5.0.0", "v6.1.0", True),
             ("v5.0.0", "v6.0.0", True)]
        for item in s:
            self.assertEqual(Version(item[0]).less(Version(item[1])), item[2])

    def test_is_branch(self):
        s = [("v5.2.0", True),
             ("v5.1.1", False),
             ("v4.0.0", True)]
        for item in s:
            self.assertEqual(Version(item[0]).is_branch(), item[1])

    def test_is_adjacent(self):
        s = [("v5.0.1", "v5.0.0", True),
             ("v5.0.0", "v4.0.16", False),
             ("v5.0.1", "v5.0.2", True),
             ("v5.0.0", "v6.1.0", False),
             ("v5.0.0", "v6.0.0", False)]
        for item in s:
            self.assertEqual(Version(item[0]).is_adjacent(Version(item[1])), item[2])

    def test_is_branch_adjacent(self):
        s = [("v5.0.1", "v5.1.0", True),
             ("v5.0.1", "v5.2.2", False),
             ("v5.0.0", "v6.1.0", False)]
        for item in s:
            self.assertEqual(Version(item[0]).is_branch_adjacent(Version(item[1])), item[2])


if __name__ == "__main__":
    unittest.main()
