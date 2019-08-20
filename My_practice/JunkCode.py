import random, sys, os, string,traceback
print('start..')
TargetPath 	= sys.argv[1]

FileExt = ['png','jpg', 'mp3', 'lua', 'json']

def randomStr(randomlength=8):
	str = ''
	chars = '_!@#$%^&*()_+,./;~`!'
	length = len(chars) - 1
	for i in range(randomlength):
	    str+=chars[random.randint(0, length)]
	return str

def newJunkFile(path, ext, randomNum=95):
	rint = random.randint(1,100)
	if rint > randomNum:
		fileName = ''.join(random.sample(['Mgr','Helper','Load','Base','Notificat','Tcp','Ton','Def','Check','File','Bind','er','Fng','Cache','Image','zhucheng','bg','Data','Pool','My','Cocos','Work','SDK','config','Ccb','Player', 'Fight', 'main', 'bit'], 2)).replace(' ','')
		full_path = path + '/' + fileName + '.' + ext
		print(full_path)
		rstr = randomStr(random.randint(10,1300))
		nFd = open(full_path,'wb')
		# write flag
		nFd.write('\xDD')
		nFd.write('\xFF')
		nFd.write('\xDD')
		nFd.write('\xFF')
		nFd.write(rstr)
		nFd.close()

def newJunkDir(path):
	rint = random.randint(1,100)
	if rint > 80:
		fileName = ''.join(random.sample(['pack','frame','vip','view','Helper','Load','Base','Chat','common','Ton','Def','Check','File','Bind','model','Game','Cache','item','zhucheng','bg','Data','Pool','My','Cocos','Work','SDK','config','Ccb','Player', 'Fight', 'main', 'bit', 'team'], 2)).replace(' ','')
		dirname = path + '/' + fileName
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		print(fileName,dirname)

		newJunkFile(dirname, 'lua', 10)    

def checkPath(path):
	try:
		for item in os.listdir(path):
			full_path = os.path.join(path, item)
			file_ext = item.split(".")[-1]
			if os.path.isdir(full_path):
				newJunkDir(full_path)
				checkPath(full_path)
			if file_ext not in FileExt:
				continue
			newJunkFile(path, file_ext, 95)
	except Exception as ex:
		print(ex)

checkPath(TargetPath)

print('done..')
