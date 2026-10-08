# Windows AD Lab Setup Guide

## Recommended VM layout

Use a Windows virtualization platform that supports a private/host-only network. Hyper-V is a good option on Windows Pro/Enterprise; VMware Workstation is another option if already installed.

Recommended starting resources:

| VM | RAM | CPU | Disk |
|---|---:|---:|---:|
| DC01 | 4 GB | 2 vCPU | 50 GB |
| SERVER01 | 3 GB | 2 vCPU | 40 GB |
| PC01 | 3 GB | 2 vCPU | 40 GB |

If the host has limited RAM, run only DC01 first, then add SERVER01 and PC01 later.

## Network

Create a private/host-only virtual switch. Do not bridge the lab to the physical LAN or expose the lab services to the Internet.

Use a simple private range such as `192.168.56.0/24` only if it does not conflict with your existing network. Example lab addresses:

- DC01: `192.168.56.10`
- SERVER01: `192.168.56.20`
- PC01: `192.168.56.30`

Set DC01 as the DNS server for the member machines.

## DC01

1. Install a supported Windows Server evaluation edition.
2. Rename the server to `DC01`.
3. Configure the private lab IP.
4. Run `01-install-dc01.ps1` as Administrator.
5. Allow the VM to reboot.
6. Sign in using the domain administrator created by the promotion process.
7. Run `02-create-ad-objects.ps1`.
8. Run `03-configure-lab-relationships.ps1`.

## SERVER01 and PC01

1. Install Windows on each VM.
2. Give each VM a private lab IP.
3. Set DNS to the DC01 private IP.
4. Join each machine to `corp.local`.
5. Use only throwaway lab credentials.
6. On SERVER01, optionally run `04-configure-server01.ps1`.

## Verification

From DC01, verify:

```powershell
Get-ADUser -Filter * | Select SamAccountName
Get-ADGroup -Filter * | Select SamAccountName
Get-ADGroupMember Employees
Get-ADGroupMember Helpdesk
Get-ADGroupMember ServerAdmins
Get-ADGroupMember DomainAdmins
```

From a domain-joined machine, verify DNS and domain membership before connecting the project to LDAP.
