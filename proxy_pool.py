import requests
import re
from bs4 import BeautifulSoup as bs
import Queue
import threading

url = "https://www.xicidaili.com/nn/"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

class Ip_collect(threading.Thread):
    def __init__(self,que):
        threading.Thread.__init__(self)
        self._que=que

    def run(self):
        while not self._que.empty():
            url = self._que.get()
            html = requests.get(url, headers=headers, timeout=5)
            soup = bs(html.content,'lxml',from_encoding='utf-8')
            ips = soup.find_all(name='tr',attrs={'class':re.compile(r'|[odd]')})
            for ip in ips:
                us = ip.find_all(name='td')
                try:
                    self.ip_proxies_confirm(str(us[5].string),str(us[1].string),str(us[2].string))
                except Exception,e:
                    # print e
                    pass
                print str(ip.find_all(name='td')[1].string)

    def ip_proxies_confirm(self,type_self,ip,port):
        ip_dic = {}
        ip_dic[type_self.lower()] = ip + ':' + port
        html = requests.get('http://ip.tool.chinaz.com/', headers=headers, proxies=ip_dic, timeout=5)
        soup = bs(html.content, 'lxml', from_encoding='utf-8')
        ips = soup.find_all(name='dd', attrs={'class': 'fz24'})
        result_ip = str(ips[0].string)
        if ip == result_ip:
            print ip + ':' + port + 'is ok!!'
            with open('ips.txt','a') as f:
                f.write(type_self+"://"+ip + ':' + port + '\n')

if __name__  == '__main__':
    thread = []
    thread_count = 20
    que = Queue.Queue()
    for i in range(1,10):
        que.put('http://www.xicidaili.com/nn',str(i))
    for i in range(thread_count):
        thread.append(Ip_collect(que))
    for i in thread:
        i.start()
    for i in thread:
        i.join()