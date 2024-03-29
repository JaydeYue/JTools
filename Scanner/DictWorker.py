__author__ = "Jayde Yue"
# Website: www.jaydeyue.com


import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import threading


class DictWorker(threading.Thread):

    def __init__(self, dict, scanner, dict_number):
        threading.Thread.__init__(self)
        self.dict = dict
        self.scanner = scanner
        self.dict_number = dict_number

    def request_with_retrys(self, session):
        retry = Retry(
            total=self.scanner.max_retrys,
            read=self.scanner.max_retrys,
            connect=self.scanner.max_retrys,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def procese_valid_url(self, request_url, response):
        print(request_url + ": " + str(response.status_code))
        self.scanner.dict_stats[self.dict_number] +=1
        if not self.scanner.allow_overlap:
            self.scanner.all_trys[request_url[len(self.scanner.base_url):]] = 1

    def run(self):
        while not self.dict.empty():
            try:
                request_url = self.scanner.base_url + self.dict.get_nowait()
                session = requests.Session()
                if self.scanner.user != '':
                    session.auth = (self.scanner.user, self.scanner.pwd)
                session.headers.update({
                             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                             'Referer': self.scanner.referer,
                             'Cookie': self.scanner.cookie,
                             })
                response = self.request_with_retrys(session).get(request_url, timeout=self.scanner.time_out, allow_redirects=self.scanner.allow_redirect)
                if response.status_code != 404:
                    if self.scanner.allow_redirect:
                        if len(response.history) > 0:
                            if response.url not in self.scanner.redirect_list:
                                self.scanner.redirect_list[response.url] = [request_url]
                            else:
                                self.scanner.redirect_list[response.url].append(request_url)
                            # self.scanner.dict_stats[self.dict_number] +=1
                        else:
                            self.procese_valid_url(request_url, response)
                    elif response.status_code != 302 and response.status_code != 301:
                        self.procese_valid_url(request_url, response)
            except Exception as e:
                print(e)
                break
