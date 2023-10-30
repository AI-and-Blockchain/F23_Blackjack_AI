# F23_Blackjack_AI
*Ryan Karch (karchr), Dominic Beyer (beyerd), Angelica Loshak (loshaka), Michael Dong (dongm2)*

### Component Diagram
![image](assets/ComponentDiagram.png)

### Sequence Diagram
![image](assets/SequenceDiagram.png)

### AI Algorithms/Models

We will be using Deep Q-learning as our algorithm.

#### Why Use Deep Q-learning, and How Does it Work?
* Normal Q-learning uses a table to store Q-values for each state-action pair.
* Deep Q-learning employs the use of a neural network, which can be used to predict these Q-values.
* Deep Q-learning is necessary for this task, as there are many different state possibilities in a blackjack game, thus resulting in a massive Q-table. We can optimize time and memory usage by predicting these values instead of performing table lookups.
* The neural network will get the state as input, and output multiple Q-values associated with multiple actions. The algorithm chooses the largest Q-value and executes the action associated with it, to maximize the “reward”.
* Instead of updating a Q-table like in normal Q-learning, the decision would update the weights in the neural network, thus allowing the neural network to learn.



### Blockchain Architecture
* Smart contract used for betting cryptocurrency against the Blackjack AI
    * Ensures that the outcomes of the betting are fair and secure
    * Enables trust between customer and the gambling service because blockchain is immutable
* Logic programmed using Remix IDE in Solidity
    * SepoliaETH used by users to make bets and receive payments
    * MetaMask Ethereum wallet is used to deploy smart contract 
* Users connect to smart contract through MetaMask
    * web3.py Python Library used to interact with the smart contract
    * Users will be prompted to login into their MetaMask wallet account
    * Smart contract will verify and send transactions between users using their Ethereum address
