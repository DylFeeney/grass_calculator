from flask import request, render_template, Blueprint
from mongo import Mongo
import json

players = Blueprint('players', __name__, template_folder='templates')

@players.route('/players', methods=['POST', 'GET'])
def players_page():
    client = mongo_setup()

    if request.method == 'POST':
        player_name = request.form.get('player')
        player_name = player_name.upper()
        client.insert_player_name("game_1", "players", player_name)

    player_list = client.list_players("game_1", "players")
    return render_template('player_info.html', players=player_list)

def mongo_setup():
    mongo = Mongo()
    return mongo
