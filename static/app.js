var configbtn = document.getElementById("configbutton");
var statsbtn = document.getElementById("statisticsbutton");
var headerbtn = document.getElementById("header");
var maincontainer = document.getElementById("maincontainer");
var btncontainer = document.getElementById("buttoncontainer");
var contentcontainer = document.getElementById("contentcontainer");
var request = new XMLHttpRequest(); //object for posting data to flask server
var testdiv = document.getElementById("testdiv")


//to show the right content when url is written in the url bar
prettypathname = prettyprinturl(window.location.pathname);
displaycontent(prettypathname)

//these if statement checks the current url and edits maincontainer depending on the url
/*
if(prettyurl == ""){
    contentcontainer.innerHTML = "This is the home page, click on statistics or configurations for more options"
    btncontainer.innerHTML = "";
    window.history.replaceState({}, null, "/");
    }

if(prettyurl == "/configurations"){
    window.history.replaceState({}, null, prettyurl);
    contentcontainer.innerHTML = "config"
    createconfigbtns();
    //display("/configurations")
}
/*
if(prettyurl == "/configurations/blacklist"){
    window.history.replaceState({}, null, prettyurl);
    contentcontainer.innerHTML = "config"
    createconfigbtns();
    let form = document.createElement("form");
    contentcontainer.appendChild(form);
    arr = ["arr", "rere"];
    createdropdown(arr)
}
*/

/*
if(prettyurl == "/configurations/blacklist"){
   //blacklistbtn.click();
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

*/
//to delete "/" at the end of url
function prettyprinturl(url){
    if (url.charAt(url.length-1) == "/"){
        url = url.substring(0,(url.length-1));
        return url;
    }
}

//onclick events for navbar and header
configbtn.onclick = function(){
    let newstate = "/configurations";
    window.history.pushState({}, null, newstate);
    displaycontent(newstate)
}
statsbtn.onclick = function(){
    let newstate = "/statistics";
    window.history.pushState({}, null, newstate);
    displaycontent(newstate)
}

headerbtn.onclick = function(){
    let newstate = "/"
    window.history.pushState({}, null, newstate);
    displaycontent(newstate)    
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
    let blacklistbtn = document.createElement("div");
    blacklistbtn.className = "menubutton";
    blacklistbtn.innerHTML = "Blacklist";
    blacklistbtn.onclick = function(){
        let newstate = "/configurations/blacklist";
        window.history.pushState({}, null, newstate);
        displaycontent(newstate)
    }
    btncontainer.appendChild(blacklistbtn);
}

//this function handles what to display in maincontiner
function displaycontent(state){
    if (state == "/configurations"){
        btncontainer.innerHTML = ""
        contentcontainer.innerHTML = "configs"
        createconfigbtns();
    }
    else if(state == "/statistics"){
        btncontainer.innerHTML = ""
        contentcontainer.innerHTML = "stats"
        createstatsbtns();
    }
    else if(state =="/" || state == ""){
        btncontainer.innerHTML = "";
        contentcontainer.innerHTML = "This is the home page, click on statistics or configurations for more options";    
    }

    else if(state == "/configurations/blacklist"){
        contentcontainer.innerHTML = "";
        arr = ["add", "remove"];
        let dropdown = createdropdown(arr);
        contentcontainer.appendChild(dropdown);
        let input = document.createElement("input");
        input.type = "text";
        input.placeholder = "ex. www.google.com"
        contentcontainer.appendChild(input);

        let button = document.createElement("button");
        button.value = "Confirm";
        button.innerHTML = "Confirm";
        button.onclick = function(){
            data = [["action", dropdown.value]];
            postdata(data, window.location.href);
        }
        contentcontainer.appendChild(button);
    }
}

//create dropdown
function createdropdown(arguments){
    let dropdown = document.createElement("select");
    for(i=0;i<arguments.length;i++){
        let option = document.createElement("option");
        option.value = arguments[i];
        option.text = arguments[i];
        dropdown.appendChild(option);
    }
    return dropdown
}

function postdata(data, destination){
    request.open('POST', destination)
    let form = new FormData();
    for(i=0; i<data.length;i++){
        console.log(data[i][0])
        console.log(data[i][1])
        form.append(String(data[i][0]), String(data[i][1]));
    }
    request.send(form);
    return false;
}