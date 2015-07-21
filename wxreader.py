#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import datetime
import json
try:
    import requests
except:
    print "import requests fail,please install by : pip install requests "
    raise SystemExit


class wx_reader:

    def __init__(self,url_file,url_api,max_per_request=20):
        '''
        init class
        '''
        self.__url_file = url_file
        self.__url_api = url_api
        self.__max_line_per_request = max_per_request

    def __get_url_from_file(self):
        '''
        get all url list from file
        '''
        url_list = []
        with open(self.__url_file) as f:
            for line in f:
                line = line.strip()
                line = line.strip('\r')
                line = line.strip('\n')
                line = line.strip('\r\n')
                url_list.append(line)

        return url_list


    def __format_post_data(self, wx_url_list):
        '''
        format the post data 
        '''
        data = {}
        data['urls'] = '\n'.join(wx_url_list)

        return data


    def __write_result(self, result):
        '''
        save the result to file 
        '''
        filename = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + '.txt'
        with open(filename, 'w') as f:
            for r in result:
                f.write('%d,%d,%s%s' % (r[0], r[1], r[2], os.linesep))
        return filename

    def __do_request(self, wx_url_list):
        '''
        request the page ,get response and result
        '''
        response_result = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        post_data = self.__format_post_data(wx_url_list)

        r = requests.post(self.__url_api, data=post_data, headers=headers)
        if r.status_code == requests.codes.ok:
            print u'读取接口页面成功！'
            jdata = r.json()
            if jdata['msg'] == 'succ':
                print u'获取数据分析中。。。'
                for data in jdata['data']:
                    response_result.append((data['supports'],data['readnums'],data['url']))
            else:
                print u'获取数据失败：'+ jdata['msg']

        else:
            print u'读取接口页面失败！'
 

        return response_result

    def run(self):
        '''
        run
        '''
        results = []
        url_list = self.__get_url_from_file()

        request_round = len(url_list) / self.__max_line_per_request
        if len(url_list) % self.__max_line_per_request > 0:
            request_round += 1
        for i in range(request_round):
            urls = url_list[
                i*self.__max_line_per_request:(i+1)*self.__max_line_per_request]
            r = self.__do_request(urls)
            results.extend(r)

        # print results
        if len(results) > 0:
            file_name = self.__write_result(results)
            print u'保存查询结果到文件%s成功！' % file_name


def main():
    #define url list file and api
    url_file = 'url.txt'
    url_api = 'http://51tools.info/wx/api.ashx?uin=MTg4MDIwOTg4Mg=='
    max_line_per_request = 20
    #call 
    app = wx_reader(url_file,url_api,max_line_per_request)
    app.run()


if __name__ == '__main__':
    main()
