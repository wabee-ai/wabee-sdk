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

    # todo
