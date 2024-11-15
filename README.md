# pip-clean

**pip-clean** is a utility to help Python developers identify and clean unused dependencies from their `requirements.txt` file. It analyzes the imports in your codebase and compares them against the packages listed in `requirements.txt`, making it easier to maintain a lean and secure dependency list.

## Features

- Analyze Python Imports: Uses the Python Abstract Syntax Tree (AST) to extract all imports used in your project.
- Compare Against `requirements.txt`: Identifies unused dependencies by cross-referencing the imports with the packages listed in `requirements.txt`.
- Streamline Dependencies: Helps keep your project free of unnecessary dependencies, improving security and reducing potential attack surfaces.
- Easy to Use: Simple command-line interface for quick integration into your workflow.

## Installation

Clone the repository:

git clone https://github.com/yourusername/pip-clean.git  
cd pip-clean

Make the script executable (optional):

chmod +x pip-clean.py

## Usage

Run the script with the following options:

python pip-clean.py -r requirements.txt -t /path/to/python/project

### Arguments
- `-r`, `--requirements`: Path to your `requirements.txt` file.
- `-t`, `--target`: Root directory of your Python project.

### Example

Analyze a project in the `my_project/` directory with a `requirements.txt` file:

python pip-clean.py -r requirements.txt -t my_project/

### Output

The script will:
1. Parse the `requirements.txt` file and collect all explicitly listed dependencies.
2. Analyze your Python codebase to extract all imported modules.
3. Compare the two lists and identify unused dependencies.
4. Print the results, showing which dependencies can be safely removed.

### Example Output

Requirements from requirements.txt: {'requests', 'numpy', 'pandas'}  
Code dependencies from source files: {'requests', 'pandas'}  
Unused dependencies: {'numpy'}
