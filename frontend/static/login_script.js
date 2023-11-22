function login() {
    const dataForm = document.getElementById("dataForm");
    const formData = new FormData(dataForm);
    const jsonData = {};

    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(jsonData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        var x = 0;
        if (data.name == "invalid") {
            alert("Please enter a name");
            x = 1;
        }
        if (data.address == "invalid") {
            alert("Please enter a valid wallet address");
            x = 1;
        }
        if (x == 0) {
            document.getElementById("login_doc").innerHTML = "logging in...";
            location.href = "Blackjack.html";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
  }

  const ethereumButton = document.querySelector('.enableEthereumButton');
  const sendEthButton = document.querySelector('.sendEthButton');
  
  let accounts = ["0x5233862f7245CB0d76af46716631abFB389163C0"];
  
  // Send Ethereum to an address
  sendEthButton.addEventListener('click', () => {
    ethereum
      .request({
        method: 'eth_sendTransaction',
        // The following sends an EIP-1559 transaction. Legacy transactions are also supported.
        params: [
          {
            from: accounts[0], // The user's active address.
            to: "0xf9a568f094FEb5cfD453F1e8e13dfdbe55323B77",
            value: '1000',
            gasLimit: '0x5028', // Customizable by the user during MetaMask confirmation.
            maxPriorityFeePerGas: '0x3b9aca00', // Customizable by the user during MetaMask confirmation.
            maxFeePerGas: '0x2540be400', // Customizable by the user during MetaMask confirmation.
          },
        ],
      })
      .then((txHash) => console.log(txHash))
      .catch((error) => console.error(error));
  });
  
  ethereumButton.addEventListener('click', () => {
    getAccount();
  });
  
  async function getAccount() {
    accounts = await ethereum.request({ method: 'eth_requestAccounts' });
  }
