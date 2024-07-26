import sys
from argparse import ArgumentParser

from wabee.cli.tools.create_tool_service import CreateToolService


def main() -> None:
    parser = ArgumentParser(
        prog="Wabee AI CLI", description="Wabee AI Command Line Interface"
    )
    subparsers = parser.add_subparsers(title="Service", dest="svc_command")

    tools_parser = subparsers.add_parser("tools", help="Wabee AI Agent Tools Utilities")
    tools_subparser = tools_parser.add_subparsers(title="Action", dest="act_command")

    create_tool_parser = tools_subparser.add_parser(
        "create", help="Create New Wabee AI Agent Tool"
    )
    create_tool_parser.add_argument("name", help="Agent Tool Name")

    args = parser.parse_args()

    if args.svc_command == "tools" and args.act_command == "create":
        try:
            tool_dir = CreateToolService().execute(args.name)
            print(
                f"Wabee AI Agent Tool named {args.name} was created successfully at {tool_dir}/!"
            )
        except ValueError as e:
            print(str(e))
            sys.exit(1)
    else:
        print("Run `wb -h` to see the available services!")
