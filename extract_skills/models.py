# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Schema


class SkillProperty(str, Enum):
    id = "id"
    name = "standardizedName"


class RecordDataRequest(BaseModel):
    text: str
    language: str = "en"


class RecordRequest(BaseModel):
    recordId: str
    data: RecordDataRequest


class RecordsRequest(BaseModel):
    values: List[RecordRequest]


class RecordDataResponse(BaseModel):
    skills: List[str]


class ResponseMessage(BaseModel):
    message: str

class RecordResponse(BaseModel):
    recordId: str
    data: RecordDataResponse
    errors: Optional[List[ResponseMessage]]
    warnings: Optional[List[ResponseMessage]]


class RecordsResponse(BaseModel):
    values: List[RecordResponse]
