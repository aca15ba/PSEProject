"""evaluator.evaluator: provides entry point for main and houses verison info"""
import argparse
import sys
import os

__version__ = "0.1.0"


def main():
    print("Programme style evaluator")
    config = CommandLine()
    # print(config.args.input)


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="evaluator", description="Python command line application to evaluate source code style.")
        required_named = parser.add_argument_group('required argument')
        group = required_named.add_mutually_exclusive_group()
        group.add_argument('-f', '--file', help='specify input file')
        group.add_argument('-F', '--folder', help='specify input folder, language should also be specified')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
        parser.add_argument('-o', '--output', help='specify output file name')
        parser.add_argument('-l', '--language', help='specify language to evaluated', type=str, choices=["python", "java"])
        args = parser.parse_args()

        if args.file:
            file = FileManager(args.file)
            file_lang = file.get_language()
            if args.language:
                if args.language == file_lang:
                    self.language = file_lang
                else:
                    print("Language does not match file")
                    parser.print_help(sys.stderr)
                    sys.exit(1)
            else:
                if file_lang == "wrong":
                    print("Language not supported")
                    parser.print_help(sys.stderr)
                    sys.exit(1)
                else:
                    self.language = file_lang

            if args.output:
                if ".txt" in args.output:
                    self.out_file = str(args.output)
                else:
                    self.out_file = str(args.output) + ".txt"
                print(self.out_file)
            else:
                # print(os.path.basename(args.file))
                # file_name = str(args.file)
                # file_name = file_name.replace(".","_")
                # self.out_file = file_name + ".txt"
                # print(self.out_file)
                self.out_file = file.get_output_file()
                print(self.out_file)

        elif args.folder:
            pass
        else:
            print("You need to supply input file or folder")
            parser.print_help(sys.stderr)
            sys.exit(1)


class FileManager:
    def __init__(self,input_file):
        self.input_file = input_file

    def get_output_file(self):
        file_name = self.input_file
        file_name = file_name.replace(".", "_")
        output_file = file_name + ".txt"
        return output_file

    def get_language(self):
        file_name = self.input_file
        lang = file_name.split(".")[1]
        if lang == "py":
            language = "python"
        elif lang == "java":
            language = "java"
        else:
            language = "wrong"
        return language
