import javalang


class JavaGenEval:
    def __init__(self, in_file):
        self.file = in_file
        self.details = {}
        self.code = []
        self.classes = {}
        self.methods = {}
        self.variables = {}
        self.source = ""
        self.style = []
        self.long_lines = {}

    def get_lines(self):
        lines_of_code = 0
        lines_of_comments = 0
        blank_lines = 0
        longest_line = 0
        length_long_line = 0
        percent_comment = 0
        multiline = False

        with open(self.file) as f:

            # i is total lines
            # whitespace is included in length of a line as when printed space is also included;
            # purpose of length of line guideline is to ensure readability
            for i, l in enumerate(f):
                self.code.append(l)
                index = i
                line = l.strip()
                if len(l.rstrip()) > 100:
                    self.long_lines[i+1] = len(l.rstrip())
                if len(l) > length_long_line:
                    longest_line = i + 1
                    length_long_line = len(l)

                # count lines of comments
                if line.startswith("//") and not multiline:
                    lines_of_comments += 1
                elif (line.startswith("*/") or line.endswith("*/")) and multiline:
                    multiline = False
                    lines_of_comments += 1
                # ignore javadoc
                elif (line.startswith("/*") and not line.startswith("/**"))or multiline :
                    multiline = True
                    lines_of_comments += 1
                elif line == "" and not multiline:
                    blank_lines += 1
                else:
                    lines_of_code += 1

        self.source = "\n".join(self.code)
        percent_comment = lines_of_comments * 100 / (i + 1)
        percent_comments = str("%.2f" % percent_comment) + "%"

        self.classes = self.get_classes()
        self.methods = self.get_methods()
        self.variables = self.get_variables()

        self.details = {"total_lines": str((i + 1)), "lines_of_code": str(lines_of_code), "blank_lines": str(blank_lines),
                   "lines_of_comments": str(lines_of_comments), "longest_line": str(longest_line),
                   "length_long_line": str(length_long_line), "percent_comments": percent_comments,
                    "number_of_classes": str(len(self.classes)), "number_of_methods": str(len(self.methods)),
                    "number_of_variables": self.variables.get("number"), "number_of_single": str(len(self.variables.get("single"))),
                        "number_of_other": str(len(self.variables.get("other")))}

        return self.details

    def get_classes(self):
        classes = {}
        index = 0
        tree = javalang.parse.parse(self.source)
        for path,node in tree.filter(javalang.tree.ClassDeclaration):
            classes[index] = node.name
            index += 1
        return classes

    def get_methods(self):
        methods = {}
        index = 0
        tree = javalang.parse.parse(self.source)
        for path,node in tree.filter(javalang.tree.MethodDeclaration):
            methods[index] = node.name
            index += 1
        return methods

    def get_variables(self):
        variables = {}
        tokens = list(javalang.tokenizer.tokenize(self.source))
        x = 0

        while x < len(tokens):
            # get basic type varibales, not methods, and not assignments
            if type(tokens[x]) is javalang.tokenizer.BasicType \
                    and not type(tokens[x - 1]) is javalang.tokenizer.Modifier \
                    and not type(tokens[x - 2]) is javalang.tokenizer.Operator:
                if type(tokens[x + 1]) is javalang.tokenizer.Identifier:
                    typename = "(type)" + str(tokens[x].value) + " '" + str(tokens[x + 1].value)+"'"
                    variables[typename] = str(tokens[x + 1].value)
                else:
                    c = x + 2
                    while c < len(tokens) and not type(tokens[c]) is javalang.tokenizer.Identifier:
                        c += 1
                    typename = "(type)" + str(tokens[x].value) + " '" + str(tokens[c].value)+"'"
                    variables[typename] = str(tokens[c].value)

            # get non basic type variables like string
            elif type(tokens[x]) is javalang.tokenizer.Identifier \
                    and type(tokens[x - 1]) is not javalang.tokenizer.Modifier \
                    and type(tokens[x - 2]) is not javalang.tokenizer.Operator:
                if type(tokens[x + 1]) is javalang.tokenizer.Identifier:
                    typename = "(type)" + str(tokens[x].value) + " '" + str(tokens[x + 1].value)+"'"
                    variables[typename] = str(tokens[x + 1].value)
            x = x + 1

        list_vars = list(variables.values())
        single_letter = [x for x in list_vars if len(x) == 1]
        others = [x for x in list_vars if len(x) != 1]
        return {"single": single_letter, "other": others, "number": str(len(list_vars))}

    # method to collate style evaluation
    def get_style_eval(self):
        self.style.extend(self.get_long_lines())
        return self.style

    def get_long_lines(self):
        result = []
        for key, value in self.long_lines.items():
            result.append("Error: line:%s pos:101 line too long (%d > 100 characters)" % (key, value))
        return result

# any(c.isupper() for c in test)
# any(c.islower() for c in test)

# (public|private|protected)\s+(static\s+)?(abstract(?!override)\s+|final\s+)?(\D\w+)\s+(\D\w+)\s*\((\s*\D\w+\s*\D\w+\s*,?)*\)\s*
# /\*.*\n.*\*\/
