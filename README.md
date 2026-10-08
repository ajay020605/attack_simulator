# Active Directory Attack Simulation — COMPLETE

Mini cybersecurity project for controlled AD enumeration, security analysis and attack-path intelligence.

## Included
- React + Vite dashboard
- FastAPI/Python backend
- Pandas enumeration
- NetworkX attack graph
- Security findings
- Risk scoring
- Attack-path analyzer
- Graph relationship view
- Evaluation metrics
- Search/filtering
- JSON export endpoint
- Methodology page
- Docker Compose
- Simulated AD dataset using ajay, tahir and rahil

## Run

```bash
docker compose up --build
```

Dashboard:
http://localhost:5173

API docs:
http://localhost:8000/docs

Stop:
```bash
docker compose down
```

## Next stage

The intended next stage is an isolated Windows Server Active Directory lab. The application should enumerate an authorized lab through a dedicated AD/LDAP provider. Do not connect it to production or third-party systems.

## Active Directory Lab

The `ad-lab/` directory contains the reproducible, isolated Windows AD lab configuration. It includes PowerShell setup scripts, topology documentation, test cases, and the LDAP integration plan. Run the scripts only inside an authorized private lab.
