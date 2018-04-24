import javalang
import math
import re

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
        self.loops = {}
        self.conds = {}
        self.tree = javalang.parse

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
                if len(l) > length_long_line:
                    longest_line = i + 1
                    length_long_line = len(l)
                if len(l.rstrip()) > 100:
                    self.long_lines[i+1] = len(l.rstrip())

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

        # use class variabale to ensure code is parsed only once
        self.tree = javalang.parse.parse(self.source)
        self.classes = self.get_classes()
        self.methods = self.get_methods()
        self.variables = self.get_variables()
        self.loops = self.get_loops()
        self.conds = self.get_conds()

        self.details = {"total_lines": str((i + 1)), "lines_of_code": str(lines_of_code), "blank_lines": str(blank_lines),
                   "lines_of_comments": str(lines_of_comments), "longest_line": str(longest_line),
                   "length_long_line": str(length_long_line), "percent_comments": percent_comments,
                    "number_of_classes": str(len(self.classes)), "number_of_methods": str(len(self.methods)),
                    "number_of_variables": self.variables.get("number"), "number_of_single": str(len(self.variables.get("single"))),
                    "number_of_other": str(len(self.variables.get("other"))), "number_of_constants": str(len(self.variables.get("constants"))),
                    "number_of_for": str(self.loops.get("For",0)),
                    "number_of_while": str(self.loops.get("While",0)),"number_of_dowhile": str(self.loops.get("DoWhile",0)),
                    "number_of_if": str(self.conds.get("if",0)),"number_of_switch": str(self.conds.get("Switch",0))}

        return self.details

    def get_classes(self):
        classes = {}
        index = 0
        classes["info"] = []
        for path, node in self.tree.filter(javalang.tree.ClassDeclaration):
            classes[index] = node.name
            index += 1
        return classes

    def get_methods(self):
        methods = {}
        index = 0
        for path,node in self.tree.filter(javalang.tree.MethodDeclaration):
            methods[index] = node.name
            index += 1
        return methods

    def get_loops(self):
        # create dict to store count of different types of loops
        loops = {}
        for path,node in self.tree.filter(javalang.tree.ForStatement):
            loops["For"] = loops.get("For", 0) + 1
        for path,node in self.tree.filter(javalang.tree.DoStatement):
            loops["DoWhile"] = loops.get("DoWhile", 0) + 1
        for path,node in self.tree.filter(javalang.tree.WhileStatement):
            loops["While"] = loops.get("While", 0) + 1
        return loops

    def get_conds(self):
        # create dict to store count of different types of conditional statements
        conds = {}
        for path,node in self.tree.filter(javalang.tree.IfStatement):
            conds["if"] = conds.get("if", 0) + 1
        for path,node in self.tree.filter(javalang.tree.SwitchStatementCase):
            conds["Switch"] = conds.get("Switch", 0) + 1
        return conds

    def get_variables(self):
        variables = {}
        constants = []
        tokens = list(javalang.tokenizer.tokenize(self.source))
        x = 0
        while x < len(tokens):
            # get basic type varibales, not methods, and not assignments
            if type(tokens[x]) is javalang.tokenizer.BasicType \
                    and not type(tokens[x - 1]) is javalang.tokenizer.Modifier \
                    and not type(tokens[x - 2]) is javalang.tokenizer.Operator:
                if type(tokens[x + 1]) is javalang.tokenizer.Identifier:
                    typename = "(type)" + str(tokens[x].value) + " '" + str(tokens[x + 1].value)+"'"
                    variables[typename] = [str(tokens[x + 1].value), tokens[x + 1].position]
                else:
                    c = x + 2
                    while c < len(tokens) and not type(tokens[c]) is javalang.tokenizer.Identifier:
                        c += 1
                    typename = "(type)" + str(tokens[x].value) + " '" + str(tokens[c].value)+"'"
                    variables[typename] = [str(tokens[c].value), tokens[x + 1].position]

            # get non basic type variables like string
            elif type(tokens[x]) is javalang.tokenizer.Identifier \
                    and type(tokens[x - 1]) is not javalang.tokenizer.Modifier \
                    and type(tokens[x - 2]) is not javalang.tokenizer.Operator:
                # regular strings
                if type(tokens[x + 1]) is javalang.tokenizer.Identifier:
                    typename = "(type)" + str(tokens[x].value) + " '" + str(tokens[x + 1].value)+"'"
                    variables[typename] = [str(tokens[x + 1].value), tokens[x + 1].position]
            # get constant variables
            elif type(tokens[x]) is javalang.tokenizer.Modifier and str(tokens[x].value) == "final":
                c = x + 1
                # variable name is the value before the '=' operator
                while c < len(tokens) and str(tokens[c].value) != "=":
                    c += 1
                constants.append([str(tokens[c-1].value), tokens[c-1].position])
            # get class names this is to provide line info since tree doesnt provide it
            elif type(tokens[x]) is javalang.tokenizer.Keyword and str(tokens[x].value) == "class":
                c = x + 1
                # class name is the value before the '{' operator
                while c < len(tokens) and str(tokens[c].value) != "{":
                    c += 1
                self.classes["info"].append([str(tokens[c-1].value), tokens[c-1].position])
            x = x + 1

        list_vars = list(variables.values())
        single_letter = [x for x in list_vars if len(x[0]) == 1]
        others = [x for x in list_vars if len(x[0]) != 1]
        return {"single": single_letter, "other": others, "number": str(len(list_vars) + len(constants)),
                "constants": constants}

    # method to collate style evaluation
    def get_style_eval(self):
        self.style.extend(self.get_long_lines())
        # print(self.classes)

        # regex for constants
        con_pattern = re.compile("^[A-Z]+(?:_[A-Z]+)*$")
        for name in self.variables.get("constants"):
            if not con_pattern.match(name[0]):
                self.style.append("line:%s pos:%s Error: constant name '%s' should use CONSTANT_CASE"
                                  % (str(math.ceil(name[1][0]/2)), str(name[1][1]), name[0]))

        #  regex for variables
        var_pattern = re.compile("^[_$a-z][\w$]*$")
        # single name variable not checked
        for name in self.variables.get("other"):
            if not var_pattern.match(name[0]):
                # divide line by two and round up as javalange counts lines in 2s
                self.style.append("line:%s pos:%s Error: variable name '%s' should use lower camelCase"
                                  % (str(math.ceil(name[1][0]/2)), str(name[1][1]), name[0]))
        # regex for class names
        class_pattern = re.compile("^(?:[A-Z][a-z]+)+$")
        # single name variable not checked
        for name in self.classes.get("info"):
            if not class_pattern.match(name[0]):
                # divide line by two and round up as javalange counts lines in 2s
                self.style.append("line:%s pos:%s Error: class name '%s' should use upper CamelCase"
                                  % (str(math.ceil(name[1][0]/2)), str(name[1][1]), name[0]))
        return sorted(self.style)

    def get_long_lines(self):
        result = []
        for key, value in self.long_lines.items():
            result.append("line:%s pos:101 Error: line too long (%d > 100 characters)" % (key, value))
        return result

# any(c.isupper() for c in test)
# any(c.islower() for c in test)

