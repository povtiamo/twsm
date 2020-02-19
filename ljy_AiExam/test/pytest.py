# 模块配置自验证

import os,sys,traceback
from time import time

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
print(os.getcwd())
try:
	from utils import ljy_run,ljy_config
except Exception:
	ex=Exception("Package utils import False!")
	raise ex

def run_time(func):
    def wrapper():
        start=time()
        func()
        end=time()
        cost_time=end-start
        print("Test done!,cost time:{0:.3}s".format(cost_time))
    return wrapper

@run_time
def start_test():
    c=ljy_config.getconf()
    print("Step 1. ",c.get_config_path())
    print("Step 2. ",c.get_config()["thread"])
    print("Step 3. ",c.getuserlist()[0])
    img_file=c.get_resource_path()
    img_file+="cyberpunk.png"
    if os.path.exists(img_file):
        print("Step 4. ",img_file)
    else:
        print("%s not found!"%(img_file))
    # r=ljy_run.common(0)
    # r.main()

if __name__ == "__main__":
    try:
        start_test()
    except Exception:
        ex=Exception("project test False!")
        raise ex