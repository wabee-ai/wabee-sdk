import sys
from argparse import ArgumentParser
import inquirer

from wabee.cli.tools.create_tool_service import CreateToolService


def main() -> None:
    parser = ArgumentParser(
        prog="Wabee AI CLI", description="Wabee AI Command Line Interface"
    )
    
    # Add subparsers
    subparsers = parser.add_subparsers(dest='svc_command')
    
    # Create the 'tools' subcommand
    tools_parser = subparsers.add_parser('tools', help='Tools related commands')
    tools_subparsers = tools_parser.add_subparsers(dest='act_command')
    
    # Create the 'create' subcommand under 'tools'
    create_parser = tools_subparsers.add_parser('create', help='Create a new tool')
    
    args = parser.parse_args()

    if args.svc_command == "tools" and args.act_command == "create":
        # Interactive prompts for tool creation
        questions = [
            inquirer.Text('name', message="What is the name of your tool?"),
            inquirer.List('type',
                         message="What type of tool do you want to create?",
                         choices=['simple', 'complete'])
        ]
        answers = inquirer.prompt(questions)
        
        if answers:
            service = CreateToolService()
            service.create_tool(answers['name'], answers['type'])
            print(f"Tool '{answers['name']}' created successfully!")
    else:
        parser.print_help()
        sys.exit(1)
