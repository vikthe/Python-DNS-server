//göra fineify url function. /statistics/ --> /statistics 

var configbtn = document.getElementById("configbutton");
var statsbtn = document.getElementById("statisticsbutton");
var headerbtn = document.getElementById("header");
var maincontainer = document.getElementById("maincontainer");
var btncontainer = document.getElementById("buttoncontainer");
var contentcontainer = document.getElementById("contentcontainer");
var testdiv = document.getElementById("testdiv")

prettyurl = prettyprinturl(window.location.pathname);

//these if statement checks the current url and edits maincontainer depending on the url
if(prettyurl == ""){
    contentcontainer.innerHTML = "This is the home page, click on statistics or configurations for more options"
    btncontainer.innerHTML = "";
    window.history.replaceState({}, null, "/");
    }


if(prettyurl == "/statistics"){
    window.history.replaceState({}, null, prettyurl);
    contentcontainer.innerHTML = "stats"
    createstatsbtns();
}

if(prettyurl == "/statistics/speed"){
    window.history.replaceState({}, null, prettyurl);
    contentcontainer.innerHTML = "stats/speed"
    createstatsbtns();
}

//to delete "/" at the end of url
function prettyprinturl(url){
    if (url.charAt(url.length-1) == "/"){
        url = url.substring(0,(url.length-1));
        return url;
    }
}

//onclick events for navbar and header
configbtn.onclick = function(){
    btncontainer.innerHTML = ""
    window.history.pushState({}, null, "/configurations");
    contentcontainer.innerHTML = "configs"
    createconfigbtns();
}
statsbtn.onclick = function(){
    btncontainer.innerHTML = ""
    window.history.pushState({}, null, "/statistics");
    contentcontainer.innerHTML = "stats"
    createstatsbtns();
}

headerbtn.onclick = function(){
    window.history.pushState({}, null, "/");
    contentcontainer.innerHTML = "This is the home page, click on statistics or configurations for more options"
}

//creates buttons and listeners for statistics menu
function createstatsbtns(){
    let speedtestbtn = document.createElement("div");
    speedtestbtn.className = "menubutton";
    speedtestbtn.innerHTML = "Speedtest"
    btncontainer.appendChild(speedtestbtn);
}

//creates buttons and listeners for configurations menu
function createconfigbtns(){
    let speedtestbtn = document.createElement("div");
    speedtestbtn.className = "menubutton";
    speedtestbtn.innerHTML = "Blacklist";
    btncontainer.appendChild(speedtestbtn);
}