import subprocess
import os
import shutil

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

if __name__ == "__main__":
    target_directory = input("Enter the target directory path: ").strip()
    if not os.path.isdir(target_directory):
        print("Invalid directory path. Please provide a valid Python project directory.")
    else:
        prepare_target_directory(target_directory)
        output = run_in_docker()
        print(f"Output from container: {output}")
