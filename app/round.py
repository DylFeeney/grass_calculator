from flask import request, render_template, Blueprint
from mongo import Mongo
import json

round_entry = Blueprint('round_entry', __name__, template_folder='templates')


@round_entry.route('/round-entry', methods=['POST', 'GET'])
def round_entry_page():
    client = Mongo()
    round_number = client.retrieve_round_number("game_1")
    if request.method == 'POST':
        formatted_form_data = get_request_form_values(request)
        process_round(round_number, formatted_form_data)

    player_list = client.list_players("game_1", "players")
    return render_template('round.html', round=round_number, player_names=player_list,
                           number_of_players=len(player_list))


def process_round(round_number, input_data):
    #write_raw_input_to_db(input_data)
    #calculate_net_profit()
    #calculate_penalties()
    #calculate_best_peddle()
    #calculate_bonus()
    #write_processed_input_to_db()
    #update_round_number()


def get_request_form_values(incoming_request):
    user_name = incoming_request.form.getlist('user_name')
    protected_peddle = incoming_request.form.getlist('protected_peddle')
    unprotected_peddle = incoming_request.form.getlist('unprotected_peddle')
    highest_peddle_in_hand = incoming_request.form.getlist('highest_peddle_in_hand')
    has_banker = process_checkbox_list(incoming_request.form.getlist('has_banker'))
    has_sold_out = process_checkbox_list(incoming_request.form.getlist('has_sold_out'))
    has_double_crossed = process_checkbox_list(incoming_request.form.getlist('has_double_crossed'))
    has_utterly_wiped_out = process_checkbox_list(incoming_request.form.getlist('has_utterly_wiped_out'))

    data = format_request_input(user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand, has_banker,
                                has_sold_out, has_double_crossed, has_utterly_wiped_out)

    return data


def format_request_input(user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand, has_banker,
                         has_sold_out, has_double_crossed, has_utterly_wiped_out):
    data = [{'name': a, 'protected_peddle': b, 'unprotected_peddle': c, 'highest_peddle_in_hand': d,
             'has_banker': e, 'has_sold_out': f, 'has_double_crossed': g, 'has_utterly_wiped_out': h} for
            a, b, c, d, e, f, g, h in
            zip(user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand, has_banker, has_sold_out,
                has_double_crossed, has_utterly_wiped_out)]
    return data


def process_checkbox_list(input_list):
    """
    This function will validate the checkbox values that are input from the webpage
    If a checkbox is not ticked a '0' is inputted.
    If a checkbox is ticket a '0' is inputted followed by a '1'.
    Because a '0' & a '1' are inputted we need to remove the 0 and keep the 1.
    Example
    Two inputs - 0,0,1
    Input one = 0 (Not checked)
    Input two = 0,1 (Checked) - We need to remove the 0 from here
    Expected output - 0,1
    Example
    Two inputs - 0,1,0,1
    Input one = 0,1 (Checked) - We need to remove the 0 from here
    Input two = 0,1 (Checked) - We need to remove the 0 from here
    Expected output - 1,1
    Example
    Two inputs - 0,1,0
    Input one = 0,1 (Checked) - We need to remove the 0 from here
    Input two = 0 (Not checked)
    Expected output - 1,0
    """
    list_length = len(input_list)
    skip_until = -1
    updated_list = []
    # Loop over the list of checkbox inputs
    for i in range(list_length):
        # Ensure the loop does not run out of bounds
        if (i + 1) < list_length:
            # Skip the next value
            if i <= skip_until:
                continue
            else:
                current_value = input_list[i]
                next_value = input_list[i + 1]
                if current_value == '0' and next_value == '1':
                    updated_list.append('1')
                    if i + 1 < list_length:
                        # Skip the next index to ensure when we get an input of 0,1 (checked box)
                        skip_until = i + 1
                else:
                    updated_list.append('0')
        elif (i + 1) == list_length:
            if i <= skip_until:
                continue
            else:
                updated_list.append(input_list[i])
    return updated_list
