from pathlib import Path
import os
from types import FunctionType
import sys

class Manager:
    """
    Create a new I/O Manager instance to automatically manage input and output files.
    
    Parameters
    ----------
    func : function

    Returns
    -------
    Manager

    Examples
    -------
    ```
    m = Manager()
    m.load_folder(path=Path("level1"))
    m.apply_to_all(func=process_input)
    ```
    """

    def __init__(self):
        if int(sys.version.split('.')[1]) < 13:
            print("🚧: You should consider using a more recent python version for features and performance.")
            print("    Further version 3.13 and above support GIL-free multithreading, you may want to give it a try.")
        elif not sys._is_gil_enabled():
            print("🚧: Using python without GIL is experimental!")
            print("    Proceed with caution. For single threaded applications consider using a python version with GIL enabled.")
            print("    Use e.g. \033[3muv venv --python 3.13rc3\033[0m to switch to the normal version and \033[3m3.13t\033[0m for the free-threaded one.")
        self.data = {}
    
    def load_file(self, in_file: Path, out_file: Path):
        if not in_file.exists() or not in_file.is_file():
            print("🆘: File does not exist.")
            return
        with open(in_file, "r") as file:
            self.data[in_file.name] = {
                "input": file.read(),
                "output_path": out_file
            }

    def load_folder(self, path: Path):
        self.path = path
        files = [f for f in os.listdir(path) if os.path.isfile(path / f)]
        if len(files) == 0:
            print("🆘: No input files found.")
            return
        output_path = path.parent / f"out_{path.name}"
        os.makedirs(output_path, exist_ok=True)
        for file in files:
            if file == ".gitkeep":
                print("🚧: Skipping .gitkeep file. You may load this file manually if you want to process this file using load_file().")
                continue
            self.load_file(path / file, output_path / file)

    def load_input(self):
        data = input("Enter input: ").strip()
        self.data["input"] = {
            "input": data,
            "output_path": None
        }

    def apply_to_all(self, func: FunctionType):
        """
        Applies a function to all files in the data dictionary.
        For each file a corresponding output file is created
        in a folder called "out_" + the name of the input folder.
        The function must take a string as input and return a string.
        If the input comes from stdin, the output is printed to stdout.

        Parameters
        ----------
        func : function

        Returns
        -------
        None
        """
        for file in self.data:
            print(f"📄: Applying function to {file}...")
            result = func(self.data[file]["input"])
            if self.data[file].get("output_path") is not None:
                if not self.data[file]["output_path"].exists():
                    self.data[file]["output_path"].parent.mkdir(parents=True, exist_ok=True)
                with open(self.data[file]["output_path"], "w") as file:
                    file.write(result)
            else:
                print(f"📄: {result}")
            print(f"✅: Applied function to {file}.")