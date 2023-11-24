var account = '';
async function getAccount() {
    await ethereum.request({ method: 'eth_requestAccounts' }).then(data => account = data[0]);
}

const hex64 = d => Number(d).toString(16).padStart(64, '0');
const pad64 = d => d.padStart(64, '0');

async function checkBalance() {
    await getAccount();
    
    await fetch('/getBalance', {
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