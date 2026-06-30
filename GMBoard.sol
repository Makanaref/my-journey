// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GMBoard {
    event GM(address indexed sender, string message, uint256 timestamp);

    function sayGM() public {
        emit GM(msg.sender, "GM", block.timestamp);
    }
}