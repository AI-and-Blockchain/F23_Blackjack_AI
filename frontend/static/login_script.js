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
