''' 
* @Author: lijiayi  
* @Date: 2019-07-02 15:03:22  
* @Last Modified by:   lijiayi  
* @Last Modified time: 2019-07-02 15:03:22  
'''
#!/usr/bin/python
#-*-coding:utf-8-*-
#python3.7

'''
--name包名称
--version(-V)包版本
--author程序的作者
--author_email程序的作者的邮箱地址
--maintainer维护者
--maintainer_email维护者的邮箱地址
--url程序的官网地址
--license程序的授权信息
--description程序的简单描述
--long_description程序的详细描述
--platforms程序适用的软件平台列表
--classifiers程序的所属分类列表
--keywords程序的关键字列表
--packages需要处理的包目录（包含__init__.py的文件夹）
--py_modules需要打包的python文件列表
--download_url程序的下载地址
--cmdclass
--data_files打包时需要打包的数据文件，如图片，配置文件等
--scripts安装时需要执行的脚步列表
--package_dir告诉setuptools哪些目录下的文件被映射到哪个源码包。一个例子：package_dir={'':'lib'}，表示“rootpackage”中的模块都在lib目录中。
--requires定义依赖哪些模块
--provides定义可以为哪些模块提供依赖
--find_packages()对于简单工程来说，手动增加packages参数很容易，刚刚我们用到了这个函数，它默认在和setup.py同一目录下搜索各个含有__init__.py的包。
其实我们可以将包统一放在一个src目录中，另外，这个包内可能还有aaa.txt文件和data数据文件夹。另外，也可以排除一些特定的包
find_packages(exclude=["*.tests","*.tests.*","tests.*","tests"])
--install_requires=["requests"]需要安装的依赖包
--entry_points动态发现服务和插件
'''

import platform
from setuptools import setup,find_packages

setup(
	name='ljy_jxzzzs',
	version='1.0',
	author='lijiayi',
	author_email='lijiayi_zr@twsm.com.cn',
	platform='Windows',
	url='http://192.168.111.244:8888/svn/aischool/doc/02.组织文档/04.测试组/自动化测试/嘉兴中职接口自动化脚本',
	packages=find_packages(),
	install_requires=[
		'requests',
	],
	scripts=[]
)