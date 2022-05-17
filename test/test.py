import unittest
from app.models import User,Blogs, Comments

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User("Owalla", "owalla@gmail.com", "1234")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_user, User))

    def test_password_setter(self):
        self.assertTrue(self.new_user.password is not None)
    
    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.secure_password

class BlogModelTest(unittest.TestCase):
    def setUp(self):
        self.new_blog = Blogs("Blog Title","Blog Body","User ID")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog, Blogs))


class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comments("User ID","Comment Body"," ID")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comments))

   
if __name__ == '__main__':
    unittest.main()