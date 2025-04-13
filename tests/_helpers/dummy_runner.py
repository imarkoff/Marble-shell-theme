from scripts.utils.command_runner.command_runner import CommandRunner


class DummyRunner(CommandRunner):
    def run(self, command: list[str], **kwargs) -> str:
        return "Dummy output"