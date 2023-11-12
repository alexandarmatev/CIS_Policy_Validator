import unittest
from DataModels import Recommendation, RecommendHeader


def run_tests(test_class):
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)


class TestControl(unittest.TestCase):
    def setUp(self):
        self.recommend_id = '1.1.1'
        self.title = 'Control Title'
        self.description = 'Control Description'
        self.level = 1
        self.audit_cmd = 'ls -l | grep -q "audit"'

    def create_recommendation(self):
        return Recommendation(recommend_id=self.recommend_id,
                              title=self.title,
                              description=self.description,
                              level=self.level,
                              audit_cmd=self.audit_cmd)

    def test_create_recommendation(self):
        control = self.create_recommendation()
        self.assertEqual(self.recommend_id, control.recommend_id)
        self.assertEqual(self.title, control.title)
        self.assertEqual(self.description, control.description)
        self.assertEqual(self.level, control.level)
        self.assertEqual(self.audit_cmd, control.audit_cmd)


run_tests(TestControl)
