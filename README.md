# F23_Blackjack_AI
*Ryan Karch (karchr), Dominic Beyer (beyerd), Angelica Loshak (loshaka), Michael Dong (dongm2)*

### Running Instructions
The Solidity code for the blockchain is hosted through Remix, but is provided in the blockchain directory.\
All code (frontend and backend) must be run through main.py or a similar .py file from the top level directory.\
main.py contains two starter functions for individual testing:
- game_test() will test the backend game's logic by allowing you to interact with the game through a terminal interface (using the basic User agent)
- web_test() will launch the website in its current development state

### Component Diagram
![image](assets/ComponentDiagram.png)

### Sequence Diagram
![image](assets/SequenceDiagram.png)

### AI Algorithms/Models

We will be using Q-learning as our algorithm.

#### Why Use Q-learning, and How Does it Work?

* Q-learning is a reinforcement-learning algorithm where a model can learn and improve its strategy over time.
* When the model makes a decision based on the current state of the environment, the Q-table is updated, and this affects the model's future decisions.
* The Q-table stores an action for each possible state of the environment - when a state is encountered, the corresponding action for that state is retrieved from the Q-table and executed, and its value is updated. The model chooses the action that provides the highest "reward".
* We can train the model, and then use its Q-table in our code, or we can train the model over time while it plays on our system.

### Blockchain Architecture
* Smart contract used for betting cryptocurrency against the Blackjack AI
    * Ensures that the outcomes of the betting are fair and secure
    * Enables trust between customer and the gambling service because blockchain is immutable
* Logic programmed using **Remix IDE** in **Solidity**
    * **SepoliaETH** used by users to make bets and receive payments
    * **MetaMask** Ethereum wallet is used to deploy smart contract 
* Users connect to smart contract through MetaMask
    * [web3.py](https://web3py.readthedocs.io/en/stable/) Python Library used to interact with the smart contract
    * Users will be prompted to login into their MetaMask wallet account
    * Smart contract will verify and send transactions between users using their Ethereum address
