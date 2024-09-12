import os
import subprocess
import json
import argparse

base_coverage_list=[]

def compile_program():
    compile_command = "gcc -fprofile-arcs -ftest-coverage -Wno-return-type -g -o printtokens printtokens.c"
    subprocess.run(compile_command, shell=True, check=True)

def generate_statement_gcov(input_file):
    run_command = f"./printtokens {input_file}"
    try:
        subprocess.run(run_command, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pass
    gcov_command = "gcov -r printtokens.c"
    subprocess.run(gcov_command, shell=True, check=True)

def generate_branch_gcov(input_file):
    run_command = f"./printtokens {input_file}"
    try:
        subprocess.run(run_command, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pass
    gcov_command = "gcov -b printtokens.c"
    subprocess.run(gcov_command, shell=True, check=True)

def parse_statement_gcov_file(file_path):
    coverable_lines = []
    with open(file_path, 'r') as file:
        lines=file.readlines()
        for line in lines:
            stripped_line=line.strip()
            l=stripped_line.split(':')
            if l[0]!='-' and l[0]!='#####':
                t=int(l[1].strip())
                coverable_lines.append(t)
    return coverable_lines


def parse_branch_gcov_file(file_path):
    index=0
    coverable_lines = []
    with open(file_path, 'r') as file:
        lines=file.readlines()
        for line in lines:
            stripped_line=line.strip()
            l=stripped_line.split(':')
            if l[0]!='-' and l[0]!='#####':
                if len(l)==1:
                    b_list= ''.join(l).split(" ")
                    if(b_list[0]=='branch' and b_list[3]=='taken' and b_list[4]!='0%'):
                        s=str(index)+'_'+b_list[2]
                        coverable_lines.append(s)
                else:
                    index=l[1].strip()
    print(coverable_lines)
    return coverable_lines

def delete_file():
    subprocess.run("rm -rf printtokens.c.gcov printtokens.gcov.json printtokens printtokens.gcda printtokens.gcno", shell=True, check=True)
    subprocess.run("ls")

def base_coverage():
    covered_statements_set = set()
    with open('json/additional_printtokens.json', 'r') as file:
        coverage_data = json.load(file)
    for test_case, statements in coverage_data.items():
        covered_statements_set.update(statements)
    base_coverage_list = list(covered_statements_set)
    base_coverage_list.sort()
    with open('json/base_coverage_additional_printtokens.json', 'w') as outfile:
        json.dump(base_coverage_list, outfile, indent=4)
    return base_coverage_list

def test_suite_generation(coverage):
    
    with open("json/additional_printtokens.json", 'r') as file:
        data = json.load(file)
    sorted_printtokens_map = dict(sorted(data.items(), key=lambda value: len(value[1]), reverse=True))

    with open('json/base_coverage_additional_printtokens.json', 'r') as file:
        base_coverage_list = json.load(file)
    base_coverage_set = set(base_coverage_list)
    temp_coverage_set = set()
    testsuit = []

    while temp_coverage_set != base_coverage_set and sorted_printtokens_map:
        max_diff = 0
        max_test = None
        for key, value in sorted_printtokens_map.items():
            current_set = set(value)
            difference = current_set.difference(temp_coverage_set)
            if len(difference) > max_diff:
                max_diff = len(difference)
                max_test = key
        if max_test:
            temp_coverage_set.update(set(sorted_printtokens_map[max_test]))
            testsuit.append(max_test)
            del sorted_printtokens_map[max_test]
    with open(coverage,'w') as file:
        for test in testsuit:
            file.write(test)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store_true', help='The -b option')
    parser.add_argument('-s', action='store_true', help='The -s option')
    args = parser.parse_args()
    if not args.b and not args.s:
        print("Invalid Arguments")
        return
    
    with open('universe.txt') as file:
        input_files = file.readlines()
    coverable_lines_map = {} 
    for input_file in input_files:
        compile_program()
        file_name=input_file.strip()
        if args.s:
            generate_statement_gcov(file_name)
            coverable_lines = parse_statement_gcov_file("printtokens.c.gcov")
            coverable_lines_map[input_file] = coverable_lines
            delete_file()
            with open('json/additional_printtokens.json', 'w') as file:
                json.dump(coverable_lines_map, file, indent=4)
            base_coverage()
            test_suite_generation("testsuite/additional-statement-suite.txt")
        elif args.b:
            generate_branch_gcov(file_name)
            coverable_lines = parse_branch_gcov_file("printtokens.c.gcov")
            coverable_lines_map[input_file] = coverable_lines
            delete_file()
            with open('json/additional_printtokens.json', 'w') as file:
                json.dump(coverable_lines_map, file, indent=4)
            base_coverage()
            test_suite_generation("testsuite/additional-branch-suite.txt")

if __name__ == "__main__":
    main()


