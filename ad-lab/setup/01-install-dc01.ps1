# Run ONLY on the isolated DC01 lab VM as Administrator.
# Installs AD DS and promotes this server to a new forest named corp.local.
# The server will reboot after promotion.

$ErrorActionPreference = 'Stop'

$domainName = 'corp.local'
$safeModePassword = Read-Host 'Enter a throwaway DSRM password for this lab' -AsSecureString

Write-Host 'Installing Active Directory Domain Services...' -ForegroundColor Cyan
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools

Write-Host "Promoting DC01 to new forest $domainName ..." -ForegroundColor Cyan
Install-ADDSForest `
    -DomainName $domainName `
    -DomainNetbiosName 'CORP' `
    -SafeModeAdministratorPassword $safeModePassword `
    -InstallDNS `
    -Force
