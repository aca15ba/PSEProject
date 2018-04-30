"""evaluator.evaluator: provides entry point for main and houses verison info"""
import argparse
import sys
import os
import fnmatch
import evaluator.general_evluator as general_evaluator


# Version
__version__ = "3.0.0"


def main():
    """Main class calls functions to parse command line options and
    evaluate the file or folder parsed. Then outputs result to file"""
    print("Programme style evaluator")
    # Create the parser and parse arguments
    parser = create_parser()
    args = parser.parse_args()
    config = CommandLine(parser, args)
    # Create file evaluator and evaluate file(s)
    general = general_evaluator.GeneralEvaluator(config.in_file, config.language)
    if config.is_folder:
        result = {}
        for file in config.in_file:
            result[file] = (general.get_info(file,config.out_file))
    else:
        result = general.get_info(config.in_file, config.out_file)

    # print style report to file
    all_results = ResultStore(config.out_file)
    if config.is_folder:
        for file in result:
            all_results.store(result[file])
            all_results.output()
    else:
        all_results.store(result)
        all_results.output()


class CommandLine:
    """Command line class: used for parsing and validating user input
    returns configuration for style evaluator"""
    def __init__(self, parser, args):
        self.is_folder = False
        if args.file:
            if not os.path.exists(args.file):
                print("File supplied does not exist")
                parser.print_help(sys.stderr)
                sys.exit(1)
            elif '.' not in args.file:
                print("File name not valid")
                parser.print_help(sys.stderr)
                sys.exit(1)
            file = FileManager(args.file)
            file_lang = file.get_language()
            self.in_file = args.file

            if args.language:
                if args.language == file_lang:
                    self.language = file_lang
                else:
                    self.language = "Language does not match file"
                    print(self.language)
                    parser.print_help(sys.stderr)
                    sys.exit(1)
            else:
                if file_lang == "wrong":
                    self.language = "Language not supported"
                    print(self.language)
                    parser.print_help(sys.stderr)
                    sys.exit(1)
                else:
                    self.language = file_lang
            print("Input file: " + self.in_file)
            print("Language: " + self.language)

            if args.output:
                if ".txt" in args.output:
                    self.out_file = str(args.output)
                else:
                    self.out_file = str(args.output) + ".txt"
            else:
                self.out_file = file.get_output_file()
            print("Output file: " + self.out_file)

        elif args.folder:
            self.is_folder = True
            self.in_file = []
            if not os.path.exists(args.folder):
                print("Folder supplied does not exist")
                parser.print_help(sys.stderr)
                sys.exit(1)
            if args.language:
                if args.language == "python":
                    self.language = args.language
                    for file in os.listdir(args.folder):
                        if fnmatch.fnmatch(file, '*.py'):
                            self.in_file.append(file)
                elif args.language == "java":
                    self.language = args.language
                    for file in os.listdir(args.folder):
                        if fnmatch.fnmatch(file, '*.java'):
                            self.in_file.append(file)
                else:
                    print("Language not supported")
                    parser.print_help(sys.stderr)
                    sys.exit(1)
            else:
                for file in os.listdir(args.folder):
                    if fnmatch.fnmatch(file, '*.py'):
                        self.in_file.append(args.folder + "/" + file)
                        self.language = "python"
                if not self.in_file:
                    for file in os.listdir(args.folder):
                        if fnmatch.fnmatch(file, '*.java'):
                            self.in_file.append(args.folder + "/" + file)
                            self.language = "java"

                if not self.in_file:
                    self.in_file = "No matching files in folder supplied"
                    print(self.in_file)
                    parser.print_help(sys.stderr)
                    sys.exit(1)
            print("Input files: " + ", ".join(self.in_file))
            print("Language: " + self.language)
            if args.output:
                if ".txt" in args.output:
                    self.out_file = str(args.output)
                else:
                    self.out_file = str(args.output) + ".txt"
            else:
                self.out_file = str(args.folder) + ".txt"
            print("Output file: " + self.out_file)

        else:
            self.in_file = "You need to supply input file or folder"
            print(self.in_file)
            parser.print_help(sys.stderr)
            sys.exit(1)


class FileManager:
    """File Manager Class: has methods to get file language and
    output file name"""
    def __init__(self,input_file):
        self.input_file = input_file

    def get_output_file(self):
        file_name = self.input_file
        file_name = file_name.replace(".", "_")
        output_file = file_name + ".txt"
        return output_file

    def get_language(self):
        file_name = self.input_file
        # split the file by dot and get the extension
        lang = file_name.split(".")[1]
        if lang == "py":
            language = "python"
        elif lang == "java":
            language = "java"
        # if language not supported
        else:
            language = "wrong"
        return language


# class for storing evaluation results
class ResultStore:
    """Result Store Class: Used to output result to report to file"""
    def __init__(self,outfile):
        self.outfile = outfile
        self.results = []

    def store(self, general):
        self.results.append(general)

    def output(self):
        print("Printing file")
        with open(self.outfile, 'w') as out:
            self.output_main(out)

    def output_main(self, outstream):
        for line in self.results:
            print("\n".join(line), file=outstream)
            print("\n", file=outstream)


# method to create parser to allow unit testing
def create_parser():
    parser = argparse.ArgumentParser(prog="evaluator", description="Python command line application to evaluate source code style.")
    required_named = parser.add_argument_group('required argument')
    group = required_named.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', help='specify input file')
    group.add_argument('-F', '--folder', help='specify input folder, language should also be specified')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 3.0.0')
    parser.add_argument('-o', '--output', help='specify output file name')
    parser.add_argument('-l', '--language', help='specify language to evaluated', type=str, choices=["python", "java"])
    return parser
