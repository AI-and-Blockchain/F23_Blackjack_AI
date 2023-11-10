// document.addEventListener("DOMContentLoaded", function() {
//     const dataForm = document.getElementById("dataForm");
//     const sendButton = document.getElementById("sendButton");
//     const outputDiv = document.getElementById("output");

//     sendButton.addEventListener("click", function() {
//         const formData = new FormData(dataForm);
//         const jsonData = {};

//         formData.forEach((value, key) => {
//             jsonData[key] = value;
//         });

//         // Make an AJAX request to the FastAPI backend
//         fetch('/F23_Blackjack_AI/frontend', {
//             method: 'POST',
//             body: JSON.stringify(jsonData),
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             // Display the response in the output div
//             outputDiv.textContent = `Response from Backend: ${data.message}`;
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//     });
// });



function login() {
    const formData = new FormData(dataForm);
    const jsonData = {};

    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    // Make an AJAX request to the FastAPI backend
    fetch('/F23_Blackjack_AI/frontend', {
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

        }

    })
    // .then(data => {
        //     // Display the response in the output div
        //     // outputDiv.textContent = `Response from Backend: ${data.message}`;
        
    // })
    .catch(error => {
        console.error('Error:', error);
    });
  }
