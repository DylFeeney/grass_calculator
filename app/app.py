from flask import Flask, render_template

from players import players

app = Flask(__name__)
app.register_blueprint(players)

@app.route("/")
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
