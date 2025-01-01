import logging
import json
from typing import Dict, Union, List


logger = logging.getLogger(__name__)


class Config:
    """
    Handles loading and setting configurations from/to a JSON file.
    """

    def __init__(self, config_file: str = "config/config.json") -> None:
        """
        Initializes the Config class with the given configuration file.

        :param config_file: The path to the configuration file. Defaults to "config/config.json".
        :type config_file: str, optional
        """
        self.config_file = config_file
        self.configs = self.get_configs()

    @property
    def config_file(self) -> str:
        """
        Returns the path to the configuration file.

        :returns: The path to the configuration file.
        :rtype: str
        """
        return self._config_file

    @config_file.setter
    def config_file(self, file: str) -> None:
        """
        Sets the configuration file path after validating the file type.

        :param file: The path to the configuration file.
        :type file: str

        :raises TypeError: If `file` is not a string.
        :raises ValueError: If the file is not a JSON file.
        """
        if not isinstance(file, str):
            raise TypeError("file should be an `str` object")

        if file.endswith(".json"):
            self._config_file = file
        else:
            logger.error(f"Config file '{file}' should be a JSON file")
            raise ValueError(f"Invalid file type: {file}. Only '.json' files are allowed")

    def get_configs(self) -> Dict[str, Union[Dict[str, str], List[str], bool, str]]:
        """
        Loads the configuration data from the JSON file.

        This method reads the configuration file, verifies required fields, and validates
        their values.

        :returns: The loaded configuration data.
        :rtype: dict

        :raises FileNotFoundError: If the configuration file does not exist.
        :raises KeyError: If any required fields are missing from the configuration file.
        :raises ValueError: If any validation errors occur (e.g., empty folder paths or too many folders).
        """
        try:
            with open(self.config_file) as config:
                config_data = json.load(config)

            required_fields = {"extension_to_folder", "folder_paths", "keep_duplicates", "status_level"}

            missing_fields = required_fields - config_data.keys()
            if missing_fields:
                raise KeyError(f"Missing '{missing_fields}' in '{self.config_file}'")

            if not len(config_data["folder_paths"]):
                raise ValueError(f"'folder_paths' in {self.config_file} cannot be empty")
            elif len(config_data["folder_paths"]) > 20:
                raise ValueError(f"'folder_paths' in {self.config_file} is too large. It should be less than 20")

            return config_data

        except FileNotFoundError:
            logger.error(f"Configuration file '{self.config_file}' not found.")
            raise
        except (KeyError, ValueError) as e:
            logger.error(e)
            raise

    def set_configs(
            self,
            *,
            extension_to_folder: List[str] = None,
            folder_paths: List[str] = None,
            keep_duplicates: str = None,
            status_level: str = None
    ) -> None:
        """
        Updates the configuration file with new values.

        This method allows you to update specific configurations in the JSON file, such as adding
        new extensions and folders, changing the duplicate file behavior, or updating the status level.

        :param extension_to_folder: A list of extension-folder mappings to update.
        :type extension_to_folder: list, optional
        :param folder_paths: A list of folder paths to update.
        :type folder_paths: list, optional
        :param keep_duplicates: A string indicating whether to keep duplicates ("true" or "false").
        :type keep_duplicates: str, optional
        :param status_level: The level of status to display ("all", "success", or "failed").
        :type status_level: str, optional

        :raises TypeError: If any argument is not of the expected type.
        :raises FileNotFoundError: If the configuration file does not exist.
        """
        if not (
            (isinstance(extension_to_folder, list) or extension_to_folder is None) and
            (isinstance(folder_paths, list) or folder_paths is None) and
            (isinstance(keep_duplicates, str) or keep_duplicates is None) and
            (isinstance(status_level, str) or status_level is None)
        ):
            raise TypeError("Invalid argument types provided")

        try:
            with open(self.config_file) as config:
                config_data = json.load(config)

            if extension_to_folder is not None:
                for data in extension_to_folder:
                    if data := data.strip():
                        data_parts = data.split(" ", 1)
                        if len(data_parts) == 2 and data_parts[0].startswith("."):
                            config_data["extension_to_folder"].update({data_parts[0]: data_parts[1].strip()})

            if (folder_paths is not None) and (0 < len(folder_paths) < 20):
                config_data["folder_paths"] = folder_paths

            if keep_duplicates is not None:
                config_data["keep_duplicates"] = True if keep_duplicates == "true" else False

            if (status_level is not None) and (status_level in ("all", "success", "failed")):
                config_data["status_level"] = status_level.lower()

            self.configs = config_data

            with open(self.config_file, "w") as config:
                json.dump(config_data, config, indent=4)
            logger.info("New configurations have been set successfully")

        except FileNotFoundError as e:
            logger.error(f"Configuration file '{self.config_file}' not found.")
            raise
        except TypeError as e:
            logger.error(e)
            raise
