# setup_and_download.ps1
# PowerShell script to fetch latest tdl Windows release, extract, run interactive login, then download a message link.

param(
    [string]$DownloadDir = "$env:USERPROFILE\Downloads\tdl_downloads",
    [string]$AssetUrl = "https://github.com/iyear/tdl/releases/latest/download/tdl_Windows_64bit.zip",
    [string]$ZipPath = "$PSScriptRoot\tdl_win.zip",
    [string]$BinDir = "$PSScriptRoot\tdl_bin"
)

Write-Host "This script will download tdl, extract it, and run an interactive login. After login, it will download a Telegram message link you provide." -ForegroundColor Cyan

# Ensure directories
if (-not (Test-Path -Path $BinDir)) { New-Item -ItemType Directory -Path $BinDir | Out-Null }
if (-not (Test-Path -Path $DownloadDir)) { New-Item -ItemType Directory -Path $DownloadDir | Out-Null }

# Download the release zip if not already present
if (-not (Test-Path -Path $ZipPath)) {
    Write-Host "Downloading tdl binary from: $AssetUrl" -ForegroundColor Yellow
    Invoke-WebRequest -Uri $AssetUrl -OutFile $ZipPath -UseBasicParsing
} else {
    Write-Host "Using existing zip: $ZipPath" -ForegroundColor Yellow
}

# Extract
Write-Host "Extracting to $BinDir" -ForegroundColor Yellow
Expand-Archive -LiteralPath $ZipPath -DestinationPath $BinDir -Force

# Find tdl.exe inside extracted folder
$tdlExe = Get-ChildItem -Path $BinDir -Filter tdl*.exe -Recurse -File | Select-Object -First 1
if (-not $tdlExe) {
    $tdlExe = Get-ChildItem -Path $BinDir -Filter tdl.exe -Recurse -File | Select-Object -First 1
}
if (-not $tdlExe) {
    Write-Error "tdl.exe not found in extracted archive. Please unzip manually and run 'tdl login' yourself."
    exit 1
}

$tdlPath = $tdlExe.FullName
Write-Host "Found tdl executable: $tdlPath" -ForegroundColor Green

# Run interactive login (user will be prompted for phone/code/password as needed)
Write-Host "Starting interactive login. Choose login type (e.g. code or desktop). Example: run with '-T code' for phone/code flow." -ForegroundColor Cyan
Write-Host "If you already logged in previously, you can skip this step by pressing CTRL+C and proceed to download." -ForegroundColor Cyan

Write-Host "Running: $tdlPath login -T code" -ForegroundColor Yellow
& $tdlPath login -T code

# After login, prompt for message link(s)
$links = Read-Host "Enter one or more Telegram message links (comma-separated), e.g. https://t.me/c/123456789/2345"
if (-not $links) { Write-Error "No links provided. Exiting."; exit 1 }
$urls = $links -split ',' | ForEach-Object { $_.Trim() }

# Build download command
$downloadArgs = @('download')
foreach ($u in $urls) { $downloadArgs += @('-u', $u) }
$downloadArgs += @('-d', $DownloadDir)
$downloadArgs += @('--group')

Write-Host "Running download: $tdlPath $($downloadArgs -join ' ')" -ForegroundColor Yellow
& $tdlPath @downloadArgs

Write-Host "Done. Files saved to: $DownloadDir" -ForegroundColor Green
