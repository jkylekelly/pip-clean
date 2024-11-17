import argparse
from packaging.utils import NormalizedName, canonicalize_name
from supported_manifests.requirements import get_requirements_deps
from supported_manifests.pipfile import get_pipfile_deps

import os
import ast

VALID_TYPES = ["Pipfile", "requirements.txt", "pyproject.toml"]


def get_pyfiles(source_dir: str) -> set[str]:
    pyfiles: set[str] = set()
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                pyfiles.add(os.path.join(root, file))
    return pyfiles


def get_code_deps(pyfiles: set[str]) -> set[NormalizedName]:
    imports: set[NormalizedName] = set()

    # adapted from
    # https://stackoverflow.com/questions/9008451/python-easy-way-to-read-all-import-statements-from-py-module
    for path in pyfiles:
        with open(path) as fh:
            root = ast.parse(fh.read(), path)

        for node in ast.walk(root):
            if isinstance(node, ast.Import):
                print(canonicalize_name(node.names[0].name))
                imports.add(canonicalize_name(node.names[0].name))
            elif isinstance(node, ast.ImportFrom):
                # print(canonicalize_name(node.module))
                if node.module is not None:
                    imports.add(canonicalize_name(node.module))

    return imports


def clean_deps(manifest_type, manifest_file: str, source_dir: str) -> bool:
    # get a list of package names from the requirements.txt
    # requirements_deps = get_requirements_deps(manifest_file)
    if manifest_type == 'requirements.txt':
        manifest_deps = get_requirements_deps(manifest_file)
    
    elif manifest_type == 'pipfile':
        manifest_deps = get_pipfile_deps(manifest_file)
    
    else:
        print("not yet supported")

    # get package names used in code based on ASTs
    pyfiles = get_pyfiles(source_dir)
    code_deps = get_code_deps(pyfiles)


    # Print missing dependencies
    missing = list(sorted(manifest_deps - code_deps))
    if missing:
        print("Unused dependencies:")
        for dep in missing:
            print(f"- {dep}")
    else:
        print("No missing dependencies found.")

def validate_type(manifest_type):
    value_lower = manifest_type.lower()
    if value_lower in map(str.lower, VALID_TYPES):
        return manifest_type
    raise argparse.ArgumentTypeError(
        f"Invalid type: {manifest_type}. Choose from {', '.join(VALID_TYPES)}."
    )


def main():
    parser = argparse.ArgumentParser(
        prog="pip-clean",
        description="identify unused dependencies and remove them from requirements.txt",
    )
    parser.add_argument(
        "manifest_type",
        type=validate_type,
        help="Manifest type to analyze. Supported: Pipfile. Experimental: requirements.txt. Coming soon: pyproject.toml.",
    )
    parser.add_argument("-m", "--manifest", help="path to manifest file", required=True)
    parser.add_argument(
        "-t", "--target", help="root directory of python project", required=True
    )

    args = parser.parse_args()

    clean_deps(args.manifest_type, args.manifest, args.target)


if __name__ == "__main__":
    main()
