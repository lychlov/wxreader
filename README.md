# wxreader
利用第三方接口调用，查询微信文章的阅读量和点赞量

#一、需安装的软件

1. 安装python 2.7

2. 安装python requests扩展库：
	* 在windows的命令行窗口下，进入c:\python27\scripts，运行pip install requests命令进行安装；
	* 在linux或osx下，直接用pip install requests安装

#二、运行方法及说明

##（方式一）、使用绑定的api接口：
 
 1. 在命令行窗口下进入脚本所在的在目录，运行python wxreader.py
 
 2. 注意事项:</br>
  
  	* 该脚本需要一个读取微信文章的api接口，设置在在wxreader.py的main()函数中的url_api变量中。
  
  	* 要读取的文章的url在url.txt中，每个url一行
  	
  	* 读取成功后，生产的结果文件保存在当前目录下，阅读量、点赞量和url地址分别为‘,'分隔开
  
  * 该接口绑定后，好象只有2个小时的有效期，超过2小时，就会出现“key失效”，就得重新绑定和设置api接口（url_api变量）


##（方式二）、使用手工验证码方式：

  1. 在命令行窗口下，运行python wxreader_yzm.py，会自动读取验证码并存为图片yzm.jpg，手动输入验证码后，即可读取指定的阅读量和点赞量。

  2. 使用该方式，需要安装一个图形PIL库，安装方法为：pip install pillow
  
  3. 该方式的优点是接口永不过期，麻烦的地方是每读1条就要输入一次验证码，偶尔会出现key失效。(目前好象是只能一条一条地查询了）
  4. 调用的接口可在[http://51tools.info/wx/weixin.aspx](http://51tools.info/wx/weixin.aspx)相关页面上获取。
