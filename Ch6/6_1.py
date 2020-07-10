class Point:
    def __init__(self):
        self.x = input()
        self.y = input()
    
    def setx(self,x):
        self.x = input()

    def sety(self,y):
        self.y = input()

    def get(self):
        tup = (self.x, self.y)
        return tup

    def mov(self,dx,dy):
        self.x = self.x + dx
        self.y = self.y + dy



Z = Point()
print(Z.get())

