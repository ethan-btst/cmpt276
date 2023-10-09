from flask import Flask
from flask import *
from chat_request import text_request
from chat_request import youtube_request

app = Flask(__name__)

@app.route("/",methods=("GET","POST"))
def chat():
    if request.method == "POST":
        user_in = request.form["chatbox"]

        if(request.form["type"] == "youtube"):
            response = youtube_request(user_in)
        
        else:
            response = text_request(user_in)
        return redirect(url_for("chat",result=response))

    result = request.args.get("result")
    return render_template("chat.html", result=result)