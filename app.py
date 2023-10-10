from flask import Flask
from flask import *
from chat_request import text_request
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/chat',methods=("GET","POST"))
def chat():
    if request.method == "POST":
        user_in = request.form["chatbox"]
        type = request.form["type"]
        api_key = request.form["api_key"]

        response = text_request(user_in,type,api_key)
        return redirect(url_for("chat",result=response))

    result = request.args.get("result")
    return render_template("chat.html", result=result, userResponse=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle the login form submission
        username = request.form['username']
        # Perform authentication and validation here
        # Redirect to a new page on successful login
        session['username'] = username
        if (username == 'admin'):
            return redirect(url_for('admin'))
        return redirect(url_for('chat'))

    # Render the login page for GET requests
    return render_template('login.html')

@app.route('/admin')
def admin():
    if session['username'] == 'admin':
        return render_template('admin.html')
    return redirect(url_for('/'))
