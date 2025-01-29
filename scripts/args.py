import tkinter as tk
import argparse
import pathlib
import logging
from tkinter import filedialog
from typing import List


logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    :returns: Parsed command-line arguments as an argparse.Namespace object.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Organize files into categorized folders.")

    parser.add_argument(
        "-e",
        "--ext",
        nargs="+",
        help=(
            "Specify associated extension for folder in the format '.ext1 folder1' '.ext2 folder2'..."
        )
    )

    parser.add_argument(
        "-d",
        "--dup",
        type=str.lower,
        choices=("true", "false"),
        help=(
            "If 'true', renames duplicate files to avoid overwriting, and"
            "if 'false', overwrites existing files with the same name."
        ),
        default="true"
    )

    parser.add_argument(
        "-s",
        "--status",
        type=str.lower,
        choices=("all", "success", "failed"),
        help=(
            "Determines which messages to print in the console based on their status. "
            "Choose from 'all', 'success', or 'failed'."
        ),
        default="failed"
    )

    return parser.parse_args()


def get_folders() -> List[str]:
    """
    Get a list of folders selected by the user via file dialog. The user can select up to 20 folders.

    :returns: A list of selected folder paths.
    :rtype: List[str]

    :raises ValueError: If no folder is selected by the user.
    """
    tk_root = tk.Tk()
    tk_root.withdraw()

    folder_paths = []
    last_directory = pathlib.Path.home()

    while len(folder_paths) < 20:
        folder_path = filedialog.askdirectory(title="Select a folder", initialdir=last_directory)

        if not folder_path:
            break
        if folder_path in folder_paths:
            continue

        folder_paths.append(folder_path)
        last_directory = pathlib.Path(folder_path).parent

    tk_root.destroy()

    if not folder_paths:
        logger.error("There is no selected folder to organize")
        raise ValueError("There is no selected folder to organize")

    return folder_paths
