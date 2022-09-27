> # Deprecation Notice
> We've launched a better version of this service with Azure Cognitive Services - Text Analytics in the new V3 of the Named Entity Recognition (NER) endpoint. 

> ## NER V3 Information
> You can read more about this work and how to use it here:
> * Calling the API - https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/how-tos/text-analytics-how-to-entity-linking?tabs=version-3
> * `Skill` Type information - https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/named-entity-types?tabs=general#skill

> ## (NEW) Custom Entity Lookup Skill
> Azure Cognitive Search recently introduced a new built-in Cognitive Skill that does essentially what this repository does. You provide a dictionary of terms you want to match and it will extract those for you from any text field in your search index. You can read more about that here: https://docs.microsoft.com/en-us/azure/search/cognitive-search-skill-custom-entity-lookup

> ## Custom Cognitive Skill with Containers
> This repo is no longer supported but you're free to use the index and skill definitions provided to enable the personalized job recommendations scenario. If you are just looking to deploy a container as a custom skill, I highly recommend utilizing this more generic cookiecutter repository: https://github.com/microsoft/cookiecutter-spacy-fastapi. We will continue to support this project.
> For more information on deploying Containers on Azure see:
> * [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service)
> * [Azure Container Instances (ACI)](https://azure.microsoft.com/en-us/services/container-instances/)

---

# Introduction

The Skills Extractor is a Named Entity Recognition (NER) model that takes text as input, extracts skill entities from that text, then matches these skills to a knowledge base (in this sample a simple JSON file) containing metadata on each skill. It then returns a flat list of the skills identified.

## Definitions

### What is a Cognitive Skill?
A Cognitive Skill is a Feature of Azure Search designed to Augment data in a search index.

### What is a Skill in terms of the Skills Extractor?
A Skill is a Technical Concept/Tool or a Business related/Personal attribute.

Example skills:
Machine Learning, Artificial Intelligence, PyTorch, Business, Advertising

For the current goals of the service, we are focused on technical skills. Technical skills are the abilities and knowledge needed to perform specific tasks. They are practical, and often relate to mechanical, information technology, mathematical, or scientific tasks. 
The Taxonomies the API pulls from primarily consist of concepts and tools related to technology. For example, Programming Languages are considered a higher-level technical skill, and C# or Python are a sub of that larger skill.

> P.S. Sorry for the confusing naming.

## Skill Sources 

We pull skills and technologies from many open online sources and build [Record Linkage](https://github.com/dedupeio/dedupe-examples/tree/master/record_linkage_example) models to conflate skills and categories across each source into a single [Knowledge Graph](https://en.wikipedia.org/wiki/Knowledge_Graph).

Here is a list of our sources: 
* [Coursera](https://www.coursera.org/gsi/)
* [Microsoft Academic Graph](https://academic.microsoft.com/topics)
* [GitHub Featured Topics](https://github.com/topics)
* [StackShare Tools](https://stackshare.io/categories)
* [Class Central Subjects Github](https://github.com/classcentral/online-course-taxonomy)
* [ONET Online Hot Technology Index](https://www.onetonline.org/search/hot_tech/)
* [ACM Classifications](https://dl.acm.org/ccs/ccs_flat.cfm)

# Use Cases
The original idea stemmed from a few organizational needs. Here are a few: 
*   #### Determine the skills required for a job opening at your company and match applicant resumes based on skills. 
*   #### Extract skills from Learning Content that your company creates to improve search and recommendations. 
*   #### Identify the technical and professional skills of your team or organization and work to close skill gaps.

## Prerequisites

Before running this sample, you must have the following:

* Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest). This article requires the Azure CLI version 2.0 or later. Run `az --version` to find the version you have.  
You can also use the [Azure Cloud Shell](https://shell.azure.com/bash).

## Dependencies

* SpaCy v2.1 - NLP in Python https://spacy.io
* Azure Functions Python Worker - https://github.com/Azure/azure-functions-python-worker

# Quickstart: Extract Skills for your data in Azure Search using a Custom Cognitive Skill

If you're unfamiliar with Azure Search Cognitive Skills you can read more about them here:
https://docs.microsoft.com/en-us/azure/search/cognitive-search-concept-intro

### Follow one of the scenarios below

1. [Extract Skills from an Existing Search Index](docs/existing_search_index.md)
2. [Use the sample Search Scenario of extracting Skills from Jobs and Resumes](docs/sample_search_scenario.md)


### Create your own Custom Cognitive Skill

If you would like to create your own Custom Skill leveraging the NLP power of the Python Ecosystem you can use this cookiecutter project to bootstrap a containerized API to deploy in your own infrastructure.

<a href="https://github.com/Microsoft/cookiecutter-azure-search-cognitive-skill" target="_blank">https://github.com/Microsoft/cookiecutter-azure-search-cognitive-skill</a>

### Feedback & Support 
We’re eager to improve, so please take a couple of minutes to answer some questions about your experience https://aka.ms/AA4xoy5.
For support, please contact: WWL_Skills_Service@microsoft.com

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
