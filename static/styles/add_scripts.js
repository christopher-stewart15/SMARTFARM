// URL of the server 
var serverURL = "http://10.10.22.218:5500";

let button = document.querySelector(".button");
button.addEventListener("click", function(event){
    let sprinklers_name = document.getElementById("sprinklers_name").value;
    let sprinklers_location = document.getElementById("sprinklers_location").value;
    let sprinklers_id = document.getElementById("sprinklers_id").value;

    //  make POST request
    console.log("Make POST Request");

    // Construct the JSON body to be sent in the POST request
    jsonBody = {
        "sprinklers_name": sprinklers_name,
        "sprinklers_location": sprinklers_location,
        "sprinklers_id": sprinklers_id,
        };

    // Send the POST request 
    fetch(serverURL + "/sprinklers", {
         method: "POST",
        body: JSON.stringify(jsonBody),
        headers:{
                 "Content-type": "application/json",
            },
        })
    .then((res) => res.json)
    .then((json) => console.log(json));

    // Clear the boxes so the user knows his request has gone through
    document.getElementById("sprinklers_name").value = "";
    document.getElementById("sprinklers_location").value = "";
    document.getElementById("sprinklers_id").value = "";
    
});