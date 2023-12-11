import dataclasses
import unittest
from DataModels import Recommendation, RecommendHeader, AuditCmd, CISControl, CISControlFamily


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
        self.audit_cmd = AuditCmd(command='ls -l', expected_output='rw-r-x folder1')

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
        self.recommend_id = 'H-1.1.1'
        self.level = 1
        self.title = 'Header Title'
        self.description = 'Header Description'

    def create_recommend_header(self):
        return RecommendHeader(recommend_id=self.recommend_id,
                               level=self.level,
                               title=self.title,
                               description=self.description)

    def test_create_recommend_header(self):
        recommend_header = self.create_recommend_header()
        self.assertEqual(self.recommend_id, recommend_header.recommend_id)
        self.assertEqual(self.level, recommend_header.level)
        self.assertEqual(self.title, recommend_header.title)
        self.assertEqual(self.description, recommend_header.description)

    def test_create_invalid_types(self):
        invalid_values = {
            'recommend_id': 1,
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
            RecommendHeader(recommend_id=self.recommend_id,
                            level=self.level,
                            title=self.title)

    def test_immutability_recommend_header(self):
        header = RecommendHeader(recommend_id='H-1.1.1',
                                 level=1,
                                 title='Header Title',
                                 description='Header Description')
        with self.assertRaises(dataclasses.FrozenInstanceError):
            header.title = 'New Title'

    def test_edge_case_long_title(self):
        long_title = 'a' * 1000
        recommendation = RecommendHeader(recommend_id=self.recommend_id,
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


class TestAuditCmd(unittest.TestCase):
    def setUp(self):
        self.command = "ls -l | grep -q 'auditcmd'"
        self.expected_output = "true"

    def create_auditcmd(self):
        return AuditCmd(command=self.command, expected_output=self.expected_output)

    def test_create_auditcmd(self):
        audit_cmd = self.create_auditcmd()
        self.assertEqual(self.command, audit_cmd.command)
        self.assertEqual(self.expected_output, audit_cmd.expected_output)

    def test_create_invalid_types(self):
        invalid_values = {
            'command': 1,
            'expected_output': 1
        }
        for attr, invalid_value in invalid_values.items():
            setattr(self, attr, invalid_value)
            with self.assertRaises(TypeError):
                self.create_auditcmd()

    def test_missing_required_attributes(self):
        with self.assertRaises(TypeError):
            AuditCmd(command=self.command)

    def test_immutability_auditcmd(self):
        audit_cmd = AuditCmd(command=self.command, expected_output=self.expected_output)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            audit_cmd.command = 'New Command'

    def test_edge_case_long_cmd(self):
        long_cmd = 'a' * 1000
        audit_cmd = AuditCmd(command=long_cmd, expected_output='true')
        self.assertEqual(long_cmd, audit_cmd.command)

    def test_equality_of_instances(self):
        audit_cmd1 = self.create_auditcmd()
        audit_cmd2 = self.create_auditcmd()
        self.assertEqual(audit_cmd1, audit_cmd2)

    def test_hashability(self):
        audit_cmd_set = {self.create_auditcmd(), self.create_auditcmd()}
        self.assertEqual(len(audit_cmd_set), 1)


class TestCISControl(unittest.TestCase):
    def setUp(self):
        self.safeguard_id = '1.1.1'
        self.asset_type = 'devices'
        self.domain = 'detect'
        self.title = 'CISControl Title'
        self.description = 'CISControl Description'

    def create_cis_control(self):
        return CISControl(safeguard_id=self.safeguard_id, asset_type=self.asset_type,
                          domain=self.domain, title=self.title, description=self.description)

    def test_create_cis_control(self):
        cis_control = self.create_cis_control()
        self.assertEqual(self.safeguard_id, cis_control.safeguard_id)
        self.assertEqual(self.asset_type, cis_control.asset_type)
        self.assertEqual(self.domain, cis_control.domain)
        self.assertEqual(self.title, cis_control.title)
        self.assertEqual(self.description, cis_control.description)

    def test_create_invalid_types(self):
        invalid_values = {
            'safeguard_id': 1,
            'asset_type': 1,
            'domain': 1,
            'title': 1,
            'description': 1
        }
        for attr, invalid_value in invalid_values.items():
            setattr(self, attr, invalid_value)
            with self.assertRaises(TypeError):
                self.create_cis_control()

    def test_missing_required_attributes(self):
        with self.assertRaises(TypeError):
            CISControl(safeguard_id=self.safeguard_id, asset_type=self.asset_type, domain=self.domain, title=self.title)

    def test_immutability_cis_control(self):
        cis_control = CISControl(safeguard_id=self.safeguard_id, asset_type=self.asset_type,
                                 domain=self.domain, title=self.title, description=self.description)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            cis_control.safeguard_id = '1.2.3'

    def test_edge_case_long_cis_control_title(self):
        long_cis_control_title = 'a' * 1000
        cis_control = CISControl(safeguard_id=self.safeguard_id, asset_type=self.asset_type,
                                 domain=self.domain, title=long_cis_control_title, description=self.description)
        self.assertEqual(long_cis_control_title, cis_control.title)

    def test_equality_of_instances(self):
        cis_control1 = self.create_cis_control()
        cis_control2 = self.create_cis_control()
        self.assertEqual(cis_control1, cis_control2)

    def test_hashability(self):
        cis_control_set = {self.create_cis_control(), self.create_cis_control()}
        self.assertEqual(len(cis_control_set), 1)


class TestCISControlFamily(unittest.TestCase):
    def setUp(self):
        self.title = 'CISControlFamily Title'
        self.description = 'CISControlFamily Description'

    def create_cis_control_family(self):
        return CISControlFamily(title=self.title, description=self.description)

    def test_create_cis_control_family(self):
        cis_control_family = self.create_cis_control_family()
        self.assertEqual(self.title, cis_control_family.title)
        self.assertEqual(self.description, cis_control_family.description)

    def test_create_invalid_types(self):
        invalid_values = {
            'title': 1,
            'description': 1
        }
        for attr, invalid_value in invalid_values.items():
            setattr(self, attr, invalid_value)
            with self.assertRaises(TypeError):
                self.create_cis_control_family()

    def test_missing_required_attributes(self):
        with self.assertRaises(TypeError):
            CISControlFamily(title=self.title)

    def test_immutability_cis_control_family(self):
        cis_control_family = CISControlFamily(title=self.title, description=self.description)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            cis_control_family.title = 'New CISControlFamily Title'

    def test_edge_case_long_cis_control_family(self):
        long_cis_control_family_title = 'a' * 1000
        cis_control_family = CISControlFamily(title=long_cis_control_family_title, description=self.description)
        self.assertEqual(long_cis_control_family_title, cis_control_family.title)

    def test_equality_of_instances(self):
        cis_control_family1 = self.create_cis_control_family()
        cis_control_family2 = self.create_cis_control_family()
        self.assertEqual(cis_control_family1, cis_control_family2)

    def test_hashability(self):
        cis_control_family_set = {self.create_cis_control_family(), self.create_cis_control_family()}
        self.assertEqual(len(cis_control_family_set), 1)


if __name__ == '__main__':
    run_tests(TestRecommendation)
    run_tests(TestRecommendHeader)
    run_tests(TestAuditCmd)
    run_tests(TestCISControl)
    run_tests(TestCISControlFamily)
