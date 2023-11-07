// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "hardhat/console.sol";


contract BlackjackBettingContract {

    address payable owner;

     event Received(address, uint);

    constructor() payable{
        owner = payable(msg.sender); 
    }

    function payWinner(address payable _to, uint256 _value) external payable returns (bool) 
    {
        require(msg.sender == owner);
        require(_value <= address(this).balance);
        bool success = payable(_to).send(_value);
        return(success);
    }

    function receivePayment() external payable
    {
       emit Received(msg.sender, msg.value);
    }
} 