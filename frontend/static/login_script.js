var cashOutCode = "";
var depositCode = "";
const deposit = document.querySelector('.deposit');
const withdraw = document.querySelector('.withdraw');


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


withdraw.addEventListener("click", async() => {
    await getAccount();

    var amount = hex64(document.getElementById("wamount").value);
    if (isNaN(parseInt(amount)) || amount == 0) {
        alert("Please enter a valid and non-zero amount to withdraw.")
        return;
    }

    ethereum
      .request({
        method: 'eth_sendTransaction',
        params: [
          {
            from: account, // The user's active address.
            to: contract,
            data: cashOutCode + amount,
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

  })

  // Send Ethereum to an address
deposit.addEventListener('click', async() => {
    var amount = hex64(document.getElementById("amount").value);
    if (isNaN(parseInt(amount)) || amount == 0) {
        alert("Please enter a valid and non-zero amount to deposit.")
        return;
    }
    await getAccount();
    ethereum
      .request({
        method: 'eth_sendTransaction',
        params: [
          {
            from: account, // The user's active address.
            to: contract,
            value: amount,
            data: depositCode,
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
  
  
window.onload = function() {
    const MMSDK = new MetaMaskSDK.MetaMaskSDK()
    // Because init process of the MetaMaskSDK is async.
    setTimeout(() => {
        const ethereum = MMSDK.getProvider() // You can also access via window.ethereum
    }, 0)
    fetch('/byteCode', {
        method: 'POST',
        body: JSON.stringify({func: "cashOut(uint256)"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        cashOutCode = data.func;
    })
    fetch('/byteCode', {
        method: 'POST',
        body: JSON.stringify({func: "deposit()"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        depositCode = data.func;
    })
  }
  