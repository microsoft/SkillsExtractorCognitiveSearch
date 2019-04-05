from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Schema


class SkillProperty(str, Enum):
    id = "id"
    name = "standardizedName"

# Azure Search Cognitive Skills Models
class AzureSearchDocumentDataRequest(BaseModel):
    text: str
    language: str = "en"


class AzureSearchDocumentRequest(BaseModel):
    recordId: str
    data: AzureSearchDocumentDataRequest


class AzureSearchDocumentsRequest(BaseModel):
    values: List[AzureSearchDocumentRequest]


class AzureSearchDocumentDataResponse(BaseModel):
    skills: List[str]


class AzureSearchDocumentResponse(BaseModel):
    recordId: str
    data: AzureSearchDocumentDataResponse
    errors: Optional[List[str]]
    warnings: Optional[List[str]]


class AzureSearchDocumentsResponse(BaseModel):
    values: List[AzureSearchDocumentResponse]
