import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from data.urls.urls import headers, domain


def get_last_post_datetime_str(dater):
    return f"{(date.today() - timedelta(days=int(dater))).strftime('%d.%m.%Y')} 00:00"


def get_soup(url, header=headers):
    req = requests.get(url, headers=header)
    return BeautifulSoup(req.text, "lxml")


def get_all_post_dict(soup, post_date):
    all_post_articles = soup.find_all(class_="col-13 article-time")
    all_post_dict = {}

    for art in all_post_articles:
        item_art = get_post_datetime(art)
        item_href = get_post_href(art)
        item_title = get_post_title(art)

        if str_to_datetime(item_art) > str_to_datetime(post_date):
            all_post_dict[item_art] = [item_href, item_title]
    return all_post_dict


def get_post_datetime(art):
    return f'{art.find("span").find_next_sibling().string} {art.find("span").string}'


def get_post_href(art):
    return f'{domain}{art.find_previous(class_="grid article").find(class_="article-link").get("href")}'


def get_post_title(art):
    return f'{art.find_previous(class_="grid article").find(class_="article-link").string.strip()}'


def str_to_datetime(str):
    return datetime.strptime(str, "%d.%m.%Y %H:%M")


def main(dater, url):
    last_post_datetime_str = get_last_post_datetime_str(dater)
    soup = get_soup(url=url)
    all_post_dict = get_all_post_dict(soup, last_post_datetime_str)
    all_pages_list = []
    if all_post_dict:
        while all_post_dict:
            all_pages_list.append(all_post_dict)
            url = f'{domain}{soup.find(class_="pager").find("a", class_=False).get("href")}'
            soup = get_soup(url, headers)
            all_post_dict = get_all_post_dict(soup, last_post_datetime_str)
    else:
        print("Новостей нет")
    return all_pages_list






