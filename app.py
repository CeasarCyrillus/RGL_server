from flask import Flask

app = Flask("webapp")

@app.route("/")
def home():
    return "Hello World!"

if __name__ == "__main__":
    app.run("0.0.0.0")