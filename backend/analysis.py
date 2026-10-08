import os
import time
import pandas as pd
import networkx as nx

DATA_DIR=os.path.join(os.path.dirname(__file__),"data")

def load_data():
    names=["users","groups","computers","relationships","services","shares","test_scenarios"]
    return {n:pd.read_csv(os.path.join(DATA_DIR,f"{n}.csv")) for n in names}

def build_graph(rel):
    g=nx.DiGraph()
    for _,r in rel.iterrows():
        g.add_edge(str(r.source),str(r.target),relationship=str(r.relationship))
    return g

def enumerate_environment():
    t=time.perf_counter(); d=load_data()
    return {
        "users":d["users"].to_dict("records"),
        "groups":d["groups"].to_dict("records"),
        "computers":d["computers"].to_dict("records"),
        "services":d["services"].to_dict("records"),
        "shares":d["shares"].to_dict("records"),
        "relationships":d["relationships"].to_dict("records"),
        "processing_time_ms":round((time.perf_counter()-t)*1000,2),
        "counts":{k:len(d[k]) for k in ["users","groups","computers","services","shares","relationships"]}
    }

def privileged_groups():
    d=load_data()
    return d.groups.loc[d.groups.group_type.eq("Privileged"),"group_name"].tolist()

def attack_path(source,target):
    d=load_data(); g=build_graph(d.relationships); t=time.perf_counter()
    try:
        nodes=nx.shortest_path(g,source,target)
        edges=[{"source":a,"relationship":g[a][b]["relationship"],"target":b}
               for a,b in zip(nodes,nodes[1:])]
        status="path_found"
    except (nx.NetworkXNoPath,nx.NodeNotFound):
        nodes=[]; edges=[]; status="no_path"
    ms=round((time.perf_counter()-t)*1000,2)
    return {"source":source,"target":target,"status":status,"nodes":nodes,
            "edges":edges,"hops":len(edges),"processing_time_ms":ms}

def all_attack_paths():
    d=load_data(); out=[]
    for u in d.users.username:
        for g in privileged_groups():
            p=attack_path(str(u),g)
            if p["status"]=="path_found": out.append(p)
    return out

def findings():
    d=load_data(); out=[]; rid=1
    def add(sev,cat,title,evidence,reco,score):
        nonlocal rid
        out.append({"id":f"F{rid:03d}","severity":sev,"category":cat,
                    "title":title,"evidence":evidence,"recommendation":reco,
                    "risk_score":score})
        rid+=1
    for _,r in d.relationships.iterrows():
        if r.relationship in ["ADMIN_OF","HAS_ADMIN_ACCESS"]:
            add("HIGH","Excessive Privilege",
                f"{r.source} has administrative access to {r.target}",
                f"{r.source} -> {r.relationship} -> {r.target}",
                "Review administrative access and apply least privilege.",80)
        if r.relationship=="MEMBER_OF" and r.target in ["DomainAdmins","ServerAdmins"]:
            add("HIGH","Privileged Group Membership",
                f"{r.source} is directly linked to {r.target}",
                f"{r.source} -> MEMBER_OF -> {r.target}",
                "Remove unnecessary privileged membership and review group nesting.",100)
    for _,r in d.shares.iterrows():
        if str(r.exposure).lower()=="broad":
            add("MEDIUM","Share Exposure",f"Broadly exposed share: {r.share_name}",
                f"{r.computer} / {r.share_name} ({r.purpose})",
                "Restrict access using groups and least privilege.",40)
    for _,r in d.services.iterrows():
        if str(r.exposure).lower()=="exposed":
            add("MEDIUM","Exposed Service",f"{r.service} exposed on {r.computer}",
                f"Port {r.port}/{r.protocol} / exposure={r.exposure}",
                "Restrict management services to trusted networks.",50)
    return out

def graph_data():
    d=load_data(); g=build_graph(d.relationships)
    nodes=[{"id":str(n),"label":str(n)} for n in g.nodes()]
    edges=[]
    for i,(a,b,x) in enumerate(g.edges(data=True),1):
        edges.append({"id":f"e{i}","source":str(a),"target":str(b),
                      "label":x["relationship"]})
    return {"nodes":nodes,"edges":edges}

def risk_summary():
    f=findings()
    high=sum(x["severity"]=="HIGH" for x in f)
    med=sum(x["severity"]=="MEDIUM" for x in f)
    raw=sum(x["risk_score"] for x in f)
    score=min(100,round(raw/3.5))
    level="LOW" if score<35 else "MEDIUM" if score<70 else "HIGH"
    return {"score":score,"level":level,"high":high,"medium":med,"total":len(f)}

def evaluate():
    d=load_data(); rows=[]; detected=expected=0; times=[]
    t=time.perf_counter(); enumerate_environment()
    enum_ms=round((time.perf_counter()-t)*1000,2)
    for _,s in d.test_scenarios.iterrows():
        exp=str(s.expected).lower()=="yes"
        expected+=int(exp)
        p=attack_path(str(s.source),str(s.target)); found=p["status"]=="path_found"
        detected+=int(found); times.append(p["processing_time_ms"])
        rows.append({"source":s.source,"target":s.target,"expected":exp,
                     "detected":found,"status":p["status"]})
    return {"expected_paths":expected,"detected_paths":detected,
            "detection_rate_percent":round(detected/expected*100,2) if expected else 0,
            "enumeration_time_ms":enum_ms,
            "average_path_time_ms":round(sum(times)/len(times),2) if times else 0,
            "scenarios":rows}

def summary():
    d=load_data(); f=findings(); p=all_attack_paths(); r=risk_summary()
    return {"users":len(d.users),"groups":len(d.groups),"computers":len(d.computers),
            "relationships":len(d.relationships),"services":len(d.services),
            "shares":len(d.shares),"findings":len(f),"attack_paths":len(p),
            "severity":{"HIGH":r["high"],"MEDIUM":r["medium"],"LOW":0},
            "risk":r}
