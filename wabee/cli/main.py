import sys
from argparse import ArgumentParser
import inquirer

from wabee.cli.tools.create_tool_service import CreateToolService
from wabee.cli.tools.build_tool_service import BuildToolService


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
    
    # Create the 'build' subcommand under 'tools'
    build_parser = tools_subparsers.add_parser('build', help='Build a tool container')
    build_parser.add_argument('path', help='Path to the tool directory')
    build_parser.add_argument('--image', help='Name for the built image', default=None)
    build_parser.add_argument('--s2i-commit', help='S2I commit hash to use', default=None)
    
    args = parser.parse_args()

    if args.svc_command == "tools":
        if args.act_command == "create":
            # Interactive prompts for tool creation
            questions = [
                inquirer.Text('name', message="What is the name of your tool?"),
                inquirer.List('type',
                            message="What type of tool do you want to create?",
                            choices=['simple', 'complete']),
                inquirer.Text('description',
                            message="Provide a description for your tool"),
                inquirer.Text('version',
                            message="What is the initial version?",
                            default="0.1.0")
            ]
            answers = inquirer.prompt(questions)
            
            if answers:
                service = CreateToolService()
                service.create_tool(
                    name=answers['name'],
                    tool_type=answers['type'],
                    description=answers['description'],
                    version=answers['version']
                )
                print(f"Tool '{answers['name']}' created successfully!")
        elif args.act_command == "build":
            service = BuildToolService(s2i_commit=args.s2i_commit)
            try:
                service.build_tool(args.path, args.image)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
