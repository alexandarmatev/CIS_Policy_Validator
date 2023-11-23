import dataclasses
import unittest
from DataModels import Recommendation, RecommendHeader


def run_tests(test_class):
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)


class TestRecommendation(unittest.TestCase):
    def setUp(self):
        self.recommend_id = '1.1.1'
        self.level = 1
        self.title = 'Control Title'
        self.rationale = 'Rationale Statement'
        self.impact = 'Impact Statement'
        self.safeguard_id = '7.3'
        self.assessment_method = 'Automated'
        self.audit_cmd = 'ls -l | grep -q "audit"'

    def create_recommendation(self):
        return Recommendation(recommend_id=self.recommend_id,
                              level=self.level,
                              title=self.title,
                              rationale=self.rationale,
                              impact=self.impact,
                              safeguard_id=self.safeguard_id,
                              assessment_method=self.assessment_method,
                              audit_cmd=self.audit_cmd)

    def test_create_recommendation(self):
        recommendation = self.create_recommendation()
        self.assertEqual(self.recommend_id, recommendation.recommend_id)
        self.assertEqual(self.level, recommendation.level)
        self.assertEqual(self.rationale, recommendation.rationale)
        self.assertEqual(self.title, recommendation.title)
        self.assertEqual(self.impact, recommendation.impact)
        self.assertEqual(self.safeguard_id, recommendation.safeguard_id)
        self.assertEqual(self.assessment_method, recommendation.assessment_method)
        self.assertEqual(self.audit_cmd, recommendation.audit_cmd)

    def test_create_invalid_types(self):
        invalid_values = {
            'recommend_id': 1,
            'level': '1',
            'title': 1,
            'rationale': 1,
            'impact': 1,
            'safeguard_id': 1,
            'assessment_method': 1,
            'audit_cmd': 1
        }
        for attr, invalid_value in invalid_values.items():
            setattr(self, attr, invalid_value)
            with self.assertRaises(TypeError):
                self.create_recommendation()

    def test_null_value_for_optional_attribute(self):
        recommendation = Recommendation(recommend_id=self.recommend_id,
                                        level=self.level,
                                        title=self.title,
                                        rationale=self.rationale,
                                        impact=self.impact,
                                        safeguard_id=self.safeguard_id,
                                        assessment_method=self.assessment_method,
                                        audit_cmd=None)
        self.assertIsNone(recommendation.audit_cmd)

    def test_default_value_audit_cmd(self):
        recommendation = Recommendation(recommend_id=self.recommend_id,
                                        level=self.level,
                                        title=self.title,
                                        rationale=self.rationale,
                                        impact=self.impact,
                                        safeguard_id=self.safeguard_id,
                                        assessment_method=self.assessment_method)
        self.assertIsNone(recommendation.audit_cmd)

    def test_missing_required_attributes(self):
        with self.assertRaises(TypeError):
            Recommendation(recommend_id=self.recommend_id,
                           level=self.level,
                           title=self.title,
                           rationale=self.rationale,
                           impact=self.impact,
                           safeguard_id=self.safeguard_id)

    def test_edge_case_long_title(self):
        long_title = 'a' * 1000
        recommendation = Recommendation(recommend_id=self.recommend_id,
                                        level=self.level,
                                        title=long_title,
                                        rationale=self.rationale,
                                        impact=self.impact,
                                        safeguard_id=self.safeguard_id,
                                        assessment_method=self.assessment_method)
        self.assertEqual(long_title, recommendation.title)

    def test_attribute_mutability(self):
        recommendation = self.create_recommendation()
        new_title = 'Updated Title'
        recommendation.title = new_title
        self.assertEqual(new_title, recommendation.title)

    def test_equality_of_instances(self):
        recommendation1 = self.create_recommendation()
        recommendation2 = self.create_recommendation()
        self.assertEqual(recommendation1, recommendation2)


class TestRecommendHeader(unittest.TestCase):
    def setUp(self):
        self.header_id = 'H-1.1.1'
        self.level = 1
        self.title = 'Header Title'
        self.description = 'Header Description'

    def create_recommend_header(self):
        return RecommendHeader(header_id=self.header_id,
                               level=self.level,
                               title=self.title,
                               description=self.description)

    def test_create_recommend_header(self):
        recommend_header = self.create_recommend_header()
        self.assertEqual(self.header_id, recommend_header.header_id)
        self.assertEqual(self.level, recommend_header.level)
        self.assertEqual(self.title, recommend_header.title)
        self.assertEqual(self.description, recommend_header.description)

    def test_create_invalid_types(self):
        invalid_values = {
            'header_id': 1,
            'level': '1',
            'title': 1,
            'description': 1,
        }
        for attr, invalid_value in invalid_values.items():
            setattr(self, attr, invalid_value)
            with self.assertRaises(TypeError):
                self.create_recommend_header()

    def test_missing_required_attributes(self):
        with self.assertRaises(TypeError):
            RecommendHeader(header_id=self.header_id,
                            level=self.level,
                            title=self.title)

    def test_immutability_recommend_header(self):
        header = RecommendHeader(header_id='H-1.1.1',
                                 level=1,
                                 title='Header Title',
                                 description='Header Description')
        with self.assertRaises(dataclasses.FrozenInstanceError):
            header.title = 'New Title'

    def test_edge_case_long_title(self):
        long_title = 'a' * 1000
        recommendation = RecommendHeader(header_id=self.header_id,
                                         level=self.level,
                                         title=long_title,
                                         description=self.description)
        self.assertEqual(long_title, recommendation.title)

    def test_equality_of_instances(self):
        header1 = self.create_recommend_header()
        header2 = self.create_recommend_header()
        self.assertEqual(header1, header2)

    def test_hashability(self):
        header_set = {self.create_recommend_header(), self.create_recommend_header()}
        self.assertEqual(len(header_set), 1)


if __name__ == '__main__':
    run_tests(TestRecommendation)
    run_tests(TestRecommendHeader)
