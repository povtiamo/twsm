from aip import AipOcr


APP_ID = '16600152'
API_KEY = 'oNnWciQupqWPH871GU0T77dy'
SECRET_KEY = 'xMNjsEhc1RbIxGlhWdX9ACDe5LjktDHi'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('C:\\Users\\povti\\Desktop\\test\\test2.jpg')

# """ 调用通用文字识别, 图片参数为本地图片 """
# result=client.basicGeneral(image);
# print(result)

""" 如果有可选参数 """
options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
options["probability"] = "true"

""" 带参数调用通用文字识别, 图片参数为本地图片 """
print(client.basicGeneral(image, options))

# url = "http//www.x.com/sample.jpg"

# """ 调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url);

# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"

# """ 带参数调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url, options)

