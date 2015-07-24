#!/usr/bin/env python
#-*- coding:utf-8 -*-
import subprocess
import re
import os
from StringIO import StringIO
try:
    import requests
except:
    print "import requests,please install by : pip install requests "
    raise SystemExit
try:
    from PIL import Image
except:
    print "import PIL fail,please install by : pip install pillow "
    raise SystemExit


class wx_reader:

    def __init__(self):
        self.__url_file = 'url.txt'
        self.__result_file = "result.txt"
        self.__url_index = 'http://51tools.info/wx/weixin.aspx'
        self.__url_verifycode = 'http://51tools.info/captcha.aspx'
        self.__url_post = 'http://51tools.info/wx/getnum.ashx'
        # 每次查询请求时最多的条数
        self.__max_line_per_request = 20

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

    def __get_http_image(self, url, req=None, pic_type='JPEG', pic_type_name='jpg'):
        '''
        get http image to local picture file
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        if req == None:
            r = requests.get(url, headers=headers, stream=True)
        else:
            r = req.get(url, headers=headers, stream=True)
        file_name = 'yzm.'+pic_type_name
        if r.status_code == requests.codes.ok:
            try:
                i = Image.open(StringIO(r.content))
                i .save(file_name, pic_type)
                return file_name
            except:
                raise
                return None
        return None

    def __get_yzm_image_and_input(self, req):
        '''
        get yzm from url,and prompt user input code 
        '''
        image_file = self.__get_http_image(self.__url_verifycode, req)
        if image_file == None:
            print u'[-]获得验证码图片失败！'
            return None
        subprocess.Popen(image_file, shell=True)
        code = raw_input('input the yzm:')

        return code

    def __format_post_data(self, wx_url_list, yzm):
        '''
        format the post data 
        '''
        data = {}
        urls = '\n'.join(wx_url_list)

        data['urls'] = urls
        data['yzm'] = yzm

        return data

    def __get_response_number(self, str):
        '''
        get number from response text 
        '''
        n1, n2 = '-1', '-1'
        line_list = str.split('/')
        patter = r'(\d+)'
        if len(line_list) >= 2:
            m1 = re.findall(patter, line_list[0])
            if m1:
                n1 = m1[0]
            m2 = re.findall(patter, line_list[1])
            if m2:
                n2 = m2[0]

        return (int(n1), int(n2))

    def __check_response(self, response_text):
        '''
        check response is success
        '''
        fail_message = {u'验证码错误', u'key失效'}
        r = response_text.decode('utf-8')
        for msg in fail_message:
            if r.find(msg) >= 0:
                return (False, msg)

        return (True, '')

    def __get_response(self, response_text):
        '''
        parser response result 
        '''
        data = []
        # response_text = '''
        #(阅读数：100001 / 点赞数：1454)http://mp.weixin.qq.com/s?__biz=MjM5MDAzNDcwMA==&mid=211552128&idx=5&sn=50879ac7678fe8e6ffd9b97c8c3d027a&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：100001 / 点赞数：466)http://mp.weixin.qq.com/s?__biz=MjM1ODIzNTU2MQ==&mid=224593819&idx=4&sn=62ac4b39176e98fb67032c8336f82e3c&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：91549 / 点赞数：340)http://mp.weixin.qq.com/s?__biz=MjMyMzYyNzg2MA==&mid=212423440&idx=2&sn=4b944b1bdb18ee701de91ec0b9fb8e8a&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：100001 / 点赞数：1454)http://mp.weixin.qq.com/s?__biz=MjM5MDAzNDcwMA==&mid=211552128&idx=5&sn=50879ac7678fe8e6ffd9b97c8c3d027a&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：100001 / 点赞数：466)http://mp.weixin.qq.com/s?__biz=MjM1ODIzNTU2MQ==&mid=224593819&idx=4&sn=62ac4b39176e98fb67032c8336f82e3c&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：91549 / 点赞数：340)http://mp.weixin.qq.com/s?__biz=MjMyMzYyNzg2MA==&mid=212423440&idx=2&sn=4b944b1bdb18ee701de91ec0b9fb8e8a&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：100001 / 点赞数：1454)http://mp.weixin.qq.com/s?__biz=MjM5MDAzNDcwMA==&mid=211552128&idx=5&sn=50879ac7678fe8e6ffd9b97c8c3d027a&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：100001 / 点赞数：466)http://mp.weixin.qq.com/s?__biz=MjM1ODIzNTU2MQ==&mid=224593819&idx=4&sn=62ac4b39176e98fb67032c8336f82e3c&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：91549 / 点赞数：340)http://mp.weixin.qq.com/s?__biz=MjMyMzYyNzg2MA==&mid=212423440&idx=2&sn=4b944b1bdb18ee701de91ec0b9fb8e8a&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>(阅读数：100001 / 点赞数：1454)http://mp.weixin.qq.com/s?__biz=MjM5MDAzNDcwMA==&mid=211552128&idx=5&sn=50879ac7678fe8e6ffd9b97c8c3d027a&3rd=MzA3MDU4NTYzMw==&scene=6#rd<br/><br/>
        #'''
        r_list = response_text.split('<br/><br/>')
        pattern = r'(\(.+?\))(.+)'
        for r in r_list:
            m = re.findall(pattern, r)
            if m:
                for x in m:
                    (n1, n2) = self.__get_response_number(x[0])
                    url = x[1].strip()
                    data.append((n1, n2, url))

        return data

    def __write_result(self, result):
        '''
        save the result to file 
        '''
        with open(self.__result_file, 'w') as f:
            for r in result:
                f.write('%d,%d,%s%s' % (r[0], r[1], r[2], os.linesep))

        return True

    def __do_request(self, wx_url_list):
        '''
        request the page ,get response and result
        '''
        response_result = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        s = requests.session()
        r = s.get(self.__url_index, headers=headers)
        if r.status_code == requests.codes.ok:
            print u'[+]读取接口页面成功！'
            yzm = self.__get_yzm_image_and_input(s)
            if yzm == None:
                return None
            post_data = self.__format_post_data(wx_url_list, yzm)

            r = s.post(self.__url_post, data=post_data, headers=headers)
            if r.status_code == requests.codes.ok:
                print u'[+]读取查询页面成功！'
                (success, msg) = self.__check_response(r.content)
                if success:
                    print u'[+]获得数据并分析。。。'
                    response_result = self.__get_response(r.content)
                else:
                    print u'[-]获取数据失败：', msg
            else:
                print u'[-]读取查询页面失败！'
        else:
            print u'[-]读取接口页面失败！'

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
        print u'[+]读取文章列表成功，共%d条记录！'%len(url_list)

        try:
            for i in range(request_round):
                urls = url_list[
                    i*self.__max_line_per_request:(i+1)*self.__max_line_per_request]
                while True:
                    print u'[+]正在处理第%d条记录' %(i*self.__max_line_per_request + 1)
                    r = self.__do_request(urls)
                    if len(r) > 0 :
                        results.extend(r)
                        break
            # print results
            if len(results) > 0:
                if self.__write_result(results):
                    print u'[+]保存%d条查询结果到文件%s成功！' % (len(results),self.__result_file)
                else:
                    print u'[-]保存%d条查询结果到文件%s失败！' % (len(results),self.__result_file)
        except KeyboardInterrupt:
            print '[-]用户中断，程序退出'

def main():
    app = wx_reader()
    app.run()

if __name__ == '__main__':
    main()
