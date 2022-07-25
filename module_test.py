class Bird:
    ruClassName = "Птица"
    objInstancesCount = 0

    def __init__(self, name, id, age):
        self.name = name
        self.id = id
        self.age = age
        Bird.objInstancesCount = Bird.objInstancesCount + 1

    def info(self):
        print(self.name)
        print("Идентификационный номер: " + str(self.id))
        print("Возраст: " + str(self.age))
