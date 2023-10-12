
// Text that replaces usage notes in JSON form

// Keep name the same as found in "value"
// of the type buttons
const usage_notes ={
    "text" : "General chatgpt request, need to write<br>"+
             "example: 'Summarize the bible'",

    "youtube" : "Use only the the youtube id <br> " + 
                "example: \"www.youtube.com/watch?v=bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnRz\" <br> " +
                "becomes: \"bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnR\"",

    "article" : "Only applicable to CNN articles as of now",
}

// Changes usage notes
var request_type_list = document.getElementsByTagName("button")

for(var i = 0; i < request_type_list.length;i++){
    request_type_list[i].addEventListener("click", () =>{

        // Switch the all the buttons on
        for(var i = 0; i < request_type_list.length;i++){
            request_type_list[i].disabled = false;
            request_type_list[i].name = '';
        }
        
        // Turn the clicked button off and change usage notes
        event.target.disabled = true
        document.getElementById("type").value = event.target.innerHTML
        document.getElementById("usage notes").innerHTML = usage_notes[event.target.innerHTML]
    })
}

document.getElementById("usage notes").innerHTML = usage_notes[document.getElementById("type").value]