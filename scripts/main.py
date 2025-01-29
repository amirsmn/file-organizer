import logging
from pathlib import Path
from console_manager.console_manager import ConsoleManager
from file_handler.file_handler import FileHandler
from scripts.args import parse_args, get_folders
from config.config import Config


def organize_files() -> None:
    """
    Organize files in specified folders based on their extensions.
    """
    handler = FileHandler(folder_path=Path(""))

    for folder_path in configs["folder_paths"]:
        handler.folder_path = Path(folder_path)

        console.print(f"--- Starting file organization for '{folder_path}' ---")
        logger.info(f"Starting file organization for '{folder_path}'")

        for file in handler.get_files():
            target_folder = configs["extension_to_folder"].get(file.suffix, "OTHERS")

            try:
                handler.create_folder(folder_name=target_folder)
                handler.move_file(file=file, folder_name=target_folder, keep_dup=configs["keep_duplicates"])
                console.print(msg=f"'{file.name}' moved to '{target_folder}' folder", flag="success")

            except (TypeError, FileExistsError, FileNotFoundError, NotADirectoryError, PermissionError) as e:
                console.print(msg=f"Failed to move '{file.name}' to '{target_folder}' folder", flag="failed")
                logger.warning(f"Error processing '{file.name}': {e}")

        console.print(f"--- File organization completed successfully for '{folder_path}' ---")
        logger.info(f"File organization completed successfully for '{folder_path}'")


def filter_messages(max_cycle: int = 5, max_retry: int = 3) -> None:
    """
    Filter and display messages by their status.

    :param max_cycle: The maximum number of interaction cycles (prompts).
    :type max_cycle: int
    :param max_retry: The maximum number of retries allowed for invalid inputs
    :type max_retry: int

    :raises ValueError: If `max_cycle` or `max_retry` are not integers.
    """
    if not (isinstance(max_cycle, int) and isinstance(max_retry, int)):
        raise ValueError("`max_cycle` and `max_retry` must be integers")

    max_cycle = 0 if max_cycle < 0 else max_cycle
    max_retry = 1 if max_retry <= 0 else max_retry

    while max_cycle:
        max_cycle -= 1
        flag = input("Filter messages by status ('success', 'failed', 'all', 'cancel'): ").lower()

        if flag == "cancel" or not max_retry:
            break

        try:
            console.filter_by_flag(flag)
        except ValueError:
            max_retry -= 1


def create_logger() -> logging.Logger:
    """
    Create a logger instance for logging information and errors.

    :return: A logging.Logger instance
    :rtype: logging.Logger
    """
    logging.basicConfig(
        filename="file_organizer.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    return logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        logger = create_logger()

        args = parse_args()
        config = Config()
        config.set_configs(
            folder_paths=get_folders(),
            extension_to_folder=args.ext,
            keep_duplicates=args.dup,
            status_level=args.status
        )
        configs = config.configs
        console = ConsoleManager(output_level=configs["status_level"])

        organize_files()
        filter_messages()

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise
