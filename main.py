import logging
from math import ceil
from bd_sg import *
from aiogram import Bot,Dispatcher,executor,types
from config import TOKEN,link
import sqlite3
bd = sqlite3.connect("bd_pars_sg.db")
cursor = bd.cursor()
from bd_sg import *
from klav_sg import *
from parsers_sg import *
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode="html", disable_web_page_preview=True)
dp = Dispatcher(bot)



async def proverka(user_id):
    for i in link:
        chat = await bot.get_chat_member(chat_id=i[1], user_id=user_id)
        if chat.status == "left":
            return False
    return True

@dp.message_handler(commands=["start"])
async def start(message):
    if message.chat.type == "private":
        otvet = await proverka(message.from_user.id)
        if otvet == True:
            zapis_kat(message.from_user.id,1)
            await bot.send_message(message.chat.id,"Спасибо, что подписались на спонсоров \n Доступ к функционалу бота открыт",reply_markup=start_kat())
        else:
            await bot.send_message(message.chat.id, "Подпишитесь на спонсоров:", reply_markup=klav_proverka(link))


@dp.message_handler(content_types="text")
async def tekst(message):
    if message.chat.type == "private":
        if await proverka(message.from_user.id):
            text = message.text # забираем запрос пользователя
            otvet = zapros(text,message.from_user.id) # вызываем функцию для формирования ссылки и получение ступени пользователя
            otvet_parser = parser_sg(otvet[0]) # вызываем парсер и отправляем в него ссылку с функции на 39 строке
            otvet_klav = sg_novosti(otvet_parser[0],otvet[1]) # вызываем функцию для формирования кнопок,
                                                              # отправляем в неё список с названиями статьей с функции на 40 строчке
                                                              # и ступень с функции 39 строчки
            zapis_links_v_bd(otvet_parser[1],message.from_user.id,otvet[1])
            if otvet_klav[1] == "Статей не найдено":
                await bot.send_message(message.chat.id, otvet_klav[1], reply_markup=otvet_klav[0])
            else:
                await bot.send_message(message.chat.id,f"Ответы по запросу `{text}`\n{otvet_klav[1]}", reply_markup=otvet_klav[0])
        else:
            await bot.send_message(message.chat.id, "Подпишитесь на спонсоров:", reply_markup=klav_proverka(link))

