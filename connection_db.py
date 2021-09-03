import const
import sqlite3

from manipulacao_json import dict_to_binary


class Database:
    def __init__(self, file):
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def create_player(self, _id, name, breed, classe, years, link_img):
        self.cursor.execute('INSERT OR IGNORE INTO jogador (id, name, breed, classe, years, link_img, exp, level,'
                            'helmet, armor, legs, boots, shield, weapon, backpack, gold, inventory, health, mana, skill)'
                            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (_id, name, breed, classe, years, link_img, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8,
                             dict_to_binary([]), 500, 300, 1))
        self.conn.commit()

    def consult_player(self, _id):
        self.cursor.execute('SELECT name, breed, classe, years, link_img, exp, level, helmet, armor, legs, boots, '
                            'shield, weapon, backpack, gold, inventory, health, mana, skill FROM jogador WHERE id=?', (_id,))
        consulta = self.cursor.fetchone()
        return consulta

    def consult_set(self, _id):
        self.cursor.execute('SELECT helmet, armor, legs, boots, shield, weapon, backpack, gold '
                            'FROM jogador WHERE id=?', (_id,))
        consulta = self.cursor.fetchone()
        return consulta

    def update_inventory(self, _id, inventory):
        self.cursor.execute('UPDATE jogador SET inventory=? WHERE id=?', (dict_to_binary(inventory), _id))
        self.conn.commit()

    def update_set(self, _id, item_type, item):
        self.cursor.execute(f'UPDATE jogador SET {item_type}=? WHERE id=?', (item, _id))
        self.conn.commit()

    def delete_player(self, _id):
        self.cursor.execute('DELETE FROM jogador WHERE id=?', (_id,))
        self.conn.commit()

    def update_level_player(self, _id, exp, level, health, mana, skill):
        self.cursor.execute('UPDATE jogador SET exp=?, level=?, health=?, mana=?, skill=? WHERE id=?',
                            (exp, level, health, mana, skill, _id))
        self.conn.commit()


database = Database(const.DB)
