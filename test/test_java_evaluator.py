import unittest
import evaluator.java_evaluator as GenEVal


class JavaGenEvalTest(unittest.TestCase):
    def setUp(self):
        self.file = "test_files/BeanMachine.java"
        self.java = GenEVal.JavaGenEval(self.file)

    def tearDown(self):
        self.file = ""
        self.java = None

    def test_get_lines(self):
        details = self.java.get_lines()
        self.assertEqual("174", details.get("total_lines"))
        self.assertEqual("119", details.get("lines_of_code"))
        self.assertEqual("29", details.get("lines_of_comments"))
        self.assertEqual("26", details.get("blank_lines"))
        self.assertEqual("21", details.get("longest_line"))
        self.assertEqual("118", details.get("length_long_line"))
        self.assertEqual("16.67%", details.get("percent_comments"))
        self.assertEqual("2", details.get("number_of_classes"))
        self.assertEqual("6", details.get("number_of_methods"))
        self.assertEqual("27", details.get("number_of_variables"))
        self.assertEqual("16", details.get("number_of_other"))
        self.assertEqual("6", details.get("number_of_single"))
        self.assertEqual("5", details.get("number_of_constants"))
        self.assertEqual("6", details.get("number_of_for"))
        self.assertEqual("0", details.get("number_of_while"))
        self.assertEqual("1", details.get("number_of_dowhile"))
        self.assertEqual("0", details.get("number_of_switch"))
        self.assertEqual("7", details.get("number_of_if"))
