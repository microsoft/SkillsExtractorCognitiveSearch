# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import json
import logging

import azure.functions as func
import spacy
from spacy.lang.en import English

from ..services.skills import SkillsExtractor
from .models import *

nlp = English()
skills_extractor = SkillsExtractor(nlp)


async def extract_from_record(
    record: RecordRequest, skill_property: str = "id"
):
    """Extract Skills from a single RecordRequest"""
    extracted_skills = skills_extractor.extract_skills(record.data.text)
    skills = set()
    for skill_id, skill_info in extracted_skills.items():
        if skill_property == "name":
            skills.add(skill_info["displayName"])
        else:
            skills.add(skill_id)

    return {
        "recordId": record.recordId,
        "data": {"skills": sorted(list(skills))},
        "warnings": None,
        "errors": None,
    }


async def extract_from_records(
    records: RecordsRequest, skill_property: str = "id"
) -> RecordsResponse:
    """Handles async logic to extract skills from each record."""
    results = []
    for record in records:
        result = extract_from_record(record, skill_property=skill_property)
        results.append(result)

    res = await asyncio.gather(*results)

    values_res = {"values": res}

    return RecordsResponse(**values_res)


async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Extract Skills from a Batch of Records.
    e.g.
    Request Body:
    {
        "values": [
                {
                    "recordId": "a1",
                    "data": {
                        "text": "This Job will require expertise in Machine Learning and Data Analysis"
                    }
                }
        ]
    }

    Response:
    {
        "values": [
                {
                    "recordId": "a1",
                    "data": {
                        "skills": [
                            "Machine Learning",
                            "Data Analysis"
                        ]
                    }
                }
        ]
    }
    """

    skill_property = req.params.get("skill_property", "id")

    try:
        body = RecordsRequest(**req.get_json())
        logging.info(body)
    except ValueError:
        return func.HttpResponse("Please pass a valid request body", status_code=400)

    if body:
        logging.info(f"Extracting Skills from {len(body.values)} Records.")

        response_headers = {"Content-Type": "application/json"}
        values_res = await extract_from_records(body.values, skill_property)

        return func.HttpResponse(values_res.json(), headers=response_headers)
