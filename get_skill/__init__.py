import json
import logging

import azure.functions as func
import srsly


skills = srsly.read_json("data/skills.json")


def main(req: func.HttpRequest) -> func.HttpResponse:
    skill_id = req.route_params.get("skill_id")
    logging.info(f"Fetching skill by id {skill_id}")

    if skill_id:
        if skill_id not in skills:
            res = func.HttpResponse(
                f"Not Found: Skill with id {skill_id} does not exist", status_code=404
            )
        else:
            res = func.HttpResponse(json.dumps(skills[skill_id]))
    else:
        res = func.HttpResponse(
            "Please pass a skill_id on the query string or in the request body",
            status_code=400,
        )

    return res
