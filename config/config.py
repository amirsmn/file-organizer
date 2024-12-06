from typing import Dict, Union, List
import logging
import colorama
import json


class Config:
    """Handles loading, setting configurations from/to a JSON file.

    This class provides functionality to load configuration from a JSON file, set new
    configurations, and display the status of certain operations based on a configured
    level of verbosity.

    Attributes:
            config_file (str): The path to the JSON configuration file.
            configs (Dict): Loaded configurations from the JSON file.
    """

    def __init__(self, config_file: str = "config/config.json") -> None:
        """Initializes the Config class with the given configuration file.

        Args:
            config_file (str, optional): The path to the configuration file. Defaults to
                                         "config/config.json".
        """
        self.config_file = config_file
        self.configs = self.get_configs()

    @property
    def config_file(self) -> str:
        """Returns the path to the configuration file.

        Returns:
            str: The path to the configuration file.
        """
        return self._config_file

    @config_file.setter
    def config_file(self, file: str) -> None:
        """Sets the configuration file path after validating the file type.

        Args:
            file (str): The path to the configuration file.

        Raises:
            TypeError: If `file` is not a string.
            ValueError: If the file is not a JSON file.
        """
        if not isinstance(file, str):
            raise TypeError("file should be an `str` object")

        if file.endswith(".json"):
            self._config_file = file
        else:
            logging.error(f"Config file '{file}' should be a JSON file")
            raise ValueError(f"Invalide file type: {file}. Only '.json' files are allowed")

    def get_configs(self) -> Dict[str, Union[Dict[str, str], List[str], bool, str]]:
        """Loads the configuration data from the JSON file.

        This method reads the configuration file, verifies required fields, and validates
        their values.

        Returns:
            Dict[str, Union[Dict[str, str], List[str], bool, str]]: The loaded configuration data.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            KeyError: If any required fields are missing from the configuration file.
            ValueError: If any validation errors occur (e.g., empty folder paths or too many folders).
        """
        try:
            with open(self.config_file) as config:
                config_data = json.load(config)

            if "extension_to_folder" not in config_data:
                raise KeyError(f"Missing 'extension_to_folder' in '{self.config_file}'")

            if "folder_paths" not in config_data:
                raise KeyError(f"Missing 'folder_paths' in '{self.config_file}'")
            elif not (folders_count := len(config_data["folder_paths"])):
                raise ValueError(f"'folder_paths' in {self.config_file} cannot be empty")
            elif folders_count > 20:
                raise ValueError(
                        f"folder_paths in {self.config_file} is too large. "
                        f"Current folders number is {folders_count}"
                )

            if "keep_duplicates" not in config_data:
                raise KeyError(f"Missing 'keep_duplicates' in '{self.config_file}'")

            if "status_level" not in config_data:
                raise KeyError(f"Missing 'status_level' in '{self.config_file}'")

            return config_data

        except FileNotFoundError:
            logging.error(f"Configuration file '{self.config_file}' not found.")
            raise
        except KeyError as e:
            logging.error(e)
            raise
        except ValueError as e:
            logging.error(e)
            raise

    def set_configs(
            self,
            *,
            extension_to_folder: List[str] = None,
            folder_paths: List[str] = None,
            keep_duplicates: str = None,
            status_level: str = None
    ) -> None:
        """Updates the configuration file with new values.

        This method allows you to update specific configurations in the JSON file, such as adding
        new extensions and folders, changing the duplicate file behavior, or updating the status level.

        Args:
            extension_to_folder (List[str], optional): A list of extension-folder mappings to update.
            folder_paths (List[str], optional): A list of folder paths to update.
            keep_duplicates (str, optional): A string indicating whether to keep duplicates ("true" or "false").
            status_level (str, optional): The level of status to display ("all", "success", or "failed").

        Raises:
            TypeError: If any argument is not of the expected type.
            FileNotFoundError: If the configuration file does not exist.
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
                        if len(data_parts) == 2 and "." in data_parts[0]:
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
            logging.info("New configurations have been set successfully")

        except FileNotFoundError as e:
            logging.error(f"Configuration file '{self.config_file}' not found.")
            raise
        except TypeError as e:
            logging.error(e)
            raise

    def display_status(self, status: str, msg: str) -> None:
        """Displays a status message to the console, formatted with color based on the status.

        Args:
            status (str): The status of the operation ("success" or "failed").
            msg (str): The message to display.

        If the `status_level` in the configuration is set to a value that does not match the provided
        `status`, the message is not displayed.
        """
        if self.configs["status_level"] != "all" and self.configs["status_level"] != status:
            return

        status_symbols = {
            "success": f"{colorama.Fore.GREEN}●{colorama.Fore.RESET}",
            "failed": f"{colorama.Fore.RED}●{colorama.Fore.RESET}",
        }

        if status not in status_symbols:
            logging.warning(f"Invalid status: '{status}'. Valid options are 'success' and 'failed'")
            return

        print(f"{status_symbols[status]} {msg}")

