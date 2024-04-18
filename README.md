# 🔧 Semantix Agent Tools

## 📋 Requirements

### Quick off

- ✅ Provide user a tool configuration class that holds all the necessary parameters to initialize a tool
- ✅ Ensure tool configuration class contains `name`, `description` by default
- ✅ Provide user a tool input class that holds the tool input schema and a method to parse the query string into the input object
- ✅ Provide user a validation decorator to perform data validation on both input and configuration fields
- ✅ Provide user a base tool class that should be the parent class of all tools
- ✅ Ensure base tool class works as a facade for the [langchain base tool](https://python.langchain.com/docs/modules/tools) and contains `name` and `description` as fields

### First team meeting suggestions

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

### Second team meeting suggestions

- ✅ Remove name and description from config
- ✅ Force developer to define the name and description on the create method
- ✅ Remove binding between handlers and semantix agent tool
- ⬜ Explore input typing on tool run
- ⬜ Enable calling the tool with typed input

### Publishing

- ⬜ Publish package on [pypi](https://pypi.org)
- ⬜ Create CI/CD to publish the package on pypi at every package release

## ⚠️ Issues

### ❗🛡️ Vulnerabilities

```
-> Vulnerability found in restrictedpython version 6.0
   Vulnerability ID: 59430
   Affected spec: >=6.0a1.dev0,<6.1
   ADVISORY: Restrictedpython 6.1 and 5.3 include a fix for
   CVE-2023-37271: Arbitrary code execution via stack frame sandbox escape.ht
   tps://github.com/zopefoundation/RestrictedPython/security/advisories/GHSA-
   wqc8-x2pr-7jqh
   CVE-2023-37271
   For more information about this vulnerability, visit
   https://data.safetycli.com/v/59430/97c
   To ignore this vulnerability, use PyUp vulnerability id 59430 in safety’s
   ignore command-line argument or add the ignore to your safety policy file.


-> Vulnerability found in restrictedpython version 6.0
   Vulnerability ID: 60840
   Affected spec: >=6.0,<6.2
   ADVISORY: RestrictedPython 6.2 and 5.4 include a fix for an
   Information Disclosure vulnerability. Python's "format" functionality
   allows someone controlling the format string to "read" all objects
   accessible through recursive attribute lookup and subscription from
   objects he can access. This can lead to critical information disclosure.
   With 'RestrictedPython', the format functionality is available via the
   'format' and 'format_map' methods of 'str' (and 'Unicode') and via
   'string.Formatter'.https://github.com/advisories/GHSA-xjw2-6jm9-rf67
   CVE-2023-41039
   For more information about this vulnerability, visit
   https://data.safetycli.com/v/60840/97c
   To ignore this vulnerability, use PyUp vulnerability id 60840 in safety’s
   ignore command-line argument or add the ignore to your safety policy file.


-> Vulnerability found in langchain version 0.1.6
   Vulnerability ID: 66051
   Affected spec: <0.1.12
   ADVISORY: Langchain 0.1.12 addresses path traversal vulnerability
   CVE-2024-28088 by deprecating certain functionality in its recursive URL
   loader, enhancing security against unsanitized user input
   exploitation.https://github.com/langchain-ai/langchain/pull/18600
   CVE-2024-28088
   For more information about this vulnerability, visit
   https://data.safetycli.com/v/66051/97c
   To ignore this vulnerability, use PyUp vulnerability id 66051 in safety’s
   ignore command-line argument or add the ignore to your safety policy file.


-> Vulnerability found in langchain version 0.1.6
   Vulnerability ID: 65703
   Affected spec: <0.1.8
   ADVISORY: langchain_experimental (aka LangChain Experimental) in
   LangChain before 0.1.8 allows an attacker to bypass the CVE-2023-44467 fix
   and execute arbitrary code via the __import__, __subclasses__,
   __builtins__, __globals__, __getattribute__, __bases__, __mro__, or
   __base__ attribute in Python code. These are not prohibited by
   pal_chain/base.py. See CVE-2024-27444.
   CVE-2024-27444
   For more information about this vulnerability, visit
   https://data.safetycli.com/v/65703/97c
   To ignore this vulnerability, use PyUp vulnerability id 65703 in safety’s
   ignore command-line argument or add the ignore to your safety policy file.
```
