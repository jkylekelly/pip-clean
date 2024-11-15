import argparse
from pip._internal.network.session import PipSession
from pip._internal.req.req_file import parse_requirements
from pip._internal.req.constructors import install_req_from_line
from packaging.utils import NormalizedName, canonicalize_name

import os
import ast

# This function is adapted from the pip-check-reqs project by adamtheturtle.
# Source: https://github.com/adamtheturtle/pip-check-reqs
def get_requirements_deps(filename: str) -> set[NormalizedName]:
    explicit: set[NormalizedName] = set()
    for requirement in parse_requirements(
        filename,
        session=PipSession(),
    ):
        requirement_name = install_req_from_line(
            requirement.requirement,
        ).name
        explicit.add(canonicalize_name(requirement_name))
    return explicit

def get_pyfiles(source_dir: str) -> set[str]:
    pyfiles: set[str] = set()
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.py'):
                pyfiles.add(os.path.join(root, file))
    return pyfiles

def get_code_deps(pyfiles: set[str]) -> set[NormalizedName]:
    imports: set[NormalizedName] = set()

    # https://stackoverflow.com/questions/9008451/python-easy-way-to-read-all-import-statements-from-py-module
    # not currently working fully
    for path in pyfiles:
        with open(path) as fh:        
            root = ast.parse(fh.read(), path)

        for node in ast.walk(root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):  
                module = node.module.split('.') if node.module else []
            else:
                continue

            for n in node.names:
                imports.add(canonicalize_name(n.name))

    return imports


def clean_deps(requirements_file: str, source_dir: str) -> bool:
    # get a list of package names from the requirements.txt
    requirements = get_requirements_deps(requirements_file)
    
    # get package names used in code based on ASTs
    pyfiles = get_pyfiles(source_dir)
    print(get_code_deps(pyfiles))


def main():
    parser = argparse.ArgumentParser(
                        prog='pip-clean',
                        description='identify unused dependencies and remove them from requirements.txt')
    parser.add_argument('-r', '--requirements', help='path to requirements.txt file')
    parser.add_argument('-t', '--target', help='root directory of python project')
    args = parser.parse_args()
    
    clean_deps(args.requirements, args.target)
    # parse_deps(args.r)
    

if __name__ == "__main__":
    main()
