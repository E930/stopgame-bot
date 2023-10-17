from main import types,cursor,bd
from parsers_sg import *


def klav_proverka(link):
    menu = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Первый спонсор", url=link[0][0])
    btn2 = types.InlineKeyboardButton("Второй спонсор", url=link[1][0])
    btn3 = types.InlineKeyboardButton("Проверить подписку", callback_data="proverka")
    menu.add(btn1, btn2, btn3)
    return menu

def start_kat():
    menu = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton("Игры", callback_data="igri_kat")
    btn2 = types.InlineKeyboardButton("Новости", callback_data="novosti_kat")
    btn3 = types.InlineKeyboardButton("Блоги", callback_data="blogi_kat")
    btn4 = types.InlineKeyboardButton("Статьи", callback_data="stati_kat")
    btn5 = types.InlineKeyboardButton("Видео", callback_data="video_kat")
    btn6 = types.InlineKeyboardButton("Читы", callback_data="chiti_kat")
    btn7 = types.InlineKeyboardButton("Помощь", callback_data="pomosh_kat")
    btn8 = types.InlineKeyboardButton("", callback_data="asd")
    menu.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return menu

def sg_novosti(text, stup):
    if stup == 1:
        len_ = len(text)
        if len_ >= 4:
            if len_ >= 9:
                inl_klav = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(f"{text[0]}", callback_data="nov1")
                btn2 = types.InlineKeyboardButton(f"{text[1]}", callback_data="nov2")
                btn3 = types.InlineKeyboardButton(f"{text[2]}", callback_data="nov3")
                btn4 = types.InlineKeyboardButton(f"{text[3]}", callback_data="nov4")
                btn5 = types.InlineKeyboardButton("", callback_data="nazad")
                btn6 = types.InlineKeyboardButton(">", callback_data="vpered")
                btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
                inl_klav.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
                return inl_klav, "Ступень 1/3"
            elif len_ <= 8:
                inl_klav = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(f"{text[0]}", callback_data="nov1")
                btn2 = types.InlineKeyboardButton(f"{text[1]}", callback_data="nov2")
                btn3 = types.InlineKeyboardButton(f"{text[2]}", callback_data="nov3")
                btn4 = types.InlineKeyboardButton(f"{text[3]}", callback_data="nov4")
                btn5 = types.InlineKeyboardButton("", callback_data="nazad")
                btn6 = types.InlineKeyboardButton(">", callback_data="vpered")
                btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
                inl_klav.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
                return inl_klav, "Ступень 1/2"
        elif len_ == 3:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[0]}", callback_data="nov1")
            btn2 = types.InlineKeyboardButton(f"{text[1]}", callback_data="nov2")
            btn3 = types.InlineKeyboardButton(f"{text[2]}", callback_data="nov3")
            btn5 = types.InlineKeyboardButton("", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn2, btn3, btn5, btn7)
            return inl_klav, "Ступень 1/1"
        elif len_ == 2:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[0]}", callback_data="nov1")
            btn2 = types.InlineKeyboardButton(f"{text[1]}", callback_data="nov2")
            btn5 = types.InlineKeyboardButton("", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn2, btn5, btn7)
            return inl_klav, "Ступень 1/1"
        elif len_ == 1:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[0]}", callback_data="nov1")
            btn5 = types.InlineKeyboardButton("", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn5, btn7)
            return inl_klav, "Ступень 1/1"
        elif len_ == 0:
            inl_klav = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1)
            return inl_klav, "Статей не найдено"

    elif stup == 2:
        len_ = len(text) - 4
        if len_ >= 4:
            if len_ >= 5:
                inl_klav = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(f"{text[4]}", callback_data="nov1")
                btn2 = types.InlineKeyboardButton(f"{text[5]}", callback_data="nov2")
                btn3 = types.InlineKeyboardButton(f"{text[6]}", callback_data="nov3")
                btn4 = types.InlineKeyboardButton(f"{text[7]}", callback_data="nov4")
                btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
                btn6 = types.InlineKeyboardButton(">", callback_data="vpered")
                btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
                inl_klav.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
                return inl_klav, "Ступень 2/3"
            elif len_ == 4:
                inl_klav = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(f"{text[4]}", callback_data="nov1")
                btn2 = types.InlineKeyboardButton(f"{text[5]}", callback_data="nov2")
                btn3 = types.InlineKeyboardButton(f"{text[6]}", callback_data="nov3")
                btn4 = types.InlineKeyboardButton(f"{text[7]}", callback_data="nov4")
                btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
                btn6 = types.InlineKeyboardButton("", callback_data="wera")
                btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
                inl_klav.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
                return inl_klav, "Ступень 2/2"
        elif len_ == 3:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[4]}", callback_data="nov1")
            btn2 = types.InlineKeyboardButton(f"{text[5]}", callback_data="nov2")
            btn3 = types.InlineKeyboardButton(f"{text[6]}", callback_data="nov3")
            btn8 = types.InlineKeyboardButton("", callback_data="qwe2")
            btn4 = types.InlineKeyboardButton("", callback_data="qwe")
            btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn2, btn3, btn4, btn5, btn8, btn7)
            return inl_klav, "Ступень 2/2"
        elif len_ == 2:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[4]}", callback_data="nov1")
            btn2 = types.InlineKeyboardButton(f"{text[5]}", callback_data="nov2")
            btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn2, btn5, btn7)
            return inl_klav, "Ступень 2/2"
        elif len_ == 1:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[4]}", callback_data="nov1")
            btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn5, btn7)
            return inl_klav, "Ступень 2/2"
    elif stup == 3:
        len_ = len(text) - 8
        if len_ >= 4:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[8]}", callback_data="nov1")
            btn2 = types.InlineKeyboardButton(f"{text[9]}", callback_data="nov2")
            btn3 = types.InlineKeyboardButton(f"{text[10]}", callback_data="nov3")
            btn4 = types.InlineKeyboardButton(f"{text[11]}", callback_data="nov4")
            btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
            btn6 = types.InlineKeyboardButton("", callback_data="vpered")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
            return inl_klav, "Ступень 3/3"
        elif len_ == 3:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[8]}", callback_data="nov1")
            btn2 = types.InlineKeyboardButton(f"{text[9]}", callback_data="nov2")
            btn3 = types.InlineKeyboardButton(f"{text[10]}", callback_data="nov3")
            btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
            btn6 = types.InlineKeyboardButton("", callback_data="vpered")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn2, btn3, btn5, btn6, btn7)
            return inl_klav, "Ступень 3/3"
        elif len_ == 2:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[8]}", callback_data="nov1")
            btn2 = types.InlineKeyboardButton(f"{text[9]}", callback_data="nov2")
            btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn2, btn5, btn7)
            return inl_klav, "Ступень 3/3"
        elif len_ == 1:
            inl_klav = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton(f"{text[8]}", callback_data="nov1")
            btn5 = types.InlineKeyboardButton("<", callback_data="nazad")
            btn7 = types.InlineKeyboardButton("В выбор категорий", callback_data="nazad_v_kat")
            inl_klav.add(btn1, btn5, btn7)
            return inl_klav, "Ступень 3/3"
