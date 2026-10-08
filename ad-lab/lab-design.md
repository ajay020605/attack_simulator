# Lab Design

## Purpose

The lab provides a small Active Directory environment that mirrors the entities used by the CSV simulation so that the same React/FastAPI dashboard can eventually consume either simulated or real LDAP data.

## Objects

| Type | Objects |
|---|---|
| Domain | corp.local |
| Domain Controller | DC01 |
| Member server | SERVER01 |
| Client | PC01 |
| Users | ajay, tahir, rahil, sarah, admin |
| Groups | Employees, Helpdesk, IT, ServerAdmins, DomainAdmins |

## Intentional relationships

- ajay and tahir are ordinary members of Employees.
- rahil is a member of Helpdesk.
- Employees is nested in Helpdesk to demonstrate transitive group membership.
- Helpdesk is nested in ServerAdmins to create a controlled privilege-path example.
- ServerAdmins is nested in DomainAdmins to create the final privileged-group relationship.
- sarah is an IT user with a separate administrative relationship to SERVER01 for comparison.
- admin is a member of DomainAdmins as the known high-privilege baseline.

These relationships are deliberately simple so the project can explain why a graph path exists.

## Expected graph

```text
ajay
  |
  +-- MEMBER_OF --> Employees
                       |
                       +-- MEMBER_OF --> Helpdesk
                                           |
                                           +-- MEMBER_OF --> ServerAdmins
                                                               |
                                                               +-- MEMBER_OF --> DomainAdmins
```

## Security analysis

The application should treat these as relationships to analyze and report. It should not automatically exploit them. Findings should include evidence, severity, and remediation guidance such as least privilege, avoiding unnecessary nested privileged groups, and reviewing administrative access.
