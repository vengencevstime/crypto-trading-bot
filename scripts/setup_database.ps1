<#
PowerShell setup script for the crypto-trading-bot project.
What it does:
 - Prompts for PostgreSQL connection details
 - Creates the database if it doesn't exist
 - Copies `.env.example` to `.env` (and fills DB values)
 - Installs Python dependencies from `requirements.txt`
 - Runs the migrations module to create tables
 - Runs a quick connection test

Run: Open PowerShell as Administrator (or normal if PostgreSQL accessible) and run:
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_database.ps1
#>

Set-StrictMode -Version Latest

<#
PowerShell setup script for the crypto-trading-bot project.
What it does:
 - Prompts for PostgreSQL connection details
 - Creates the database if it doesn't exist
 - Copies `.env.example` to `.env` (and fills DB values)
 - Installs Python dependencies from `requirements.txt`
 - Runs the migrations module to create tables
 - Runs a quick connection test

Run: Open PowerShell as Administrator (or normal if PostgreSQL accessible) and run:
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_database.ps1
#>

Set-StrictMode -Version Latest

function Prompt-Default {
    param($Message, $Default)
    $value = Read-Host "$Message [$Default]"
    if ([string]::IsNullOrWhiteSpace($value)) { return $Default }
    return $value
}

Write-Host "=== Crypto Trading Bot - Database Setup ===" -ForegroundColor Cyan

$pgBinDefault = 'C:\Program Files\PostgreSQL\18\bin'
$psqlPath = Prompt-Default "PostgreSQL bin folder (contains psql.exe)" $pgBinDefault
$psqlExe = Join-Path $psqlPath 'psql.exe'
$createdbExe = Join-Path $psqlPath 'createdb.exe'

if (-Not (Test-Path $psqlExe)) {
    Write-Host "psql.exe not found at $psqlExe" -ForegroundColor Yellow
    Write-Host "If PostgreSQL is installed in a different location, please provide the correct path." -ForegroundColor Yellow
    $psqlExe = Read-Host "Full path to psql.exe"
}

$dbHost = Prompt-Default "DB host" "localhost"
$dbPort = Prompt-Default "DB port" "5432"
$dbName = Prompt-Default "Database name to create" "crypto_trading_bot"
$dbUser = Prompt-Default "DB user" "postgres"

Write-Host "Enter the password for user '$dbUser' (input will be hidden)" -ForegroundColor Cyan
$securePass = Read-Host -AsSecureString
$plainPass = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePass)
)

# Check if database exists
$env:PGPASSWORD = $plainPass

# Use psql to check DB existence
try {
    $exists = & "$psqlExe" -U $dbUser -h $dbHost -p $dbPort -t -c "SELECT 1 FROM pg_database WHERE datname = '$dbName';" 2>$null
} catch {
    Write-Host "Failed to run psql. Please verify path and credentials." -ForegroundColor Red
    Write-Host "psql path: $psqlExe"
    exit 1
}

if ($exists -and $exists.Trim() -eq '1') {
    Write-Host "Database '$dbName' already exists." -ForegroundColor Green
} else {
    # Try createdb if available, else use psql CREATE DATABASE
    if (Test-Path $createdbExe) {
        Write-Host "Creating database using createdb..."
        & "$createdbExe" -U $dbUser -h $dbHost -p $dbPort $dbName
    } else {
        Write-Host "Creating database using psql CREATE DATABASE..."
        & "$psqlExe" -U $dbUser -h $dbHost -p $dbPort -c "CREATE DATABASE \"$dbName\" ENCODING 'UTF8';"
    }
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Database '$dbName' created successfully." -ForegroundColor Green
    } else {
        Write-Host "Failed to create database. Exit code: $LASTEXITCODE" -ForegroundColor Red
        exit 1
    }
}

# Copy .env.example to .env and replace DB values
$envExamplePath = Join-Path $PSScriptRoot '..\ .env.example' -replace '\\ ','\\'
$envExample = Join-Path $PSScriptRoot '..\.env.example'
$envFile = Join-Path $PSScriptRoot '..\.env'
if (-Not (Test-Path $envExample)) {
    Write-Host "Couldn't find .env.example at project root." -ForegroundColor Yellow
} else {
    if (-Not (Test-Path $envFile)) {
        Copy-Item $envExample -Destination $envFile -Force
        Write-Host "Copied .env.example -> .env" -ForegroundColor Green
    } else {
        Write-Host ".env already exists; not overwriting." -ForegroundColor Yellow
    }

    # Update .env DB values (simple replace)
    $envPath = $envFile
    (Get-Content $envPath) | ForEach-Object {
        $_ -replace '^DB_HOST=.*', "DB_HOST=$dbHost" -replace '^DB_PORT=.*', "DB_PORT=$dbPort" -replace '^DB_NAME=.*', "DB_NAME=$dbName" -replace '^DB_USER=.*', "DB_USER=$dbUser" -replace '^DB_PASSWORD=.*', "DB_PASSWORD=$plainPass"
    } | Set-Content $envPath
    Write-Host "Updated DB settings in .env" -ForegroundColor Green
}

# Install Python requirements
Write-Host "Installing Python dependencies from requirements.txt..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r (Join-Path $PSScriptRoot '..\requirements.txt')
if ($LASTEXITCODE -ne 0) {
    Write-Host "pip install failed. Please inspect the output." -ForegroundColor Red
    exit 1
}

# Run migrations (module)
Write-Host "Running migrations (python -m src.database.migrations)..." -ForegroundColor Cyan
python -m src.database.migrations
if ($LASTEXITCODE -ne 0) {
    Write-Host "Migrations failed. See errors above." -ForegroundColor Red
    exit 1
}

# Quick connection test - write a temporary Python file and run it
Write-Host "Testing DB connection..." -ForegroundColor Cyan
$testPy = @'
from src.database.connection import db
try:
    db.connect()
    print('DB CONNECTED')
except Exception as e:
    print('DB CONNECTION_FAILED:', e)
finally:
    try:
        db.disconnect()
    except:
        pass
'@

$testPath = Join-Path $PSScriptRoot 'tmp_test_db.py'
$testPy | Out-File -Encoding utf8 $testPath
python $testPath
$pyExit = $LASTEXITCODE
Remove-Item $testPath -Force -ErrorAction SilentlyContinue
if ($pyExit -ne 0) {
    Write-Host "DB connection test failed (exit code $pyExit)." -ForegroundColor Red
    exit 1
}

Write-Host "Setup script finished." -ForegroundColor Green
Write-Host "If any step failed, paste the error here and I'll help debug." -ForegroundColor Yellow
