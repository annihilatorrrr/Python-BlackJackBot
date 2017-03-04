# -*- coding: utf-8 -*-
import os
import sqlite3

__author__ = 'Rico'


class DBwrapper(object):
    class __DBwrapper(object):
        dir_path = os.path.dirname(os.path.abspath(__file__))

        def __init__(self):
            self.connection = sqlite3.connect(self.dir_path + "\\users.db")
            self.connection.text_factory = lambda x: str(x, 'utf-8', "ignore")
            self.cursor = self.connection.cursor()

        def get_user(self, user_id):
            self.cursor.execute("SELECT * FROM users WHERE userID=?;", [str(user_id)])

            result = self.cursor.fetchall()
            if len(result) > 0:
                return result[0]
            else:
                return []

        def get_all_users(self):
            self.cursor.execute("SELECT rowid, * FROM users;")
            all_users = self.cursor.fetchall()
            return all_users

        def write(self, user_id, lang_id, first_name, last_name):
            self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?);", (str(user_id), str(lang_id), str(first_name), str(last_name), "male", "0", "0"))
            self.connection.commit()

        def insert(self, column_name, value, user_id):
            self.cursor.execute("UPDATE users SET " + str(column_name) + "= ? WHERE userID = ?;",
                                [str(value), str(user_id)])
            self.connection.commit()

        def check_if_user_saved(self, user_id):
            self.cursor.execute("SELECT rowid, * FROM users WHERE userID=?;", [str(user_id)])

            result = self.cursor.fetchall()
            if len(result) > 0:
                return result[0]
            else:
                return -1

        def user_data_changed(self, user_id, first_name, last_name, username):
            self.cursor.execute("SELECT * FROM users WHERE userID=?;", [str(user_id)])

            result = self.cursor.fetchone()

            if result[2] == first_name and result[3] == last_name and result[4] == username:
                return False
            return True

        def update_user_data(self, user_id, first_name, last_name, username):
            self.cursor.execute("UPDATE users SET first_name=?, last_name=?, username=? WHERE userID=?;", (str(first_name), str(last_name), str(username), str(user_id)))
            self.connection.commit()

        def reset_stats(self, user_id):
            self.cursor.execute("UPDATE users SET gamesPlayed='0', gamesWon='0', gamesTie='0', lastPlayed='0' WHERE userID=?;", [str(user_id)])
            self.connection.commit()

        def close_conn(self):
            self.connection.close()

    instance = None

    def __init__(self):
        if not DBwrapper.instance:
            DBwrapper.instance = DBwrapper.__DBwrapper()

    @staticmethod
    def get_instance():
        if not DBwrapper.instance:
            DBwrapper.instance = DBwrapper.__DBwrapper()

        return DBwrapper.instance
