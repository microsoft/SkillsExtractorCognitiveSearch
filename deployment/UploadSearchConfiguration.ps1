param(
[parameter(mandatory=$true)] [string] $searchAccountName,
[parameter(mandatory=$true)] [string] $searchApiKey,
[parameter(mandatory=$true)] [string] $cosmosDBConnectionString,
[parameter(mandatory=$true)] [string] $cosmosDBAccountName,
[parameter(mandatory=$true)] [string] $storageAccountConnectionString,
[parameter(mandatory=$true)] [string] $storageAccountName,
[parameter(mandatory=$true)] [string] $cognitiveServiceAccountKey
)

# SETUP search service
$search_service_url = "https://$searchAccountName.search.windows.net"
$api_version = "?api-version=2017-11-11-preview"

$search_service_headers = @{
    "api-key" = $searchApiKey
    "Content-Type" = "application/json"
}

# datasources and indexes must be uploaded before indexers
write-host "Uploading datasources..."
$data_sources = get-childitem ./Search/DataSources
foreach ($data_source in $data_sources) {
    $data_source_name = $data_source.BaseName

    $data_source_url = $search_service_url + "/datasources/$data_source_name" + $api_version
    $data_source = get-content ./Search/DataSources/$data_source -raw | ConvertFrom-Json

    if ($data_source_name -eq "resumes") {
        $data_source.credentials.connectionString = $storageAccountConnectionString
    } elseif ($data_source_name -eq "jobs") {
        $data_source.credentials.connectionString = $cosmosDBConnectionString
    }

    $data_source_json = $data_source | ConvertTo-Json

    write-host "url: $data_source_url"
    write-host "body: $data_source_json"
    Invoke-RestMethod -Method Put -Headers $search_service_headers -Uri $data_source_url -Body $data_source_json
}

write-host "Uploading indexes..."
$search_indexes = get-childitem ./Search/Indexes
foreach ($index in $search_indexes) {

    # Upload indexes
    $index_name = $index.BaseName

    $index_url = $search_service_url + "/indexes/$index_name" + $api_version
    $index_json = get-content ./Search/Indexes/$index -raw

    write-host "url: $index_url"
    write-host "body: $index_json"
    try {
        Invoke-RestMethod -Method Put -Headers $search_service_headers -Uri $index_url -Body $index_json
    } catch {
        Invoke-RestMethod -Method Delete -Headers $search_service_headers -Uri $index_url
        Invoke-RestMethod -Method Put -Headers $search_service_headers -Uri $index_url -Body $index_json
    }
}

write-host "Uploading Skillsets..."
$search_skillsets = get-childitem ./Search/Skillsets
foreach ($skillset in $search_skillsets) {
    $skillset_name = $skillset.BaseName

    $skillset_url = $search_service_url + "/skillsets/$skillset_name" + $api_version
    $skillset = get-content ./Search/skillsets/$skillset -raw | ConvertFrom-Json
    $skillset.cognitiveServices.key = $cognitiveServiceAccountKey
    $skillset_json = $skillset | ConvertTo-Json -Depth 6

    write-host "url: $skillset_url"
    write-host "body: $skillset_json"
    Invoke-RestMethod -Method Put -Headers $search_service_headers -Uri $skillset_url -Body $skillset_json
}

write-host "Uploading and running indexers..."
$search_indexers = get-childitem ./Search/Indexers
foreach ($indexer in $search_indexers) {
    $indexer_name = $indexer.BaseName

    $indexer_url = $search_service_url + "/indexers/$indexer_name" + $api_version
    $indexer_json = get-content ./Search/Indexers/$indexer -raw

    write-host "url: $indexer_url"
    write-host "body: $indexer_json"
    Invoke-RestMethod -Method Put -Headers $search_service_headers -Uri $indexer_url -Body $indexer_json

    $reset_indexer_url = $search_service_url + "/indexers/$indexer_name/reset" + $api_version
    $run_indexer_url = $search_service_url + "/indexers/$indexer_name/run" + $api_version
    
    Invoke-RestMethod -Method Post -Headers $search_service_headers -Uri $reset_indexer_url
    Invoke-RestMethod -Method Post -Headers $search_service_headers -Uri $run_indexer_url
}
