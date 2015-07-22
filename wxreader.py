#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import datetime
import json
import time
try:
    import requests
except:
    print "import requests fail,please install by : pip install requests "
    raise SystemExit


class wx_reader:

    def __init__(self,url_file,result_file,url_api,max_per_request=20,delay_second_per_request=3):
        '''
        init class
        '''
        self.__url_file = url_file
        self.__result_file = result_file
        self.__url_api = url_api
        self.__max_line_per_request = max_per_request
        self.__delay_second_per_request = delay_second_per_request
        #
        self.__url_buffer_txtfile = "url_buffer.txt"

    def __get_url_from_file(self,file_name):
        '''
        get all url list from file
        '''
        url_list = []
        with open(file_name) as f:
            for line in f:
                line = line.strip()
                line = line.strip('\r')
                line = line.strip('\n')
                line = line.strip('\r\n')
                url_list.append(line)

        return url_list

    def __writeto_url_buffer_textfile(self,wx_url_list):
        '''
        write the origin url list to buffer text file
        '''
        with open(self.__url_buffer_txtfile,'w') as f:
            for line in wx_url_list:
                f.write(line)
                f.write(os.linesep)

    def __write_result(self, result, writemode):
        '''
        save the result to file 
        '''
        with open(self.__result_file, writemode) as f:
            for r in result:
                f.write('%d,%d,%s%s' % (r[0], r[1], r[2], os.linesep))
        return True
    
    def __format_post_data(self, wx_url_list):
        '''
        format the post data 
        '''
        data = {}
        data['urls'] = '\n'.join(wx_url_list)

        return data

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
            print u'[+]读取接口页面成功！'
            jdata = r.json()
            if jdata['msg'] == 'succ':
                print u'[+]获取数据分析中。。。'
                for data in jdata['data']:
                    response_result.append((data['supports'],data['readnums'],data['url']))
            else:
                print u'[-]获取数据失败：'+ jdata['msg']

        else:
            print u'[-]读取接口页面失败！'
 

        return response_result

    def run(self):
        '''
        run
        '''
        results = []
        #get url list 
        #check the url buffer file ,if the buffer file is empty,then get url from url.txt 
        url_list = self.__get_url_from_file(self.__url_buffer_txtfile)
        result_file_writemode = 'a'
        if len(url_list) <= 0:
            url_list = self.__get_url_from_file(self.__url_file)
            result_file_writemode = 'w'

        print u'[+]读取文章列表成功，共%d条记录！'%len(url_list)
        #compute the round to read all url
        request_round = len(url_list) / self.__max_line_per_request
        if len(url_list) % self.__max_line_per_request > 0:
            request_round += 1

        for i in range(request_round):
            #do request by one time
            urls = url_list[
                i*self.__max_line_per_request:(i+1)*self.__max_line_per_request]
            print u'[+]正在处理第%d条记录' %(i*self.__max_line_per_request + 1)
            r = self.__do_request(urls)
            #if the result > 0,then this request is success;so save the result and delay
            if len(r) >0:
                results.extend(r)
            else:
            #if the result <=0,this request is fail,so save the rest url list to url buffer text for next run
            #and stop reading next url list
                self.__writeto_url_buffer_textfile(url_list[i*self.__max_line_per_request:])
                break
            if i+1 < request_round:
                print u'[+]暂停%d秒。。。' % self.__delay_second_per_request
                time.sleep(self.__delay_second_per_request)
 
        #if all the url have success read,then empty the url buffer file
        if len(results) == len(url_list):
            self.__writeto_url_buffer_textfile([])

        # print results
        if len(results) > 0:
            if self.__write_result(results,result_file_writemode):
                print u'[+]保存%d条查询结果到文件%s成功！' % (len(results),self.__result_file)
            else:
                print u'[-]保存%d条查询结果到文件%s失败！' % (len(results),self.__result_file)


def main():
    #define url list file and api
    url_file = 'url.txt'
    result_file = 'result.txt'
    url_api = 'http://51tools.info/wx/api.ashx?uin=MTg4MDIwOTg4Mg=='
    max_line_per_request = 20
    delay_second_per_request = 3
    #call 
    app = wx_reader(url_file,result_file,url_api,max_line_per_request,delay_second_per_request)
    app.run()


if __name__ == '__main__':
    main()
