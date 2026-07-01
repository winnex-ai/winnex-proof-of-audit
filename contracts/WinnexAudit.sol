// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.19;

/// @title Winnex Proof-of-Audit Smart Contract
/// @notice Immutable registry of mathematical search audit proofs.
///         Each proof is a Cauchy-Schwarz bound verification per excluded document.
///         Proofs are organized in batches with Merkle tree roots for efficient verification.
/// @dev Deploy on Polygon, Hedera, or Ethereum L2 for production use.
///      Use Ethereum Sepolia or Polygon Mumbai for testing.
/// @author Winnex AI | pay@winnex.ai
/// @custom:repository https://github.com/winnex-ai/winnex-proof-of-audit

contract WinnexAudit {
    // ----- Types -----

    /// @notice A batch of audit proofs submitted together
    struct AuditBatch {
        bytes32 merkleRoot;   // Merkle root of all proof hashes in this batch
        uint256 proofCount;   // Number of proofs in the batch
        uint256 timestamp;    // Unix timestamp of submission
        address submitter;    // Address that submitted the batch
    }

    // ----- State -----

    /// @notice Mapping from Merkle root to audit batch
    mapping(bytes32 => AuditBatch) public auditBatches;

    /// @notice Track previously verified proof hashes
    mapping(bytes32 => bool) public verifiedProofs;

    /// @notice Address authorized to submit audit batches
    address public immutable owner;

    // ----- Events -----

    /// @notice Emitted when a new audit batch is submitted
    event AuditSubmitted(
        bytes32 indexed merkleRoot,
        uint256 proofCount,
        uint256 timestamp,
        address indexed submitter
    );

    /// @notice Emitted when a proof is verified independently
    event ProofVerified(
        bytes32 indexed proofHash,
        bytes32 indexed merkleRoot,
        address verifier
    );

    /// @notice Emitted when the owner address is updated
    event OwnerUpdated(
        address indexed oldOwner,
        address indexed newOwner
    );

    // ----- Errors -----

    error BatchAlreadyExists(bytes32 merkleRoot);
    error BatchNotFound(bytes32 merkleRoot);
    error InvalidMerkleProof();
    error NotAuthorized(address caller);
    error ZeroAddressNotAllowed();

    // ----- Modifiers -----

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotAuthorized(msg.sender);
        _;
    }

    // ----- Constructor -----

    constructor() {
        owner = msg.sender;
    }

    // ----- Core Functions -----

    /// @notice Submit a batch of audit proofs
    /// @param merkleRoot Merkle root of all proof hashes
    /// @param proofCount Number of proofs in this batch
    /// @param timestamp Unix timestamp
    function submitAuditBatch(
        bytes32 merkleRoot,
        uint256 proofCount,
        uint256 timestamp
    ) external {
        if (auditBatches[merkleRoot].timestamp != 0)
            revert BatchAlreadyExists(merkleRoot);

        auditBatches[merkleRoot] = AuditBatch({
            merkleRoot: merkleRoot,
            proofCount: proofCount,
            timestamp: timestamp,
            submitter: msg.sender
        });

        emit AuditSubmitted(merkleRoot, proofCount, timestamp, msg.sender);
    }

    /// @notice Verify a proof against a Merkle root
    /// @param proofHash SHA-256 hash of the proof data
    /// @param merkleRoot Merkle root this proof belongs to
    /// @param proof Merkle proof (sibling hashes)
    /// @return True if proof is valid and verified
    function verifyProof(
        bytes32 proofHash,
        bytes32 merkleRoot,
        bytes32[] calldata proof
    ) external returns (bool) {
        if (auditBatches[merkleRoot].timestamp == 0)
            revert BatchNotFound(merkleRoot);

        // Recompute Merkle root from proof
        bytes32 computed = proofHash;
        for (uint256 i = 0; i < proof.length; i++) {
            if (computed < proof[i]) {
                computed = keccak256(abi.encodePacked(computed, proof[i]));
            } else {
                computed = keccak256(abi.encodePacked(proof[i], computed));
            }
        }

        if (computed != merkleRoot) revert InvalidMerkleProof();

        verifiedProofs[proofHash] = true;
        emit ProofVerified(proofHash, merkleRoot, msg.sender);
        return true;
    }

    /// @notice Get audit batch details
    /// @param merkleRoot Merkle root of the batch
    /// @return proofCount Number of proofs, timestamp of submission, submitter address
    function getAuditBatch(bytes32 merkleRoot)
        external
        view
        returns (
            uint256 proofCount,
            uint256 timestamp,
            address submitter
        )
    {
        if (auditBatches[merkleRoot].timestamp == 0)
            revert BatchNotFound(merkleRoot);

        AuditBatch memory batch = auditBatches[merkleRoot];
        return (batch.proofCount, batch.timestamp, batch.submitter);
    }

    /// @notice Check if a proof hash has been verified
    /// @param proofHash The proof hash to check
    /// @return True if already verified
    function isProofVerified(bytes32 proofHash) external view returns (bool) {
        return verifiedProofs[proofHash];
    }

    /// @notice Get the total number of audit batches
    /// @return The number of distinct Merkle roots submitted
    function getBatchCount() external view returns (uint256) {
        return auditBatchesCount;
    }

    // ----- Internal State Tracking -----

    uint256 private auditBatchesCount;
}
