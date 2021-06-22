// URL of the server 
var serverURL = "http://10.10.4.124:5500";



function createSprinklerCards(sprinklers){
  
    var sprinkler_DataDiv = document.createElement("DIV");
    sprinkler_DataDiv.classList.add("sprinkler_data");

    // buttom div
    
    var sprinkler_ButtonDiv = document.createElement("DIV");
    sprinkler_ButtonDiv.classList.add("buttons");

    var toggle = document.createElement("DIV");
    toggle.classList.add("w3-right");

    var toggle_1 = document.createElement("INPUT");
    toggle_1.setAttribute("type","checkbox");
    toggle_1.setAttribute("id","switch_1");
    var toggle_2 = document.createElement("label");
    toggle_2.setAttribute("class","toggle-switch")
    toggle_2.setAttribute("for","switch_1")
    

    var deleteButton = document.createElement("DIV");
    deleteButton.classList.add("delete");
    deleteButton.setAttribute("id",sprinklers._id.$oid)
    deleteButton.innerHTML = "X";
  

    
    
    
    // sprinkler Image Div
    var sprinkler_imgDiv = document.createElement("DIV");
    sprinkler_imgDiv.classList.add("sprinkler_img");

    var sprinkler_imgimg = document.createElement("IMG");
    sprinkler_imgimg.src = "/static/images/sprinkler.jpg";    
    sprinkler_imgDiv.append(sprinkler_imgimg);
    
  ;

    // Display Div
    var displayDiv = document.createElement("DIV");
    displayDiv.classList.add("display");

    var sprinkler_nameDiv = document.createElement("DIV");
    sprinkler_nameDiv.classList.add("sprinkler_name");

    var sprinkler_nameSpan1 = document.createElement("SPAN");
    sprinkler_nameSpan1.innerHTML = sprinklers.sprinklers_name;
    sprinkler_nameDiv.append(sprinkler_nameSpan1);


    var sprinkler_locationDiv = document.createElement("DIV");
    sprinkler_locationDiv.classList.add("sprinkler_location");

    var sprinkler_locationSpan1 = document.createElement("SPAN");
    sprinkler_locationSpan1.innerHTML = sprinklers.sprinklers_location
    sprinkler_locationDiv.append(sprinkler_locationSpan1);
    
    sprinkler_ButtonDiv.append(toggle);
    toggle.append(toggle_1);
    toggle.append(toggle_2);
    sprinkler_ButtonDiv.append(deleteButton);
    displayDiv.append(sprinkler_nameDiv);
    displayDiv.append(sprinkler_locationDiv);   
    sprinkler_DataDiv.append(sprinkler_ButtonDiv)
    sprinkler_DataDiv.append(sprinkler_imgDiv);
    sprinkler_DataDiv.append(displayDiv);

    return sprinkler_DataDiv;
}

var sprinklerPath = serverURL + "/sprinklers";
function getSprinklerData(){
    console.log("SprinklerData");
    return fetch(sprinklerPath).then(res => res.json()).then(json => json);
}



async function displaySprinklerData(){
    var content = document.querySelector(".content");
    content.innerHTML = "";

    let sprinklers = await getSprinklerData();  
    console.log(sprinklers);

    sprinklers.forEach(sprinklers => {
        console.log(sprinklers.sprinklers__id);
        // getSprinklerData(sprinklers.sprinklers__id).then(res => {
        //     var content = document.querySelector(".content");
        //     console.log(res);
            content.append(createSprinklerCards(sprinklers));
        // });        
    });
 // Send delete request if delete button is pressed
 var deleteButtons = document.querySelectorAll(".delete");
 deleteButtons.forEach(button => {
     button.addEventListener("click", function(){

         // Send delete request to server
         console.log("DELETE "+ button.id);
         fetch(sprinklerPath +"/"+ button.id, {
             method: "DELETE",
             headers: {
                 "Content-type": "application/json",
             },
         })
         .then(function(){
             displaySprinklerData();
         })
         
     });
 });
}

window.onload = function(){
    displaySprinklerData();

   

        // Redirect user to the page where they can view a sprinkler_s data in detail
        var sprinkler_img = document.querySelectorAll("img");
        sprinkler_img.forEach(img => {
            img.addEventListener("click", function(){
                console.log(img.id);

                // Save ID to session storage and redirect to the edit page
                sessionStorage.setItem("sprinkler__id", img.id);
                location.href = "individual_info.html";
                window.open("individual_info.html");
            });
        })
       


   
    var elements = document.getElementsByClassName("sprinkler-card");


function move(event) {
     if (event.target==this)
    window.location = "history.html";
}

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', move, false);
}

} 