from pydantic import BaseModel, Field
from typing import Optional, List

class ImageToolResponse(BaseModel):
    mime_type: str = Field(description="The MIME type of the image.")
    data: str = Field(description="The base64 encoded image data.")

class StructuredToolResponse(BaseModel):
    variable_name: str = Field(description="An intuitive name for a variable that can be used to easily infer what's stored in it. Use specific names that take the variable content into consideration.")
    content: str = Field(description="The content of the tool response.")
    local_file_path: Optional[str] = Field(None, description="Optional path to a local file that contains the full content for what is needed.")
    metadata: Optional[dict] = Field(None, description="Additional metadata to be stored with the response.")
    memory_push: bool = Field(False, description="Indicates whether tool response should be added to memory")
    images: Optional[List[ImageToolResponse]] = Field(None, description="Optional list of images that are part of the response.")
    error: Optional[str] = Field(None, description="Use this field to include an error message if an error occurred during the tool execution.")
