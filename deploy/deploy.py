#!/usr/bin/env python3
"""Deploy WinnexAudit.sol to target chain."""
import os, sys, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def compile_contract():
    import subprocess
    cp = os.path.join(os.path.dirname(__file__), "..", "contracts", "WinnexAudit.sol")
    od = os.path.join(os.path.dirname(__file__))
    try:
        subprocess.run(["solc","--abi","--bin","--overwrite","-o",od,cp],check=True,capture_output=True)
        print(f"Compiled -> {od}/WinnexAudit.abi")
        return True
    except:
        try:
            subprocess.run(["npx","hardhat","compile"],check=True,capture_output=True)
            return True
        except:
            print("WARNING: Install solc or hardhat to compile"); return False

def deploy_contract(chain, pk):
    from src.chain import WinnexChain
    from web3 import Web3
    from web3.middleware import geth_poa_middleware
    cc = WinnexChain.SUPPORTED_CHAINS[chain]
    w3 = Web3(Web3.HTTPProvider(cc["rpc"]))
    if chain in ("polygon","polygon-mumbai"):
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    acct = w3.eth.account.from_key(pk)
    print(f"Deployer: {acct.address} balance={w3.eth.get_balance(acct.address)/1e18:.4f}")
    bip = os.path.join(os.path.dirname(__file__),"WinnexAudit.bin")
    aip = os.path.join(os.path.dirname(__file__),"WinnexAudit.abi")
    if not os.path.exists(bip) or not os.path.exists(aip):
        print("ERROR: Compile first"); return None
    with open(aip) as f: abi=json.load(f)
    with open(bip) as f: bc=f.read().strip()
    C=w3.eth.contract(abi=abi,bytecode=bc)
    tx=C.constructor(True).build_transaction({"from":acct.address,
        "nonce":w3.eth.get_transaction_count(acct.address),"gas":2000000,
        "gasPrice":w3.eth.gas_price})
    s=acct.sign_transaction(tx); th=w3.eth.send_raw_transaction(s.raw_transaction)
    r=w3.eth.wait_for_transaction_receipt(th)
    print(f"Deployed: {r['contractAddress']} block={r['blockNumber']} tx={th.hex()}")
    info={"chain":chain,"chain_id":cc["chain_id"],"contract_address":r["contractAddress"],
          "tx_hash":th.hex(),"block_number":r["blockNumber"],"deployer":acct.address,"timestamp":__import__("time").time()}
    with open(os.path.join(os.path.dirname(__file__),f"deploy-{chain}.json"),"w") as f:
        json.dump(info,f,indent=2)
    return r["contractAddress"]

if __name__=="__main__":
    from src.chain import WinnexChain
    p=argparse.ArgumentParser()
    p.add_argument("--chain",default="polygon-mumbai",choices=list(WinnexChain.SUPPORTED_CHAINS.keys()))
    p.add_argument("--compile-only",action="store_true")
    p.add_argument("--private-key")
    a=p.parse_args()
    if a.compile_only: compile_contract(); return
    pk=a.private_key or os.environ.get("WINNEX_DEPLOY_KEY")
    if not pk: print("ERROR: Set WINNEX_DEPLOY_KEY"); sys.exit(1)
    compile_contract(); deploy_contract(a.chain, pk)
