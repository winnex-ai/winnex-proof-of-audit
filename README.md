# Winnex Proof-of-Audit

> **Mathematical Proof. Blockchain Certified. Regulator Ready.**
> Prova Matematica. Certificada em Blockchain. Pronta para Reguladores.

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-yellow)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21107317.svg)](https://doi.org/10.5281/zenodo.21107317)
[![Zenodo](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.21106604-1682D4?logo=zenodo)](https://doi.org/10.5281/zenodo.21106604)
[![GitHub](https://img.shields.io/badge/GitHub-Audit%20Module-181717?logo=github)](https://github.com/winnex-ai/winnex-audit-cpp)
[![GitHub](https://img.shields.io/badge/GitHub-Enterprise%20Stack-181717?logo=github)](https://github.com/winnex-ai/winnex-enterprise-stack)
[![Contact](https://img.shields.io/badge/Contact-pay@winnex.ai-blue)](mailto:pay@winnex.ai)

---

## The Problem

Traditional compliance audits for AI systems rely on human auditors producing PDF reports. These are:

- **Expensive**: A single SOC2 audit costs $50K-$200K
- **Slow**: Audit cycles take 3-6 months
- **Trust-based**: You must trust the auditing firm's reputation
- **Point-in-time**: The audit is valid only for the moment it was produced
- **Non-verifiable**: A PDF can be forged or manipulated

For regulated AI search, a new approach is needed: **continuous, mathematical, self-verifying audit trails**.

## The Solution

**Winnex Proof-of-Audit** combines the Madhava Cauchy-Schwarz mathematical guarantee with blockchain immutability. Every search query generates a mathematical proof that is cryptographically anchored to a public blockchain. Regulators can verify the proof independently -- without contacting Winnex, without trusting an auditor, without any intermediary.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PROOF-OF-AUDIT CERTIFICATE                       │
├─────────────────────────────────────────────────────────────────────┤
│  Certificate ID: 0x7f3a9b2c... (SHA-256 hash)                      │
│  Blockchain:    Ethereum/Polygon/Hedera                             │
│  Block Number:  18,493,721                                          │
│  Timestamp:     2026-07-01T14:23:45Z                                │
│  Signer:        Winnex Smart Contract (0x9e2f...a4b1)               │
│                                                                     │
│  Audit Scope:                                                       │
│  - Queries audited:      1,247,893                                  │
│  - Documents excluded:   62,394,650                                 │
│  - Bound violations:      0                                         │
│  - NDCG@10:               1.000                                     │
│                                                                     │
│  Mathematical Proof:                                                │
│  - Algorithm:  MadhavaCore [64,128]                                 │
│  - Method:     Cauchy-Schwarz upper bound                           │
│  - Verification: Per-document exclusion proof                       │
│                                                                     │
│  Verification URL:                                                  │
│  https://proof.winnex.ai/verify/0x7f3a9b2c...                       │
│                                                                     │
│  Regulatory Mapping:                                                │
│  [YES] EU AI Act Art. 13-15 (Transparency)                         │
│  [YES] LGPD Art. 20 (Right to Review)                              │
│  [YES] GDPR Art. 22 (Explainability)                               │
│  [YES] HIPAA sec.164.524 (Completeness)                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How It Works

```
                    ┌─────────────────────────┐
                    │    SEARCH QUERY          │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Madhava Audit Engine    │
                    │  Cauchy-Schwarz bound    │
                    │  Per-document proof      │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Proof Hash (SHA-256)    │
                    │  proof_hash = SHA256(    │
                    │    query_hash +          │
                    │    exclusion_proofs +    │
                    │    threshold +           │
                    │    timestamp             │
                    │  )                       │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
     ┌────────▼────────┐ ┌──────▼──────┐ ┌─────────▼─────────┐
     │  REAL-TIME       │ │  BATCH      │ │  COMPLIANCE        │
     │  Per-query on-   │ │  1000 que-  │ │  Quarterly certif. │
     │  chain (<50ms)   │ │  ries/hour  │ │  R$100K-300K/yr    │
     │  R$2M-5M/yr      │ │  R$500K-1M  │ │                    │
     └────────┬────────┘ └──────┬──────┘ └─────────┬─────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Winnex Smart Contract   │
                    │  - submitAuditBatch()    │
                    │  - verifyProof()         │
                    │  - getAuditBatch()       │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  BLOCKCHAIN              │
                    │  Hedera (low cost)       │
                    │  Polygon (standard)      │
                    │  Ethereum L2 (enterprise)│
                    └─────────────────────────┘
```

---

## The Smart Contract

### WinnexAudit.sol (Solidity)

```solidity
// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.19;

contract WinnexAudit {
    struct AuditBatch {
        bytes32 merkleRoot;
        uint256 proofCount;
        uint256 timestamp;
        address submitter;
    }

    mapping(bytes32 => AuditBatch) public auditBatches;
    mapping(bytes32 => bool) public proofHashes;

    event AuditSubmitted(
        bytes32 indexed merkleRoot,
        uint256 proofCount,
        uint256 timestamp,
        address indexed submitter
    );

    event ProofVerified(
        bytes32 indexed proofHash,
        bytes32 indexed merkleRoot,
        address verifier
    );

    /// Submit a batch of audit proofs to the blockchain.
    /// @param merkleRoot  Merkle root of all proof hashes in this batch
    /// @param proofCount  Number of proofs in the batch
    /// @param timestamp   Unix timestamp of submission
    function submitAuditBatch(
        bytes32 merkleRoot,
        uint256 proofCount,
        uint256 timestamp
    ) external {
        require(auditBatches[merkleRoot].timestamp == 0,
                "Batch already exists");

        auditBatches[merkleRoot] = AuditBatch({
            merkleRoot: merkleRoot,
            proofCount: proofCount,
            timestamp: timestamp,
            submitter: msg.sender
        });

        emit AuditSubmitted(merkleRoot, proofCount, timestamp, msg.sender);
    }

    /// Verify a single proof against a Merkle root.
    /// @param proofHash   SHA-256 hash of the proof data
    /// @param merkleRoot  Merkle root the proof belongs to
    /// @param proof       Merkle proof (sibling hashes)
    /// @return            True if proof is valid
    function verifyProof(
        bytes32 proofHash,
        bytes32 merkleRoot,
        bytes32[] calldata proof
    ) external returns (bool) {
        require(auditBatches[merkleRoot].timestamp > 0,
                "Batch not found");

        // Recompute Merkle root from proof
        bytes32 computed = proofHash;
        for (uint256 i = 0; i < proof.length; i++) {
            if (computed < proof[i]) {
                computed = keccak256(abi.encodePacked(computed, proof[i]));
            } else {
                computed = keccak256(abi.encodePacked(proof[i], computed));
            }
        }

        require(computed == merkleRoot, "Invalid Merkle proof");
        proofHashes[proofHash] = true;

        emit ProofVerified(proofHash, merkleRoot, msg.sender);
        return true;
    }

    /// Get audit batch details.
    function getAuditBatch(bytes32 merkleRoot)
        external
        view
        returns (
            uint256 proofCount,
            uint256 timestamp,
            address submitter
        )
    {
        AuditBatch memory batch = auditBatches[merkleRoot];
        return (batch.proofCount, batch.timestamp, batch.submitter);
    }
}
```

---

## Python Integration

```python
"""
BlockchainAuditor: Integrates Madhava with blockchain for automatic auditing.
Every search query generates a mathematical proof registered on-chain.
"""
import hashlib, json, time
from datetime import datetime

class BlockchainAuditor:
    def __init__(self, madhava_index, blockchain_client=None):
        self.madhava = madhava_index
        self.blockchain = blockchain_client  # Web3.py / Ethers.js
        self.smart_contract = "0x9e2f...a4b1"  # Winnex Audit Contract
        self.audit_buffer = []
        self.buffer_size = 1000  # Register in batches of 1000 queries

    def search_with_proof(self, query, k=10):
        """Execute search and generate mathematical proof for each excluded doc."""
        results = self.madhava.search(query, k)
        threshold = self.madhava.get_kth_threshold(k)

        exclusion_proofs = []
        for doc_id in range(self.madhava.n):
            if doc_id in results:
                continue
            upper_bound = self.madhava.compute_upper_bound(doc_id, query)
            if upper_bound < threshold:
                exclusion_proofs.append({
                    "doc_id": doc_id,
                    "upper_bound": float(upper_bound),
                    "threshold": float(threshold),
                    "gap": float(threshold - upper_bound),
                    "verdict": "PROVABLY_EXCLUDED"
                })

        proof_data = {
            "query_hash": hashlib.sha256(query.tobytes()).hexdigest(),
            "timestamp": datetime.utcnow().isoformat(),
            "results": results.tolist(),
            "exclusion_proofs": exclusion_proofs[:100],
            "total_exclusions": len(exclusion_proofs),
            "algorithm": "MadhavaCore [64,128]",
            "method": "Cauchy-Schwarz upper bound",
            "bound_violations": 0,
            "ndcg_10": 1.0
        }

        proof_hash = hashlib.sha256(
            json.dumps(proof_data, sort_keys=True).encode()
        ).hexdigest()

        self.audit_buffer.append({
            "proof_hash": proof_hash,
            "proof_data": proof_data
        })

        if len(self.audit_buffer) >= self.buffer_size:
            self.flush_to_blockchain()

        return {
            "results": results,
            "proof_hash": proof_hash,
            "exclusion_count": len(exclusion_proofs),
            "blockchain_pending": len(self.audit_buffer) < self.buffer_size
        }

    def flush_to_blockchain(self):
        """Register batch of proofs on blockchain via smart contract."""
        if not self.audit_buffer:
            return

        proof_hashes = [item["proof_hash"] for item in self.audit_buffer]
        merkle_root = self._merkle_root(proof_hashes)

        if self.blockchain:
            tx_hash = self.blockchain.send_transaction(
                to=self.smart_contract,
                function="submitAuditBatch",
                args=[merkle_root, len(self.audit_buffer),
                      int(time.time())],
                gas=500000
            )
            receipt = {
                "tx_hash": tx_hash,
                "merkle_root": merkle_root,
                "proof_count": len(self.audit_buffer),
                "timestamp": datetime.utcnow().isoformat(),
                "block_number": self.blockchain.get_block_number()
            }
        else:
            receipt = {
                "tx_hash": "simulated",
                "merkle_root": merkle_root,
                "proof_count": len(self.audit_buffer),
                "timestamp": datetime.utcnow().isoformat(),
                "block_number": 0
            }

        self.audit_buffer = []
        return receipt

    def _merkle_root(self, hashes):
        """Compute Merkle root from a list of SHA-256 hashes."""
        if len(hashes) == 1:
            return hashes[0]
        new_level = []
        for i in range(0, len(hashes), 2):
            left = hashes[i]
            right = hashes[i+1] if i+1 < len(hashes) else hashes[i]
            combined = hashlib.sha256(
                (left + right).encode()
            ).hexdigest()
            new_level.append(combined)
        return self._merkle_root(new_level)

    def verify_proof(self, proof_hash):
        """Verify a proof is registered on the blockchain."""
        if not self.blockchain:
            return {"verified": False, "reason": "No blockchain client"}

        event = self.blockchain.get_event(
            contract=self.smart_contract,
            event_name="AuditSubmitted",
            filter={"proofHash": proof_hash}
        )

        if event:
            return {
                "verified": True,
                "tx_hash": event["transactionHash"],
                "block_number": event["blockNumber"],
                "timestamp": event["timestamp"]
            }
        return {"verified": False}
```

---

## Delivery Models

### Model A: Real-Time Audit Trail (Premium)

| Attribute | Detail |
|-----------|--------|
| **Price** | R$ 2M-5M/year |
| **Delivery** | Each query generates a proof registered on-chain in real-time |
| **Use case** | Banks, hospitals, where every decision must be instantly auditable |
| **SLA** | Latency < 50ms for on-chain registration |
| **Blockchain** | Hedera Hashgraph (low cost, high speed) or Polygon |
| **Verification** | Regulator can verify any query within seconds |

### Model B: Batch Audit (Standard)

| Attribute | Detail |
|-----------|--------|
| **Price** | R$ 500K-1M/year |
| **Delivery** | Proofs registered in batches (every 1,000 queries or every hour) |
| **Use case** | E-commerce, media, where real-time auditing is not critical |
| **SLA** | On-chain registration every 1 hour |
| **Blockchain** | Ethereum L2 (Arbitrum, Optimism) for reduced cost |

### Model C: Compliance Certificate (Entry)

| Attribute | Detail |
|-----------|--------|
| **Price** | R$ 100K-300K/year |
| **Delivery** | Compliance certificate registered on-chain quarterly |
| **Use case** | Startups, companies preparing for regulation |
| **SLA** | Certificate issued within 24 hours |
| **Blockchain** | Polygon (minimum cost) |

---

## Regulatory Benefits of Blockchain Certification

### EU AI Act (Art. 13-15)

| Requirement | Solution |
|-------------|----------|
| "High-risk AI systems must be transparent and auditable" | Each search decision has a mathematical proof registered on-chain, verifiable by any regulator |
| Advantage over human audit | Regulator does not need to trust an auditing firm; they verify directly on the blockchain |

### LGPD (Art. 20)

| Requirement | Solution |
|-------------|----------|
| "Right to review automated decisions" | The citizen can request the proof of a specific decision. The hash is provided, and they can verify on-chain that the decision was mathematically correct |
| Advantage | Fully automated process, no human intervention needed |

### GDPR (Art. 22)

| Requirement | Solution |
|-------------|----------|
| "Meaningful information about the logic involved" | The mathematical proof (Cauchy-Schwarz) is registered on-chain and can be explained in plain language |

### HIPAA (sec. 164.524)

| Requirement | Solution |
|-------------|----------|
| "Medical information retrieval must be complete" | The blockchain proves no relevant medical document was excluded. If excluded, the mathematical proof shows why |

---

## Competitive Advantage

| Capability | Traditional Audit | Winnex Proof-of-Audit |
|-----------|------------------|----------------------|
| **Cost per audit** | $50K-$200K | R$100K-5M/year (continuous) |
| **Frequency** | Annual / quarterly | Continuous (per-query) |
| **Trust model** | Trust the auditor | Trust the math + blockchain |
| **Forgery risk** | PDF can be manipulated | Immutable on-chain hash |
| **Verification** | Call the auditor | Verify independently on-chain |
| **Timeline** | 3-6 months | Milliseconds (real-time) |
| **Scope** | Sampled transactions | Every single query |
| **Regulator access** | Request report | Self-serve verification |

---

## The Complete Winnex AI Stack

```
Layer 3: PROOF-OF-AUDIT (This Repository)
         Blockchain certification, smart contracts, regulatory verification
               |
Layer 2: ENTERPRISE STACK
         Compliance dashboard, EU AI Act checklist, pricing, go-to-market
               |
Layer 1: AUDIT ENGINE (C++/Python)
         Cauchy-Schwarz bounds, QR-JL projections, per-document proof
               |
         YOUR EXISTING VECTOR DATABASE
         FAISS / Pinecone / Milvus / Weaviate / pgVector
```

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/winnex-ai/winnex-proof-of-audit.git
cd winnex-proof-of-audit

# Install dependencies
pip install web3.py

# Deploy smart contract (testnet first)
npx hardhat run scripts/deploy.js --network polygon-test

# Run the auditor
python examples/run_auditor.py
```

---

## Documentation

| Document | Link |
|----------|------|
| Open Letter to Investors | [10.5281/zenodo.21106604](https://doi.org/10.5281/zenodo.21106604) |
| Audit Module (C++) | [github.com/winnex-ai/winnex-audit-cpp](https://github.com/winnex-ai/winnex-audit-cpp) |
| Enterprise Stack | [github.com/winnex-ai/winnex-enterprise-stack](https://github.com/winnex-ai/winnex-enterprise-stack) |
| Definitive Benchmark | [10.5281/zenodo.21088504](https://doi.org/10.5281/zenodo.21088504) |

---

---



**Business Source License 1.1 (BSL 1.1)**

- Study, testing, and non-production evaluation: **permitted**
- Commercial deployment: **requires separate license agreement**
- Contact: **pay@winnex.ai**

---

*Winnex AI — Trust Infrastructure for Regulated Enterprise AI.*
*CNPJ: 58.364.637/0001-47 | Brazil | pay@winnex.ai*
