from input_manager.manager import Manager
from pathlib import Path

def process_input(inp: str) -> str:
    """
    Processes the input and returns the output.

    Parameters
    ----------
    inp : str
        The entire input to be processed.

    Returns
    -------
    str
        The output.
    """
    # lines = inp.strip().splitlines()
    return inp

m = Manager()
m.load_folder(path=Path("level1"))
m.apply_to_all(func=process_input)
