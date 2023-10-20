from pathlib import Path
import os
from types import FunctionType

class Manager:
    def __init__(self):
        self.data = {}
        pass
    
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