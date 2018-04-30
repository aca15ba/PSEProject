import unittest
import evaluator.evaluator as evaluator
from io import StringIO
from unittest.mock import patch


class CommandLineTest(unittest.TestCase):
    def setUp(self):
        self.parser = evaluator.create_parser()
        self.patcher1 = patch('sys.stdout', new=StringIO())
        self.patcher2 = patch('sys.stderr', new=StringIO())
        self.patcher1.start()
        self.patcher2.start()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    # File or Folder not supplied
    def test_no_args(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args([])
            command = evaluator.CommandLine(self.parser, args)
            self.assertIn("You need to supply input file or folder", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)

    # File test
    # File exists
    def test_input_file(self):
        args = self.parser.parse_args(["-f", "setup.py"])
        command = evaluator.CommandLine(self.parser, args)
        self.assertEqual(args.file, command.in_file)
        self.assertIsNone(args.folder)
        self.assertEqual("setup_py.txt", command.out_file)
        self.assertEqual("python", command.language)

    # File does not exist
    def test_input_file_not_exist(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args(["-f", "no_file.py"])
            command = evaluator.CommandLine(self.parser, args)
            self.assertIn("File supplied does not exist", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)

    # File name not valid
    def test_invalid_file_name(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args(["-f", "no_file"])
            command = evaluator.CommandLine(self.parser, args)
            self.assertIn("File name not valid", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)

    # Language supplied does not match file
    def test_language_match(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args(["-f", "no_file.py", "-l", "html"])
            command = evaluator.CommandLine(self.parser, args)
            self.assertEqual("Language does not match file", command.language)
            self.assertIn("Language does not match file", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)

    # file language not currently supported
    def test_language_support(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args(["-f", "no_file.rb"])
            command = evaluator.CommandLine(self.parser, args)
            self.assertEqual("Language not supported", command.language)
            self.assertIn("Language not supported", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)

    # Folder test
    # the default is python, and there are python files in test
    def test_input_folder(self):
        args = self.parser.parse_args(["-F", "test"])
        command = evaluator.CommandLine(self.parser, args)
        # self.assertEqual(args.folder, command.in_file)
        self.assertIsNone(args.file)
        self.assertEqual("test.txt", command.out_file)
        self.assertEqual("python", command.language)

    # folder supplied does not exist
    def test_input_folder_not_exist(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args(["-F", "not_exist"])
            command = evaluator.CommandLine(self.parser, args)
            self.assertIn("Folder supplied does not exist", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)

    # no matching files found in folder
    def test_no_matching_files(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args(["-F", "tests"])
            command = evaluator.CommandLine(self.parser, args)
            self.assertIn("No matching files in folder supplied", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)

    # language not supported
    def test_language_not_supported(self):
        with self.assertRaises(SystemExit) as cm:
            args = self.parser.parse_args(["-F", "not_exist", "-l", "html"])
            command = evaluator.CommandLine(self.parser, args)
            self.assertIn("Language not supported", self.patcher1.getvalue().strip())
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 1)


# unit test class for FileManager test output file and language methods
class FileManagerTest(unittest.TestCase):
    def setUp(self):
        self.file = evaluator.FileManager("file.py")
        self.file1 = evaluator.FileManager("file.java")
        self.file2 = evaluator.FileManager("file.rb")

    # test output file name creation
    def test_get_output_file(self):
        self.assertEqual(self.file.get_output_file(), "file_py.txt")
        self.assertEqual(self.file1.get_output_file(), "file_java.txt")

    # test language getter, wrong when language not supported
    def test_get_language(self):
        self.assertEqual(self.file.get_language(), "python")
        self.assertEqual(self.file1.get_language(), "java")
        self.assertEqual(self.file2.get_language(), "wrong")


if __name__ == '__main__':
    unittest.main()
