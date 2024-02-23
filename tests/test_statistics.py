import unittest
from statistics import UserResult

class TestUserResult(unittest.TestCase):
    def test_user_default(self):
        user = UserResult("xxxx")
        self.assertEqual(str(user), "xxxx: 0/0")

    def test_user_default_increment_is_1(self):
        user1 = UserResult("user1")
        user1.add_success()
        user1.add_failure()
        user1.add_failure()
        self.assertEqual(str(user1), "user1: 1/3")
    def test_user_increment_can_be_set(self):
        user2 = UserResult("user2")
        user3 = UserResult("user3")

        user2.add_success(2)
        user2.add_failure(3)
        user3.add_success(4)
        user3.add_failure(6)


        self.assertEqual(str(user2), "user2: 2/5")
        self.assertEqual(str(user3), "user3: 4/10")


if __name__ == '__main__':
    unittest.main()
