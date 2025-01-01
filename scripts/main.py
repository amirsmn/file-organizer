import logging
from pathlib import Path
from typing import Dict, Union, List
from console_manager.console_manager import ConsoleManager
from file_handler.file_handler import FileHandler
from scripts.args import parse_args, get_folders
from config.config import Config


def organize_files(
        configs: Dict[str, Union[Dict[str, str], List[str], bool, str]],
        console: ConsoleManager,
        logger: logging.Logger
) -> None:
    """
    Organize files in specified folders based on their extensions.

    :param configs: A dictionary containing configuration settings:
        - folder_paths (list[str, pathlib.Path]): List of folder paths to organize.
        - extension_to_folder (dict[str, str]): Mapping of file extensions to target folders.
        - keep_duplicates (bool): Indicates whether to keep duplicate files.
    :param console: An instance of ConsoleManager for printing messages to the console.
    :param logger: A logging.Logger instance for logging information and errors.

    :raises TypeError: If a path is not a string or pathlib.Path object.
    :raises FileExistsError: If a target folder already exists.
    :raises FileNotFoundError: If a specified file path does not exist.
    :raises NotADirectoryError: If a target folder does not exist or is not a directory.
    :raises PermissionError: If a permission error occurs during file movement.
    """
    handler = FileHandler(folder_path=Path(""))

    folders_to_organize = configs["folder_paths"]
    extension_to_folder = configs["extension_to_folder"]
    keep_duplicates = configs["keep_duplicates"]

    for folder_path in folders_to_organize:
        handler.folder_path = Path(folder_path)

        console.print(f"--- Starting file organization for '{folder_path}'... ---")
        logger.info(f"Starting file organization for '{folder_path}'")

        for file in handler.get_files():
            logger.info(f"Processing file: '{file.name}'")
            file_extension = file.suffix

            target_folder = extension_to_folder.get(file_extension, "OTHERS")
            logger.info(f"File classified as - {target_folder.split('/')[0]}")

            try:
                handler.create_folder(folder_name=target_folder)
                handler.move_file(file=file, folder_name=target_folder, keep_dup=keep_duplicates)
                console.print(msg=f"'{file.name}' moved to '{target_folder}' folder", flag="success")
            except (TypeError, FileExistsError, FileNotFoundError, NotADirectoryError, PermissionError) as e:
                console.print(
                    msg=f"[{e.__class__.__name__}] - {e}\nFailed to move '{file.name}' to '{target_folder}' folder",
                    flag="failed"
                )
                logger.warning(f"Error processing '{file.name}': {e}")

        console.print(f"--- File organization completed successfully for '{folder_path}' ---")
        logger.info(f"File organization completed successfully for '{folder_path}'")

    logger.info("File organization completed successfully for all folders")


def filter_messages(console: ConsoleManager) -> None:
    """
    Filters messages based on their status level.

    :param console: An instance of ConsoleManager for printing messages to the console.
    """
    while True:
        filter_value = input(
            "You can filter messages by their status ('success', 'failed', 'all', 'cancel'): "
        ).lower()

        if filter_value not in ("success", "failed", "all"):
            break

        console.filter_by_flag(filter_value)


def create_logger() -> logging.Logger:
    """
    Create a logger instance for logging information and errors.

    :return: A logging.Logger instance
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler("file_organizer.log")]
    )

    return logging.getLogger("main")


if __name__ == "__main__":
    try:
        logger = create_logger()

        args = parse_args()
        folder_paths = get_folders()

        config = Config()
        config.set_configs(
            folder_paths=folder_paths,
            extension_to_folder=args.ext,
            keep_duplicates=args.dup,
            status_level=args.status
        )
        configs = config.configs

        console = ConsoleManager(output_level=configs["status_level"])

        organize_files(configs, console, logger)
        filter_messages(console)

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise
