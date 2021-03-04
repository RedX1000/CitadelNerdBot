from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
import sqlite3

CREATE_PLAYER_TABLE = """CREATE TABLE IF NOT EXISTS Players(
                                        players_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        players_name VARCHAR(12),
                                        players_rank INTEGER,
                                        players_xp INTEGER,
                                        players_kills INTEGER,
                                        players_citadel INTEGER )
                      """
#todo: Consider adding a date.

INSERT_PLAYERS_BULK = """INSERT INTO Players(players_name, players_rank, 
                                     players_xp, players_kills, players_visited, 
                                     players_capped) VALUES(?, ?, ?, ?, ?)"""

GET_ALL_PLAYERS = "SELECT * FROM Players"

GET_ALL_PLAYERS_ALPHABETICAL = "SELECT * FROM Players ORDER BY players_name COLLATE NOCASE ASC"

GET_ALL_PLAYERS_ORDER_RANK = "SELECT * FROM Players ORDER BY players_rank DESC, players_name COLLATE NOCASE ASC"

GET_ALL_PLAYERS_CITADEL = "SELECT * FROM Players WHERE players_citadel > 0 ORDER BY players_name DESC"

GET_PLAYER_BY_NAME = "SELECT * FROM Players WHERE players_name = ? COLLATE NOCASE"

GET_ROW_COUNT = "SELECT COUNT(*) FROM Players"

DELETE_WITH_NAME = "DELETE FROM Players WHERE players_name = ? COLLATE NOCASE"

DELETE_WITH_ID = "DELETE FROM Players WHERE players_id = ?"



def connect():
    return sqlite3.connect('players.db')

def create_tables(conn):
    with conn:
        conn.execute(CREATE_PLAYER_TABLE)

def fill_database(conn, name, rank, xp, kills):
    nameGrab = conn.execute("SELECT players_name FROM players WHERE players_name = "+"'"+name+"'").fetchall()
    check = False
    print("about to fill database")
    try:
        print("first try")
        try:
            print("second try")
            compareName = nameGrab[0][0]
            check = True
        except:
            print("second exception")
            with conn:
                print("about to execute...")
                print(name, rank, xp, kills, 0)
                conn.execute(INSERT_PLAYERS_BULK, (name, rank, xp, kills, 0))
                print("executed")
                check = False
        if check == True:
            print("first if")
            if compareName == name:
                print("second if")
                pass
            else:
                print("second else")
                with conn:
                    conn.execute(INSERT_PLAYERS_BULK, (name, rank, xp, kills, 0))
        else:
            print("first else")
            pass

    except Exception:
        print("first exception")
        pass


def get_players(conn, command):
    with conn:
        if command == "id":
            return conn.execute(GET_ALL_PLAYERS).fetchall()
        elif command == "alpha":
            return conn.execute(GET_ALL_PLAYERS_ALPHABETICAL).fetchall()
        elif command == "rank":
            return conn.execute(GET_ALL_PLAYERS_ORDER_RANK).fetchall()
        elif command == "citadel":
            return conn.execute(GET_ALL_PLAYERS_CITADEL).fetchall()
        else:
            return "State clanlist order: $clanlist <id|alpha|rank|citadel>"

def drop_table(conn):
    with conn:
        conn.execute("DROP TABLE IF EXISTS Players")

def get_player_by_name(conn, name):
    with conn:
        return conn.execute(GET_PLAYER_BY_NAME, (name,)).fetchall()

def get_all_players_alphabetical(conn):
    with conn:
        return conn.execute(GET_ALL_PLAYERS_ALPHABETICAL).fetchall()

def remove_player_by_name(conn, name):
    with conn:
        conn.execute(DELETE_WITH_NAME, (name, ))

def remove_player_by_id(conn, id):
    with conn:
        conn.execute(DELETE_WITH_ID, (id, ))

def get_row_count(conn):
    with conn:
        return conn.execute(GET_ROW_COUNT).fetchall()
