from typing import Generator
import pathlib
import logging


class FileHandler:
    """Handles file management within a specified directory.

    This class provides utility functions for common file operations such as retrieving files, 
    creating folders, and moving files within a specified directory. Hidden files (files whose
    names start with a period '.') are excluded from all operations by default.

    Attributes:
            folder_path (pathlib.Path): The path to the root directory to manage.
    """

    def __init__(self, folder_path: str | pathlib.Path) -> None:
        """Initializes the FileHandler with the specified folder path.

        Args:
                folder_path (str | pathlib.Path): The path to the root directory to manage.

        Raises:
                TypeError: If `folder_path` is not a string or `pathlib.Path` object.
                NotADirectoryError: If `folder_path` does not exist or is not a directory.
        """
        self.folder_path = folder_path

    @property
    def folder_path(self) -> str:
        """Gets the root folder path.

        Returns:
                str: The absolute path of the root folder as a string.
        """
        return str(self._folder_path)

    @folder_path.setter
    def folder_path(self, folder_path: str | pathlib.Path) -> None:
        """Sets the root folder path.

        The provided path will be resolved to an absolute path before being stored.

        Args:
                folder_path (str | pathlib.Path): The path to the root folder.

        Raises:
                TypeError: If `folder_path` is not a string or `pathlib.Path` object.
                NotADirectoryError: If `folder_path` does not exist or is not a directory.
        """
        if not isinstance(folder_path, (str, pathlib.Path)):
            raise TypeError("folder_path should be an `str` or `pathlib.Path` object")

        folder_path = pathlib.Path(folder_path)
        if folder_path.is_dir():
            self._folder_path = folder_path.resolve()
            logging.info(f"Folder path set to: {folder_path}")
        else:
            logging.error(f"Invalid folder path provided: {folder_path}")
            raise NotADirectoryError(f"No such folder path: {folder_path}")

    def get_files(self) -> Generator[pathlib.Path, None, None]:
        """Retrieves all non-hidden files in the root folder.

        Hidden files are excluded. A file is considered hidden if its name starts with
        a period ('.').

        Yields:
                pathlib.Path: The path of each file in the root folder.
        """
        for content in self._folder_path.iterdir():
            if content.is_file() and not content.name.startswith("."):
                yield content

    def create_folder(self, folder_name: str | pathlib.Path) -> None:
        """Creates a new folder within the root folder if it does not already exist.

        Args:
                folder_name (str | pathlib.Path): The name or path of the folder to create.

        Raises:
                TypeError: If `folder_name` is not a string or `pathlib.Path` object.
                FileExistsError: If a file with the same name as `folder_name` exists in the directory.
        """
        if not isinstance(folder_name, (str, pathlib.Path)):
            raise TypeError("folder_name should be an `str` or `pathlib.Path` object")

        target_path = self._folder_path / folder_name
        if target_path.exists() and target_path.is_file():
            logging.info(f"Folder or file with '{folder_name}' name already exists")
            raise FileExistsError(f"A file with the name '{folder_name}' already exists")

        target_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Successfully created folder: '{folder_name}' at path '{target_path}'")

    def move_file(
            self,
            file: str | pathlib.Path,
            folder_name: str | pathlib.Path,
            keep_dup: bool = True
    ) -> None:
        """Moves a file to the specified folder.

        Args:
            file (str | pathlib.Path): The file to move.
            folder_name (str | pathlib.Path): The target folder name or path.
            keep_dup (bool, optional): If True, renames duplicate files to avoid overwriting. 
                             If False, overwrites existing files with the same name.

        Raises:
                TypeError: If `file` or `folder_name` is not a string or `pathlib.Path` object.
                FileNotFoundError: If `file` does not exist or is not a file.
                NotADirectoryError: If `folder_name` does not exist or is not a directory.
                PermissionError: If there are insufficient permissions to move `file`.
        """
        if not isinstance(file, (str, pathlib.Path)):
            raise TypeError("file should be an `str` or `pathlib.Path` object")
        if not isinstance(folder_name, (str, pathlib.Path)):
            raise TypeError("folder_name should be an `str` or `pathlib.Path` object")

        file_path = self._folder_path / file
        target_path = self._folder_path / folder_name

        if not file_path.is_file():
            logging.error(f"Cannot move file: '{file_path}' is invalid or does not exist")
            raise FileNotFoundError(f"No such file path: {file_path}")
        if not target_path.is_dir():
            logging.error(f"Target folder '{file_path}' is invalid or does not exist")
            raise NotADirectoryError(f"No such folder path: {target_path}")

        target_file_path = target_path / file_path.name
        if keep_dup:
            counter = 1
            while target_file_path.exists():
                target_file_path = target_path / f"{file_path.stem} ({counter}){file_path.suffix}"
                counter += 1

        try:
            file_path.rename(target_file_path)
            logging.info(f"Moved '{self._folder_path / file}' to '{target_file_path}'")
        except PermissionError as e:
            logging.error(f"Permission error when moving '{file_path.name}': '{e}'")
            raise

