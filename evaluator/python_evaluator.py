import pycodestyle
import pyflakes
from flake8.api import legacy as flake

class PythonGenEval:
    def __init__(self, in_file):
        self.file = in_file

    def get_lines(self):
        lines_of_code = 0
        lines_of_comments = 0
        blank_lines = 0
        longest_line = 0
        length_long_line = 0
        percent_comment = 0
        number_of_classes = 0
        number_of_methods = 0
        index = 0
        with open(self.file) as f:
            # i is total lines
            # whitespace is included in length of a line as when printed space is also included;
            # purpose of length of line guideline is to ensure readability
            for i, l in enumerate(f):
                index = i
                line = l.strip()
                if len(l) >= length_long_line:
                    longest_line = i + 1
                    length_long_line = len(l)
                if line.startswith("class "):
                    number_of_classes += 1
                if line.startswith("def "):
                    number_of_methods += 1
                if line.startswith("#"):
                    lines_of_comments += 1
                elif line == "":
                    blank_lines += 1
                else:
                    lines_of_code += 1

                # print(i + 1,l, len(l))
        # print(number_of_classes, number_of_methods)
        percent_comment = lines_of_comments * 100 / (index + 1)
        percent_comments = str("%.2f" % percent_comment) + "%"
        # print(blank_lines, lines_of_comments, lines_of_code)
        # print(longest_line, length_long_line, str( "%.2f" % percent_comments) + "%")
        details = {"total_lines": str((index + 1)), "lines_of_code": str(lines_of_code), "blank_lines": str(blank_lines),
                   "lines_of_comments": str(lines_of_comments), "longest_line": str(longest_line),
                   "length_long_line": str(length_long_line), "percent_comments": percent_comments,
                   "number_of_classes": str(number_of_classes), "number_of_methods": str(number_of_methods)}

        return details

    def get_style_eval(self):
        # f_checker = pycodestyle.Checker(self.file, show_source=False, quiet=True)
        # report = f_checker.report
        # print(report)
        # file_errors = f_checker.check_all()
        # print("Found %s errors (and warnings)" % file_errors)
        style_guide = flake.get_style_guide(
            # quiet=1,
            format='Error: line:%(row)d pos:%(col)d %(text)s',
            output_file="initial.txt"
        )
        report = style_guide.input_file(self.file)
        return []
