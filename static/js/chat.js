
// Text that replaces usage notes in JSON form

// Keep name the same as found in "value"
// of the type buttons
const usage_notes ={
    "text" : "General chatgpt request, need to write<br>"+
             "example: 'Summarize the bible'",

    "youtube" : "Use either the entire link or just the youtube video ID " + 
                "example: \"www.youtube.com/watch?v=bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnRz\" <br> " +
                "or just \"bBQVR4epfBQ&pp=ygUScGVydW4gcmVxdWlyZW1lbnR\"",

    "article" : "Only applicable to CNN articles as of now",
}

const input_text ={
    "text" : "Name of thing to be summarized",

    "youtube" : "Insert youtube link",

    "article" : "Insert CNN article",
}

var file_inputs_element = document.getElementById("file types")
var file_inputs = []
for (var i = 0; i < file_inputs_element.options.length;i++){
    file_inputs = file_inputs + file_inputs_element.options[i].innerHTML
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
        document.getElementById("user input").placeholder = input_text[event.target.innerHTML]

        if(file_inputs.includes(event.target.innerHTML)){
            document.getElementById("user input").hidden = true
            document.getElementById("file").hidden = false
        }
        else{
            document.getElementById("user input").hidden = false
            document.getElementById("file").hidden = true
        }
    })
}

document.getElementById("usage notes").innerHTML = usage_notes[document.getElementById("type").value]