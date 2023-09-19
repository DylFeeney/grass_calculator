from flask import Flask, render_template
from mongo import Mongo

from players import players
from round import round_entry

app = Flask(__name__)
app.register_blueprint(players)
app.register_blueprint(round_entry)

@app.route("/")
def hello_world():
    client = Mongo()
    database = "game_1"
    round_number = client.retrieve_round_number(database)
    if round_number > 1:
        players = client.get_score_info(database, "processed_round_info")
    else:
        players = []
    return render_template('index.html', round_number=round_number, players=players)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
