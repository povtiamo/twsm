一、配置文件conf.ini填写规范：
1.loop是线程数，即需要跑多少账号，如需要执行1000个账号，则填1000
2.passwd是登录密码
3.host是域名，注意不要加目录
4.userlistfile=usernamelist.txt是登录账号列表，文件在data目录下，按照格式替换成需要使用的账号，账号数量不能少于loop设置数量

二、(可选)自定义发送包：
1.custommethod=True	#需要使用自定义发送包则输入True,不需要则留空custommethod=,启用后，只会使用登陆和该自定义功能，其他功能不会执行
2.httpmethod=post#支持post和get两种方法
3.uri=http://127.0.0.1/path/name #输入需要测试的完整域名+接口路径,不可为空
4.param={"user":0,"pass"=""}#url的参数,拼接在uri后面，可直填入字符，填入json格式会自动转成urlencode格式name?user=0&pass=
5.data={"data":1}	#输入需要post的body内容，没有则留空：data=
6.headers_add={"headers_add":"1"}	#输入需要补充的请求头，没有则留空：headers_add=,值不能输入int类型
7.cookies={"cookies":"1"}	#输入需要补充的cookie，没有则留空：cookies=,值不能输入int类型