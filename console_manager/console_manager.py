import colorama
import logging
import sys
import os


colorama.init()
logger = logging.getLogger(__name__)


class ConsoleManager:
    """
    Manages console output for displaying status messages with colored flags.

    This class is responsible for formatting and printing messages to the console. It allows filtering
    of messages based on their status and keeps a log of messages in memory.
    """

    flags = {
        "success": f"{colorama.Fore.GREEN}●{colorama.Fore.RESET}",
        "failed": f"{colorama.Fore.RED}●{colorama.Fore.RESET}",
        None: ""
    }

    def __init__(self, output_level: str = "failed") -> None:
        """
        Initializes the ConsoleManager with the specified output level.

        :param output_level: Defines the level of messages to be printed. Options are "all", "success", and "failed".
        :type output_level: str, optional
        """
        self.messages = []
        self.stream = sys.stdout
        self.output_level = output_level

    def print(self, msg: str, flag: str = None) -> None:
        """
        Prints a message to the console with a colored flag indicating its status.

        :param msg: The message to be printed.
        :type msg: str
        :param flag: The status of the message. Can be "success" or "failed". Defaults to None.
        :type flag: str, optional

        :raises ValueError: If an invalid status flag is provided.
        """
        if flag not in self.flags:
            logger.error(f"Invalid status: '{flag}'. Valid options are 'success' and 'failed'")
            raise ValueError(f"Invalid status: '{flag}'. Valid options are 'success' and 'failed'")

        formatted_msg = f"{self.flags[flag]} {msg}\n"
        self.messages.append((formatted_msg, flag))

        if flag and self.output_level != "all" and self.output_level != flag:
            return

        self.stream.write(formatted_msg)

    def filter_by_flag(self, flag: str = "all") -> None:
        """
        Filters and displays messages based on their status flag.

        Displays messages with the specified flag ("all", "success", or "failed"). Clears the console
        before displaying the messages.

        :param flag: The status flag to filter messages by. Options are "all", "success", and "failed".
        :type flag: str, optional

        :raises ValueError: If an invalid status flag is provided.
        """
        if flag not in ("all", "success", "failed"):
            logger.error(f"Invalid status: '{flag}'. Valid options are 'success', 'failed', 'all'")
            raise ValueError(f"Invalid status: '{flag}'. Valid options are 'success', 'failed', 'all'")

        os.system('cls||clear')
        filtered_messages = [msg for msg, msg_flag in self.messages if flag == "all" or flag == msg_flag]

        if not filtered_messages:
            self.stream.write(f"-- There isn't any {flag} message to show. --\n")
        else:
            for msg in filtered_messages:
                self.stream.write(msg)
