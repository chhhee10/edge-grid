// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @notice Design artifact only — not deployed in the 5-day prototype.
/// Production-path sketch: HTLC-style escrow between requester and provider per job.
/// See ../simulate.py for the logic actually used in the demo.
contract Marketplace {
    struct Escrow {
        address requester;
        address provider;
        uint256 amount;
        bool settled;
    }

    mapping(bytes32 => Escrow) public escrows;

    event EscrowOpened(bytes32 indexed jobId, address requester, address provider, uint256 amount);
    event EscrowSettled(bytes32 indexed jobId, bool slashed);

    function openEscrow(bytes32 jobId, address provider) external payable {
        require(escrows[jobId].amount == 0, "job exists");
        escrows[jobId] = Escrow(msg.sender, provider, msg.value, false);
        emit EscrowOpened(jobId, msg.sender, provider, msg.value);
    }

    function settle(bytes32 jobId, bool slashed) external {
        Escrow storage e = escrows[jobId];
        require(!e.settled, "already settled");
        e.settled = true;
        if (!slashed) {
            payable(e.provider).transfer(e.amount);
        } else {
            payable(e.requester).transfer(e.amount);
        }
        emit EscrowSettled(jobId, slashed);
    }
}
