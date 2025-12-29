param(
    [Parameter(Mandatory=$true)]
    [string]$ChatId,

    [Parameter(Mandatory=$true)]
    [int]$StartId,

    [Parameter(Mandatory=$true)]
    [int]$EndId,

    [Parameter(Mandatory=$true)]
    [string]$FolderName
)

$TdlPath = ".\tdl\bin\tdl.exe"
$ExportFile = "export_${ChatId}_${StartId}_to_${EndId}.json"

# 1. Export the message metadata
Write-Host "Step 1: Exporting message metadata for Chat ID: $ChatId (Range: $StartId-$EndId)..." -ForegroundColor Cyan
& $TdlPath chat export -c $ChatId -T id -i "$StartId,$EndId" -o $ExportFile

# 2. Check if export was successful
if (Test-Path $ExportFile) {
    Write-Host "Export successful. File saved as $ExportFile." -ForegroundColor Green
    
    # 3. Start the download
    Write-Host "Step 2: downloading files to directory '$FolderName'..." -ForegroundColor Cyan
    & $TdlPath dl -f $ExportFile -d $FolderName
    
    Write-Host "Process Complete!" -ForegroundColor Green
} else {
    Write-Error "Export failed! The JSON file was not created. Please check the Chat ID and Message IDs."
}
