from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv, io, json
from analysis import summary,enumerate_environment,findings,attack_path,all_attack_paths,graph_data,evaluate,load_data,privileged_groups,risk_summary

app=FastAPI(title="AD Attack Simulation API",version="3.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.get("/api/health")
def health(): return {"status":"ok","mode":"simulation","version":"3.0"}

@app.get("/api/summary")
def get_summary(): return summary()

@app.get("/api/enumeration")
def get_enumeration(): return enumerate_environment()

@app.get("/api/findings")
def get_findings(): return {"findings":findings()}

@app.get("/api/risk")
def get_risk(): return risk_summary()

@app.get("/api/graph")
def get_graph(): return graph_data()

@app.get("/api/attack-path")
def get_attack_path(source:str,target:str): return attack_path(source,target)

@app.get("/api/attack-paths")
def get_attack_paths(): return {"paths":all_attack_paths()}

@app.get("/api/evaluation")
def get_evaluation(): return evaluate()

@app.get("/api/options")
def get_options():
    d=load_data()
    return {"users":d.users.username.tolist(),"groups":d.groups.group_name.tolist(),
            "privileged_groups":privileged_groups()}

@app.get("/api/export")
def export():
    payload={"summary":summary(),"enumeration":enumerate_environment(),
             "findings":findings(),"attack_paths":all_attack_paths(),
             "evaluation":evaluate()}
    return JSONResponse(payload)
