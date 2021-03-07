from Shapes.Block import Block

scaling_fac = 10

f = open("C:/Users/lera_/OneDrive/Dokumenter/NTNU/KBE/KBE-Prosjekt/Welding/param_vals.txt", "r")

text = f.read()
#text = text.replace("(", "")
#text = text.replace(")", "")

lines = text.split("\n")

for line in lines:
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace(" ", "")
    params = line.split(",") #x #y #width #height

    print(params)

    x = int(params[0])
    y = int(params[1] )
    width = int(params[2] )
    height = int(params[3] )

    

    blockN = Block(x,y,0,width,height,15)
    blockN.initForNX()

#bottom_plate = Block(0,0,-2,50, 50, 2)
#bottom_plate.initForNX()



