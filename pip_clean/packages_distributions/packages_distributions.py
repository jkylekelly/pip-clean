import subprocess
import os
import shutil

def prepare_target_directory(target_dir):
    # Copy the target directory to a consistent location for Docker
    if os.path.exists("./target_project"):
        shutil.rmtree("./target_project")  # Clean up any previous copies
    shutil.copytree(target_dir, "./target_project")

def run_in_docker():
    # Build the Docker image
    subprocess.run(["docker", "build", "-t", "python-helper", "."], check=True)

    # Run the container
    subprocess.run(["docker", "run", "--rm", "python-helper"], check=True)

if __name__ == "__main__":
    target_directory = input("Enter the target directory path: ").strip()
    if not os.path.isdir(target_directory):
        print("Invalid directory path. Please provide a valid Python project directory.")
    else:
        prepare_target_directory(target_directory)
    run_in_docker()
