from file_organizer.file_handler import FileHandler
from config.config import Config
import argparse
import logging


def organize(config_obj: Config) -> None:
    """Organizes files in the specified folders based on their extensions, moving them to
    designated subfolders.

    Args:
        config_obj (Config): A Config object containing the configuration settings.

    Raises:
        Exception: Any unexpected errors that occur during the file organization process, including 
                   issues with file access, permission errors, or problems with folder creation.
    """
    configs = config_obj.configs
    handler = FileHandler(folder_path="")
    extension_to_folder = configs["extension_to_folder"]
    folders_to_organize = configs["folder_paths"]
    keep_dup = configs["keep_duplicates"]

    for i in range( len(folders_to_organize) ):
        handler.folder_path = folders_to_organize[i]

        print(f"--- Starting file organization for '{folders_to_organize[i]}'... ---")
        logger.info(f"Starting file organization for '{folders_to_organize[i]}'")

        for file in handler.get_files():
            logger.info(f"Got new file: '{file.name}'")
            file_extension = file.suffix

            if file_extension in extension_to_folder:
                target_folder = extension_to_folder[file_extension]
                logger.info(f"File has been classfied as - {target_folder.split("/")[0]}")

                try:
                    handler.create_folder(folder_name=target_folder)
                    handler.move_file(file=file, folder_name=target_folder, keep_dup=keep_dup)
                    config_obj.display_status(
                        status="success",
                        msg=f"'{file.name}' moved to '{target_folder}' folder"
                    )
                except (TypeError, FileExistsError, FileNotFoundError, NotADirectoryError, PermissionError) as e:
                    config_obj.display_status(
                        status="failed",
                        msg=f"[{e.__class__.__name__}] failed to move '{file.name}' to '{target_folder}' folder"
                    )
                    logger.warning(f"An error occurred while processing '{file.name}': {e}")

            else:
                logger.info(f"File '{file.name}' has an unsupported extension")
                try:
                    handler.create_folder("OTHERS")
                    handler.move_file(file=file, folder_name="OTHERS", keep_dup=keep_dup)
                    config_obj.display_status(status="success", msg=f"{file.name} moved to 'OTHERS' folder")
                except (TypeError, FileExistsError, FileNotFoundError, NotADirectoryError, PermissionError) as e:
                    config_obj.display_status(
                        status="failed",
                        msg=f"[{e.__class__.__name__}] failed to move '{file.name}' to 'OTHERS' folder"
                    )
                    logger.warning(f"An error occurred while processing '{file.name}': {e}")

        print(f"--- File organization completed successfully for '{folders_to_organize[i]}' ---")
        logger.info(f"File organization completed successfully for '{folders_to_organize[i]}'")

    logger.info("File organization completed successfully for all folders")

if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[logging.FileHandler("file_organizer.log")]
        )
        logger = logging.getLogger("main")

        # Parse command-line arguments to get configurations
        parser = argparse.ArgumentParser(description="Organize files into categorized folders.")

        parser.add_argument(
            "folder_paths",
            nargs="+",
            help="Paths to the folders to organize in the format 'path/to/folder'..."
        )

        parser.add_argument(
            "--ext",
            nargs="+",
            help=(
                "Specify associated extension for folder in the format '.ext1 folder1' '.ext2 folder2'..."
            )
        )

        parser.add_argument(
            "--dup",
            type=str.lower,
            choices=("true", "false"),
            help=(
                "If 'true', renames duplicate files to avoid overwriting, and"
                "if 'false', overwrites existing files with the same name"
            )
        )

        parser.add_argument(
            "--status",
            type=str.lower,
            choices=("all", "success", "failed"),
            help=(
                "Determines which messages to print in the console based on their status. "
                "Choose from 'all', 'success', or 'failed'."
            )
        )

        args = parser.parse_args()
        config = Config()
        config.set_configs(
            extension_to_folder=args.ext,
            folder_paths=args.folder_paths,
            keep_duplicates=args.dup,
            status_level=args.status
        )

        organize(config_obj=config)

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise
