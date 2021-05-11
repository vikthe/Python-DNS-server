var configbtn = document.getElementById("configbutton");
var statsbtn = document.getElementById("statisticsbutton");
var headerbtn = document.getElementById("header");
var maincontainer = document.getElementById("maincontainer");
var btncontainer = document.getElementById("buttoncontainer");
var contentcontainer = document.getElementById("contentcontainer");
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
        else if (ishref == false) {
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
        btncontainer.innerHTML = "";
        contentcontainer.innerHTML = "";
        btncontainer.appendChild(createmenubutton("Blacklist", "/configurations/blacklist", false));
        btncontainer.appendChild(createmenubutton("Whitelist", "/configurations/whitelist", false));
        btncontainer.appendChild(createmenubutton("Localaddresses", "/configurations/localaddresslist", false));
        btncontainer.appendChild(createmenubutton("Wordlists", "/configurations/wordlist", false));

        if (state.startsWith("/configurations/blacklist")) {
            inputchangelist(["add", "remove", "clear"], "ex. www.google.com");
            getandsetresponse("/configurations/data?getlist=blacklists", contentcontainer);

        }

        if (state.startsWith("/configurations/whitelist")) {
            inputchangelist(["add", "remove", "clear"], "ex. www.google.com");
            getandsetresponse("/configurations/data?getlist=whitelists", contentcontainer);
        }

        if (state.startsWith("/configurations/localaddresslist")) {
            inputchangelist(["add", "remove", "clear"], "ex. 192.168.1.10 my.website.com");
            getandsetresponse("/configurations/data?getlist=localaddresslists", contentcontainer);
        }

        if (state.startsWith("/configurations/wordlist")) {
            inputchangelist(["add", "remove", "clear"], "ex. ad, ads, some word");
            getandsetresponse("/configurations/data?getlist=wordlists", contentcontainer);
        }
    }
    else if (state.startsWith("/statistics")) {
        btncontainer.innerHTML = "";
        contentcontainer.innerHTML = "";
        btncontainer.appendChild(createmenubutton("Speedtest", "/statistics/speedtest", false));

        if (state.startsWith("/statistics/speedtest")) {
            let input = document.createElement("input");
            input.type = "text";
            input.placeholder = "which domain to ping ex. youtube.com";
            contentcontainer.appendChild(input);

            let button = document.createElement("button");
            button.innerHTML = "Startspeedtest";
            let dnsul = document.createElement("ul");
            dnsul.className = "speedtestul";
            let pyul = document.createElement("ul");
            pyul.className = "speedtestul";
            button.onclick = function () {
                if (input.value != undefined && input.value != "") {
                    //this runs speedtest and displays output
                    let domainname = input.value;
                    dnsul.innerHTML = "";
                    pyul.innerHTML = "";
                    let dnstitleli = document.createElement("li");
                    dnstitleli.className = "speedtestlititle";
                    dnstitleli.innerHTML = "Replies from Google Public DNS";
                    dnsul.appendChild(dnstitleli);
                    for (i = 0; i < 10; i++) {
                        setTimeout(function () {
                            dnslatencytest("https://dns.google/resolve?name=" + domainname + "&type=A", dnsul);
                        }, 300 * i)
                    }

                    
                    let pytitleli = document.createElement("li");
                    pytitleli.innerHTML = "Replies from Python DNS";
                    pytitleli.className = "speedtestlititle";
                    pyul.appendChild(pytitleli);
                    for (i = 0; i < 10; i++) {
                        setTimeout(function () {
                            dnslatencytest("/statistics/data?resolvename=" + domainname, pyul);
                        }, 300 * i)
                    }
                }

            }
            contentcontainer.appendChild(button);
        }


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
    return dropdown;
}

//function that takes an array and return a html list
function makeulfromarray(array) {
    let ul = document.createElement("ul");
    for (i = 0; i < array.length; i++) {
        let li = document.createElement("li");
        li.innerHTML = array[i];
        ul.appendChild(li);
    }
    return ul;
}

//input and buttons for changing values of lists the dns server has
function inputchangelist(actions, placeholder) {
    contentcontainer.innerHTML = "";
    let dropdown = createdropdown(actions);
    contentcontainer.appendChild(dropdown);
    let input = document.createElement("input");
    input.type = "text";
    input.placeholder = placeholder;
    input.onkeydown = function (event) {
        if (event.key == "Enter") {
            data = [["action", dropdown.value], ["value", input.value]];
            postdata(data, window.location.href);
            input.value = "";
        }
    }
    contentcontainer.appendChild(input);

    let button = document.createElement("button");
    button.innerHTML = "Confirm";
    button.onclick = function () {
        data = [["action", dropdown.value], ["value", input.value]];
        postdata(data, window.location.href);
        displaycontent(window.location.pathname);
        input.value = "";
    }
    contentcontainer.appendChild(button);

    let refreshbtn = document.createElement("button");
    refreshbtn.innerHTML = "Refresh";
    refreshbtn.onclick = function () {
        window.location.href = window.location.href;
    }
    contentcontainer.appendChild(refreshbtn);
}

//function to post data to flask
function postdata(data, destination) {
    const request = new XMLHttpRequest()
    request.open('POST', destination)
    let form = new FormData();
    for (i = 0; i < data.length; i++) {
        form.append(data[i][0], data[i][1]);
    }
    request.send(form);
    return false;
}

//function that sends a get request and appends the response as list to appendto variable
//is used to show all lists
function getandsetresponse(requesturl, appendto) {
    const request = new XMLHttpRequest();
    request.open("POST", requesturl);
    request.send();
    request.onload = function () {
        if (this.readyState == 4 && this.status == 200) {
            const jsondata = JSON.parse(request.responseText);
            console.log(jsondata);
            appendto.appendChild(makeulfromarray(jsondata[0]));
        }
    }
}

//function that tests latency to a dns server
//add result as a list to contentcontainer
function dnslatencytest(requesturl, appendto) {
    const request = new XMLHttpRequest();
    contentcontainer.appendChild(appendto);
    request.open("GET", requesturl);
    const oldtime = new Date().getTime();
    console.log(oldtime)
    request.send();
    request.onload = function () {
        if (this.readyState == 4 && this.status == 200) {
            const jsondata = JSON.parse(request.responseText);
            console.log(jsondata)
            const ip = jsondata["Answer"][0]["data"];
            console.log(ip);
            const newtime = new Date().getTime();
            const pingtime = newtime - oldtime;
            console.log(newtime - oldtime);
            let li = document.createElement("li");
            li.className = "speedtestli"
            li.innerHTML = String(ip) + " ---- " + String(pingtime) + "  ms";
            appendto.appendChild(li);
        }
    }
}