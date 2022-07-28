# Program by Dyanesh S
# To find declared but unused variables and functions

import argparse
import subprocess


def parser(filename):
    command = ["clang", "-Xclang", "-ast-dump", "-fsyntax-only", filename]
    data = subprocess.run(command, capture_output=True, text=True)
    data_list = data.stdout.split("\n")
    for i in range(len(data_list)):
        if data_list[i].find('<'+filename+':') != -1:
            data_list = data_list[i:]
            break
    data_list.pop()  # To remove the empty string at last
    parsed_list = []

    for i in data_list:
        line = [word for word in i.split() if word != '|']
        line[0] = line[0][2:]
        parsed_list.append(line)

    return parsed_list


def find_unused_vars_funs(data_list):
    unused_funs = []
    unused_vars = []
    line_no = 0

    for line in data_list:

        # Global variables
        if line_no == 0 and line[0] == 'VarDecl' and line[5] != 'used':
            if '\'struct' in line:
                unused_vars.append([line[5], line[3][:-1]])
            else:
                unused_vars.append([line[5], line[2][1:-1]])

        # Local variables
        elif line[0] == 'DeclStmt':
            line_no = line[2][1:-1]
        elif line[0] == 'VarDecl':
            if line[5] not in ['used', 'invalid']:
                unused_vars.append([line[5], line_no])

        # Functions
        elif line[0] == 'FunctionDecl':
            if line[5] not in ['used', 'main'] and line[2] != 'prev':
                unused_funs.append([line[5], line[2][1:-1]])

    return unused_vars, unused_funs


def main():
    argparser = argparse.ArgumentParser('Analyze C Files')
    argparser.add_argument('filename', default='1.c',
                           nargs='?', help='name of file to analyze')
    args = argparser.parse_args()
    parsed_list = parser(args.filename)
    unused_vars, unused_funs = find_unused_vars_funs(
        parsed_list)
    print("Unused Variables: ", unused_vars)
    print("Unused Functions: ", unused_funs)


if __name__ == "__main__":
    main()
