## Requirements

- ✅ Enable user to implement either the sync or async version of execute on a SemantixAgentTool child class
- ✅ Set a default llm on the SemantixAgentToolConfig class
- Add file handling module to be shared by multiple tools, with the required objects:
  - \_ALLOWED_MODULES
  - PythonExecutor
  - find_split_in_csv
  - find_encoding_csv
  - get_timestamp
