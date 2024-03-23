import requests
from bs4 import BeautifulSoup as bs
import os
import re
from multiprocessing.dummy import Pool

class crawl():
    settings = []
    # with open('userInfo.txt' , 'r') as info:
    #     for line in info.readlines():
    #         settings += [line.strip('\n').split(':')[-1].strip()]
    # info.close()
    _cookies = {
        # 'cf_clearance': settings[0],
        # 'csrftoken': settings[1],
        'cf_clearance': '',
    'csrftoken': '',}
    _header = {
        # 'user-agent': settings[2],
        'user-agent': '',
        }
    _url = ''
    _pitType = []
    _dirBase = None
    _dirName = None
    _base = None
    _a    = None
    _b    = None
    _error = False
    _isUsingThreadPool = True
    _mkdir = True
    _downloadProcess = 0
    
    
    def __init__(self):
        self._orgpath = os.path.abspath(os.getcwd()) 
    
    def dirAdress(self , adress):
        self._dirBase = adress

    def webAddress(self , number):
        try:
            regex_url = r'(\d{6,})'
            self._url = 'https://nhentai.net/g/' + re.search(regex_url , str(number))[0] + '/'
            self.webInfo(self._url)
        except:
            self._dirName = '無法取得內容，請確認是否存在或檢查userInfo內的資料(可能過期，須更新)'
    def webInfo(self , url):
        self._pitType = []
        res = requests.get(url=url , headers=self._header , cookies=self._cookies)
        if res.status_code != 200:
            print(res.status_code)
            print(self._cookies)
            self._dirName = '無法取得內容，請確認是否存在或檢查userInfo內的資料(可能過期，須更新)'
            return
        soup = bs(res.content , 'html.parser')

        nameli = soup.select('h2>span')
        #即將更改的名稱
        name = ''
        for i in nameli:
            name += i.text
        cannt = ["\\" , "\|" , "*" , "!" , ":" , "/" , '"' , "<" , ">"]
        for i in cannt:
            name = name.replace(i , "")

        # pit_url 的處理
        pit_front = r'(.+).(\d+\.)nhentai'
        pit_back =  r'(nhentai.+[\d]+\/)\d+'
        pit_type = r'\d+\/\d+\D(.+)'

        pitList = soup.select('a.gallerythumb>img.lazyload')
        
        self._base = re.search(pit_front , pitList[0]['data-src'])[1] + 'i' \
                    + re.search(pit_front , pitList[0]['data-src'])[2] + \
                    re.search(pit_back , pitList[0]['data-src'])[1]
        for i in pitList:
            self._pitType += [re.search(pit_type , i['data-src'])[1]]
        self._dirName = name
        self._a    = 1
        self._b    = len(pitList) + 1
        self._downloadProcess = 0

        

    def doDownload(self):
        # 重複資料夾則加'_1'
        if not self._mkdir:
            dirpath = self._dirBase
        elif not self._dirBase:
            dirpath = self._dirName
            if os.path.exists(dirpath) :
                dirpath += '_1'
            os.mkdir(dirpath)
        else:
            dirpath = self._dirBase + '/' + self._dirName
            if os.path.exists(dirpath) :
                dirpath += '_1'
            os.mkdir(dirpath)
        
        os.chdir(dirpath)

        # 下載囉
        if self._isUsingThreadPool:
            self._threadingDownload()
        else:
            self._linearDownload()
        
        os.chdir(self._orgpath)
    
    def _linearDownload(self):
        # 線性下載
        for i in range(self._a, self._b) :
            self._dlMethod(i)

    def _threadingDownload(self):
        # 開線程池 十二個線程
        p = Pool(12)
        # 下面需要口說解釋
        p.map(self._dlMethod, range(self._a, self._b))

    def _dlMethod(self, i = 'titlePage'):
        if self._error:
            return 
        # 這裡下載單張圖片
        r = requests.get(self._base + (f"{i}{self._pitType[i-1]}" if i != 'titlePage' else f'1{self._pitType[0]}'))
        filename = '%03d.jpg'%i if i != 'titlePage' else f'{i}.jpg'
        with open(filename, 'wb') as fp:
            if r.status_code == 200:
                fp.write(r.content)
            else:
                self._error = True
        fp.close()
        
        if i != 'titlePage':
            self._downloadProcess += 1

