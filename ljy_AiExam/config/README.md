# config
### 一、配置文件conf.ini填写规范：
[info]
1.loop是线程数，即需要跑多少账号，如需要执行1000个账号，则填1000
#thread是并发数，压力过大时建议降低，云考试建议用100以内

2.host是域名，注意不要加目录

3.token=98587efd85f8fb055a489e38d1341e03，未实现登录流程，改用手动填入token方式实现登录验证

4.tenant-id=LBB0001，租户id

[client]
5.客户端上传学生作答试卷：
	5.1 studentidfile=studentIDList.txt，需要提交试卷的学生ID列表存放到上层的data目录中，数量不能小于loop设置数量
	5.2 gradeid=1,填入学生的年级id，1为1年级
	5.3 subjectname=数学，填入当前扫描的科目名称
	5.4 upload_examname=全题型考试，填入考试名称
	5.5 schoolid=TWDEVS1200000001483，填入学校ID

	*另需手动上传一份完整匹配到学生的试卷，并抓取接口/openapi-aiexamscoring-1-1-1/submit/saveAnswer，获取到的数填入以下对应配置中
	5.6 totalleft=758，整张试卷大小数据
	5.7 totaltop=758，整张试卷大小数据
	5.8 questionidlist=S000586201805,S000586201692，题目ID列表，用逗号隔开，有多少题目就填多少个
	5.9 typelevel=1,2，题目对应的题目类型，必须按照题目的顺序匹配，逗号隔开
	5.10 snapshot=aiexam/2019/7/30/zip/answerSheet/S000586600000000139/S000586200151/2019072601/073009444217/1_origin.jpg，第一份试卷快照的完整路劲
	5.11 snapshot_2=，第二页试卷快照的完整路劲，有就填入，没有则记得删除留空，确定只有一页必须保证该参数是空的

### 二、(可选)自定义发送包：
1.custommethod=True	#需要使用自定义发送包则输入True,不需要则留空custommethod=,启用后，只会使用登陆和该自定义功能，其他功能不会执行

2.httpmethod=post#支持post和get两种方法

3.uri=http://127.0.0.1/path/name #输入需要测试的完整域名+接口路径,不可为空

4.param={"user":0,"pass"=""}#url的参数,拼接在uri后面，可直填入字符，填入json格式会自动转成urlencode格式name?user=0&pass=

5.data={"data":1}	#输入需要post的body内容，没有则留空：data=

6.headers_add={"headers_add":"1"}	#输入需要补充的请求头，没有则留空：headers_add=,值不能输入int类型

7.cookies={"cookies":"1"}	#输入需要补充的cookie，没有则留空：cookies=,值不能输入int类型
