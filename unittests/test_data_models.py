import unittest
from DataModels import Recommendation, RecommendHeader


def run_tests(test_class):
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)


class TestControl(unittest.TestCase):
    def setUp(self):
        self.recommend_id = '1.1.1'
        self.level = 1
        self.title = 'Control Title'
        self.rationale = 'Rationale Statement'
        self.impact = 'Impact Statement'
        self.assessment_method = 'Automated'
        self.audit_cmd = 'ls -l | grep -q "audit"'

    def create_recommendation(self):
        return Recommendation(recommend_id=self.recommend_id,
                              level=self.level,
                              title=self.title,
                              rationale=self.rationale,
                              impact=self.impact,
                              assessment_method=self.assessment_method,
                              audit_cmd=self.audit_cmd)

    def test_create_recommendation(self):
        recommendation = self.create_recommendation()
        self.assertEqual(self.recommend_id, recommendation.recommend_id)
        self.assertEqual(self.level, recommendation.level)
        self.assertEqual(self.rationale, recommendation.rationale)
        self.assertEqual(self.title, recommendation.title)
        self.assertEqual(self.impact, recommendation.impact)
        self.assertEqual(self.assessment_method, recommendation.assessment_method)
        self.assertEqual(self.audit_cmd, recommendation.audit_cmd)


run_tests(TestControl)
