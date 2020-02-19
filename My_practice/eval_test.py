import os,sys

#eval(expression[, globals[, locals]])
def func_1(a):
    return a()

def func_2():
    return "abc"

print(eval("func_2()")) #结果是打印abc,eval中的func_2是func_2()函数，不是纯字符串
print(func_1(eval("func_2")))

dic=eval("{'name':name,'age':age}",{"name":"python"},{"age":18})#eval("字符串",全局,局部)
print(dic)