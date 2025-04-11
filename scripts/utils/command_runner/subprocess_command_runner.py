import subprocess

from scripts.utils.command_runner.command_runner import CommandRunner


class SubprocessCommandRunner(CommandRunner):
    def run(self, command: list[str], **kwargs) -> subprocess.CompletedProcess:
        return subprocess.run(command, **kwargs)