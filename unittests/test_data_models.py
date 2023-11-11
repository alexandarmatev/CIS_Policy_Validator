import unittest
from DataModels import Control, Header


def run_tests(test_class):
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)


class TestControl(unittest.TestCase):
    def setUp(self):
        self.control_id = '1.1.1'
        self.title = 'Control Title'
        self.description = 'Control Description'
        self.level = 1
        self.audit_cmd = 'ls -l | grep -q "audit"'

    def create_control(self):
        return Control(control_id=self.control_id,
                       title=self.title,
                       description=self.description,
                       level=self.level,
                       audit_cmd=self.audit_cmd)

    def test_create_control(self):
        control = self.create_control()
        self.assertEqual(self.control_id, control.control_id)
        self.assertEqual(self.title, control.title)
        self.assertEqual(self.description, control.description)
        self.assertEqual(self.level, control.level)
        self.assertEqual(self.audit_cmd, control.audit_cmd)


run_tests(TestControl)