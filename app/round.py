from flask import request, render_template, Blueprint
from mongo import Mongo

round_entry = Blueprint('round_entry', __name__, template_folder='templates')

@round_entry.route('/round-entry', methods=['POST', 'GET'])
def round_entry_page():
    client = Mongo()
    round_number = client.retrieve_round_number("game_1")
    if request.method == 'POST':
        print("POST")

    player_list = client.list_players("game_1", "players")
    return render_template('round.html', round=round_number, player_names=player_list, number_of_players=len(player_list))

