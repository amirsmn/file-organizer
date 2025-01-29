import pathlib
import logging
from typing import Generator, Union


logger = logging.getLogger(__name__)


class FileHandler:
    """
    Handles file management within a specified directory.

    This class provides utility functions for common file operations such as retrieving files, 
    creating folders, and moving files within a specified directory. Hidden files (files whose
    names start with a period '.') are excluded from all operations by default.
    """

    def __init__(self, folder_path: Union[str, pathlib.Path]) -> None:
        """
        Initialize the FileHandler with the specified folder path.

        :param folder_path: The path to the root directory to manage.
        :type folder_path: Union[str, pathlib.Path]

        :raises TypeError: If folder_path is not a string or pathlib.Path object.
        :raises NotADirectoryError: If folder_path does not exist or is not a directory.
        """
        self.folder_path = folder_path

    def get_files(self) -> Generator[pathlib.Path, None, None]:
        """
        Retrieve all non-hidden files in the root folder.

        :yields: The path of each file in the root folder.
        :rtype: Generator[pathlib.Path, None, None]
        """
        for content in self._folder_path.iterdir():
            if content.is_file() and not content.name.startswith("."):
                yield content

    def create_folder(self, folder_name: Union[str, pathlib.Path]) -> None:
        """
        Create a new folder within the root folder if it does not already exist.

        :param folder_name: The name or path of the folder to create.
        :type folder_name: Union[str, pathlib.Path]

        :raises TypeError: If folder_name is not a string or pathlib.Path object.
        :raises FileExistsError: If a file with the same name as folder_name exists in the directory.
        """
        if not isinstance(folder_name, (str, pathlib.Path)):
            raise TypeError("folder_name should be a `str` or `pathlib.Path` object")

        target_path = self._folder_path / folder_name
        if target_path.exists() and target_path.is_file():
            raise FileExistsError(f"A file with the name '{folder_name}' already exists")

        target_path.mkdir(parents=True, exist_ok=True)

    def move_file(
            self,
            file: Union[str, pathlib.Path],
            folder_name: Union[str, pathlib.Path],
            keep_dup: bool = True
    ) -> None:
        """
        Move a file to the specified folder.

        :param file: The file to move. Can be a string or pathlib.Path object.
        :type file: Union[str, pathlib.Path]
        :param folder_name: The target folder name or path. Can be a string or pathlib.Path object.
        :type folder_name: Union[str, pathlib.Path]
        :param keep_dup: If True, renames duplicate files to avoid overwriting. If False, overwrites existing files with the same name. Defaults to True.
        :type keep_dup: bool, optional

        :raises TypeError: If file or folder_name is not a string or pathlib.Path object.
        :raises FileNotFoundError: If file does not exist or is not a file.
        :raises NotADirectoryError: If folder_name does not exist or is not a directory.
        :raises PermissionError: If there are insufficient permissions to move file.
        """
        if not isinstance(file, (str, pathlib.Path)):
            raise TypeError("file should be a `str` or `pathlib.Path` object")
        if not isinstance(folder_name, (str, pathlib.Path)):
            raise TypeError("folder_name should be a `str` or `pathlib.Path` object")

        file_path = self._folder_path / file
        target_path = self._folder_path / folder_name

        if not file_path.is_file():
            logger.error(f"Cannot move file: '{file_path}' is invalid or does not exist")
            raise FileNotFoundError(f"No such file path: {file_path}")
        if not target_path.is_dir():
            logger.error(f"Target folder '{target_path}' is invalid or does not exist")
            raise NotADirectoryError(f"No such folder path: {target_path}")

        target_file_path = target_path / file_path.name
        if keep_dup:
            counter = 1
            while target_file_path.exists():
                target_file_path = target_path / f"{file_path.stem} ({counter}){file_path.suffix}"
                counter += 1

        try:
            file_path.rename(target_file_path)
        except PermissionError as e:
            logger.error(f"Permission error when moving '{file_path.name}': '{e}'")
            raise

    @property
    def folder_path(self) -> str:
        """
        Get the root folder path.

        :returns: The absolute path of the root folder as a string.
        :rtype: str
        """
        return str(self._folder_path)

    @folder_path.setter
    def folder_path(self, folder_path: Union[str, pathlib.Path]) -> None:
        """
        Set the root folder path. The provided path will be resolved to an absolute path before being stored.

        :param folder_path: The path to the root folder.
        :type folder_path: Union[str, pathlib.Path]

        :raises TypeError: If folder_path is not a string or pathlib.Path object.
        :raises NotADirectoryError: If folder_path does not exist or is not a directory.
        """
        if not isinstance(folder_path, (str, pathlib.Path)):
            raise TypeError("folder_path should be a `str` or `pathlib.Path` object")

        folder_path = pathlib.Path(folder_path)
        if folder_path.is_dir():
            self._folder_path = folder_path.resolve()
        else:
            logger.error(f"Invalid folder path provided: {folder_path}")
            raise NotADirectoryError(f"No such folder path: {folder_path}")
