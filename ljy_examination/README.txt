一、准备环境(必须)：
1.安装Python3.7，安装过程参考"python3安装.docx"
2.解压Python三方支持库(site-packages.zip)所有文件到运行电脑指定目录(Python安装目录\Python\Lib\site-packages\)中,参考"python3安装.docx"
3.目前只在Windows环境运行
4.程序在当前目录的ljy_examination文件夹中

二、配置文件conf.ini填写规范：
1.loop是线程数，即需要跑多少账号，如需要执行1000个账号，则填1000
2.passwd是登录密码
3.host是域名，注意不要加目录
4.线上考试自动作答(暂时仅支持以下四种题型#1单选题、2多选题、4填空题、5简答题)：
	4.1 userlistfile=usernamelist.txt是登录账号列表，按照格式替换成需要使用的账号，账号数量不能少于loop设置数量
	4.2 examname=千人斩测试,填入考试名称
	4.3 r_questionidlist=CCEXXX1204522,CCEXXX1204685，当前考试的题目ID列表，根据答题卡的题目ID用逗号隔开组成列表填入
	4.4 r_typelevel=1,1,4,5，题目对应的题目类型，必须按照题目的顺序匹配，逗号隔开
	4.5 answerlist=1,2,123/123,12345，学生作答列表，必须按照题目的顺序匹配，用逗号隔开
		#填空题每空作答用/隔开，如有一个三空的填空题，在该填空题的位置输入a/b/c,如果题目有多个空，脚本配置只输入了一个空的作答，则批改会出现只显示一个空的问题
		#选择题输入数字对应的选项(0A/1B/2C/3D)，填空题所有空都共用一个作答内容
	附：题目ID获取方法：
		1.打开抓包工具
		2.创建考试进入组卷页面
		3.选择好题目后，点击预览进入试卷预览页面
		4.查看接口"/examination/api/paper/save"中的发送内容
		5.questionList字段的questionID为对应顺序题目的题目ID，填入conf.ini对应字段即可
5.客户端上传学生作答试卷：
	5.1 studentidfile=studentIDList.txt，需要提交试卷的学号列表，按照格式替换成需要使用的学号，学号数量不能少于loop设置数量
	5.2 upload_examname=千人斩测试，填入考试名称
	5.3 schoolid=TWDEVS1200000001483，填入学校ID
	*另需手动上传一份完整匹配到学生的试卷，并抓包获取需要的数据，后面所有的学生的试卷都会套用第一份手动上传的试卷
	*抓取接口/examination/ClientApi/saveStudentAnswer，填入第一份试卷的以下数据
	5.5 totalleft=758，整张试卷大小数据
	5.6 totaltop=758，整张试卷大小数据
	5.7 top_left=924/985，每个题目作答图片切割大小，top和left用/隔开，手动填入所有题目中最大的值
	5.8 questionidlist=S000586201805,S000586201692，题目ID列表，用逗号隔开，有多少题目就填多少个
	5.9 typelevel=1,1,2，题目对应的题目类型，必须按照题目的顺序匹配，逗号隔开
	5.10 snapshot=aiexam/2019/7/30/zip/answerSheet/S000586600000000139/S000586200151/2019072601/073009444217/1_origin.jpg
		第一份试卷快照的完整路劲
	5.11 snapshot_2=，第二页试卷快照的完整路劲，有就填入，没有则记得删除留空，确定只有一页必须保证该参数是空的


三、运行脚本
1.准备好环境后
2.线上作答功能，运行"C05云考试自动作答脚本\ljy_examination\start.bat"即可
3.线下学生试卷扫描功能，运行"C05云考试自动作答脚本\ljy_examination\start_client.bat"即可
4.两个功能是分开单独运行的

四、实现功能
线上作答：
1.根据账号表批量登录账号
2.登录后进入配置中的考试
3.提交所有题目的作答数据
线下学生作答：
1.根据学号表批量套用上传第一份手动上传的作答试卷数据
2.提交所有学生的试卷

五、(可选)自定义发送包：
1.custommethod=True	#需要使用自定义发送包则输入True,不需要则留空custommethod=,启用后，只会使用登陆和该自定义功能，其他功能不会执行
2.httpmethod=post#支持post和get两种方法
3.uri=http://127.0.0.1/path/name #输入需要测试的完整域名+接口路径,不可为空
4.param={"user":0,"pass"=""}#url的参数,拼接在uri后面，可直填入字符，填入json格式会自动转成urlencode格式name?user=0&pass=
5.data={"data":1}	#输入需要post的body内容，没有则留空：data=
6.headers_add={"headers_add":"1"}	#输入需要补充的请求头，没有则留空：headers_add=,值不能输入int类型
7.cookies={"cookies":"1"}	#输入需要补充的cookie，没有则留空：cookies=,值不能输入int类型