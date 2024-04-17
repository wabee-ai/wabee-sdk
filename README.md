# Semantix Agent Tools

## Requirements

### Quick off

- ✅ Provide user a tool configuration class that holds all the necessary parameters to initialize a tool
- ✅ Ensure tool configuration class contains `name`, `description` by default
- ✅ Provide user a tool input class that holds the tool input schema and a method to parse the query string into the input object
- ✅ Provide user a validation decorator to perform data validation on both input and configuration fields
- ✅ Provide user a base tool class that should be the parent class of all tools
- ✅ Ensure base tool class works as a facade for the langchain base tool and contains `name` and `description` as fields

### First team suggestions

- ✅ Enable user to implement either the sync or async version of execute on a SemantixAgentTool child class
- ✅ Set a default llm on the SemantixAgentToolConfig class
- ✅ Add handlers module to be shared by multiple tools, with the required objects:
  - ✅ \_ALLOWED_MODULES
  - ✅ PythonExecutor
  - ✅ find_split_in_csv
  - ✅ find_encoding_csv
  - ✅ get_timestamp
  - ✅ get_outputfile_path
  - ✅ mount_file_url
