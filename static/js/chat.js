
// Text that replaces usage notes in JSON form

// Keep name the same as found in "value"
// <select name="type" id="request_type">
//                <option value="text">text</option> 
//                <option value="youtube"...
const usage_notes ={
    "text" : "General chatgpt request, need to write<br>"+
             "example: 'Summarize the bible'",

    "youtube" : "Use only the the youtube id <br> " + 
                "example: \"www.youtube.com/watch?v=bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnRz\" <br> " +
                "becomes: \"bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnR\"",

    "article" : "Only applicable to CNN articles as of now",
}

let request_type = document.getElementById("request_type")

// Changes usage notes
function change_notes(){
    document.getElementById("usage notes").innerHTML = usage_notes[request_type.value]
}
request_type.addEventListener("change",change_notes)

// Initial loading of usage notes 
change_notes()