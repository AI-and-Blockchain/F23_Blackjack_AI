function login() {
    const dataForm = document.getElementById("dataForm");
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
    .then(data => {
        var x = 0;
        if (data.name == "invalid") {
            alert("Please enter a name");
            x = 1
        }
        // if (data.bet == "invalid") {
        //     alert("Please enter your bet as an integer");
        //     x = 1
        // }
        if (data.address == "invalid") {
            alert("Please enter a valid wallet address");
            x = 1
        }
        if (x == 0) {
            document.getElementById("login_doc").innerHTML = "logging in...";
            location.href = "Blackjack.html";
            fetch("/getBet", {
                method: "POST",
                body: JSON.stringify({address: data.address, bet: 0, message: ""}),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response => response.json())
            .then(data => alert(data.bet))
        }
    })
    // .then(text => {
    //     if (text == "valid") {
    //         document.getElementById("login_doc").innerHTML = "logging in...";
    //         location.href = "Blackjack.html";
    //     } else if (text == "invalid address") {
    //         alert("Please enter a valid wallet address");
    //     } else if (text == "invalid bet") {
    //         alert("Please enter your bet as an integer");
    //     } else {
    //         alert("An error occurred, please try again")
    //     }
    // })
    .catch(error => {
        console.error('Error:', error);
    });
  }
