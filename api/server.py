#!/usr/bin/env python3
"""Winnex Proof-of-Audit API — FastAPI verification service."""
import os, sys, json, hashlib
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
sys.path.insert(0, os.path.join(os.path.dirname(__file__),".."))
from src.chain import WinnexChain

app = FastAPI(title="Winnex Proof-of-Audit API", version="2.0.0",
    contact={"name":"Winnex AI","email":"pay@winnex.ai"},
    license_info={"name":"BSL 1.1","url":"https://github.com/winnex-ai/winnex-proof-of-audit"})

chains = {}

def get_chain(n="polygon"):
    if n not in chains:
        a = os.environ.get(f"CONTRACT_{n.upper()}")
        if a: chains[n] = WinnexChain(chain=n, contract_address=a)
    return chains.get(n)

class ProofRequest(BaseModel):
    proof_hash: str; chain: str = "polygon"

class BatchSubmit(BaseModel):
    merkle_root: str; proof_count: int; chain: str = "polygon"

@app.get("/")
def root():
    return {"service":"Winnex Proof-of-Audit","version":"2.0.0",
        "blockchains":WinnexChain.supported_chains(),
        "regulations":["EU_AI_ACT","LGPD","GDPR","HIPAA"]}

@app.get("/verify/{proof_hash}")
def verify(proof_hash: str, chain: str = "polygon"):
    bc = get_chain(chain)
    if not bc: raise HTTPException(404,f"Chain {chain} not configured")
    return bc.verify_on_chain(proof_hash)

@app.post("/verify")
def verify_post(req: ProofRequest):
    bc = get_chain(req.chain)
    if not bc: raise HTTPException(404,f"Chain {req.chain} not configured")
    return bc.verify_on_chain(req.proof_hash)

@app.post("/submit-batch")
def submit_batch(req: BatchSubmit):
    pk = os.environ.get("WINNEX_DEPLOY_KEY")
    if not pk: raise HTTPException(500,"Deploy key not configured")
    bc = get_chain(req.chain)
    if not bc: raise HTTPException(404,f"Chain {req.chain} not configured")
    return bc.submit_batch(req.merkle_root, req.proof_count)

@app.get("/stats")
def stats(chain: str = "polygon"):
    bc = get_chain(chain)
    if not bc: raise HTTPException(404,f"Chain {chain} not configured")
    return bc.get_stats()

@app.get("/compliance/{regulation}")
def compliance(regulation: str):
    regs = {
        "EU_AI_ACT":{"status":"compliant","articles":["Art.13","Art.14","Art.15"],
            "evidence":"Per-document Cauchy-Schwarz bound proof"},
        "LGPD":{"status":"compliant","articles":["Art.20"],
            "evidence":"Full audit trail with on-chain verification"},
        "GDPR":{"status":"compliant","articles":["Art.22"],
            "evidence":"Mathematical proof on blockchain"},
        "HIPAA":{"status":"compliant","articles":["sec.164.524"],
            "evidence":"Deterministic search, zero bound violations"}
    }
    r = regulation.upper()
    if r not in regs: raise HTTPException(404,f"Regulation {r} not found")
    return regs[r]

@app.get("/chains")
def list_chains():
    return {"chains":WinnexChain.supported_chains()}

if __name__=="__main__":
    port = int(os.environ.get("PORT",8443))
    uvicorn.run("api.server:app", host="0.0.0.0", port=port)
