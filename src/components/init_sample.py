#定义一个Person类，父类（超类，基类）
class Person:
    def __init__(self,name): # 定义私有类
        self.name = name
    def run(self):#定义一个类函数
        print('person:'+ self.name+'正在奔跑啊啊啊')

class Student(Person): #继承自Person
    def __init__(self,name,set,age):# 定义私有类
        #调用父类的构造方法
       # Person.__init__(name) # 方式一：直接指定父类的构造方法
        super().__init__(name)# 方式二：使用super()，推荐使用该方法
        # 自己类中的构造方法且父类中没有的，直接定义即可
        self.set = set
        self.age = age
    def study(self): #定义一个类函数
        print('stadent:' + self.name + '正在学习。。。。')
    def show(self):#定义一个类函数
        print('name:%s , set:%s,age:%s'%(self.name,self.set,self.age))
    #可以自定义n个类函数 。。。

if __name__=="__main__":
  stu = Student('ccx','man',22)
  stu.run() #因为继承了父类，当然也可以直接调用父类函数
  stu.study()
  stu.show()
