import unittest
import evaluator.evaluator as evaluator


class CommandLineTest(unittest.TestCase):
    def setUp(self):
        self.parser = evaluator.create_parser()

    def test_input_file(self):
        args = self.parser.parse_args(["-f", "setup.py"])
        command = evaluator.CommandLine(self.parser, args)
        self.assertEqual(args.file, command.in_file)
        self.assertIsNone(args.folder)
        self.assertEqual("setup_py.txt", command.out_file)
        self.assertEqual("python", command.language)


class FileManagerTest(unittest.TestCase):
    def setUp(self):
        self.file = evaluator.FileManager("file.py")
        self.file1 = evaluator.FileManager("file.java")

    def test_get_output_file(self):
        self.assertEqual(self.file.get_output_file(), "file_py.txt")
        self.assertEqual(self.file1.get_output_file(), "file_java.txt")

    def test_get_language(self):
        self.assertEqual(self.file.get_language(), "python")
        self.assertEqual(self.file1.get_language(), "java")




if __name__ == '__main__':
    unittest.main()
