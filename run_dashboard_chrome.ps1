param(
    [int]$Port = 8501,
    [switch]$ReuseExisting
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

$Url = "http://localhost:$Port"

$ChromeCandidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$Chrome = $ChromeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $Chrome) {
    $ChromeCommand = Get-Command chrome.exe -ErrorAction SilentlyContinue
    if ($ChromeCommand) {
        $Chrome = $ChromeCommand.Source
    }
}
if (-not $Chrome) {
    throw "Google Chrome was not found. Install Chrome or add chrome.exe to PATH."
}

function Test-DashboardReady {
    param([string]$TargetUrl)
    try {
        $Response = Invoke-WebRequest -Uri $TargetUrl -UseBasicParsing -TimeoutSec 2
        return $Response.StatusCode -eq 200
    } catch {
        return $false
    }
}

if (-not $ReuseExisting) {
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -like "*streamlit_app.py*" -and
            $_.CommandLine -like "*--server.port $Port*"
        } |
        ForEach-Object {
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
        }
}

if ((-not $ReuseExisting) -or (-not (Test-DashboardReady -TargetUrl $Url))) {
    $StreamlitCommand = Get-Command streamlit -ErrorAction SilentlyContinue
    if ($StreamlitCommand) {
        Start-Process -FilePath $StreamlitCommand.Source -ArgumentList @(
            "run",
            "streamlit_app.py",
            "--server.port",
            "$Port",
            "--server.headless",
            "true"
        ) -WorkingDirectory $ProjectRoot -WindowStyle Hidden | Out-Null
    } else {
        Start-Process -FilePath python -ArgumentList @(
            "-m",
            "streamlit",
            "run",
            "streamlit_app.py",
            "--server.port",
            "$Port",
            "--server.headless",
            "true"
        ) -WorkingDirectory $ProjectRoot -WindowStyle Hidden | Out-Null
    }

    $Ready = $false
    for ($Attempt = 0; $Attempt -lt 30; $Attempt++) {
        Start-Sleep -Seconds 1
        if (Test-DashboardReady -TargetUrl $Url) {
            $Ready = $true
            break
        }
    }
    if (-not $Ready) {
        throw "Streamlit did not respond at $Url."
    }
}

Start-Process -FilePath $Chrome -ArgumentList @($Url)
Write-Host "Dashboard opened in Google Chrome: $Url"
