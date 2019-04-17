from collections import defaultdict
from pathlib import Path

from spacy.language import Language
from spacy.pipeline import EntityRuler
from spacy.lang.en.stop_words import STOP_WORDS
import srsly


class SkillsExtractor:
    """Extracts skills from text"""

    def __init__(
        self,
        nlp: Language,
        data_path: Path = Path("_data"),
        query: bool = False,
    ):
        self.nlp = nlp
        self.data_path = data_path
        self.skills = self._get_skills(query=query)

        patterns = self._build_patterns(self.skills)
        ruler = EntityRuler(nlp, overwrite_ents=True)
        ruler.add_patterns(patterns)
        if not self.nlp.has_pipe("skills_ruler"):
            self.nlp.add_pipe(ruler, name="skills_ruler")

    def _get_skills(self, query: bool = False):
        """Query skills from skills collection"""
        skills_path = self.data_path/"skills.json"
        skills = srsly.read_json(skills_path)
        return skills

    def _skill_pattern(self, skill: str, split_token: str = None):
        """Create a single skill pattern"""
        pattern = []
        if split_token:
            split = skill.split(split_token)
        else:
            split = skill.split()
        for b in split:
            if b.upper() == skill:
                pattern.append({"TEXT": b})
            else:
                pattern.append({"LOWER": b.lower()})

        return pattern

    def _build_patterns(self, skills: list, create: bool = False):
        patterns_path = self.data_path/"skill_patterns.jsonl"
        if not patterns_path.exists() or create:
            """Build up lists of spacy token patterns for matcher"""
            patterns = []
            split_tokens = [".", "/", "-"]

            for skill_id, skill_info in skills.items():
                aliases = skill_info['aliases']
                sources = skill_info['sources']
                skill_names = set()
                for al in aliases[skill_id]:
                    skill_names.add(al)
                for source in sources:
                    if "displayName" in source:
                        skill_names.add(source["displayName"])

                for name in skill_names:
                    if name.upper() == name:
                        skill_name = name
                    else:
                        skill_name = name.lower().strip()

                    if skill_name not in STOP_WORDS:
                        pattern = self._skill_pattern(skill_name)

                        if pattern:
                            label = f"SKILL|{skill_id}"
                            patterns.append({"label": label, "pattern": pattern})

                            for t in split_tokens:
                                if t in skill_name:
                                    patterns.append(
                                        {
                                            "label": label,
                                            "pattern": self._skill_pattern(
                                                skill_name, t
                                            ),
                                        }
                                    )

            srsly.write_jsonl(patterns_path, patterns)
            return patterns
        else:
            patterns = srsly.read_jsonl(patterns_path)
            return patterns

    def extract_skills(self, text: str):
        """Extract skills from text"""
        doc = self.nlp(text)
        found_skills = defaultdict(lambda: defaultdict(list))

        for ent in doc.ents:
            if "|" in ent.label_:
                ent_label, skill_id = ent.label_.split("|")
                if ent_label == "SKILL" and skill_id:
                    skill_info = self.skills[skill_id]
                    sources = skill_info['sources']

                    # Some sources have better Skill Descriptions than others.
                    # This is a simple heuristic for cascading through the sources 
                    # to pick the best description available per skill
                    main_source = sources[0]
                    for source in sources:
                        if source["sourceName"] == "Github Topics":
                            main_source = source
                            break
                        elif source["sourceName"] == "Microsoft Academic Topics":
                            main_source = source
                            break
                        elif source["sourceName"] == "Stackshare Skills":
                            main_source = source
                            break

                    found_skills[skill_id]["matches"].append(
                        {
                            "start": ent.start_char,
                            "end": ent.end_char,
                            "label": ent_label,
                            "text": ent.text,
                        }
                    )

                    keys = ["displayName", "shortDescription", "longDescription"]
                    for k in keys:
                        found_skills[skill_id][k] = main_source[k]
                    found_skills[skill_id]["sources"] = [
                        {"name": s["sourceName"], "url": s["url"]} for s in sources
                    ]
        return found_skills
