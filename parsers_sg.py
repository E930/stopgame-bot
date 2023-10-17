import requests
from bs4 import BeautifulSoup as bs


# скачивание скриншотов с сайта

# link = "https://stopgame.ru/newsdata/59516/game_pass_v_avguste_chast_2_firewatch_the_texas_chain_saw_massacre_sea_of_stars?utm_source=sg-read-more"
# req = requests.get(link)
# obr = bs(req.text, "html.parser")
# find = obr.find_all("div", class_="_image-wrapper_a3368_153 _image-width_a3368_98")[0].findChildren("a")
# abc = 0
# for i in find:
#     b = i.get('href')
#     req = requests.get(b)
#     open_ = open(f"./{abc}.jpeg", "wb")
#     open_.write(req.content)
#     open_.close()
#     abc += 1



def parser_sg(link):
    req = requests.get(link)
    obr = bs(req.text, "html.parser")
    all_link = []
    all_text = []
    srez_link = link[-5:]
    if srez_link == "games":
        find_ = obr.find_all("h2", class_="_title_99wqg_150")
        for i in find_:
            title = i.find("a")
            text_stati = title.text
            link = "https://stopgame.ru" + title.get("href")
            all_link.append(link)
            all_text.append(text_stati)
        return all_text, all_link
    elif srez_link == "video":
        find = obr.find_all("a", class_="_card__title_givrd_1")
        for i in find:
            text = i.text
            link = "https://stopgame.ru" + i.get("href")
            all_link.append(link)
            all_text.append(text)
        return all_text, all_link
    elif srez_link == "e=faq":
        find_text = obr.find_all("span", class_="article-card_title")
        for i in find_text:
            text = i.text
            all_text.append(text)
        find_link = obr.find_all("a", class_="article-card article-card--small article-card--no-image")
        for i in find_link:
            link = "https://stopgame.ru" + i.get("href")
            all_link.append(link)
        return all_text, all_link
    elif srez_link == "heats":
        find_title = obr.find_all("span", class_="_game-name_hjxtz_68")
        for i in find_title:
            title = i.text
            all_text.append(title)
        find_link = obr.find_all("a", class_="_card_hjxtz_1")
        for i in find_link:
            link = "https://stopgame.ru" + i.get("href")
            all_link.append(link)
        return all_text, all_link

    else:
        find_ = obr.find_all("div", class_="item")
        for i in find_:
            teg_a_link = "https://stopgame.ru" + i.findChildren("a")[2].get("href")
            teg_a_title = i.findChildren("a")[2].text
            if teg_a_title == " 0 ":
                pass
            else:
                all_link.append(teg_a_link)
                all_text.append(teg_a_title)
        return all_text, all_link

def parser_sg_novosti(link):
    req = requests.get(link)
    obr = bs(req.text, "html.parser")
    find_title = obr.find_all("div", class_="_content-wrapper_a3368_78 _material-info_a3368_149")[0].find("h1").text
    find_2 = obr.find_all("p", class_="_text_a3368_93 _text-width_a3368_93")
    text_novosti = ""
    for i2 in find_2:
        text_stati = i2.text
        text_novosti += text_stati + "\n\n"
    return find_title, text_novosti

def parser_sg_video(link):
    req = requests.get(link)
    obr = bs(req.text, "html.parser")
    find_video_link_ = obr.find_all("div", class_="_video-wrapper_a3368_359 _image-width_a3368_98")[0].find(
        "a").get("href")
    return find_video_link_

def parser_sg_pomosh(link):
    req = requests.get(link)
    obr = bs(req.text, "html.parser")
    find_vopros = obr.find_all("p", class_="_text_a3368_93 _text-width_a3368_93")[0].text
    find_otvet = obr.find_all("div", class_="_comment__body_h9b8g_1")
    text_otvet = ""
    a = 1
    for i in find_otvet:
        text = i.text
        text_otvet += f"\nОтвет №{a}\n" + text + "\n"
        a += 1
    return find_vopros, text_otvet


def parser_sg_chiti_i_text(link, user_id):
    req = requests.get(link)
    obr = bs(req.text, "html.parser")
    find_title = obr.find_all("div", class_="_content-wrapper_1tcvz_79 _material-info_1tcvz_156")[0].find("h1").text
    find_text = obr.find_all("div", class_="_content_1tcvz_8")[0].findChildren("p")
    text_otvet = ""
    for i in find_text:
        text_otvet += i.text + "\n\n"

    find_link = obr.find_all("a", class_="trainer-btn")
    if len(find_link) != 0:
        a = 1
        for i in find_link:
            links = "https://stopgame.ru" + i.get("href")
            req2 = requests.get(links)
            obr2 = bs(req2.text, "html.parser")
            find_download = obr2.find_all("div", class_="_download-insert_1tcvz_2191")[0].find("input").get("value")
            req3 = requests.get(find_download)
            open_ = open(f"./{user_id}-Ваши-читы-{a}.zip", "wb")
            open_.write(req3.content)
            a += 1
        return a, find_title, "Есть файл"
    else:
        find_title = obr.find_all("div", class_="_content-wrapper_1tcvz_79 _material-info_1tcvz_156")[0].find("h1").text
        find_text = obr.find_all("div", class_="_content_1tcvz_8")
        text_novosti = ""
        for i in find_text:
            text_stati = i.text
            text_novosti += text_stati + "\n"
        return text_novosti, find_title, "Нет файла"
