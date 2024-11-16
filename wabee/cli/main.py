import sys
from argparse import ArgumentParser
import inquirer

from wabee.cli.tools.create_tool_service import CreateToolService


def main() -> None:
    parser = ArgumentParser(
        prog="Wabee AI CLI", description="Wabee AI Command Line Interface"
    )
    
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
