document.getElementsByClassName("loader")[0].style.display = "block";
document.getElementsByTagName("body")[0].style.backgroundColor = "#383b38";
document.getElementById("content-container").style.display = "none";
document.getElementById("addlink-container").style.display = "none";
document.getElementById("error-container").style.display = "none";
document.getElementById("learn-container").style.display = "none";

(async () => {
    const response = await chrome.runtime.sendMessage({message: "link"});
    link = response.url
    console.log(response.url)
    if (link != "Empty") {
        fetchData(link)
    }
    else {
        console.log(link)
        console.log("link wasn't found")
        addLink()
    }
})();



function fetchData(link) {
    const myHeaders = new Headers();
    myHeaders.append("privacyPolicy", link);

    const requestOptions = {
        mode:  'cors', 
        method: "GET",
        headers: myHeaders,
        redirect: "follow"
    };
    //"http://127.0.0.1:5000/sum"
    // https://csc324spring2024.us.reclaim.cloud/sum
    fetch("https://csc324spring2024.us.reclaim.cloud/sum", requestOptions
    ).then(function (response) {
        // return result
        return response.text()
    }).then(function (data) {
        try {
           console.log(data);
           addContent(data);
        }
        // error -- assume couldn't find link or it was broken, which is why we couldn't parse the JSON
        catch(err) { 
            console.log('Request failed', err);
            appearAlert("Our programs are unable to parse and summarize the contents of this webpage. We apologize.")
        }

    });
}

function addContent(data) {
    // if successful, we can parse json 
    const privacy_data = JSON.parse(data); 
                
    // if JSON was completed, but its empty
    if (data == "{}") {
        appearAlert("Our programs are unable to parse and summarize the contents of this webpage. We apologize.")
    }

    // get the "content" and "rating" divs to place the json content 
    const content = document.getElementById("content");
    const rating = document.getElementById("rating");

    // NEED TO ROUND to 2 to 3 places
    let print_score = Math.round(privacy_data["PrivacyPolicyScore"] * 100) / 100;
    
    // -- change color of rating font by privacy safety level
    let bad = 6.9; 
    let good = 6.6; 

    // default font color is black
    let color = "black"
    
    // assign color to font 
    if (print_score <= good) {
        color = "#1F993D"; 
    }
    else if (print_score >= bad) {
        console.log(rating.style)
        color = "#E5362E"; 
    }
    else {
        color = "#E5BA2E"; 
    }

    // add the rating to its container 
    rating.innerHTML += `<h1 style="background-color:` + color + `;">` + "Score: " + print_score.toString() + `</h1>` 

    // each heading and summary pairing, place them with the correct tags inside the "content" div
    for (let [heading, summary] of Object.entries(privacy_data)) {
        console.log(summary)
        if (summary.length > 0 && summary != "\u00a0") {
            content.innerHTML += `<h2>` + heading.trim().replace(/\u00a0/g, ' ') + `</h2>` + `<p>` + summary + `</p>` ; 
        }
    }

    // stop loader and show content now 
    document.getElementsByClassName("loader")[0].style.display = "none";
    document.getElementsByTagName("body")[0].style.backgroundColor = "#f9f9f9";
    document.getElementById("content-container").style.display = "block";
    document.getElementById("learn-container").style.display = "block";
    
}

function addLink() {
    // loader disappears and our form opens
    document.getElementsByClassName("loader")[0].style.display = "none";
    document.getElementsByTagName("body")[0].style.backgroundColor = "#f9f9f9";
    document.getElementById("addlink-container").style.display = "block";
    document.getElementById("learn-container").style.display = "block";
    // after submitting 
    linkForm.addEventListener("submit", (e) => {
        e.preventDefault();
        console.log("I've been submitted!")
        console.log(myLink)
        console.log(myLink.value)
        
        // checking if there is information inside input, if not then throw error
        if (myLink.value == "") {
            appearAlert("You forgot to paste the URL. Please refresh and try again.")
        } 
        else {
            document.getElementsByClassName("loader")[0].style.display = "block";
            document.getElementsByTagName("body")[0].style.backgroundColor = "#383b38";
            document.getElementById("addlink-container").style.display = "none";
            document.getElementById("learn-container").style.display = "none";

            fetchData(myLink.value)
        }
    });
}

function appearAlert(str) {
    const error = document.getElementById("error");

    error.innerHTML += `<p>` + str + `<p>`;

    document.getElementsByClassName("loader")[0].style.display = "none";
    document.getElementById("content-container").style.display = "none";
    document.getElementById("addlink-container").style.display = "none";
    document.getElementsByTagName("body")[0].style.backgroundColor = "#f9f9f9";
    document.getElementById("error-container").style.display = "block";
    document.getElementById("learn-container").style.display = "block";
    
}