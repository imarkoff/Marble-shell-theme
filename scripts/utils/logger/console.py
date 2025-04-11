import sys
import threading
from enum import Enum
from typing import Optional

from scripts.utils.logger.logger import LoggerFactory, Logger


class Console(LoggerFactory):
    """Manages console output for concurrent processes with line tracking"""
    _print_lock = threading.Lock()
    _line_mapping = {}
    _next_line = 0

    def create_logger(self, name: Optional[str]=None) -> 'Console.Line':
        """
        Create a logger instance with the given name.
        :param name: Name of the logger.
        :return: Logger instance.
        """
        return Console.Line(name)

    class Line(Logger):
        def __init__(self, name: Optional[str]=None):
            """Initialize a new managed line"""
            self.name = name or f"line_{Console._next_line}"
            self._reserve_line()

        def update(self, message, icon="⏳"):
            """Update the status message for the line"""
            with Console._print_lock:
                # Calculate how many lines to move up
                lines_up = Console._next_line - Console._line_mapping[self.name]
                # Move the cursor to correct line
                if lines_up > 0:
                    sys.stdout.write(f"\033[{lines_up}F")
                # Clear line and write status
                if icon.strip() == "":
                    sys.stdout.write(f"\r\033[K{message}")
                else:
                    sys.stdout.write(f"\r\033[K{icon} {message}")
                # Move the cursor back down
                if lines_up > 0:
                    sys.stdout.write(f"\033[{lines_up}E")
                sys.stdout.flush()

        def success(self, message):
            self.update(message, "✅")

        def error(self, message):
            self.update(message, "❌")

        def warn(self, message):
            self.update(message, "⚠️")

        def info(self, message):
            self.update(message, "ℹ️ ")

        def _reserve_line(self):
            """Reserve a line for future updates"""
            with Console._print_lock:
                line_number = Console._next_line
                Console._next_line += 1
                Console._line_mapping[self.name] = line_number
                sys.stdout.write(f"\n")  # Ensure we have a new line
                sys.stdout.flush()
                return line_number

    @staticmethod
    def format(text: str, color: Optional['Color']=None, format_type: Optional['Format']=None):
        """Apply color and formatting to text"""
        formatted_text = text

        if color:
            formatted_text = color.value + formatted_text + Color.NORMAL.value
        if format_type:
            formatted_text = format_type.value + formatted_text + Format.NORMAL.value

        return formatted_text


class Color(Enum):
    """ANSI color codes for terminal output"""
    NORMAL = '\033[0m'  # Reset color
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

    @classmethod
    def get(cls, color: str, default: Optional['Color']=None) -> Optional['Color']:
        return getattr(cls, color.upper(), default)


class Format(Enum):
    """ANSI formatting codes for terminal output"""
    NORMAL = '\033[0m'  # Reset formatting
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'