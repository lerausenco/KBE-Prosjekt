class Wall():
    def __init__(self, x,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def params(self):
        return self.x, self.y, self.width, self.height
    
    def print(self):
        print("[X,Y]: ", self.x, self.y, "Width: ", self.width, " Height:", self.height)