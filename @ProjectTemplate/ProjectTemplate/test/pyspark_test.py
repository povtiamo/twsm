from pyspark import SparkContext,SparkFiles
import os,sys
workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, workspace_path)
'''
Master- 它是连接到的集群的URL。
appName- 您的工作名称。
sparkHome - Spark安装目录。
pyFiles - 要发送到集群并添加到PYTHONPATH的.zip或.py文件。
environment - 工作节点环境变量。
batchSize - 表示为单个Java对象的Python对象的数量。设置1以禁用批处理，设置0以根据对象大小自动选择批处理大小，或设置为-1以使用无限批处理大小。
serializer- RDD序列化器。
Conf - L {SparkConf}的一个对象，用于设置所有Spark属性。
gateway  - 使用现有网关和JVM，否则初始化新JVM。
JSC - JavaSparkContext实例。
profiler_cls - 用于进行性能分析的一类自定义Profiler（默认为pyspark.profiler.BasicProfiler）
'''
'''
>>> from pyspark import SparkFiles
>>> path = os.path.join(tempdir, "test.txt")
>>> with open(path, "w") as testFile:
...    _ = testFile.write("100")
>>> sc.addFile(path)
>>> def func(iterator):
...    with open(SparkFiles.get("test.txt")) as testFile:
...        fileVal = int(testFile.readline())
...        return [x * fileVal for x in iterator]
>>> sc.parallelize([1, 2, 3, 4]).mapPartitions(func).collect()
[100, 200, 300, 400]
'''



tempdir=workspace_path
path=os.path.join(tempdir,"test.txt")
sc=SparkContext("local","app")
with open(path,"w") as f:
    _=f.write("122333444455555")
# sc.addFile(path)
# def func(iterator):
#     with open(SparkFiles.get("test.txt")) as testFile:
#         fileVal=int(testFile.readline())
#         return [x*fileVal for x in iterator]
# sc.parallelize([1,2,3,4]).mapPartitions(func).collect()

logData = sc.textFile(path).cache()
# numAs = logData.filter(lambda s: '2' in s).count()
# numBs = logData.filter(lambda s: '3' in s).count()
# print("Line with '2':%d,lines with '3' :%d" % (numAs, numBs))
print(logData.collect())
