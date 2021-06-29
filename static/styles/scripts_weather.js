var serverURL = "http://10.10.22.218:5500";



function createWeatherCards(weathers){
  
    var Weather_DataDiv = document.createElement("DIV");
    Weather_DataDiv.classList.add("Weather_data");


    var RAINDiv = document.createElement("DIV");
    RAINDiv.classList.add("RAIN");

    var RAINSpan1 = document.createElement("SPAN");
    RAINSpan1.innerHTML = weathers.rain_data;
    
    var RAINSpan2 = document.createElement("SPAN");
    RAINSpan2.innerHTML = "RAINY DAY: ";

    RAINDiv.append(RAINSpan2);
    RAINDiv.append(RAINSpan1);

    var SUNDiv = document.createElement("DIV");
    SUNDiv.classList.add("SUN");

    var SUNSpan1 = document.createElement("SPAN");
    SUNSpan1.innerHTML = weathers.sun_data;

    var SUNSpan2 = document.createElement("SPAN");
    SUNSpan2.innerHTML = "SUNNY DAY: ";

    SUNDiv.append(SUNSpan2);
    SUNDiv.append(SUNSpan1);

    Weather_DataDiv.append(RAINDiv);
    Weather_DataDiv.append(SUNDiv);
    return Weather_DataDiv;
}

var weatherPath = serverURL + "/weathers";

function getweatherData(){
    console.log("Weather Data");
    return fetch(weatherPath).then(res => res.json()).then(json => json);
}



async function displayWeatherData(){
    var content = document.querySelector(".content");
    

    let weathers = await getweatherData();  
    console.log(weathers);

    weathers.forEach(weathers => {
     content.append(createWeatherCards(weathers));
            
    });
 
}

window.onload = function(){
    displayWeatherData();
} 