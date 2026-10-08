# Run ONLY on the isolated SERVER01 member-server VM as Administrator.
# Creates a harmless lab share for enumeration testing.

$ErrorActionPreference = 'Stop'

$path = 'C:\LabShare'
New-Item -ItemType Directory -Path $path -Force | Out-Null
Set-Content -Path "$path\README.txt" -Value 'Authorized AD lab share for enumeration testing.'

if (-not (Get-SmbShare -Name 'LabShare' -ErrorAction SilentlyContinue)) {
    New-SmbShare -Name 'LabShare' -Path $path -Description 'Authorized AD lab test share' -ReadAccess 'Everyone'
}

Write-Host 'SERVER01 LabShare created.' -ForegroundColor Green
Write-Host 'This share is intentionally broad for the lab and should be reported as a finding.' -ForegroundColor Yellow