# print(parser_sg_chiti_i_text("https://stopgame.ru/show/112163/minecraft_dungeons_12_trainer", 213712636123))

def parser_sg_igri(link):
    req = requests.get(link)
    obr = bs(req.text, "html.parser")
    find_title = obr.find_all("h2", class_="_title_fcjhe_163")[0].text.replace("\n", "")
    find_info = obr.find_all("div", class_="_info-grid_fcjhe_200")
    data = find_info[0].findChildren("div")[1].text.replace("\n", "")
    genre = find_info[0].findChildren("div")[11].findChildren("a")
    itog_genre = ""
    for i in genre:
        itog_genre += i.text.replace("\n", "") + " "
    platform = find_info[0].findChildren("div")[9].findChildren("a")
    itog_platform = ""
    for i in platform:
        itog_platform += i.text.replace("\n", "") + " "

    find_req = obr.find_all("div", class_="_requirements_1cmf7_647")
    itog_minim = ""
    itog_rekom = ""
    if len(find_req) == 0:
        pass
    else:
        a = find_req[0].findChildren("div")
        itog_minim += f"<b>{a[0].text}:</b> {a[1].text} \n" \
                   f"<b>{a[2].text}:</b> {a[3].text} \n" \
                   f"<b>{a[4].text}:</b> {a[5].text} \n" \
                   f"<b>{a[6].text}:</b> {a[7].text} \n" \
                   f"<b>{a[8].text}:</b> {a[9].text} \n" \
                   f"<b>{a[10].text}:</b> {a[11].text} \n" \
                   f"<b>{a[12].text}:</b> {a[13].text} \n" \
                   f"<b>{a[14].text}:</b> {a[15].text} \n"
        a = find_req[1].findChildren("div")
        itog_rekom += f"<b>{a[0].text}:</b> {a[1].text} \n" \
                   f"<b>{a[2].text}:</b> {a[3].text} \n" \
                   f"<b>{a[4].text}:</b> {a[5].text} \n" \
                   f"<b>{a[6].text}:</b> {a[7].text} \n" \
                   f"<b>{a[8].text}:</b> {a[9].text} \n" \
                   f"<b>{a[10].text}:</b> {a[11].text} \n" \
                   f"<b>{a[12].text}:</b> {a[13].text} \n" \
                   f"<b>{a[14].text}:</b> {a[15].text} \n" \
                   f"<b>{a[16].text}:</b> {a[17].text} \n"

    find_video_obzor_link = obr.find_all("a", class_="_card__title_hep3d_1")
    asd = []
    for i in find_video_obzor_link:
        asd.append("https://stopgame.ru" + i.get("href"))
    find_video_link_ = ""
    itog_tekst = ""
    if len(find_video_obzor_link) == 0:
        pass
    else:
        if len(find_video_obzor_link) == 1:
            try:
                req2 = requests.get(asd[0])
                obr2 = bs(req2.text, "html.parser")
                find_video_link_ += obr2.find_all("div", class_="_video-wrapper_a3368_359 _image-width_a3368_98")[0].find("a").get("href")
            except:
                req2 = requests.get(asd[0])
                obr2 = bs(req2.text, "html.parser")
                find_video_link = obr2.find_all("div", class_="_video-wrapper_a3368_359 _image-width_a3368_98")
                if len(find_video_link) == 0:
                    find_tekst_obzor_link = "https://stopgame.ru" + str(obr.find_all("a", class_="_card__title_hep3d_1")[0].get("href"))
                    req = requests.get(find_tekst_obzor_link)
                    obr = bs(req.text, "html.parser")
                    find_tekst = obr.find_all("p", class_="_text_a3368_93 _text-width_a3368_93")
                    for i in find_tekst:
                        itog_tekst += i.text + "\n\n"
        elif len(find_video_obzor_link) == 2:
            req2 = requests.get(asd[0])
            obr2 = bs(req2.text, "html.parser")
            find_video_link_ += obr2.find_all("div", class_="_video-wrapper_a3368_359 _image-width_a3368_98")[0].find("a").get("href")

            req2 = requests.get(asd[1])
            obr2 = bs(req2.text, "html.parser")
            find_video_link = obr2.find_all("div", class_="_video-wrapper_a3368_359 _image-width_a3368_98")
            if len(find_video_link) == 0:
                find_tekst_obzor_link = "https://stopgame.ru" + str(
                    obr.find_all("a", class_="_card__title_hep3d_1")[0].get("href"))
                req = requests.get(find_tekst_obzor_link)
                obr = bs(req.text, "html.parser")
                find_tekst = obr.find_all("p", class_="_text_a3368_93 _text-width_a3368_93")
                for i in find_tekst:
                    itog_tekst += i.text + "\n\n"

    return find_title, itog_genre, data, itog_platform, itog_minim, itog_rekom, find_video_link_, itog_tekst
