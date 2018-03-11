import requests
import os
import os.path
from bs4 import BeautifulSoup
import re
import time
from download_file import download_file


class ZhuokuCrawler(object):

    def __init__(self, home_url, base_path, headers, max_pages):
        self.home_url = home_url
        self.base_path = base_path
        self.headers = headers
        self.max_pages = max_pages
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)

    def my_soup(self, url):
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        return soup

    #获取前n页的相册列表
    def ablum_url(self):
        time_start1 = time.time()
        full_url_list = [] #相册集
        for i in range(self.max_pages): #第1页至第n页所有相册
            if i == 1:
                index_url = self.home_url + '/new/index.html'
            else:
                index_url = self.home_url + '/new/index_' + str(i) + '.html'
            soup = self.my_soup(index_url)
            a_list = soup.findAll('a', attrs={'class': 'title'},)
            re_rule = re.compile(r'href="(.*?)" target')
            detail_url = re.findall(re_rule, str(a_list))
            for n in detail_url:
                ablum_url = self.home_url + n
                print('获取相册地址: %s   OK' % ablum_url)
                full_url_list.append(ablum_url)
        print('\n 获取相册地址耗时：%.2f s\n' % (time.time() - time_start1))
        print('------------------')
        time.sleep(1)
        time_start2 = time.time()
        pic_url_list = [] #所有相册的图片集
        for url in full_url_list:
            pic_list = self.my_soup(url).findAll('div', attrs={'class': 'bizhiin'})
            max = len(pic_list)+1
            for n in range(1, max):
                pic_url = url.replace('.htm', '(%s).htm' % n)
                pic_url_list.append(pic_url)
                print('获取详情页地址： %s  OK' % pic_url)
        print('\n 获取详情页地址耗时：%.2f s\n' % (time.time() - time_start2))
        print('------------------')
        time.sleep(1)
        return pic_url_list


    #获取图片名称与src
    def get_pic(self):
        time_start3 = time.time()
        src_list = {} #源文件与原地址集合
        for url in self.ablum_url():
            src = str(self.my_soup(url).findAll('img', attrs={'id': 'imageview'}))
            name = re.search(r'alt="(.*?)" id', src).group(1)
            rule = re.compile(r':|：|/')
            pic_name = re.sub(rule, ' ', name)
            dir_name = re.sub('\((.*)\)', '', pic_name)
            file_path = self.base_path + '/' + dir_name
            if not os.path.exists(file_path): #创建目录
                os.makedirs(file_path)
            file_name = file_path + '/' + pic_name + '.jpg'
            pic_src = re.search(r'src="(.*?)"', src).group(1)
            src_list[pic_name] = pic_src
            print('开始下载图片： %s  ' % pic_name)
            download_file(pic_src, file_name, headers)
        print('\n 下载图片耗时：%.2f s\n' % (time.time() - time_start3))
        print('----------')


if __name__ == '__main__':
    url = 'http://www.zhuoku.com'
    path = './zhuoku_images'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Referer": 'http://www.zhuoku.com'
    }
    zk = ZhuokuCrawler(url, path, headers, 2)
    zk.get_pic()
