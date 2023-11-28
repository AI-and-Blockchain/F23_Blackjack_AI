var cashOutCode = "";
var depositCode = "";
const deposit = document.querySelector('.deposit-btn');
const withdraw = document.querySelector('.withdraw-btn');

var slider = document.getElementById("AILevel");
var output = document.getElementById("slidelabel");

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value + "%";
}


async function login() {
    await checkBalance();
    
    const jsonData = {name: document.getElementById("name").value, address: account, smartness: slider.value};

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
        } else if (Number(document.getElementById("balanceLabel").innerHTML) < 10) {
            alert("Please deposit at least 10 Wei into your account.")
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
    document.getElementById("balanceLabel").innerHTML = "⟳ Balance Loading ⟳";
    ethereum
      .request({
        method: 'eth_sendTransaction',
        params: [
          {
            from: account, // The user's active address.
            to: contract,
            data: cashOutCode + amount,
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
    document.getElementById("balanceLabel").innerHTML = "⟳ Balance Loading ⟳";
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
  
  
window.onload = async function() {
    slider.value = '50';
    output.innerHTML = slider.value + "%"; // Display the default slider value

    try {
        await checkBalance();
    } catch {
        console.log("first time user");
    }
    const MMSDK = new MetaMaskSDK.MetaMaskSDK();
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
  