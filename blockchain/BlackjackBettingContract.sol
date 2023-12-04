// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "hardhat/console.sol";

// Contract that runs the accounts of users
contract BlackjackBettingContract {

    address owner;

    event Received(address, uint);
    event Sent(address, uint);
    // storage system to keep track of user balances
    mapping (address => uint256) private users;
    // keeps track of all participants
    address[] private user_list;

    // upon construction the owner is set. This function also receives money so that the contract has funds
    constructor() payable {
        owner = msg.sender; 
    }

    /**
     * @dev currency can be sent at any time
     */
    receive() external payable {}

    /**
     * @dev ensures that the sender is the owner
     */
    modifier isAuthority() {
        require(msg.sender == owner);
        _;
    }

    /**
     * @dev ensures that a given address is the owner's
     */
    modifier knowsOwner(address input) {
        require(input == owner);
        _;
    }

    /**
     * @dev accepts currency from a user
     */
    function deposit() external payable {
        // if the user does not have any balance, add them to the participants list
        if (users[msg.sender] == 0) {
            user_list.push(msg.sender);
        }
        // update the user's balance
        users[msg.sender] += msg.value;
        emit Received(msg.sender, msg.value);
    }

    /**
     * @dev check if the user has the requested withdraw value
     */
    modifier canWithdraw(uint256 amount) {
        require(amount < users[msg.sender]);
        _;
    }

    /**
     * @dev Withdraws a certain amount of currency from the user's account
     */
    function cashOut(uint256 _value) external payable canWithdraw(_value) returns (bool) {
        (bool sent, ) = payable(msg.sender).call{value: _value}("Cash Out");
        if (sent) {
            users[msg.sender] -= _value;
            emit Sent(msg.sender, _value);
        }
        return sent;
    }

    /**
     * @dev modifies a user's balance without taking or sending more currency, is locked with the owner's address as a password
     */
    function changeBalance(address owner_, uint256 value, bool increase) public knowsOwner(owner_) returns (uint256) {
        // ensures that the user's balance will not underflow
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
     * @dev Returns any money that a person has in their account to them, and returns the remainder to the owner
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