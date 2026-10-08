# LDAP Integration Plan

The existing application has a simulation mode based on CSV files. The next application phase should add an `ad` mode that reads the same logical entities through LDAP.

## Recommended flow

```text
Active Directory
      |
      | LDAP/LDAPS
      v
Python AD collector
      |
      v
Normalized records
      |
      +--> users
      +--> groups
      +--> computers
      +--> memberships
      +--> relationships
      |
      v
Existing NetworkX analysis
      |
      v
FastAPI
      |
      v
React dashboard
```

## Configuration

Keep secrets outside Git. Use environment variables or a local `.env` file that is ignored by Git.

Example variables:

```text
AD_MODE=ad
AD_SERVER=192.168.56.10
AD_DOMAIN=corp.local
AD_USERNAME=<lab-account>
AD_PASSWORD=<lab-password>
```

Use a dedicated low-privilege read-only lab account for enumeration rather than a domain administrator account.

## Normalization

The collector should convert LDAP results to the same schema already used by the CSV simulation. That allows the React dashboard and NetworkX analysis to remain mostly unchanged.

## Scope

For the mini project, start with:

- users
- groups
- group memberships
- computers
- selected service information
- selected shares

Do not add automated exploitation, credential dumping, persistence, or destructive actions.
