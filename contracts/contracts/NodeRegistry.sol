// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @notice Design artifact only — not deployed in the 5-day prototype.
/// Production-path sketch: providers stake ETH to register as inference nodes.
/// See ../simulate.py for the logic actually used in the demo.
contract NodeRegistry {
    mapping(address => uint256) public stakes;

    event Registered(address indexed provider, uint256 amount);

    function registerStake() external payable {
        require(msg.value > 0, "stake required");
        stakes[msg.sender] += msg.value;
        emit Registered(msg.sender, msg.value);
    }
}
