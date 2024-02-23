import unittest
from report import TextReport
from statistics import Statistics,UserResult

class TestTextReport(unittest.TestCase):
    def test_all_success(self):
        s = Statistics(
            user1=UserResult('user1', 1, 0),
            user2=UserResult('user2', 1, 0)
        )
        r = TextReport(s)
        title, content = r.build()
        self.assertIn('成功', title)

    def test_has_failure(self):
        s = Statistics(
            user1=UserResult('user1', 1, 0),
            user2=UserResult('user2', 1, 1))

        r = TextReport(s)
        title, content = r.build()
        self.assertIn('失败', title)

if __name__ == '__main__':
    unittest.main()