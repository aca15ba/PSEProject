import unittest
import evaluator.python_evaluator as GenEVal


class PythonGenEvalTest(unittest.TestCase):
    def setUp(self):
        self.file = "test_files/evaluator.py"
        self.python = GenEVal.PythonGenEval(self.file,"test_files/evaluator_py.txt")

    def tearDown(self):
        self.file = ""
        self.java = None

    def test_get_lines(self):
        details = self.python.get_lines()
        self.assertEqual("189", details.get("total_lines"))
        self.assertEqual("162", details.get("lines_of_code"))
        self.assertEqual("4", details.get("lines_of_comments"))
        self.assertEqual("23", details.get("blank_lines"))
        self.assertEqual("181", details.get("longest_line"))
        self.assertEqual("133", details.get("length_long_line"))
        self.assertEqual("2.12%", details.get("percent_comments"))
        self.assertEqual("3", details.get("number_of_classes"))
        self.assertEqual("10", details.get("number_of_methods"))
