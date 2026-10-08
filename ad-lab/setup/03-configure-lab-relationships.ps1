# Run ONLY on DC01 in the isolated lab.
# Creates intentionally simple nested-group relationships for attack-path analysis.
# This does not execute an attack or deploy any payload.

$ErrorActionPreference = 'Stop'
Import-Module ActiveDirectory

# ajay -> Employees -> Helpdesk -> ServerAdmins -> DomainAdmins
# The nesting is intentionally visible and should be reported by the project as a risky privilege path.
Add-ADGroupMember -Identity Helpdesk -Members Employees -ErrorAction SilentlyContinue
Add-ADGroupMember -Identity ServerAdmins -Members Helpdesk -ErrorAction SilentlyContinue
Add-ADGroupMember -Identity DomainAdmins -Members ServerAdmins -ErrorAction SilentlyContinue

# Give the IT user a separate direct membership for comparison in the graph.
Add-ADGroupMember -Identity ServerAdmins -Members sarah -ErrorAction SilentlyContinue

Write-Host 'Intentional lab relationships configured.' -ForegroundColor Green
Write-Host ''
Write-Host 'Expected path:' -ForegroundColor Cyan
Write-Host 'ajay -> Employees -> Helpdesk -> ServerAdmins -> DomainAdmins'
Write-Host 'tahir -> Employees -> Helpdesk -> ServerAdmins -> DomainAdmins'
Write-Host 'rahil -> Helpdesk -> ServerAdmins -> DomainAdmins'
Write-Host 'sarah -> ServerAdmins -> DomainAdmins'
