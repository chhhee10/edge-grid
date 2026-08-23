// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @notice Design artifact only — not deployed in the 5-day prototype.
/// Production-path sketch: records the judge verdict on-chain and triggers slashing.
/// See ../simulate.py for the logic actually used in the demo.
contract VerificationContract {
    mapping(bytes32 => bool) public verdicts; // jobId => passed

    event Verified(bytes32 indexed jobId, bool passed, bytes32 outputHash);

    function recordVerdict(bytes32 jobId, bool passed, bytes32 outputHash) external {
        verdicts[jobId] = passed;
        emit Verified(jobId, passed, outputHash);
    }
}
