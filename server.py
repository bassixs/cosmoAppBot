from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players 
                 (user_id TEXT PRIMARY KEY, score INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/tap', methods=['POST'])
def tap():
    data = request.json
    user_id = data['user_id']

    conn = sqlite3.connect('game.db')
    c = conn.cursor()

    # Проверяем, есть ли пользователь в базе
    c.execute("SELECT score FROM players WHERE user_id = ?", (user_id,))
    result = c.fetchone()

    if result:
        # Обновляем счёт
        new_score = result[0] + 1
        c.execute("UPDATE players SET score = ? WHERE user_id = ?", (new_score, user_id))
    else:
        # Добавляем нового игрока
        c.execute("INSERT INTO players (user_id, score) VALUES (?, 1)", (user_id,))

    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/score', methods=['POST'])
def get_score():
    data = request.json
    user_id = data['user_id']
    
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT score FROM players WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    
    score = result[0] if result else 0
    return jsonify({"score": score})

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000)