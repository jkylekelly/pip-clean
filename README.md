# pip-clean
This is AI generated, may not be 100% accurate.

**pip-clean** is a Python tool for identifying unused dependencies in your project. It analyzes your project's manifest file (e.g., `Pipfile`, `requirements.txt`) and compares it with the actual imports used in your Python code. The tool helps keep your dependency list lean and secure by highlighting dependencies that can be removed.

## Features

- Support for Multiple Manifest Types: Works with `Pipfile` (beta), `requirements.txt` (experimental), and `pyproject.toml` (coming soon).
- Accurate Analysis: Cross-references the dependencies in your manifest with actual imports in your Python files.
- Simple CLI Interface: Easy-to-use command-line tool for efficient dependency management.

## Usage

1. Clone the repository:  
   `git clone https://github.com/yourusername/pip-clean.git`  
   `cd pip-clean`  

Run the tool using the following format:  
`uv run python pip_clean/clean.py <manifest_type> -m <manifest_file> -t <target_directory>`

### Arguments

- `<manifest_type>`: The type of manifest file to analyze. Supported values are:
  - `Pipfile` (beta)
  - `requirements.txt` (experimental)
  - `pyproject.toml` (coming soon)
- `-m`, `--manifest`: Path to the manifest file (e.g., `Pipfile` or `requirements.txt`).
- `-t`, `--target`: Path to the root directory of your Python project containing the codebase to analyze.

### Example

To analyze a project using a `Pipfile` located at `/tmp/projects/example`:  
`uv run python pip_clean/clean.py pipfile -m /tmp/projects/example/Pipfile -t /tmp/projects/example/`

### Output

- **Unused Dependencies**: The tool will list any dependencies in the manifest file that are not used in the codebase. For example:  
  `Unused dependencies:`  
  `- flask`  
  `- requests`

- **No Unused Dependencies**: If all dependencies are in use, it will output:  
  `No unused dependencies found.`

## Known Limitations

While `pip-clean` is a helpful tool, there are some limitations to be aware of:

1. **Mismatch Between Package and Import Names**: Some Python packages are installed with a name that differs from the one used to import them in code. For example:
   - Package name: `python-dateutil`
   - Import name: `dateutil`
   This can result in false positives where a dependency is marked as unused because its import name doesn’t directly match the package name.

2. **Dynamic Imports**: The tool does not detect dynamically generated imports, such as those created using `importlib` or `__import__`. These imports might not be visible in the static analysis.

3. **Indirect Dependencies**: Dependencies that are imported indirectly (e.g., through another library) are not analyzed. The tool focuses only on imports explicitly used in your code. Pip-clean expects `requirements.txt` and `Pipfile` files to include direct dependencies only. Dev dependencies and other non-production dependencies are also ignored.

4. **Manifest Type Limitations**: Currently, `Pipfile` is the most stable format supported. Analysis for `requirements.txt` is experimental, and support for `pyproject.toml` is planned but not yet implemented.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have suggestions or improvements.
