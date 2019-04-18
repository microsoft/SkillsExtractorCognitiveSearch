# Introduction

The Skills Extractor API is a Named Entity Recognition (NER) tool that takes text input, extracts entities related to skills, then matches concepts mentioned in text to metadata about skills and returns a list of skills from the that text.

## What is a Skill?
For the current goals of the service, we are focused on technical skills. Technical skills are the abilities and knowledge needed to perform specific tasks. They are practical, and often relate to mechanical, information technology, mathematical, or scientific tasks. 
The Taxonomies the API pulls from primarily consist of concepts and tools related to technology. For example, Programming Languages are considered a higher-level technical skill, and C# or Python are a sub of that larger skill.

More examples of Skills:
Machine Learning, Artificial Intelligence, PyTorch, Business, Advertising

## Skill Sources 

We pull skills and technologies from many open online sources and build [Record Linkage](https://github.com/dedupeio/dedupe-examples/tree/master/record_linkage_example) models to conflate skills and categories across each source into a single [Knowledge Graph](https://hackernoon.com/wtf-is-a-knowledge-graph-a16603a1a25f).

Here is a list of our sources: 
* [Coursera](https://www.coursera.org/gsi/)
* [Microsoft Academic Graph](https://academic.microsoft.com/topics)
* [LinkedIn Learning](https://www.linkedin.com/learning/me/skills)
* [GitHub Featured Topics](https://github.com/topics)
* [StackShare Tools](https://stackshare.io/categories)
* [Class Central Subjects Github](https://github.com/classcentral/online-course-taxonomy)
* [ONET Online Hot Technology Index](https://www.onetonline.org/search/hot_tech/)
* [ACM Classifications](https://dl.acm.org/ccs/ccs_flat.cfm)

# Use Cases
The original idea stemmed from a few organizational needs. Here a few: 
*   ### Determine the skills required for a job opening at your company and match applicant resumes based on skills. 
*   ### Extract skills from Learning Content that your company creates to improve search and recommendations. 
*   ### Identify the technical and professional skills of your team or organization and work to close skill gaps.

## Prerequisites

Before running this sample, you must have the following:

* Install [Azure Core Tools version 2.x](functions-run-local.md#v2).

* Install the [Azure CLI]( /cli/azure/install-azure-cli). This article requires the Azure CLI version 2.0 or later. Run `az --version` to find the version you have.  
You can also use the [Azure Cloud Shell](https://shell.azure.com/bash).

# Quickstart: Extract Skills for your data in Azure Search using a Custom Cognitive Skill

If you're unfamiliar with Azure Search Cognitive Skills you can read more about them here:
https://docs.microsoft.com/en-us/azure/search/cognitive-search-concept-intro

### Follow one of the scenarios below

* [Extract Skills from an Existing Search Index](docs/existing_search_index.md)
* [Use the sample Search Scenario of extracting Skills from Jobs and Resumes](docs/sample_search_scenario.md)

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
