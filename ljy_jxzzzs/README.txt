一、准备环境(必须)：
1.安装Python3.7，安装过程参考"python3安装.docx"
2.解压Python三方支持库(site-packages.zip)所有文件到运行电脑指定目录(Python安装目录\Python\Lib\site-packages\)中,参考"python3安装.docx"
3.目前只在Windows环境运行
4.程序在当前目录的ljy_jxzzzs文件夹中

二、配置文件conf.ini填写规范：
1.loop是线程数，即需要跑多少账号，如需要执行1000个账号，则填1000
2.jxzzzs_userlist.txt是登录账号列表，按照格式替换成需要使用的账号，账号数量不能少于loop设置数量
3.passwd是登录密码，注意第一次登陆的账号是身份证后六位，需填入加密过的密码,修改后再次使用记得更新为新密码
4.updatepwd修改密码的新密码，需填入加密过的密码，如123456则填入dxk689kxb9j4OUEe7NHVRQ%%3D%%3D
5.volunteercode是志愿代码，如A02,如果未找到输入的代码，则使用随机学校
6.volunteercode_2是第二志愿代码，可为空volunteercode_2=则不选择第二志愿
7.batch=0,批次
8.基本信息：
	8.1 classname:1	#班级
	8.2 guardianName:j	#监护人姓名加上账号的运行编号，如运行1000个账号，则命名为j0-j999，注意不能超过5个字符上限，如1001个用户，输入jhr，则jhr1000会超出命名规则
	8.3 guardianmobile:13666666666	#不可输入已被其他号绑定的手机号，必须和修改密码页面填的手机号一致，监护人手机号加上账号的运行编号，如运行2个账号，则命名为13666666666~13666666667
	如果需要强制修改手机号码，编辑ljy_jxzzzs.py文件修改if login_result["serverResult"]["resultCode"]=="201"其中的201为200，则会固定执行修改密码并填入手机号步骤
	8.4 address:address	#家庭住址
	8.5 studentno:90000000	#注册学籍号加上账号的运行编号，如运行2个账号，则命名为90000000~90000001
9.填写的值中如果有%，需加转义，如1%3D%需改成1%%3D%%

三、运行脚本
1.准备好环境后，点击"嘉兴中职招生自动化脚本\ljy_jxzzzs\start.bat"即可

四、实现功能
1.根据账号表批量登录账号
2.登录后判断是否第一次登陆则修改一次密码，否则进入跳过进入下一步
3.填入基本信息
4.默认每个账号随机选择一个志愿代码/如果配置文件填了志愿代码，则统一选择该志愿代码
5.数据库查询手机验证码，并提交

五、(可选)自定义发送包：
1.custommethod=True	#需要使用自定义发送包则输入True,不需要则留空custommethod=,启用后，只会使用登陆和该自定义功能，其他功能不会执行
2.httpmethod=post#支持post和get两种方法
3.uri=http://127.0.0.1/path/name #输入需要测试的完整域名+接口路径,不可为空
4.param={"user":0,"pass"=""}#url的参数,拼接在uri后面，可直填入字符，填入json格式会自动转成urlencode格式name?user=0&pass=
5.data={"data":1}	#输入需要post的body内容，没有则留空：data=
6.headers_add={"headers_add":"1"}	#输入需要补充的请求头，没有则留空：headers_add=,值不能输入int类型
7.cookies={"cookies":"1"}	#输入需要补充的cookie，没有则留空：cookies=,值不能输入int类型