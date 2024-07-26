![PyPI - Downloads](https://img.shields.io/pypi/dm/wabee-sdk)
![PyPI - Format](https://img.shields.io/pypi/format/wabee-sdk)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/wabee-sdk)
![PyPI - License](https://img.shields.io/pypi/l/wabee-sdk)
![PyPI - Status](https://img.shields.io/pypi/status/wabee-sdk)
![PyPI - Version](https://img.shields.io/pypi/v/wabee-sdk)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/wabee-sdk)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wabee-sdk)

![Wabee AI](https://wabee-public-assets.s3.amazonaws.com/images/wabee-small-box-white.png)

**wabee-sdk** is a Python module for development of modules and extensions for the Wabee agentic AI platform.

Website: https://wabee.ai/

# Installation

## Dependencies

wabee-sdk requires:

- python = ">=3.10,<3.12"
- langchain = "^0.1.14"
- chardet = "^5.2.0"
- pandas = "^2.2.2"
- restrictedpython = "^7.1"
- matplotlib = "^3.8.4"

## User Installation

The easiest way to install the package is through `pip`:

```sh
pip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple wabee-sdk
```

# Command Line Interface

The wabee-sdk also comes as a CLI to make the process of development wabee agents tools faster and easier!

To create a brand new tool, one just needs to run:

```sh
wb tools create tool-name
```

And that's it, with no time wasted implementing boilerplate code, the tool is ready to be executed and updated according to the business requirements.

# Example

## Tool Configuration

To create a tool manually, the first step is to define its configuration. In other words, all the necessary data to initialize the tool must be held by this object.

```python
class APIGatewayToolConfig(WabeeAgentToolConfig):
    base_url: str
    api_key: str
```

## Tool Input

Then, define the tool input, which is the data that will be processed by the tool, for instance

```python
class APIGatewayToolConfig(WabeeAgentToolInput):
    headers: dict[str, str] = WabeeAgentToolField(
        name="headers",
        description="http request headers",
        example={
            "Content-Type": "application/json"
        }
    )
```

Finally, implement the tool itself, following the example below:

## Tool

```python
class APIGatewayTool(WabeeAgentTool):
    base_url: str
    api_key: str

    def execute(
        self,
        api_gateway_tool_input: APIGatewayToolInput
    ) -> str:
        print(f"Requesting API on {self.base_url} with headers: {api_gateway_tool_input.headers}")
        return "200"

    @classmethod
    def create(
        cls,
        api_gateway_tool_config: APIGatewayToolConfig
    ) -> APIGatewayTool:
        return cls(
            name="api_gateway_tool",
            description="api_gateway_tool",
            base_url=api_gateway_tool_config.base_url,
            api_key=api_gateway_tool_config.api_key
        )
```

## Tool Factory

The last step is to expose a factory function so other modules can easily instantiate the tool.

```python
def _create_tool(**kwargs: Any) -> WabeeAgentTool:
    return APIGatewayTool.create(APIGatewayToolConfig(**kwargs))
```

Although, it is possible to create the tool manually, it is highly recommended to create it using the CLI. Moreover, it is mandatory to keep all the classes and functions on the same file!
