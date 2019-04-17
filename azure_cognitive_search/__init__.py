import logging
import json
import asyncio
import azure.functions as func
import spacy
from spacy.lang.en import English

from .models import *
from ..services.skills import SkillsExtractor


nlp = English()
skills_extractor = SkillsExtractor(nlp)


async def extract_from_doc(
    doc: AzureSearchDocumentsRequest, skill_property: str = "id"
):
    """Extract Skills from a single Document"""
    extracted_skills = skills_extractor.extract_skills(doc.data.text)
    skills = set()
    for skill_id, skill_info in extracted_skills.items():
        if skill_property == "name":
            skills.add(skill_info["displayName"])
        else:
            skills.add(skill_id)

    return {
        "recordId": doc.recordId,
        "data": {"skills": sorted(list(skills))},
        "warnings": None,
        "errors": None,
    }


async def extract_from_docs(
    docs: AzureSearchDocumentsRequest, skill_property: str = "id"
) -> AzureSearchDocumentsResponse:
    results = []
    for doc in docs:
        result = extract_from_doc(doc, skill_property=skill_property)
        results.append(result)

    res = await asyncio.gather(*results)

    values_res = {"values": res}

    return AzureSearchDocumentsResponse(**values_res)


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    skill_property = req.params.get("skill_property", "id")

    try:
        body = AzureSearchDocumentsRequest(**req.get_json())
        logging.info(body)
    except ValueError:
        return func.HttpResponse("Please pass a valid request body", status_code=400)

    if body:
        response_headers = {"Content-Type": "application/json"}
        values_res = await extract_from_docs(body.values, skill_property)

        return func.HttpResponse(values_res.json(), headers=response_headers)
