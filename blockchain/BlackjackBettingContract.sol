/*
/ guys this is so scuffed i just took the code from our lab and we need to modify it
*/
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "hardhat/console.sol";


contract BlackjackBettingContract {

    address payable owner;

    event Received(address, uint);
    mapping (address => uint256) private users;

    constructor() payable{
        owner = payable(msg.sender); 
    }

    // 
    receive() external payable {
        users[msg.sender] += msg.value;
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

    event DepositMade(address _from, address _to, uint _amount);
    event WithdrawMade(address _from, address _to, uint _amount);

    // modifier to check if caller has enough money
    modifier canWithdraw(uint256 amount) {
        require(amount < users[msg.sender]);
        _;
    }


    /**
     * @dev Deposits amount into the users account
     */
    function deposit() external payable {
        emit DepositMade(msg.sender, address(this), msg.value);
        users[msg.sender] += msg.value;
    }

    /**
     * @dev Returns the user's balance
     */
    function getBalance(address user) public view returns (uint256) {
        return users[user];
    }

    /**
     * @dev Returns the total money stored in the contract
     */
    function contractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    /**
     * @dev Withdraws money from the user's account if they have enough
     */
    function withdraw(uint256 amount) public payable canWithdraw(amount) {
        emit WithdrawMade(address(this), msg.sender, amount);
        (bool sent, ) = payable(msg.sender).call{value: amount}("");
        users[msg.sender] -= amount;
        require(sent, "Failed to withdraw");
    }

    /**
     * @dev Withdraws all money from a user's account
     */
    function withdrawAll() public payable {
        emit WithdrawMade(address(this), msg.sender, users[msg.sender]);
        (bool sent, ) = payable(msg.sender).call{value: users[msg.sender]}("");
        users[msg.sender] = 0;
        require(sent, "Failed to withdraw");
    }
} 