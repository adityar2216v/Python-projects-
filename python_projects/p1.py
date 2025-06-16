class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        #Dot product of two vectors
        return self.x *other.x + self.y *other.y
    def __str__(self):
        return f"(self.x), (self.y))"
#Example usage
v1 =Vector(2, 3)
v2 =Vector(4, 5)
v3=v1+v2
v4=v1- v2
dot_product=v1*v2
print("v1:", v1)
print("v2:", v2)
print("v1+v2:", v3)
print("v1-v2:", v4)
print("v1*v2 (dot product):", dot_product)