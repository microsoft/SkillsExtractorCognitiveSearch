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


async def extract_from_text(text: str):
    """Extract skills from raw text"""
    skills = skills_extractor.extract_skills(text)
    skills_list = []

    for skill_id, skill_info in skills.items():
        skills_list.append(
            {
                "id": skill_id,
                "standardizedName": skill_info["name"]
            }
        )
    return skills_list


async def extract_from_doc(doc, skill_property='id'):
    """Extract Skills from a single Document"""

    skills = await extract_from_text(doc.data.text)
    return {
        "recordId": doc.recordId,
        "data": {
            "skills": [s[skill_property] for s in skills]
        },
        "warnings": None,
        "errors": None
    }


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    skill_property = req.params.get('skill_property', 'id')
    
    try:
        body = AzureSearchDocumentsRequest(**req.get_json())
        logging.info(body)
    except ValueError:
        return func.HttpResponse(
             "Please pass a valid request body",
             status_code=400
        )

    if body:
        response_headers = {
            'Content-Type': 'application/json'
        }
        results = []
        for doc in body.values:
            result = extract_from_doc(doc, skill_property=skill_property)
            results.append(result)
        
        res = await asyncio.gather(*results)

        values_res = {
            'values': res
        }

        return func.HttpResponse(json.dumps(values_res), headers=response_headers)
