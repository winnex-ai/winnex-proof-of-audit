# Winnex Audit Trail Plugins

> **Pluggable audit trail backends for the Madhava proof engine.**
> O basico ja funciona. Estes sao plugs para cenarios especificos.

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-yellow)](LICENSE)
[![Kaggle](https://img.shields.io/badge/Kaggle-Benchmark%20SIFT--1M-20BEFF?logo=kaggle)](https://www.kaggle.com/code/kleniopadilha/winnex-definitive-benchmark-v1-0)
[![Contact](https://img.shields.io/badge/Contact-pay@winnex.ai-blue)](mailto:pay@winnex.ai)

---

## How Audit Trails Work in the Winnex Stack

The Madhava Audit Engine (Layer 1) produces a **mathematical proof per excluded document** via Cauchy-Schwarz bounds. This proof IS the audit trail. How you store and verify it is a deployment choice.

```
Madhava Engine -> JSON proof -> [Plugin: choose one]
                                |
                    +-----------+-----------+
                    |           |           |
               Local Log    Ed25519     Blockchain
               Append-only  Signed      Smart Contract
               (default)    Hash Chain  (experimental)
```

---

## Plugin 1: Default -- Append-Only Log (Free, Instant, Recommended)

**This is what you should use for 99% of deployments.** No blockchain, no tokens, no gas fees.

```python
import json, time, hashlib

class AuditLog:
    def __init__(self):
        self.entries = []
        self.prev_hash = b''

    def append(self, proof: dict) -> dict:
        block_hash = hashlib.sha3_256(
            json.dumps(proof, sort_keys=True).encode() + self.prev_hash
        ).hexdigest()
        entry = {
            "timestamp": time.time(),
            "proof": proof,
            "prev_hash": self.prev_hash.hex(),
            "block_hash": block_hash,
        }
        self.entries.append(entry)
        self.prev_hash = block_hash.encode()
        return entry

    def verify_chain(self) -> bool:
        prev = b''
        for e in self.entries:
            expected = hashlib.sha3_256(
                json.dumps(e["proof"], sort_keys=True).encode() + prev
            ).hexdigest()
            if expected != e["block_hash"]: return False
            if e["prev_hash"] != prev.hex(): return False
            prev = e["block_hash"].encode()
        return True
```

**Cost:** $0. **Latency:** <1ms. **Legal weight:** Admissible as business record.

---

## Plugin 2: Ed25519 Signed Hash Chain ($0, NIST-Standard)

Adds cryptographic non-repudiation via Ed25519 digital signatures.

```bash
# Generate keypair
openssl genpkey -algorithm ed25519 -out winnex_audit_private.pem
openssl pkey -in winnex_audit_private.pem -pubout -out winnex_audit_public.pem

# Sign the audit log
python3 -c "
import nacl, json
key = nacl.signing.SigningKey.generate()
sig = key.sign(json.dumps(audit_entries).encode())
print(sig.hex())
"
```

**Cost:** $0. **Latency:** <1ms. **Legal weight:** NIST-standard, admissible in court.

---

## Plugin 3: Blockchain Smart Contract ($0.01-0.50/tx, Experimental)

For the rare case where a regulator explicitly demands on-chain proof.

```solidity
contract AuditProof {
    mapping(bytes32 => bool) public proofs;
    function store(bytes32 hash) external { proofs[hash] = true; }
    function verify(bytes32 hash) external view returns (bool) { return proofs[hash]; }
}
```

**Cost:** $0.01-0.50 per transaction + infrastructure. **Latency:** 2-60s.
**Legal weight:** Same as Plugin 2 -- blockchain adds no additional legal weight.

Only use if **explicitly required** by regulation or contract.

---

## Decision Guide

| If your requirement is... | Use this plugin |
|--------------------------|----------------|
| I need to prove the audit trail was not modified | **Plugin 1** (hash chain) -- $0, instant |
| I need cryptographic proof of authenticity | **Plugin 2** (Ed25519) -- $0, instant |
| The regulator explicitly requires on-chain proof | **Plugin 3** (blockchain) -- $0.01-0.50/tx |
| I want the cheapest option that works | **Plugin 1** (hash chain) -- $0 |

---

## The Winnex Stack

| Layer | Repository | What | Status |
|-------|-----------|------|--------|
| Layer 1 | [winnex-audit-cpp](https://github.com/winnex-ai/winnex-audit-cpp) | C++ proof engine | Research-grade, benchmarked |
| Layer 2 | [winnex-enterprise-stack](https://github.com/winnex-ai/winnex-enterprise-stack) | Enterprise product | Blueprint |
| Plugins | This repo | Audit trail backends | Pluggable |
| Tools | [winnex-production-tools](https://github.com/winnex-ai/winnex-production-tools) | Production tooling | Blueprint |

**License:** BSL 1.1 | **Contact:** pay@winnex.ai
