# Active Directory Lab

This folder contains the reproducible lab configuration for the **AD Attack Simulation with Automated Enumeration and Attack-Path Analysis** project.

## Safety

This is an intentionally configured, isolated lab for authorized educational testing only. Keep the virtual machines on a private/host-only network. Do not connect the lab domain to a production, college, office, or public network.

The scripts create test accounts, groups, memberships, and a small number of documented security relationships. They do not deploy malware, steal credentials, or perform destructive actions.

## Lab topology

```text
Windows Host
    |
    +-- Private/Host-only Virtual Network
           |
           +-- DC01       Windows Server / AD DS / DNS
           |     Domain: corp.local
           |
           +-- SERVER01  Windows Server member machine
           |
           +-- PC01      Windows client
```

## Lab identities

Users: `ajay`, `tahir`, `rahil`, `sarah`, `admin`

Groups: `Employees`, `Helpdesk`, `IT`, `ServerAdmins`, `DomainAdmins`

The intended demonstration relationship is:

```text
ajay -> Employees -> Helpdesk -> ServerAdmins -> DomainAdmins
```

This is a **configuration relationship for graph analysis**, not an instruction to exploit a real environment.

## Setup order

1. Create an isolated private/host-only virtual network in your Windows hypervisor.
2. Create `DC01` and install Windows Server.
3. Run `setup/01-install-dc01.ps1` as Administrator on DC01.
4. After the automatic reboot, run `setup/02-create-ad-objects.ps1` on DC01.
5. Create `SERVER01` and `PC01`, configure static/private lab networking, and join them to `corp.local`.
6. Run `setup/03-configure-lab-relationships.ps1` on DC01.
7. On SERVER01, optionally run `setup/04-configure-server01.ps1` to create the documented lab share.
8. Use `docs/ldap-integration.md` when connecting the existing FastAPI application to the lab.

## Credentials

Do not commit real passwords. The scripts prompt for passwords interactively. Use throwaway lab credentials only.

## Reset

The safest reset is to delete the lab VMs/snapshots and recreate them from the documented scripts. Do not run these scripts against a production domain.
