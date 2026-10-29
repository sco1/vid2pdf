import tkinter as tk
from pathlib import Path
from tkinter import filedialog

CURRENT_DIR = Path()

DEFAULT_FILTER = [("All Files", "*.*")]


def prompt_for_file(
    title: str,
    start_dir: Path = CURRENT_DIR,
    filetypes: list[tuple[str, str]] = DEFAULT_FILTER,
) -> Path:
    """Open a Tk file selection dialog to prompt the user to select a single file for processing."""
    root = tk.Tk()
    root.withdraw()

    try:
        picked = filedialog.askopenfilename(
            title=title,
            initialdir=start_dir,
            filetypes=filetypes,
        )
    finally:
        root.destroy()

    if not picked:
        raise ValueError("No file selected.")

    return Path(picked)
