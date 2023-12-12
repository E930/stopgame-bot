import sqlite3
bd = sqlite3.connect("bd_pars_sg.db")
cursor = bd.cursor()


def zapis_kat(user_id,kat):
    user_kat = cursor.execute("SELECT `kategoria` FROM `kategorii` WHERE `user_id` =?",(user_id,)).fetchall()
    if len(user_kat) == 0:
        cursor.execute("INSERT OR IGNORE INTO `kategorii` (`kategoria`,`user_id`) VALUES (?,?)", (1, user_id,))
        bd.commit()
    else:
        cursor.execute("UPDATE `kategorii` SET `kategoria` =? WHERE `user_id` =?", (kat, user_id))
        bd.commit()


def zapros(text,user_id):
    cursor.execute("UPDATE `kategorii` SET `zapros` =? WHERE `user_id` =?",(text,user_id,))
    bd.commit()
    user_kat = cursor.execute("SELECT `kategoria`, `stup` FROM `kategorii` WHERE `user_id` =?",(user_id,)).fetchall()
    otvet = f"https://stopgame.ru/search?s={text}&where={user_kat[0][0]}"
    return otvet, user_kat[0][1]

def user_zapros(user_id):
    zapros_user = cursor.execute("SELECT `zapros` FROM `kategorii` WHERE `user_id` =?",(user_id,)).fetchall()[0][0]
    return zapros_user

def stup_vpered(user_id):
    user_stup = cursor.execute("SELECT `stup` FROM `kategorii` WHERE `user_id` =?", (user_id,)).fetchall()
    if user_stup[0][0] == 1:
        cursor.execute("UPDATE `kategorii` SET `stup` =? WHERE `user_id` =?", (2,user_id,))
        bd.commit()
    elif user_stup[0][0] == 2:
        cursor.execute("UPDATE `kategorii` SET `stup` =? WHERE `user_id` =?", (3,user_id,))
        bd.commit()

def stup_nazad(user_id):
    user_stup = cursor.execute("SELECT `stup` FROM `kategorii` WHERE `user_id` =?", (user_id,)).fetchall()
    if user_stup[0][0] == 3:
        cursor.execute("UPDATE `kategorii` SET `stup` =? WHERE `user_id` =?", (2,user_id,))
        bd.commit()
    elif user_stup[0][0] == 2:
        cursor.execute("UPDATE `kategorii` SET `stup` =? WHERE `user_id` =?", (1,user_id,))
        bd.commit()

def stup_obnulenie(user_id):
    cursor.execute("UPDATE `kategorii` SET `stup` =? WHERE `user_id` =?", (1,user_id,))
    bd.commit()

def zapis_links_v_bd(link,user_id,stup):
    if stup == 1:
        cursor.execute(
            "UPDATE `kategorii` SET `news_link1` =?, `news_link2`=?, `news_link3`=?, `news_link4` =? WHERE `user_id` =? ",
            (link[0], link[1], link[2], link[3], user_id,))
        bd.commit()
    elif stup == 2:
        cursor.execute(
            "UPDATE `kategorii` SET `news_link1` =?, `news_link2`=?, `news_link3`=?, `news_link4` =? WHERE `user_id` =? ",
            (link[4], link[5], link[6], link[7], user_id,))
        bd.commit()
    elif stup == 2:
        cursor.execute(
            "UPDATE `kategorii` SET `news_link1` =?, `news_link2`=?, `news_link3`=?, `news_link4` =? WHERE `user_id` =? ",
            (link[8], link[9], link[10], link[11], user_id,))
        bd.commit()

def select_link(user_id):
    link = cursor.execute("SELECT `news_link1`, `news_link2`, `news_link3`, `news_link4` FROM `kategorii` WHERE `user_id` =?",(user_id,)).fetchall()
    return link

def kat_novosti(user_id):
    kategoria = cursor.execute("SELECT `kategoria` FROM `kategorii` WHERE `user_id` =?", (user_id,)).fetchall()
    return kategoria[0][0]

# def zapis_obzor_id(user_id):
