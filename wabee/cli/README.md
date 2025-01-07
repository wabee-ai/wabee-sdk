# Wabee AI CLI

This CLI is part of the Wabee SDK and provides two main functionalities for working with tools:    

1. Creating Tools (CreateToolService in create_tool_service.py):
- Allows creating new tool projects with a basic structure
- Supports both Python and JavaScript/TypeScript tools
- Creates two types of tools:
  - "simple" tools (function-based)
  - "complete" tools (class-based)
- Generated files include:
  - For Python: tool file, requirements.txt, toolspec.yaml, server.py
  - For JavaScript: package.json, TypeScript files, tsconfig.json, server.js

2. Building Tools (BuildToolService in build_tool_service.py):
- Builds tools into container images using Source-to-Image (S2I)
- Supports both Python and JavaScript tools
- Main features:
  - Downloads and manages S2I binary
  - Generates gRPC proto files
  - Detects tool type automatically
  - Builds Python tools using a Python builder image
  - Builds JavaScript tools with additional build steps (TypeScript compilation)
  - Configures the build environment 
  
The CLI handles all the scaffolding and build process complexities, making it easier for developers to create and package tools that can be run as gRPC services. 