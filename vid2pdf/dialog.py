import tkinter as tk
from pathlib import Path
from tkinter import filedialog

CURRENT_DIR = Path()

DEFAULT_FILTER = [("All Files", "*.*")]


def prompt_for_file(
    title: str,
    start_dir: Path = CURRENT_DIR,
    multiple: bool = False,
    filetypes: list[tuple[str, str]] = DEFAULT_FILTER,
) -> Path:
    """Open a Tk file selection dialog to prompt the user to select a single file for processing."""
    root = tk.Tk()
    root.withdraw()

    picked = filedialog.askopenfilename(  # type: ignore[call-arg]  # stub issue
        title=title,
        initialdir=start_dir,
        multiple=multiple,
        filetypes=filetypes,
    )

    if not picked:
        raise ValueError("No file(s) selected.")

    return Path(picked)
