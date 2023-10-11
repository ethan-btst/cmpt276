from flask import Flask
from flask import *
from chat_request import text_request
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Homepage, redirects to login page
@app.route('/')
def index():
    return render_template('login.html')

# Login page
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

# Admin page
@app.route('/admin')
def admin():
    if session['username'] == 'admin':
        return render_template('admin.html')
    return redirect(url_for('/'))

# 404 error page
@app.errorhandler(404)
def notfound(e):
    return render_template("404.html")

# Page for chat
@app.route('/chat',methods=("GET","POST"))
def chat():

    # Redirect if not logged in
    if 'username' not in session:
        return redirect("login")

    # Set a default empty response
    if 'current_response' not in session:
        session["current_response"] = '' 

    # Processes chat request
    if request.method == "POST":
        user_in = request.form["chatbox"]
        type = request.form["type"]
        api_key = request.form["api_key"]

        session["current_response"] = text_request(user_in,type,api_key)
        return redirect(request.path)

    # Display result to page
    if request.method == "GET":
        return render_template("chat.html",result=session['current_response'],userResponse=session['username'])

    return render_template("chat.html", userResponse=session['username'])