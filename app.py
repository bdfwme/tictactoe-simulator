from flask import Flask, render_template, jsonify, request
import random
import string

app = Flask(__name__)

# GLOBAL STORAGE (In a real app, use a database. For school, this is fine.)
# Structure: {'room_code': {'board': [...], 'turn': 'X', 'players': 0}}
games = {}

def check_winner(board):
    # Winning combinations (rows, cols, diagonals)
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None

def computer_move(board):
    # Simple AI: Try to win, otherwise pick random
    available = [i for i, x in enumerate(board) if x == ""]
    if available:
        return random.choice(available)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    mode = request.json.get('mode') # 'pvc' or 'pvp'
    room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    games[room_id] = {
        'board': [""] * 9,
        'turn': 'X',
        'mode': mode,
        'winner': None
    }
    return jsonify({'room_id': room_id})

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    room_id = data['room_id']
    index = data['index']
    player = data['player'] # 'X' or 'O'
    
    if room_id not in games:
        return jsonify({'error': 'Game not found'}), 404
        
    game = games[room_id]
    
    # Validation
    if game['winner'] or game['board'][index] != "" or game['turn'] != player:
        return jsonify({'status': 'invalid'})

    # Make Move
    game['board'][index] = player
    
    # Check Win
    game['winner'] = check_winner(game['board'])
    
    # Switch Turn
    game['turn'] = 'O' if player == 'X' else 'X'

    # If Computer Mode and Game Active, Computer plays immediately
    if game['mode'] == 'pvc' and not game['winner'] and game['turn'] == 'O':
        comp_idx = computer_move(game['board'])
        if comp_idx is not None:
            game['board'][comp_idx] = 'O'
            game['winner'] = check_winner(game['board'])
            game['turn'] = 'X'

    return jsonify({'status': 'success', 'board': game['board'], 'winner': game['winner'], 'turn': game['turn']})

@app.route('/status/<room_id>')
def status(room_id):
    if room_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(games[room_id])

if __name__ == '__main__':
    app.run(debug=True)

    @app.route('/reset', methods=['POST'])
def reset():
    data = request.json
    room_id = data['room_id']
    
    if room_id in games:
        games[room_id]['board'] = [""] * 9  # Wipe the board
        games[room_id]['winner'] = None      # Clear the winner
        games[room_id]['turn'] = 'X'         # X always starts new game
        return jsonify({'status': 'success'})
    
    return jsonify({'error': 'Room not found'}), 404