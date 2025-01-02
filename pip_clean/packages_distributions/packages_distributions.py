import subprocess
import os
import shutil
import ast

def prepare_target_directory(target_dir):
    # Copy the target directory to a consistent location for Docker
    if os.path.exists("pip_clean/packages_distributions/target_project"):
        shutil.rmtree("pip_clean/packages_distributions/target_project")  # Clean up any previous copies
    shutil.copytree(target_dir, "pip_clean/packages_distributions/target_project")

def run_in_docker():
    # Build the Docker image
    subprocess.run(["docker", "build", "-t", "python-helper", "pip_clean/packages_distributions/"], check=True)

    # Run the container and capture the output
    result = subprocess.run(
        ["docker", "run", "--rm", "python-helper"],
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE,  # Capture standard error
        text=True  # Decode output as text (not bytes)
    )
    if result.returncode != 0:
        raise RuntimeError(f"Container failed: {result.stderr}")
    return result.stdout.strip()  # Return the container's output

def manifest_to_import_names(manifest_deps, module_mapping):
    # Parse the string into a dictionary
    try:
        module_mapping = ast.literal_eval(module_mapping)
        if not isinstance(module_mapping, dict):
            raise ValueError("Parsed module_mapping is not a dictionary")
    except Exception as e:
        raise ValueError(f"Invalid module_mapping format: {e}")
    
    result = set()

    for package in manifest_deps:
        # Normalize package name to lowercase
        package_lower = package.lower()

        # Find all module names corresponding to the package
        matching_modules = {
            module for module, packages in module_mapping.items()
            if package_lower in map(str.lower, packages)
        }

        if matching_modules:
            # Add the package and matching modules as a tuple
            result.add((package, frozenset(matching_modules)))
        else:
            # If no match, retain the original package name with an empty set
            result.add((package, frozenset()))
    
    return result

if __name__ == "__main__":
    target_directory = input("Enter the target directory path: ").strip()
    if not os.path.isdir(target_directory):
        print("Invalid directory path. Please provide a valid Python project directory.")
    else:
        prepare_target_directory(target_directory)
        output = run_in_docker()
        print(f"Output from container: {output}")
