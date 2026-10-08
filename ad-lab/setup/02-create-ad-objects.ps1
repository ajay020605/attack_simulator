# Run ONLY on DC01 after AD DS promotion and reboot.
# Creates the lab users and groups. Passwords are entered interactively and are not stored in Git.

$ErrorActionPreference = 'Stop'
Import-Module ActiveDirectory

$domain = Get-ADDomain
$domainDN = $domain.DistinguishedName

$groups = @(
    @{Name='Employees'; Description='Standard employee group'; Category='Security'; Scope='Global'},
    @{Name='Helpdesk'; Description='Helpdesk support group'; Category='Security'; Scope='Global'},
    @{Name='IT'; Description='IT support group'; Category='Security'; Scope='Global'},
    @{Name='ServerAdmins'; Description='Lab server administration group'; Category='Security'; Scope='Global'},
    @{Name='DomainAdmins'; Description='Built-in privileged domain group used as lab target'; Category='Security'; Scope='Global'}
)

foreach ($g in $groups) {
    if (-not (Get-ADGroup -Filter "SamAccountName -eq '$($g.Name)'" -ErrorAction SilentlyContinue)) {
        New-ADGroup -Name $g.Name -SamAccountName $g.Name -GroupScope $g.Scope -GroupCategory $g.Category -Description $g.Description
        Write-Host "Created group $($g.Name)"
    } else {
        Write-Host "Group $($g.Name) already exists"
    }
}

$users = @('ajay','tahir','rahil','sarah','admin')

foreach ($username in $users) {
    $existing = Get-ADUser -Filter "SamAccountName -eq '$username'" -ErrorAction SilentlyContinue
    if (-not $existing) {
        $password = Read-Host "Enter throwaway lab password for $username" -AsSecureString
        New-ADUser `
            -Name $username `
            -SamAccountName $username `
            -UserPrincipalName "$username@$($domain.DNSRoot)" `
            -AccountPassword $password `
            -Enabled $true `
            -ChangePasswordAtLogon $false
        Write-Host "Created user $username"
    } else {
        Write-Host "User $username already exists"
    }
}

# Baseline memberships.
Add-ADGroupMember -Identity Employees -Members ajay,tahir -ErrorAction SilentlyContinue
Add-ADGroupMember -Identity Helpdesk -Members rahil -ErrorAction SilentlyContinue
Add-ADGroupMember -Identity IT -Members sarah -ErrorAction SilentlyContinue

# Known high-privilege baseline for the lab.
Add-ADGroupMember -Identity DomainAdmins -Members admin -ErrorAction SilentlyContinue

Write-Host 'Base AD objects created.' -ForegroundColor Green
Write-Host 'Run 03-configure-lab-relationships.ps1 next.' -ForegroundColor Yellow
