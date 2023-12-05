from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_pymongo import PyMongo
from openai import OpenAI
from authlib.integrations.flask_client import OAuth

client = OpenAI(
    api_key=process.env.OPENAI_API_KEY
)

app = Flask(__name__)
app.config["MONGO_URI"] = proccess.env.MONGO_URI
mongo = PyMongo(app)

# Authlib configuration for Google OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=proccess.env.GOOGLE_CLIENT_ID,
    client_secret=proccess.env.GOOGLE_CLIENT_SECRET,
    authorize_url=proccess.env.GOOGLE_AUTHORIZE_URL,
    authorize_params=None,
    access_token_url=proccess.env.GOOGLE_ACCESS_TOKEN_URL,
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=proccess.env.GOOGLE_REDIRECT_URI,
    client_kwargs={'scope': proccess.env.GOOGLE_CLIENT_SCOPE},
)

@app.route("/")
def index():
    chats = mongo.db.chats.find({}).sort("datefield", -1).limit(10)
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", myChats=myChats)
    #return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle sign-up logic here
        username = request.form["username"]
        password = request.form["password"]


        # If sign-up is successful, redirect to index.html
        return redirect(url_for("home"))

    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Handle sign-in logic here, for example, check username and password
        # If sign-in is successful, store user information in session
        session["user"] = {"username": request.form["username"]}  # Replace with your user data
        return redirect(url_for("home"))

    return render_template("signin.html")

#return redirect(url_for("index"))
#if "user" in session:
@app.route("/home")
def home():
     # User is signed in, proceed to index.html
    chats = mongo.db.chats.find({}).sort("datefield", -1).limit(10)
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", myChats=myChats)

    # If user is not signed in, redirect to signup
    

@app.route("/api", methods=["POST"])
def qna():
    if request.method == "POST":
        print(request.json)
        data = {"result": "Thank you I am just learning"}
        selected_model = request.json.get("model")

        if request.json.get("voiceInput"):
             # Handle voice input
            voice_input = request.json.get("voiceInput")
            question = voice_input

        else:
            question = request.json.get("question")

        messages = [
            {"role": "user", "content": question},
        ]

        response = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print(response)
        answer = response.choices[0].message.content

        data = {"question": question, "answer": answer}
        mongo.db.chats.insert_one({"question": question, "answer": answer})

        return jsonify(data)

    data = {"result": "Thank you! I'm just a machine learning model designed to respond to questions and generate text based on my training data. Is there anything specific you'd like to ask or discuss? "}
    return jsonify(data)

@app.route("/signout")
def signout():
    # Clear user session to sign out
    session.pop("user", None)
    return redirect(url_for("signup"))

@app.route("/about.html")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

# app.run(debug=True)

  
