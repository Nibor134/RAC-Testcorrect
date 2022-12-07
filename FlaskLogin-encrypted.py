# Import the necessary modules
from flask import Flask, request, render_template
from bcrypt import hashpw, checkpw

# Create a new Flask app
app = Flask(__name__)

# Create a database of users and their hashed passwords
users = {
    "user1": hashpw("password1".encode("utf-8"), b"$2b$12$zJcZRVv9F0fZGj1rOcDPJe"),
    "user2": hashpw("password2".encode("utf-8"), b"$2b$12$zJcZRVv9F0fZGj1rOcDPJe"),
    "user3": hashpw("password3".encode("utf-8"), b"$2b$12$zJcZRVv9F0fZGj1rOcDPJe")
}

# Define a route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get the username and password from the form
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")

        # Check if the username and password are correct
        if username in users and checkpw(password, users[username]):
            # Login was successful
            return "Login successful!"
        else:
            # Login failed
            return "Invalid username or password!"
    else:
        # Show the login form
        return render_template("login.html")

# Start the app
if __name__ == "__main__":
    app.run()
