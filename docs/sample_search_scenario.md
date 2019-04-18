## Prerequisites

Before running this sample, you must have the following:

* Install the [Az Powershell Module](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-1.7.0)

```powershell
Install-Module -Name Az -AllowClobber -Scope CurrentUser
```

* Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest). This article requires the Azure CLI version 2.0 or later. Run `az --version` to find the version you have.  
You can also use the [Azure Cloud Shell](https://shell.azure.com/bash).

## Deployment Quickstart

Deploy a full sample search scenario with Azure Cosmos DB, Blob Storage, Azure Search and the Skills Extractor as an Azure Function.

Open a Powershell prompt and run the following.
```powershell
git clone https://github.com/Microsoft/SkillsExtractorCognitiveSearch
cd SkillsExtractorCognitiveSearch\deployment
```

You only need to edit 1 parameter in azuredeploy.parameters.json
Change YOUR_PREFIX_HERE to something unique

`azuredeploy.parameters.json`
```json
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "prefixparam": {
            "type": "string",
            "value": "{YOUR_PREFIX_HERE}"
        },
        "dockerImageName": {
            "type": "string",
            "value": "mcr.microsoft.com/wwllab/skills/skills-extractor-cognitive-search"
        }
    }
}
```

Login to your Azure Account using Powershell
```powershell
Connect-AzAccount
```

Set the Azure Subscription you want to use
```powershell
$context = Get-AzSubscription -SubscriptionId ...
Set-AzContext $context
```

Deploy the ARM Template and Search Configuration
```powershell
.\Deploy.ps1 -ResourceGroupName MyResourceGroupName -ResourceGroupLocation westus2
```