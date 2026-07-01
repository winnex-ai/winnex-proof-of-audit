# Winnex Proof-of-Audit (Experimental)

> **Experimental exploration of blockchain-anchored audit trails.**
> ⚠️ **Most likely unnecessary for your use case. Read below first.**

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-yellow)](LICENSE)
[![Contact](https://img.shields.io/badge/Contact-pay@winnex.ai-blue)](mailto:pay@winnex.ai)

---

## ⚠️ Honest Assessment: This Repository Is Experimental

**We do not recommend deploying this in production.** We maintain this repository as a research experiment.

### The Core Problem (Why Blockchain Probably Doesn't Make Sense)

The Winnex Proof-of-Audit concept -- using a blockchain to store proof hashes -- sounds impressive but has **limited practical value**:

| Audit Method | Cost | Legal Weight | Complexity |
|-------------|------|-------------|------------|
| **Signed PDF from Winnex** | ~$0 | Admissible as business record | None |
| **PGP/GPG digital signature** | ~$0 | Strong legal precedent | Low |
| **RFC 3161 timestamp authority** | ~$0.10/timestamp | Widely accepted in e-discovery | Low |
| **Blockchain (Polygon/Hedera)** | $0.01-$0.50/tx + infrastructure | **No additional legal weight** | High |

A cryptographic signature from a trusted authority (PGP, timestamp service) **already provides the same legal admissibility** as a blockchain transaction, without the complexity, gas fees, latency, or key management overhead.

### What This Repository Actually Contains

This is a **reference study** exploring how blockchain could theoretically be layered on top of the Madhava audit engine. It demonstrates:

| Component | Description | Production Readiness |
|-----------|-------------|---------------------|
| `WinnexAudit.sol` | Minimal Solidity contract storing Merkle roots | ❌ No access control, no spam protection |
| `src/chain.py` | Web3.py integration scaffolding | ❌ Requires Web3 setup, no error handling |
| `api/server.py` | FastAPI verification service | ❌ Blueprint only, no auth, no rate limiting |

### What You Should Actually Use

### The Winnex Stack — Without Blockchain

```
Layer 1: Madhava Audit Engine (C++/Python)
         Per-document Cauchy-Schwarz bound proof
         --> This IS the product. Proven, validated, zero violations.

Layer 2: Compliance Dashboard (planned)
         Bound monitoring, regulatory reports, JSON audit logs

Layer 3: This repository (experimental)
         --> Unnecessary for 99% of clients. Skip it.
```

**For regulatory compliance, the mathematical proof produced by the Madhava engine (Layer 1) is sufficient.** The per-document audit trail -- a JSON record showing the Cauchy-Schwarz bound calculation for each excluded document -- can be:
1. Logged to a standard database
2. Signed with your own GPG key
3. Timestamped by a trusted authority (RFC 3161)
4. Submitted to regulators as a standard business record

**All of these options are cheaper, simpler, and carry the same legal weight as blockchain.**

---

## If You Still Want to Explore Blockchain...

### When It Might (Theoretically) Add Value

| Scenario | Why Blockchain | Realistic? |
|----------|---------------|------------|
| Publicly verifiable audit trail | Anyone can verify without trusting Winnex | ✅ Valid, but niche |
| Decentralized multi-stakeholder audit | Multiple regulators need independent verification | ✅ Possibly useful |
| Permanent immutable record | No possibility of backdating or alteration | ⚠️ Same as timestamp service |
| Compliance theater | "We use blockchain for audit" sounds good | ❌ Not a real requirement |

### How the Reference Contract Works

```solidity
// Extremely simple: just stores SHA-3-256 hashes on-chain
contract WinnexAudit {
    mapping(bytes32 => bool) public proofHashes;
    
    function submitBatch(bytes32 merkleRoot, uint256 proofCount) external {
        // No access control. Anyone can submit. No spam protection.
    }
    
    function verifyProof(bytes32 proofHash, bytes32 merkleRoot, ...) external {
        // Checks Merkle proof existence only
    }
}
```

**This contract does nothing that a simple database table cannot do.** Its only value is that the data lives on a public blockchain -- which may or may not matter for your specific regulatory requirements.

---

## Recommendation

| If you are... | Use this stack | Skip this repo |
|---------------|---------------|----------------|
| A bank needing EU AI Act compliance | Layer 1 + Layer 2 | ✅ |
| A hospital with HIPAA requirements | Layer 1 | ✅ |
| A law firm needing e-discovery proof | Layer 1 + signed audit logs | ✅ |
| A crypto-native company wanting on-chain proofs | Layer 1 + Layer 3 (maybe) | Optional |
| An investor evaluating the technology | Layer 1 (this is the real product) | ✅ |

**Contact:** pay@winnex.ai | **Real product:** [github.com/winnex-ai/winnex-audit-cpp](https://github.com/winnex-ai/winnex-audit-cpp) | **Benchmark:** [10.5281/zenodo.21088504](https://doi.org/10.5281/zenodo.21088504)
