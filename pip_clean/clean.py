import argparse
import logging
from packaging.utils import NormalizedName, canonicalize_name
from supported_manifests.requirements import get_requirements_deps
from supported_manifests.pipfile import get_pipfile_deps
import os
import ast

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

VALID_TYPES = ["Pipfile", "requirements.txt", "pyproject.toml"]


def get_pyfiles(source_dir: str) -> set[str]:
    logger.info("Scanning source directory for Python files: %s", source_dir)
    pyfiles: set[str] = set()
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                pyfiles.add(filepath)
                logger.debug("Found Python file: %s", filepath)
    logger.info("Total Python files found: %d", len(pyfiles))
    return pyfiles


def get_code_deps(pyfiles: set[str]) -> set[NormalizedName]:
    logger.info("Analyzing imports in Python files...")
    imports: set[NormalizedName] = set()

    for path in pyfiles:
        try:
            with open(path) as fh:
                logger.debug("Parsing file: %s", path)
                root = ast.parse(fh.read(), path)
        except Exception as e:
            logger.warning("Failed to parse file %s: %s", path, e)
            continue

        for node in ast.walk(root):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imported = canonicalize_name(name.name)
                    imports.add(imported)
                    logger.debug("Found import: %s", imported)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported = canonicalize_name(node.module)
                imports.add(imported)
                logger.debug("Found import from: %s", imported)

    logger.info("Total imports found: %d", len(imports))
    return imports


def clean_deps(manifest_type, manifest_file: str, source_dir: str) -> list[str]:
    logger.info("Analyzing manifest file: %s (type: %s)", manifest_file, manifest_type)
    if manifest_type == "requirements.txt":
        manifest_deps = get_requirements_deps(manifest_file)
    elif manifest_type == "pipfile":
        manifest_deps = get_pipfile_deps(manifest_file)
    else:
        logger.error("Unsupported manifest type: %s", manifest_type)
        raise ValueError(f"Unsupported manifest type: {manifest_type}")

    logger.info("Manifest contains %d dependencies", len(manifest_deps))
    pyfiles = get_pyfiles(source_dir)
    code_deps = get_code_deps(pyfiles)

    # Calculate unused dependencies
    unused_deps = list(sorted(manifest_deps - code_deps))
    return unused_deps


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
        description="Identify unused dependencies and remove them from requirements.txt",
    )
    parser.add_argument(
        "manifest_type",
        type=validate_type,
        help="Manifest type to analyze. Supported: Pipfile. Experimental: requirements.txt. Coming soon: pyproject.toml.",
    )
    parser.add_argument("-m", "--manifest", help="Path to manifest file", required=True)
    parser.add_argument(
        "-t", "--target", help="Root directory of Python project", required=True
    )

    args = parser.parse_args()

    try:
        unused_deps = clean_deps(args.manifest_type, args.manifest, args.target)
        if unused_deps:
            print("Unused dependencies:")
            for dep in unused_deps:
                print(f"- {dep}")
        else:
            print("No unused dependencies found.")
    except Exception as e:
        logger.error("Error during dependency analysis: %s", e)
        exit(1)


if __name__ == "__main__":
    main()
