class t1(object):
    def __init__(self,a,b):
        # outfunc.__init__(self,a,b)
        self.a=a+1
        self.b=b+1
        self.__inside()

    def output(self):
        print("t1.a:%s,\nt1.b:%s\n"%(self.a,self.b))

    def __inside(self):
        print("you can't take me outside,*%s*<-come from"%(__name__))

class t2(t1):
    def __init__(self,a,b,c):
        t1.__init__(self,a,b)
        '''
        super() 函数是用于调用父类(超类)的一个方法。
        super 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，
        会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。
        '''
        # super(t2,self).__init__(a,b)
        self.c=c

    def output_2(self):
        print("t2.a:%s,\nt2.b:%s,\nt2.c:%s\n"%(self.a,self.b,self.c))

from test import hello
class call_test(hello):
    def __init__(self,msg):
        hello.__init__(self,msg)

a=t2(1,2,3)
a.output()# 子类继承父类，使用父类的output方法
a.output_2()

c=call_test("pov")
c.output()