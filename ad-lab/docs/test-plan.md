# AD Lab Test Plan

| Test | Expected result |
|---|---|
| Enumerate users | ajay, tahir, rahil, sarah, admin are returned |
| Enumerate groups | Employees, Helpdesk, IT, ServerAdmins and DomainAdmins are returned |
| Enumerate nested memberships | Employees -> Helpdesk -> ServerAdmins -> DomainAdmins is visible |
| Enumerate computers | DC01, SERVER01 and PC01 are returned when all VMs are online |
| Detect privileged nesting | ServerAdmins -> DomainAdmins is reported as high risk |
| Detect broad share | SERVER01 LabShare is reported as a medium-risk finding |
| Find ajay -> DomainAdmins | A path is detected through the configured memberships |
| Find rahil -> DomainAdmins | A path is detected through Helpdesk and ServerAdmins |
| Evaluation | Detection rate and processing time are recorded |
