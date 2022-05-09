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


if __name__ == "__main__":
    unittest.main()
