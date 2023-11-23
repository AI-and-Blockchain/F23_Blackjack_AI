// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "hardhat/console.sol";


contract BlackjackBettingContract {

    address owner;
    address private infura = 0x0000000000000000000000000000000000000000;

    event Received(address, uint);
    event Sent(address, uint);
    mapping (address => uint256) private users;
    address[] private user_list;

    constructor() payable {
        owner = msg.sender; 
    }

    receive() external payable {
        if (users[msg.sender] == 0) {
            user_list.push(msg.sender);
        }
        users[msg.sender] += msg.value;
        emit Received(msg.sender, msg.value);
    }

    modifier isAuthority() {
        require(msg.sender == owner || msg.sender == infura);
        _;
    }

    modifier canWithdraw(address user, uint256 amount) {
        require(amount < users[user]);
        _;
    }

    function cashOut(address payable _to, uint256 _value) external payable isAuthority() canWithdraw(_to, _value) returns (bool) {
        (bool sent, ) = payable(_to).call{value: _value}("Cash Out");
        if (sent) {
            users[_to] -= _value;
            emit Sent(_to, _value);
        }
        return sent;
    }

    function changeBalance(address user, uint256 value, bool increase) public isAuthority() returns (uint256) {
        if (users[user] < value && !increase) {
            users[user] = 0;
            return 0;
        }
        else {
            users[user] = increase ? users[user] + value : users[user] - value;
            return users[user];
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