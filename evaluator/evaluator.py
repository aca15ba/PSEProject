"""evaluator.evaluator: provides entry point for main and houses verison info"""
import argparse

__version__ = "0.1.0"
version = "0.1.0"


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
        group.add_argument('-F', '--folder', help='specify input folder')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
        parser.add_argument('-o', '--output', help='specify output file name')
        parser.add_argument('-l', '--language', help='specify language to evaluated', type=str, choices=["python", "java"])
        args = parser.parse_args()

        if args.output:
            self.out_file = str(args.output)
            print(args.output)
        else:

            self.out_file = str(args.input) +".txt"
