class hello(object):
    def __init__(self,args):
        self.msg=args

    def output(self):
        print("hello %s,welcome to %s"%(self.msg,__name__))

if __name__ == "__main__":
    h=hello("home")
    h.output()