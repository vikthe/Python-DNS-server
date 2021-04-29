var configbtn = document.getElementById("configbutton");
var statsbtn = document.getElementById("statisticsbutton");
var headerbtn = document.getElementById("header");
var maincontainer = document.getElementById("maincontainer");
var btncontainer = document.getElementById("buttoncontainer");
var contentcontainer = document.getElementById("contentcontainer");
var request = new XMLHttpRequest(); //object for posting data to flask server
var testdiv = document.getElementById("testdiv");

//to show the right content when url is written in the url bar
prettypathname = prettyprinturl(window.location.pathname);
displaycontent(prettypathname)

//to delete "/" at the end of url
function prettyprinturl(url) {
    if (url.charAt(url.length - 1) == "/" && url.length != 1) {
        url = url.substring(0, (url.length - 1));
    }
    return url;
}

//onclick events for navbar and header
configbtn.onclick = function () {
    let newstate = "/configurations";
    window.history.pushState({}, null, newstate);
    displaycontent(newstate)
}
statsbtn.onclick = function () {
    let newstate = "/statistics";
    window.history.pushState({}, null, newstate);
    displaycontent(newstate)
}

headerbtn.onclick = function () {
    let newstate = "/"
    window.history.pushState({}, null, newstate);
    displaycontent(newstate)
}

//returns a button with chosen text and an onclick method
//that pushstates to the newonsclickstate variable
function createmenubutton(text, newonclickstate, ishref) {
    let btn = document.createElement("div");
    btn.className = "menubutton";
    btn.innerHTML = text;

    btn.onclick = function () {
        if (ishref == true) {
            window.location.href = newonclickstate;
        }


        if (ishref == false) {
            let newstate = newonclickstate;
            window.history.pushState({}, null, newstate);
            displaycontent(newstate)
        }
    }

    return btn;
}

//this function handles what to display in maincontiner
function displaycontent(state) {
    if (state.startsWith("/configurations")) {
        btncontainer.innerHTML = ""
        contentcontainer.innerHTML = "configs"
        btncontainer.appendChild(createmenubutton("Blacklist", "/configurations/blacklist", true));
        btncontainer.appendChild(createmenubutton("Whitelist", "/configurations/whitelist", true));

        if (state.startsWith("/configurations/blacklist")) {
            inputchangelist(["add", "remove"], "ex. www.google.com");
            console.log(flaskdata);
        }

        if (state.startsWith("/configurations/whitelist")) {
            inputchangelist(["add", "remove"], "ex. www.google.com");
        }
    }
    else if (state.startsWith("/statistics")) {
        btncontainer.innerHTML = ""
        contentcontainer.innerHTML = "stats"
        btncontainer.appendChild(createmenubutton("Speedtest", "statistics/speedtest"))
    }
    else if (state.startsWith("/")) {
        btncontainer.innerHTML = "";
        contentcontainer.innerHTML = "This is the home page, click on statistics or configurations for more options";
    }
}

//create dropdown
function createdropdown(arguments) {
    let dropdown = document.createElement("select");
    for (i = 0; i < arguments.length; i++) {
        let option = document.createElement("option");
        option.value = arguments[i];
        option.text = arguments[i];
        dropdown.appendChild(option);
    }
    return dropdown
}

//input and button for changing values of lists the dns server has
function inputchangelist(actions, placeholder) {
    contentcontainer.innerHTML = "";
    let dropdown = createdropdown(actions);
    contentcontainer.appendChild(dropdown);
    let input = document.createElement("input");
    input.type = "text";
    input.placeholder = placeholder;
    contentcontainer.appendChild(input);

    let button = document.createElement("button");
    //button.value = "Confirm";
    button.innerHTML = "Confirm";
    button.onclick = function () {
        data = [["action", dropdown.value], ["value", input.value]];
        postdata(data, window.location.href);
    }
    contentcontainer.appendChild(button);
}

//function to post data to flask
function postdata(data, destination) {
    request.open('POST', destination)
    let form = new FormData();
    for (i = 0; i < data.length; i++) {
        console.log(data[i][0])
        console.log(data[i][1])
        form.append(String(data[i][0]), String(data[i][1]));
    }
    request.send(form);
    return false;
}