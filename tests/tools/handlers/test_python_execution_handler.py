from semantix_agents.tools.handlers.python_execution_handler import (
    _ALLOWED_MODULES,
    PythonExecutionHandler,
)


class TestPythonExecutionHandler:
    def test_should_execute_python_code_safely(self) -> None:
        sut = PythonExecutionHandler()

        assert sut.run("print('Hello, world!')") == ["Hello, world!\n"]

    def test_ensure_python_executor_handler_exposes_allowed_modules_as_attribute(
        self,
    ) -> None:
        sut = PythonExecutionHandler()

        assert sut.allowed_modules == _ALLOWED_MODULES
