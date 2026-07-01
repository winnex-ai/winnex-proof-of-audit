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


---

## 🏗️ Project History & Transparency Note

### When This Was Built

The Winnex AI project was **started in December 2024** as a private research initiative by Klenio Araujo Padilha under Winnex Brasil Solucoes Empresariais LTDA - ME (CNPJ: 58.364.637/0001-47).

The core mathematical research (Riemannian HMC, Cauchy-Schwarz bounds, QR-JL projections) was developed privately over **18 months (Dec 2024 -- Jun 2026)** before any code was made public. The algorithm went through 12 major iterations (Madhava v1 through v12) as a private codebase.

### Why All Repositories Were Published on the Same Day

All public repositories were created on **July 1, 2026**. This is not because they were built in a day:

1. **The project was private for 18 months** during the research and development phase
2. **The repositories were opened simultaneously** to present the complete stack architecture to potential investors and partners

### Code Maturity by Layer

| Layer | Development Period | Public Since | Maturity |
|-------|-------------------|-------------|----------|
| **Layer 1: Audit Engine** | Dec 2024 -- Jun 2026 (18 mo) | Jul 1, 2026 | Research-grade, compiled, benchmarked |
| **Layer 2: Enterprise Stack** | Jun 2026 (blueprint) | Jul 1, 2026 | Product vision, not built yet |
| **Layer 3: Proof-of-Audit** | Jun 2026 (reference) | Jul 1, 2026 | Experimental, not production |
| **Production Tools** | Jun 2026 (blueprint) | Jul 1, 2026 | Blueprint, not built yet |

### Timeline

```
Dec 2024    Project started (private)
Jun 2025    Six bugs identified and corrected; Zenodo records begin
Jan 2026    Madhava v12; zero bound violations verified on SIFT-1M
Jun 30, 2026 All 11 Zenodo records published
Jul 1, 2026  GitHub repositories opened; Open Letter to Investors published
```

This repository is shared under **Business Source License 1.1 (BSL 1.1)**. The code was previously private and is now opened for transparency and study. Commercial deployment requires a separate license agreement.

**Contact:** pay@winnex.ai
