import os
import subprocess
import json
import sys
import argparse

results=dict()
base_results=[]
faults_exposed=set()

def compile_c_file(folder_path, c_file_name):
    compile_command = f"gcc -Wno-return-type -g -o schedule2 {folder_path}/schedule2.c"
    subprocess.run(compile_command, shell=True, check=True)

def run_test_suite(test_suite_file):
    with open(test_suite_file, 'r') as file:
        test_suite_commands = file.readlines()
    
    test_results = []
    for command in test_suite_commands:
        result = subprocess.run(f"./schedule2 {command.strip()}", shell=True, stdout=subprocess.PIPE,encoding='ISO-8859-1', text=True)
        test_results.append(result.stdout.strip())
    return test_results

def process_folders(test_suite_file):
    for item in os.listdir():
        if os.path.isdir(item) and item.startswith('v'):
            c_files = [file for file in os.listdir(item) if file.endswith('.c')]
            if c_files:
                compile_c_file(item, c_files[0])
                results[item] = run_test_suite(test_suite_file)
    return results


def compile_base_program():
    compile_command = "gcc -Wno-return-type -g -o schedule2 schedule2.c"
    subprocess.run(compile_command, shell=True, check=True)


def base_run(test_suite_file):
    compile_base_program()
    with open(test_suite_file, 'r') as file:
        test_suite_commands = file.readlines()
    test_results=[]
    for command in test_suite_commands:
        result = subprocess.run(f"./schedule2 {command.strip()}", shell=True, stdout=subprocess.PIPE,encoding='ISO-8859-1', text=True)
        base_results.append(result.stdout.strip())
    


def faults_exposure(base_results, results,faults_path):
    for idx, base_result in enumerate(base_results):
        for version, version_results in results.items():
            if base_result != version_results[idx]:
                faults_exposed.add(version) 
    faults_exposed_sorted=sorted(faults_exposed,key=lambda x:int(x[1:]))
    print(faults_exposed_sorted)
    with open(faults_path, 'w') as file:
        json.dump(list(faults_exposed_sorted), file)
    return faults_exposed_sorted

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tsc', action='store_true', help='The -tsc option')
    parser.add_argument('-tbc', action='store_true', help='The -tbc option')
    parser.add_argument('-asc', action='store_true', help='The -asc option')
    parser.add_argument('-abc', action='store_true', help='The -abc option')
    parser.add_argument('-rsc', action='store_true', help='The -rsc option')
    parser.add_argument('-rbc', action='store_true', help='The -rbc option')
    parser.add_argument('-u', action='store_true', help='The -u option')
    args = parser.parse_args()
    if not args.tsc and not args.tbc and not args.asc and not args.abc and not args.rsc and not args.rbc and not args.u:
        print("Invalid Arguments")
        return
    if args.tsc:
        test_suite_file = 'testsuite/total-statement-suite.txt' 
        base_path = '../benchmarks/schedule2/'  
        base_run(test_suite_file)
        results = process_folders(test_suite_file)
        with open('json/fault_exposure_tsc_schedule2.json', 'w') as file:
            json.dump(results, file, indent=4)
        faults_exposure(base_results,results,"faults/total_statement_faults.txt")
    
    elif args.tbc:
        test_suite_file = 'testsuite/total-branch-suite.txt' 
        base_path = '../benchmarks/schedule2/'  
        base_run(test_suite_file)
        results = process_folders(test_suite_file)
        with open('json/fault_exposure_tbc_schedule2.json', 'w') as file:
            json.dump(results, file, indent=4)
        faults_exposure(base_results,results,"faults/total_branch_faults.txt")
    
    elif args.asc:
        test_suite_file = 'testsuite/additional-statement-suite.txt' 
        base_path = '../benchmarks/schedule2/'  
        base_run(test_suite_file)
        results = process_folders(test_suite_file)
        with open('json/fault_exposure_asc_schedule2.json', 'w') as file:
            json.dump(results, file, indent=4)
        faults_exposure(base_results,results,"faults/additional_statement_faults.txt")
    
    elif args.abc:
        test_suite_file = 'testsuite/additional-branch-suite.txt' 
        base_path = '../benchmarks/schedule2/'  
        base_run(test_suite_file)
        results = process_folders(test_suite_file)
        with open('json/fault_exposure_abc_schedule2.json', 'w') as file:
            json.dump(results, file, indent=4)
        faults_exposure(base_results,results,"faults/additional_branch_faults.txt")
    
    elif args.rsc:
        test_suite_file = 'testsuite/random-statement-suite.txt' 
        base_path = '../benchmarks/schedule2/'  
        base_run(test_suite_file)
        results = process_folders(test_suite_file)
        with open('json/fault_exposure_rsc_schedule2.json', 'w') as file:
            json.dump(results, file, indent=4)
        faults_exposure(base_results,results,"faults/random_statement_faults.txt")
    
    elif args.rbc:
        test_suite_file = 'testsuite/random-branch-suite.txt' 
        base_path = '../benchmarks/schedule2/'  
        base_run(test_suite_file)
        results = process_folders(test_suite_file)
        with open('json/fault_exposure_rbc_schedule2.json', 'w') as file:
            json.dump(results, file, indent=4)
        faults_exposure(base_results,results,"faults/random_branch_faults.txt")
    
    elif args.u:
        test_suite_file = 'universe.txt' 
        base_path = '../benchmarks/schedule2/'  
        base_run(test_suite_file)
        results = process_folders(test_suite_file)
        with open('json/fault_exposure_universe_schedule2.json', 'w') as file:
            json.dump(results, file, indent=4)
        faults_exposure(base_results,results,"faults/universe_faults.txt")


if __name__ == "__main__":
    main()
