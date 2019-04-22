# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from spacy.lang.en import English

from ..services.skills import SkillsExtractor


def test_pipe_names():
    nlp = English()
    data_path = '../_data'
    skills_extractor = SkillsExtractor(nlp, data_path=data_path)
    assert skills_extractor.nlp.pipe_names == ['skills_ruler']