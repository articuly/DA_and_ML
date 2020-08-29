# coding:utf-8
import warnings
import jieba
import jieba.analyse
import re
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs

warnings.filterwarnings('ignore')
matplotlib.rcParams['figure.figsize'] = (16, 9)

# 必须指定，否则无法访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


# 分析网页的函数
def getNowPlayingMovie_list():
    url = 'https://movie.douban.com/cinema/nowplaying/guangzhou/'
    global headers
    r = Request(url, headers=headers)
    resp = urlopen(r)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')

    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')  # 得到网页所有上映电影
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']  # 实际为电影的ID
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)
    return nowplaying_list


# 根据电影ID获得评论
def getCommentsById(movie_id, page_num):
    each_comment_list = []
    if page_num > 0:
        start = (page_num - 1) * 20
    else:
        return False
    url = f'https://movie.douban.com/subject/{movie_id}/comments?start={start}&limit=20'
    print('getting', url)
    global headers
    r = Request(url, headers=headers)
    resp = urlopen(r)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')

    comment_div_list = soup.find_all('div', class_='comment')  # 找到本页的评论
    for item in comment_div_list:
        comment_str = item.p.get_text()
        if comment_str is not None:
            each_comment_list.append(comment_str)
    return each_comment_list


def main():
    comment_list = []
    nowplaying_movie_list = getNowPlayingMovie_list()
    for i in range(10):  # 前10页
        num = i + 1
        comment_list_temp = getCommentsById(nowplaying_movie_list[0]['id'], num)  # 索引0为当前上映的《八佰》
        comment_list.append(comment_list_temp)
        # print(comment_list)
    # 将列表中转换为字符串
    comments = ''
    for j in range(len(comment_list)):
        comments = comments + (str(comment_list[j])).strip()
    # 使用正则表达式去掉标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filter_data = re.findall(pattern, comments)
    cleaned_comments = ''.join(filter_data)
    # 使用jieba分词，并获得词频排列列表
    result = jieba.analyse.textrank(cleaned_comments, topK=50, withWeight=True)
    keywords = {}
    for k in result:
        keywords[k[0]] = k[1]  # 把列表里的二元组形成字典
    print('before delete stopword:', keywords)
    # 读取为停用词集合
    stopwords = set()
    f = open('./movie_stopwords.txt', encoding='utf-8')
    while True:
        word = f.readline()
        if word == '':
            break
        stopwords.add(word[:-1])
    print(stopwords)
    keywords = {x: keywords[x] for x in keywords if x not in stopwords}
    print('after delete stopword:', keywords)

    wordcloud = WordCloud(font_path='simhei.ttf', background_color='white', max_font_size=80, stopwords=stopwords)
    word_frequence = keywords
    myword = wordcloud.fit_words(word_frequence)
    plt.axis('off')
    plt.imshow(myword)
    plt.savefig('movie_comments_from_douban.png', dpi=300, bbox_inches='tight')
    plt.show()  # 先保存，show之后生成空对象


if __name__ == '__main__':
    main()
