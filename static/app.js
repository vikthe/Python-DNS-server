//göra fineify url function. /statistics/ --> /statistics 

var configbtn = document.getElementById("configbutton");
var statsbtn = document.getElementById("statisticsbutton");
var headerbtn = document.getElementById("header");
var maincontainer = document.getElementById("maincontainer");
var btncontainer = document.getElementById("buttoncontainer");
var contentcontainer = document.getElementById("contentcontainer");
var testdiv = document.getElementById("testdiv")


if(window.location.pathname == "/statistics" || window.location.pathname == "/statistics/"){
    btncontainer.innerHTML = "";
    window.history.replaceState({}, null, "/statistics");
    contentcontainer.innerHTML = "stats"
    createstatsbtns();
}

if(window.location.pathname == "/statistics/speed"){
    btncontainer.innerHTML = "";
    window.history.replaceState({}, null, "/statistics");
    contentcontainer.innerHTML = "stats"
    createstatsbtns();
}


//onclick events for navbar and header
configbtn.onclick = function(){
    btncontainer.innerHTML = "";
    window.history.pushState({}, null, "/configurations");
    contentcontainer.innerHTML = "configs"
}
statsbtn.onclick = function(){
    btncontainer.innerHTML = "";
    window.history.pushState({}, null, "/statistics");
    contentcontainer.innerHTML = "stats"
    createstatsbtns();
}

headerbtn.onclick = function(){
    btncontainer.innerHTML = "";
    window.history.pushState({}, null, "/");
    testdiv.innerHTML = "This is the home page, click on statistics or configurations for more options"
}

//creates buttons and listeners for statistics menu
function createstatsbtns(){
    let speedtestbtn = document.createElement("div");
    speedtestbtn.className = "menubutton";
    speedtestbtn.innerHTML = "Speedtest"
    btncontainer.appendChild(speedtestbtn);

    let speetestbtn = document.createElement("div");
    speetestbtn.className = "menubutton";
    speetestbtn.innerHTML = "Speedsdt"
    btncontainer.appendChild(speetestbtn);

    let spetestbtn = document.createElement("div");
    spetestbtn.className = "menubutton";
    spetestbtn.innerHTML = "Speedsdt"
    btncontainer.appendChild(spetestbtn);
}