from collections import defaultdict
import json
import os

from spacy.tokens import Span
from spacy.matcher import Matcher
from spacy.lang.en.stop_words import STOP_WORDS


Span.set_extension("skill_id", default=None, force=True)
Span.set_extension("skill_standardized_name", default=None, force=True)
Span.set_extension("skill_standardized_description", default=None, force=True)
Span.set_extension("skill_synonyms", default=None, force=True)
Span.set_extension("skill_related_skills", default=None, force=True)
Span.set_extension("skill_sources", default=None, force=True)


class SkillMatcher:
    """Spacy pipeline component for matching skills"""

    def __init__(self, nlp, name, skills, entity_label):
        self.nlp = nlp
        self.name = name
        self.skills = skills
        nlp.vocab.strings.add(entity_label)
        self.entity_label_id = nlp.vocab.strings[entity_label]
        patterns = self.build_patterns(skills)
        self.matcher = self.build_matcher(patterns)

    def __call__(self, doc):
        """Identify skill matches, add custom extension attributes to spans,
        and append the skill match spans to the doc.ents"""
        matches = list(self.matcher(doc))
        matches = set(
            [(m_id, start, end) for m_id, start, end in matches if start != end]
        )

        matches = sorted(matches, key=self.get_sort_key, reverse=True)
        entities = list(doc.ents)
        new_entities = []
        seen_tokens = set()

        for match_id, start, end in matches:
            # check for end - 1 here because boundaries are inclusive
            if start not in seen_tokens and end - 1 not in seen_tokens:
                span = Span(doc, start, end, label=self.entity_label_id)
                skill_id = self.nlp.vocab.strings[match_id]

                sources = self.skills[skill_id]

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
                for source in sources:
                    if "displayName" in source:
                        span._.skill_id = skill_id
                        span._.skill_standardized_name = main_source["displayName"]
                        span._.skill_standardized_description = main_source[
                            "shortDescription"
                        ]

                span._.skill_sources = [
                    {"name": s["sourceName"], "url": s["url"]} for s in sources
                ]
                new_entities.append(span)

                entities = [
                    e for e in entities if not (e.start < end and e.end > start)
                ]
                seen_tokens.update(range(start, end))
        doc.ents = entities + new_entities
        return doc

    def get_sort_key(self, m):
        """Used to disambiguate overlapping entities"""
        return (m[2] - m[1], m[1])

    def skill_pattern(self, skill, split_token=None):
        """Create a single skill pattern"""
        pattern = []
        if split_token:
            split = skill.split(split_token)
        else:
            split = skill.split()
        for b in split:
            if b.upper() == skill:
                pattern.append({"ORTH": b})
            else:
                pattern.append({"LOWER": b.lower()})

        return pattern

    def build_patterns(self, skills):
        """Build up lists of spacy token patterns for matcher"""
        patterns = defaultdict(list)
        split_tokens = [".", "/"]
        special_case_synonyms = {
            "algorithm": ["algorithms"],
            "artificial-intelligence": ["ai", "AI"],
            "machine-learning": ["ml", "ML"],
            "natural-language-processing": ["nlp", "NLP"],
        }

        for skill_id, sources in skills.items():
            skill_names = set()
            if skill_id in special_case_synonyms:
                for syn in special_case_synonyms[skill_id]:
                    skill_names.add(syn)
            for source in sources:
                if "displayName" in source:
                    skill_names.add(source["displayName"])

            for name in skill_names:
                if name.upper() == name:
                    skill_name = name
                else:
                    skill_name = name.lower().strip()

                if skill_name not in STOP_WORDS:
                    pattern = self.skill_pattern(skill_name)

                    if pattern:
                        patterns[skill_id].append(pattern)

                        for t in split_tokens:
                            if t in skill_name:
                                patterns[skill_id].append(
                                    (self.skill_pattern(skill_name, t))
                                )
        return patterns

    def build_matcher(self, patterns):
        """Build rule-based token matcher for skills"""
        matcher = Matcher(self.nlp.vocab)
        for skill_id, patterns in patterns.items():
            if patterns:
                matcher.add(skill_id, None, *patterns)
        return matcher


class SkillsExtractor:
    """Extracts skills from text"""

    def __init__(self, nlp):
        self.nlp = nlp

        with open("_data/skills.json") as skills_file:
            self.skills = json.load(skills_file)

        skill_matcher = SkillMatcher(self.nlp, "skill_matcher", self.skills, "SKILL")
        if not self.nlp.has_pipe(skill_matcher.name):
            self.nlp.add_pipe(skill_matcher)

    def extract_skills(self, text):
        """Extract skills from text using the 
        Spacy Matcher API for custom Skills Patterns"""
        doc = self.nlp(text)
        found_skills = defaultdict(lambda: defaultdict(list))

        for ent in doc.ents:
            if ent.label_ == "SKILL":
                found_skills[ent._.skill_id]["matches"].append(
                    {
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "label": ent.label_,
                        "text": ent.text,
                    }
                )
                if "name" not in found_skills[ent._.skill_id]:
                    found_skills[ent._.skill_id]["name"] = ent._.skill_standardized_name
                if "description" not in found_skills[ent._.skill_id]:
                    found_skills[ent._.skill_id][
                        "description"
                    ] = ent._.skill_standardized_description
                if "sources" not in found_skills[ent._.skill_id]:
                    found_skills[ent._.skill_id]["sources"] = ent._.skill_sources

        return found_skills