@dp.callback_query_handler(lambda call:call.data)
async def call(call):
    user_id = call.from_user.id

    if call.data == "proverka":
        if call.message.chat.type == "private":
            if await proverka(call.from_user.id):
                await bot.send_message(call.message.chat.id,
                                       "Спасибо, что подписались на спонсоров \n Доступ к функционалу бота открыт")
                await bot.delete_message(call.message.chat.id,call.message.message_id)
            else:
                await bot.send_message(call.message.chat.id, "Подпишитесь на спонсоров:", reply_markup=klav_proverka(link))

    elif call.data == "nazad_v_kat":
        await bot.send_message(call.message.chat.id, "Выбор категорий", reply_markup=start_kat())
    elif call.data == "vpered":
        stup_vpered(call.from_user.id) # меняем ступень пользователя на следующую
        otvet_zapros = user_zapros(call.from_user.id) # вызываем функцию, которая вытаскивает запрос пользователя с бд
        otvet = zapros(otvet_zapros, call.from_user.id) # вызываем функцию для формирования ссылки и получение ступени пользователя
        otvet_parser = parser_sg(otvet[0]) # вызываем парсер и отправляем в него ссылку с функции на 66 строке
        otvet_klav = sg_novosti(otvet_parser[0], otvet[1]) # вызываем функцию для формирования кнопок,
                                                              # отправляем в неё список с названиями статьей с функции на 67 строчке
                                                              # и ступень с функции 66 строчки
        zapis_links_v_bd(otvet_parser[1], call.from_user.id, otvet[1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберите новость\n{otvet_klav[1]}", reply_markup=otvet_klav[0], parse_mode="html")

    elif call.data == "nazad":
        stup_nazad(call.from_user.id) # меняем ступень пользователя на предыдущую
        otvet_zapros = user_zapros(call.from_user.id) # вызываем функцию, которая вытаскивает запрос пользователя с бд
        otvet = zapros(otvet_zapros, call.from_user.id) # вызываем функцию для формирования ссылки и получение ступени пользователя
        otvet_parser = parser_sg(otvet[0]) # вызываем парсер и отправляем в него ссылку с функции на 76 строке
        otvet_klav = sg_novosti(otvet_parser[0], otvet[1]) # вызываем функцию для формирования кнопок,
                                                              # отправляем в неё список с названиями статьей с функции на 77 строчке
                                                              # и ступень с функции 76 строчки
        zapis_links_v_bd(otvet_parser[1], call.from_user.id, otvet[1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберите новость\n{otvet_klav[1]}", reply_markup=otvet_klav[0], parse_mode="html")


    elif call.data == "nov1":
        zapis_obzor_id = cursor.execute("UPDATE `kategorii` SET `obzor_id` =? WHERE `user_id` =?", (1,user_id))
        bd.commit()
        x = 0
        link_ = select_link(call.from_user.id)[0][0]
        kategorii_nov = kat_novosti(user_id)
        if kategorii_nov == "news" or kategorii_nov == "blogs" or kategorii_nov == "articles":
            novost = parser_sg_novosti(link_)
            kolvo_sym = ceil(len(novost[1])/3500)
            for i in range(kolvo_sym):
                if i == 0:
                    await bot.send_message(call.message.chat.id, novost[0] + "\n\n" + novost[1][x:x+3500])
                    x += 3500
                else:
                    await bot.send_message(call.message.chat.id,novost[1][x:x+3500])
                    x += 3500

        elif kategorii_nov == "video":
            video_ = parser_sg_video(link_)
            await bot.send_message(call.message.chat.id, f"Ссылка на видео:\n{video_}", disable_web_page_preview=False)

        elif kategorii_nov == "faq":
            text = parser_sg_pomosh(link_)
            await bot.send_message(call.message.chat.id, f"Задаваемый вопрос:\n\n{text[0]}\n\nОтветы на вопрос:\n{text[1]}")

        elif kategorii_nov == "cheats":
            chiti = parser_sg_chiti_i_text(link_, user_id)
            if chiti[2] == "Есть файл":
                for i in range(1, chiti[0]):
                    if i == 1:
                        cheats = open(f"./{user_id}-Ваши-читы-{i}.zip", "rb")
                        await bot.send_message(call.message.chat.id, chiti[1])
                        await bot.send_document(call.message.chat.id, cheats)
                    else:
                        cheats = open(f"./{user_id}-Ваши-читы-{i}.zip", "rb")
                        await bot.send_document(call.message.chat.id, cheats)
            else:
                text = parser_sg_chiti_i_text(link_, user_id)
                for i in range(0,len(text[0]), 4000):
                    if i == 0:
                        await bot.send_message(call.message.chat.id, text[1] + "\n" + text[0][i:i + 4000])
                    else:
                        await bot.send_message(call.message.chat.id, text[0][i:i + 4000])

        elif kategorii_nov == "games":
            pokaz_obzor = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("Показать текстовый обзор", callback_data="pokaz_tekst")
            pokaz_obzor.add(btn1)
            novost = parser_sg_igri(link_)
            if len(novost[0]) != 0 and len(novost[1]) != 0 and len(novost[2]) != 0 and len(novost[3]) != 0 \
            and len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>",
                                           reply_markup=pokaz_obzor)
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                # ставим условие если есть миним. и реком. но нет видео и текстового обзоров
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                           f"<a href='{novost[6]}'>Видеообзор</a>", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n"
                                            , reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4])

    elif call.data == "nov2":
        zapis_obzor_id = cursor.execute("UPDATE `kategorii` SET `obzor_id` =? WHERE `user_id` =?", (1,user_id))
        bd.commit()
        x = 0
        link_ = select_link(call.from_user.id)[0][1]
        kategorii_nov = kat_novosti(user_id)
        if kategorii_nov == "news" or kategorii_nov == "blogs" or kategorii_nov == "articles":
            novost = parser_sg_novosti(link_)
            kolvo_sym = ceil(len(novost[1])/3500)
            for i in range(kolvo_sym):
                if i == 0:
                    await bot.send_message(call.message.chat.id, novost[0] + "\n\n" + novost[1][x:x+3500])
                    x += 3500
                else:
                    await bot.send_message(call.message.chat.id,novost[1][x:x+3500])
                    x += 3500

        elif kategorii_nov == "video":
            video_ = parser_sg_video(link_)
            await bot.send_message(call.message.chat.id, f"Ссылка на видео:\n{video_}", disable_web_page_preview=False)

        elif kategorii_nov == "faq":
            text = parser_sg_pomosh(link_)
            await bot.send_message(call.message.chat.id, f"Задаваемый вопрос:\n\n{text[0]}\n\nОтветы на вопрос:\n{text[1]}") #

        elif kategorii_nov == "cheats":
            chiti = parser_sg_chiti_i_text(link_, user_id)
            if chiti[2] == "Есть файл":
                for i in range(1, chiti[0]):
                    if i == 1:
                        cheats = open(f"./{user_id}-Ваши-читы-{i}.zip", "rb")
                        await bot.send_message(call.message.chat.id, chiti[1])
                        await bot.send_document(call.message.chat.id, cheats)
                    else:
                        cheats = open(f"./{user_id}-Ваши-читы-{i}.zip", "rb")
                        await bot.send_document(call.message.chat.id, cheats)
            else:
                text = parser_sg_chiti_i_text(link_, user_id)
                for i in range(0, len(text[0]), 4000):
                    if i == 0:
                        await bot.send_message(call.message.chat.id, text[1] + "\n" + text[0][i:i + 4000])
                    else:
                        await bot.send_message(call.message.chat.id, text[0][i:i + 4000])

        elif kategorii_nov == "games":
            pokaz_obzor = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("Показать текстовый обзор", callback_data="pokaz_tekst")
            pokaz_obzor.add(btn1)
            link_ = select_link(call.from_user.id)[0][1]
            novost = parser_sg_igri(link_)
            if len(novost[0]) != 0 and len(novost[1]) != 0 and len(novost[2]) != 0 and len(novost[3]) != 0 \
            and len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>",
                                           reply_markup=pokaz_obzor)
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                # ставим условие если есть миним. и реком. но нет видео и текстового обзоров
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                           f"<a href='{novost[6]}'>Видеообзор</a>", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n"
                                            , reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4])


    elif call.data == "nov3":
        zapis_obzor_id = cursor.execute("UPDATE `kategorii` SET `obzor_id` =? WHERE `user_id` =?", (1,user_id))
        bd.commit()
        x = 0
        link_ = select_link(call.from_user.id)[0][2]
        kategorii_nov = kat_novosti(user_id)
        if kategorii_nov == "news" or kategorii_nov == "blogs" or kategorii_nov == "articles":
            novost = parser_sg_novosti(link_)
            kolvo_sym = ceil(len(novost[1])/3500)
            for i in range(kolvo_sym):
                if i == 0:
                    await bot.send_message(call.message.chat.id, novost[0] + "\n\n" + novost[1][x:x+3500])
                    x += 3500
                else:
                    await bot.send_message(call.message.chat.id,novost[1][x:x+3500])
                    x += 3500

        elif kategorii_nov == "video":
            video_ = parser_sg_video(link_)
            await bot.send_message(call.message.chat.id, f"Ссылка на видео:\n{video_}", disable_web_page_preview=False)

        elif kategorii_nov == "faq":
            text = parser_sg_pomosh(link_)
            await bot.send_message(call.message.chat.id, f"Задаваемый вопрос:\n\n{text[0]}\n\nОтветы на вопрос:\n{text[1]}") #

        elif kategorii_nov == "cheats":
            chiti = parser_sg_chiti_i_text(link_, user_id)
            if chiti[2] == "Есть файл":
                for i in range(1, chiti[0]):
                    if i == 1:
                        cheats = open(f"./{user_id}-Ваши-читы-{i}.zip", "rb")
                        await bot.send_message(call.message.chat.id, chiti[1])
                        await bot.send_document(call.message.chat.id, cheats)
                    else:
                        cheats = open(f"./{user_id}-Ваши-читы-{i}.zip", "rb")
                        await bot.send_document(call.message.chat.id, cheats)
            else:
                text = parser_sg_chiti_i_text(link_, user_id)
                for i in range(0, len(text[0]), 4000):
                    if i == 0:
                        await bot.send_message(call.message.chat.id, text[1] + "\n" + text[0][i:i + 4000])
                    else:
                        await bot.send_message(call.message.chat.id, text[0][i:i + 4000])

        elif kategorii_nov == "games":
            pokaz_obzor = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("Показать текстовый обзор", callback_data="pokaz_tekst")
            pokaz_obzor.add(btn1)
            link_ = select_link(call.from_user.id)[0][2]
            novost = parser_sg_igri(link_)
            if len(novost[0]) != 0 and len(novost[1]) != 0 and len(novost[2]) != 0 and len(novost[3]) != 0 \
            and len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>",
                                           reply_markup=pokaz_obzor)
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                # ставим условие если есть миним. и реком. но нет видео и текстового обзоров
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                           f"<a href='{novost[6]}'>Видеообзор</a>", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n"
                                            , reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4])

    elif call.data == "nov4":
        zapis_obzor_id = cursor.execute("UPDATE `kategorii` SET `obzor_id` =? WHERE `user_id` =?", (1,user_id))
        bd.commit()
        x = 0
        link_ = select_link(call.from_user.id)[0][3]
        kategorii_nov = kat_novosti(user_id)
        if kategorii_nov == "news" or kategorii_nov == "blogs" or kategorii_nov == "articles":
            novost = parser_sg_novosti(link_)
            kolvo_sym = ceil(len(novost[1])/3500)
            for i in range(kolvo_sym):
                if i == 0:
                    await bot.send_message(call.message.chat.id, novost[0] + "\n\n" + novost[1][x:x+3500])
                    x += 3500
                else:
                    await bot.send_message(call.message.chat.id,novost[1][x:x+3500])
                    x += 3500

        elif kategorii_nov == "video":
            video_ = parser_sg_video(link_)
            await bot.send_message(call.message.chat.id, f"Ссылка на видео:\n{video_}", disable_web_page_preview=False)

        elif kategorii_nov == "faq":
            text = parser_sg_pomosh(link_)
            await bot.send_message(call.message.chat.id, f"Задаваемый вопрос:\n\n{text[0]}\n\nОтветы на вопрос:\n{text[1]}") #

        elif kategorii_nov == "cheats":
            chiti = parser_sg_chiti_i_text(link_, user_id)
            if chiti[2] == "Есть файл":
                for i in range(1, chiti[0]):
                    if i == 1:
                        cheats = open(f"./{user_id}: Ваши читы-{i}.zip", "rb")
                        await bot.send_message(call.message.chat.id, chiti[1])
                        await bot.send_document(call.message.chat.id, cheats)
                    else:
                        cheats = open(f"./{user_id}: Ваши читы-{i}.zip", "rb")
                        await bot.send_document(call.message.chat.id, cheats)
            else:
                text = parser_sg_chiti_i_text(link_, user_id)
                for i in range(0, len(text[0]), 4000):
                    if i == 0:
                        await bot.send_message(call.message.chat.id, text[1] + "\n" + text[0][i:i + 4000])
                    else:
                        await bot.send_message(call.message.chat.id, text[0][i:i + 4000])

        elif kategorii_nov == "games":
            pokaz_obzor = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("Показать текстовый обзор", callback_data="pokaz_tekst")
            pokaz_obzor.add(btn1)
            link_ = select_link(call.from_user.id)[0][3]
            novost = parser_sg_igri(link_)
            if len(novost[0]) != 0 and len(novost[1]) != 0 and len(novost[2]) != 0 and len(novost[3]) != 0 \
            and len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>",
                                           reply_markup=pokaz_obzor)
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                # ставим условие если есть миним. и реком. но нет видео и текстового обзоров
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n" + f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) != 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4] + "\n" + "Рекомендуемые: \n" + novost[5] + "\n", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                           f"<a href='{novost[6]}'>Видеообзор</a>", reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) != 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n"
                                            , reply_markup=pokaz_obzor)
            elif len(novost[4]) == 0 and len(novost[5]) == 0 and len(novost[6]) != 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            f"<a href='{novost[6]}'>Видеообзор</a>")
            elif len(novost[4]) != 0 and len(novost[5]) == 0 and len(novost[6]) == 0 and len(novost[7]) == 0:
                await bot.send_message(call.message.chat.id, "Название Игры: " + f"<i>{novost[0]}</i>" + "\n\n" + "Дата Выхода: " + novost[2] +
                                           "\n" + "Жанры: " + novost[1] + "\n" + "Платформы: " + novost[3] + "\n\n" +
                                            "Минимальные: \n" + novost[4])

    elif call.data == "igri_kat":
        zapis_kat(user_id,"games")
        stup_obnulenie(user_id)
        await bot.send_message(call.message.chat.id, "Выбрана категория: Игры")
    elif call.data == "novosti_kat":
        zapis_kat(user_id,"news")
        stup_obnulenie(user_id)
        await bot.send_message(call.message.chat.id, "Выбрана категория: Новости")
    elif call.data == "blogi_kat":
        zapis_kat(user_id,"blogs")
        stup_obnulenie(user_id)
        await bot.send_message(call.message.chat.id, "Выбрана категория: Блоги")
    elif call.data == "stati_kat":
        zapis_kat(user_id,"articles")
        stup_obnulenie(user_id)
        await bot.send_message(call.message.chat.id, "Выбрана категория: Статьи")
    elif call.data == "video_kat":
        zapis_kat(user_id,"video")
        stup_obnulenie(user_id)
        await bot.send_message(call.message.chat.id, "Выбрана категория: Видео")
    elif call.data == "chiti_kat":
        zapis_kat(user_id,"cheats")
        stup_obnulenie(user_id)
        await bot.send_message(call.message.chat.id, "Выбрана категория: Читы")
    elif call.data == "pomosh_kat":
        zapis_kat(user_id,"faq")
        stup_obnulenie(user_id)
        await bot.send_message(call.message.chat.id, "Выбрана категория: Помощь")

    elif call.data == "pokaz_tekst":
        id_stati = cursor.execute("SELECT `obzor_id` FROM `kategorii` WHERE `user_id` =?", (user_id,)).fetchall()[0][0]
        link_ = select_link(call.from_user.id)[0][id_stati]
        otvet = parser_sg_igri(link_)
        for i in range(0, len(otvet[7]), 3500):
            await bot.send_message(call.message.chat.id, otvet[7][i:i + 3500])

if __name__ == '__main__':
    executor.start_polling(dp)