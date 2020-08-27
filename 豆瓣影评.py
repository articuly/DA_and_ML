# coding:utf-8
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


def getNowPlayingMovie_list():
    url = 'https://movie.douban.com/cinema/nowplaying/guangzhou/'
    global headers
    r = Request(url, headers=headers)
    resp = urlopen(r)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')

    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']  # 实际为电影的ID
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)
    return nowplaying_list


def getCommentsById(movie_id, page_num):
    each_comment_list = []
    if page_num > 0:
        start = (page_num - 1) * 20
    else:
        return False
    url = f'https://movie.douban.com/subject/{movie_id}/comments?start={start}&limit=20'
    print(url)
    global headers
    r = Request(url, headers=headers)
    resp = urlopen(r)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')

    comment_div_list = soup.find_all('div', class_='comment')
    for item in comment_div_list:
        comment_str = item.p.get_text()
        if comment_str is not None:
            each_comment_list.append(comment_str)
    return each_comment_list


def main():
    comment_list = []
    nowplaying_movie_list = getNowPlayingMovie_list()
    for i in range(2):
        num = i + 1
        comment_list_temp = getCommentsById(nowplaying_movie_list[0]['id'], num)
        comment_list.append(comment_list_temp)
        print(comment_list)

    # comments=''
    # for j in range(len(comment_list)):
    #     comments=comments+(str(comment_list[j])).strip()


if __name__ == '__main__':
    main()
