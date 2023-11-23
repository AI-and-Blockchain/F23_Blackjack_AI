const hex = d => Number(d).toString(16).padStart(2, '0')
var contract = "";
const deposit = document.querySelector('.deposit');

async function login() {
    await getAccount();
    
    const jsonData = {name: document.getElementById("name").value, address: account};

    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(jsonData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.name == "invalid") {
            alert("Please enter a name");
        } else {
            location.href = "Blackjack.html";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
  }
  
  async function checkBalance() {
    await getAccount();
    
    fetch('/getBalance', {
        method: 'POST',
        body: JSON.stringify({address: account, balance: 0}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("balanceLabel").innerHTML = data.balance;
    })
    
  }
  
  // Send Ethereum to an address
  deposit.addEventListener('click', async() => {
    var amount = hex(document.getElementById("amount").value);
    if (isNaN(parseInt(amount)) || amount == 0) {
        alert("Please enter a valid and non-zero amount to deposit.")
        return;
    }
    await getAccount();
    ethereum
      .request({
        method: 'eth_sendTransaction',
        // The following sends an EIP-1559 transaction. Legacy transactions are also supported.
        params: [
          {
            from: account, // The user's active address.
            to: contract,
            value: amount,
            gasLimit: '0x5028', // Customizable by the user during MetaMask confirmation.
            maxPriorityFeePerGas: '0x3b9aca00', // Customizable by the user during MetaMask confirmation.
            maxFeePerGas: '0x2540be400', // Customizable by the user during MetaMask confirmation.
          },
        ],
      })
      .then((txHash) => {
            console.log(txHash);
            fetch('/trackTransaction', {
                method: 'POST',
                body: JSON.stringify({address: txHash}),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(_ => checkBalance())
      })
      .catch((error) => console.error(error));
  });
  
  async function getAccount() {
    await ethereum.request({ method: 'eth_requestAccounts' }).then(data => account = data[0]);
  }

  window.onload = function() {
    const MMSDK = new MetaMaskSDK.MetaMaskSDK()
    // Because init process of the MetaMaskSDK is async.
    setTimeout(() => {
        const ethereum = MMSDK.getProvider() // You can also access via window.ethereum
    }, 0)
    fetch('/contractAddress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        contract = data.address;
    })
  }
  