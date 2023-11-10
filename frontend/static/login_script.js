function login() {
    const formData = new FormData(dataForm);
    const jsonData = {};

    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    // Make an AJAX request to the FastAPI backend
    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(jsonData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(text => {
        if (text == "valid") {
            document.getElementById("login_doc").innerHTML = "logging in...";
            location.href = "Blackjack.html";
        } else {
            alert("Please enter a valid wallet address");
        }

    })
    .catch(error => {
        console.error('Error:', error);
    });
  }
