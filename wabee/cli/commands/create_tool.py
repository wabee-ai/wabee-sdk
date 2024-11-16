import inquirer
from wabee.cli.tools.create_tool_service import CreateToolService

def create_tool_command():
    questions = [
        inquirer.Text('name',
                     message="What is your tool's name?"),
        inquirer.List('type',
                     message="What type of tool do you want to create?",
                     choices=['simple', 'complete']),
        inquirer.Text('description',
                     message="Provide a description for your tool"),
        inquirer.Text('version',
                     message="What is the initial version?",
                     default="0.1.0"),
    ]
    
    answers = inquirer.prompt(questions)
    
    if answers:
        service = CreateToolService()
        try:
            service.create_tool(
                name=answers['name'],
                tool_type=answers['type'],
                description=answers['description'],
                version=answers['version']
            )
            print(f"Successfully created tool: {answers['name']}")
        except Exception as e:
            print(f"Error creating tool: {str(e)}")
    else:
        print("Tool creation cancelled")
