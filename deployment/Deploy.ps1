param(
[parameter(mandatory=$true)] [string] $ResourceGroupName,
[parameter(mandatory=$true)] [string] $ResourceGroupLocation
)

New-AzResourceGroup -Name $ResourceGroupName -Location $ResourceGroupLocation
$deployment = New-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateFile .\azuredeploy.json -TemplateParameterFile azuredeploy.parameters.json -Mode Complete

$searchConfigParams = @{}

foreach ($output in $deployment.Outputs.GetEnumerator()) {
    $searchConfigParams.Add($output.Key, $output.Value.Value)
}
$cosmosDBAccountName = $searchConfigParams["cosmosDBAccountName"]
$storageAccountName = $searchConfigParams["storageAccountName"]
$storageAccountKey = $searchConfigParams["storageAccountKey"]
$searchConfigParams.Remove("storageAccountKey")

$searchConfigParamsJson = $searchConfigParams | ConvertTo-Json

write-host "Saving outputs"
write-host $searchConfigParamsJson
$searchConfigParamsJson | set-content .\Search\parameters.json

write-host "Creating Cosmos DB jobs collection"
Invoke-Expression -command "az cosmosdb database create --name $cosmosDBAccountName --db-name db -g $ResourceGroupName"
Invoke-Expression -command "az cosmosdb collection create --name $cosmosDBAccountName --db-name db -g $ResourceGroupName --collection-name jobs --partition-key-path /subCategory --throughput 1000"

write-host "Creating Azure Storage resumes container"
Invoke-Expression -command "az storage container create --account-name $storageAccountName --account-key $storageAccountKey --name resumes"

# & .\UploadSearchConfiguration.ps1 @searchConfigParams