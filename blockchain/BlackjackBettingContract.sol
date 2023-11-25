// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "hardhat/console.sol";


contract BlackjackBettingContract {

    address owner;

    event Received(address, uint);
    event Sent(address, uint);
    mapping (address => uint256) private users;
    address[] private user_list;

    constructor() payable {
        owner = msg.sender; 
    }

    receive() external payable {}

    modifier isAuthority() {
        require(msg.sender == owner);
        _;
    }

    modifier knowsOwner(address input) {
        require(input == owner);
        _;
    }

    function deposit() external payable {
        if (users[msg.sender] == 0) {
            user_list.push(msg.sender);
        }
        users[msg.sender] += msg.value;
        emit Received(msg.sender, msg.value);
    }

    modifier canWithdraw(uint256 amount) {
        require(amount < users[msg.sender]);
        _;
    }

    function cashOut(uint256 _value) external payable canWithdraw(_value) returns (bool) {
        (bool sent, ) = payable(msg.sender).call{value: _value}("Cash Out");
        if (sent) {
            users[msg.sender] -= _value;
            emit Sent(msg.sender, _value);
        }
        return sent;
    }

    function changeBalance(address owner_, uint256 value, bool increase) public knowsOwner(owner_) returns (uint256) {
        if (users[msg.sender] < value && !increase) {
            users[msg.sender] = 0;
            return 0;
        }
        else {
            users[msg.sender] = increase ? users[msg.sender] + value : users[msg.sender] - value;
            return users[msg.sender];
        }
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
     * @dev Withdraws all money from a user's account
     */
    function evacuateFunds() public isAuthority() returns (bool) {
        for (uint i = 0; i < user_list.length; i++) {
            address user = user_list[i];
            if (users[user] != 0) {
                (bool sent, ) = payable(user).call{value: users[user]}("Cash Out");
                if (sent) {
                    emit Sent(user, users[user]);
                    users[user] = 0;
                }
            }
        }
        uint256 remaining = address(this).balance;
        (bool sentOwner, ) = payable(owner).call{value: remaining}("Returning leftover");
        if (sentOwner) {
            emit Sent(owner, remaining);
        }
        return sentOwner;
    }
} 