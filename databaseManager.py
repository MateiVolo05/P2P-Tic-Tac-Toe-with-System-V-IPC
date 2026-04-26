import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="gameHistory.db"):
        self.db_path = db_path
        self.initDb()

    def initDb(self):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS GAMES (id INTEGER PRIMARY KEY AUTOINCREMENT, player1 VARCHAR(100) NOT NULL, player2 VARCHAR(100) NOT NULL, p1_score INTEGER NOT NULL, p2_score INTEGER NOT NULL, lastPlayed VARCHAR(100))''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS PLAYERS (name VARCHAR(100) PRIMARY KEY)''')
            db.commit()
            cursor.close()

    def getScore(self, player1, player2):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute('''SELECT id, p1_score, p2_score, player1, player2, lastPlayed FROM GAMES WHERE (player1 = ? AND player2 = ?) OR (player1 = ? AND player2 = ?) ''', (player1, player2, player2, player1))
            data = cursor.fetchone()
            cursor.close()
            if data:
                return (data[0], data[1], data[2], data[3], data[4], data[5])
            else:
                return (None, None, None, None, None, None)

    def saveScore(self, player1, player2, score):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            id, p1_score, p2_score, player1db, player2db, _ = self.getScore(player1, player2)
            if id==None:
                cursor.execute('''INSERT INTO GAMES(player1, player2, p1_score, p2_score, lastPlayed) VALUES (?, ?, ?, ?, ?)''', (player1, player2, 1 if score==1 else 0, 1 if score==2 else 0, now))
                db.commit()
            else:
                winner = player1 if score==1 else (player2 if score==2 else None)
                if winner:
                    if winner == player1db:
                        p1_score += 1
                    else:
                        p2_score += 1
                cursor.execute('''UPDATE GAMES SET p1_score = ?, p2_score = ?, lastPlayed = ? WHERE id = ?''', (p1_score, p2_score, now, id))
                db.commit()
            cursor.execute('''INSERT OR IGNORE INTO PLAYERS (name) VALUES (?)''', (player1, ))
            cursor.execute('''INSERT OR IGNORE INTO PLAYERS (name) VALUES (?)''', (player2, ))
            db.commit()
            cursor.close()
