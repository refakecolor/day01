class Person():
    def __init__(self, name):
        self.__name = name
        print('Peron init...')

    def get_name(self):
        return self.__name

class Mother(Person):
    def __init__(self, name, age, job):
        # super(Mother, self).__init__(name, age)
        super().__init__(name,age)
        self.__job = job
        print('Mother init...')

    def get_job(self):
        return self.__job

class Father(Person):
    def __init__(self,name, age):
        # super(Father, self).__init__(name)
        super().__init__(name)
        self.__age = age
        print('Father init...')

    def get_age(self):
        return self.__age

class Son(Mother, Father):
    def __init__(self, name, age, gender, job):
        # super(Son, self).__init__(name, age, job)
        super().__init__(name,age,job)
        self.__gender = gender
        print('Son init...')


    def get_gender(self):
        return self.__gender

s = Son('Tom', 18, '男','老师')
print(s.get_name(),s.get_age(),s.get_gender(),s.get_job())