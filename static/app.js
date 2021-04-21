var configbtn = document.getElementById("configbutton");
var statsbtn = document.getElementById("statisticsbutton");
var headerbtn = document.getElementById("header");
var maincontainer = document.getElementById("maincontainer");
var btncontainer = document.getElementById("buttoncontainer");

var testdiv = document.getElementById("testdiv")

//onclick events for navbar and header
configbtn.onclick = function(){
    btncontainer.innerHTML = "";
    window.history.pushState({}, null, "/configurations");
    testdiv.innerHTML = "conf";
}
statsbtn.onclick = function(){
    btncontainer.innerHTML = "";
    window.history.pushState({}, null, "/statistics");
    testdiv.innerHTML = "stats"
    createbtns();
}

headerbtn.onclick = function(){
    btncontainer.innerHTML = "";
    window.history.pushState({}, null, "/");
    testdiv.innerHTML = "This is the home page, click on statistics or configurations for more options"
}

//creates buttons and listeners for statistics menu
function createbtns(){
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