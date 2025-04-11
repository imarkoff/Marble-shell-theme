import subprocess
from abc import ABC, abstractmethod


class CommandRunner(ABC):
    @abstractmethod
    def run(self, command: list[str], **kwargs) -> subprocess.CompletedProcess:
        """
        Run a command in the shell and return the output.
        :param command: Command to run.
        :param kwargs: Additional arguments for the command.
        :return: Output of the command.
        """
        pass