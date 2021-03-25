class Wall():

    """
        Class to store wall objects extracted from picture
        Constructor args:
            x - x pixel position
            y - y pixel position
            width - dimension of wall in x direction
            height - dimension of wall in y direction
            
    """
    def __init__(self, x,y, width, height, z_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.z_height = z_height
    
    def params(self):
        return self.x, self.y, self.width, self.height, self.z_height
    
    def print(self):
        print("[X,Y]: ", self.x, self.y, "Width: ", self.width, " Height:", self.height, "Z_height", self.z_height)