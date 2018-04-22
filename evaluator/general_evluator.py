import evaluator.python_evaluator as python_evaluator
import evaluator.java_evaluator as java_evaluator


class GeneralEvaluator:
    def __init__(self, in_file, language):
        self.input = in_file
        self.language = language

    def get_info(self,file):
        result = []
        if self.language == "python":
            python = python_evaluator.PythonGenEval(file)
            details = python.get_lines()
            result.append("Name of source code file: " + file)
            result.append("General Style Information")
            result.append("-Source Language: Python")
            result.append("-Number of Classes: %s" % details.get("number_of_classes"))
            result.append("-Number of Functions: %s" % details.get("number_of_methods"))
            result.append("-Total No. of lines in source: %s" % details.get("total_lines"))
            result.append("-No. of lines of Code: %s" % details.get("lines_of_code"))
            result.append("-No. of blank lines: %s" % details.get("blank_lines"))
            result.append("-No. of lines of comments: %s" % details.get("lines_of_comments"))
            result.append("-Percentage of lines of comments: %s" % details.get("percent_comments"))
            result.append("-Longest Line: %s" % details.get("longest_line"))
            result.append("-Length of longest line: %s" % details.get("length_long_line"))
            # print(python.get_lines())
            result.append("\n")
            result.append("Style Evaluation")
            style = python.get_style_eval()
            if len(style) < 1:
                result.append("No Style Errors")
            else:
                result.extend(style)
        #     docstrings are counted as line of code rather than comment because
        #  Normally a comment would be discarded by the compiler, but docstrings are parsed:

        elif self.language == "java":
            java = java_evaluator.JavaGenEval(file)
            details = java.get_lines()
            result.append("Name of source code file: " + file)
            result.append("General Style Information")
            result.append("-Source Language: Java")
            result.append("-Number of Classes: %s" % details.get("number_of_classes"))
            result.append("-Number of Methods: %s" % details.get("number_of_methods"))
            result.append("-Total No. of lines in source: %s" % details.get("total_lines"))
            result.append("-No. of lines of Code: %s" % details.get("lines_of_code"))
            result.append("-No. of blank lines: %s" % details.get("blank_lines"))
            result.append("-No. of lines of comments: %s" % details.get("lines_of_comments"))
            result.append("-Percentage of lines of comments: %s" % details.get("percent_comments"))
            result.append("-Longest Line: %s" % details.get("longest_line"))
            result.append("-Length of longest line: %s" % details.get("length_long_line"))
            result.append("-Number of variables: %s" % details.get("number_of_variables"))
            result.append("-Number of single character variable names: %s" % details.get("number_of_single"))
            result.append("-Number of other variables: %s" % details.get("number_of_other"))
            result.append("\n")
            result.append("Style Evaluation")
            style = java.get_style_eval()
            if len(style) < 1:
                result.append("No Style Errors")
            else:
                result.extend(style)
        return result
