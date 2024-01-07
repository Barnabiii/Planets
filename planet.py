
import pygame,math,random

from pygame.constants import WINDOWEXPOSED
pygame.init

class vec():
    def __init__(self,x,y):
        self.x = x
        self.y = y 
    def xValue(self):
        return self.x
    def yValue(self):
        return self.y   
    def mag(self):
        n1 = self.x**2
        n2 = self.y**2
        n3 = math.sqrt(n1+n2)
        return n3

def verif_fusion(Data):
    plntR = [0,0,0,0,0,-1]
    countR = -1
    while (plntR[5] != Data[len(Data)-1][5]):
        countR += 1
        plntR = Data[countR]

        plntA = [0,0,0,0,0,-1]
        countA = -1
        while (plntA[5] != Data[len(Data)-1][5]):
            countA += 1
            plntA = Data[countA]
            if(plntR[5] != plntA[5]):
                vec_distance = vec(plntR[0][0]-plntA[0][0],plntR[0][1]-plntA[0][1])
                if(vec_distance.mag() <= plntR[3] + plntA[3]):
                    if(plntR[2] > plntA[2]):
                        if(plntR[5] < plntA[5]):
                            newPlnt = [[plntR[0][0],plntR[0][1]],[plntR[1][0]/2+plntA[1][0]/2,plntR[1][1]/2+plntA[1][1]/2],plntR[2]+plntA[2],plntR[3]+plntA[3],[plntR[4][0]/2+plntA[4][0]/2,plntR[4][1]/2+plntA[4][1]/2,plntR[4][2]/2+plntA[4][2]/2],plntR[5]]
                        else:
                            newPlnt = [[plntR[0][0],plntR[0][1]],[plntR[1][0]/2+plntA[1][0]/2,plntR[1][1]/2+plntA[1][1]/2],plntR[2]+plntA[2],plntR[3]+plntA[3],[plntR[4][0]/2+plntA[4][0]/2,plntR[4][1]/2+plntA[4][1]/2,plntR[4][2]/2+plntA[4][2]/2],plntA[5]]
                    else:
                        if(plntR[5] < plntA[5]):
                            newPlnt = [[plntA[0][0],plntA[0][1]],[plntR[1][0]/2+plntA[1][0]/2,plntR[1][1]/2+plntA[1][1]/2],plntR[2]+plntA[2],plntR[3]+plntA[3],[plntR[4][0]/2+plntA[4][0]/2,plntR[4][1]/2+plntA[4][1]/2,plntR[4][2]/2+plntA[4][2]/2],plntR[5]]
                        else:
                            newPlnt = [[plntA[0][0],plntA[0][1]],[plntR[1][0]/2+plntA[1][0]/2,plntR[1][1]/2+plntA[1][1]/2],plntR[2]+plntA[2],plntR[3]+plntA[3],[plntR[4][0]/2+plntA[4][0]/2,plntR[4][1]/2+plntA[4][1]/2,plntR[4][2]/2+plntA[4][2]/2],plntA[5]]
                    if(plntR[5] < plntA[5]):
                        Data.pop(plntA[5])
                        Data.pop(plntR[5])
                        index = plntA[5]
                    else:
                        Data.pop(plntR[5])
                        Data.pop(plntA[5])
                        index = plntR[5]
                    
                    Data.insert(newPlnt[5],newPlnt)

                    while (index != len(Data)):
                        Data[index][5] -= 1
                        index += 1 
                    
                    return Data,0
    return Data,1
                
def calculate_pos(Pdata,g,DT,smooth):
    data = Pdata
    need = 0
    while (need == 0):
        feedBack = verif_fusion(data)
        data = feedBack[0]
        need = feedBack[1]

    for planetR in data:
        Forces = []
        n1 = 0
        n2 = 0

        for planetA in data:
            if(planetR[5] != planetA[5]):

                vec_RA = vec(planetA[0][0]-planetR[0][0],planetA[0][1]-planetR[0][1])
                


                vec_u = vec(vec_RA.xValue()/vec_RA.mag(),vec_RA.yValue()/vec_RA.mag())

                n1 = g*planetR[2]*planetA[2]
                n2 = vec_RA.xValue()**2+vec_RA.yValue()**2+smooth
                n3 = n1/n2

                vec_Force = vec(vec_u.xValue()*n3,vec_u.yValue()*n3)
                Forces.append([vec_Force.xValue(),vec_Force.yValue()])
                
        
       
        sigma_F = [0,0]
        for i in Forces:
            sigma_F[0] = sigma_F[0]+i[0]
            sigma_F[1] = sigma_F[1]+i[1]
    
        vec_Acc = vec(sigma_F[0]/planetR[2],sigma_F[1]/planetR[2])
        n1 = vec_Acc.xValue()*DT
        n2 = vec_Acc.yValue()*DT
        vec_Spe = vec(n1+planetR[1][0],n2+planetR[1][1])
        n1 = vec_Spe.xValue()*DT
        n2 = vec_Spe.yValue()*DT
        vec_Pos = vec(n1+planetR[0][0],n2+planetR[0][1])


        Pdata[planetR[5]][1] = [vec_Spe.xValue(),vec_Spe.yValue()]
        Pdata[planetR[5]][0] = [vec_Pos.xValue(),vec_Pos.yValue()]

    Pdata = data

def drawPlanets(Pdata):
    for planet in range(len(Pdata)):
        pygame.draw.circle(screen, Pdata[planet][4], Pdata[planet][0], Pdata[planet][3])

def init_file(name):
    with open(name + ".txt") as txt:
        file = txt.readlines()

    newFile = []

    for L in file:
        newLine = L.replace("\n", "")
        newFile.append(newLine)

    id = 0
    dataP = []

    for L in newFile:
        if L != "":
            if L[0] == "{" and L[len(L)-1] == "}":
                L = L.replace("{", "")
                L = L.replace("}", "")
                elements = L.split(":")
                data = []
                
                for elem in elements:
                    if (elem[0] == "(" and elem[len(elem)-1] == ")"):
                        elem = elem.replace("(", "")
                        elem = elem.replace(")", "")
                        elem = elem.split(",")
                        e = []
                        for i in elem:
                            e.append(float(i))
                        data.append(e)
                    else:
                        data.append(float(elem))

                data.append(id)
                dataP.append(data)
                id +=1
    
    return dataP

def INFO():
    print("\n---------------- info ----------------\n")
    print("The DeltaTime(DT) is a value that ")
    print("represented the amount of time elapsed ")
    print("in the simulation between each frame\n\n")
    print("During the simulation you can modify")
    print("the Deltatime(DT):\n")
    print("z strongly increases DT    s strongly decreases DT")
    print("e increases moderately DT    d decreases moderately DT")
    print("r hardly increases DT    f hardly decreases DT")
    print("\n---------------- info ----------------\n")

def galaxy(stars,count):
    for i in range(count):
        x = random.randint(0,screenL)
        y = random.randint(0,screenH)
        if i == 0:
            stars.append([[screenL/2,screenL/2],[0,0],1000000000,10,[255,255,255],i])    
        else:
            stars.append([[x,y],[0,0],1,1,[255,255,255],i])
    return stars

screenL = 1000
screenH = 1000
loop = True

while loop:
    DeltaTime = input("what is the DeltaTime value (for more info write, info): ")
    if(DeltaTime == "info"):
        INFO() 
    else:
        try:
            DeltaTime = float(DeltaTime)
            loop = False
        except:
            print("I did not understand")

Planets_Data = None

while Planets_Data == None:
    fileName = input("\nwhat file do you want to use to initalise (only the name, or write galaxy): ")
    if (fileName == "galaxy"):
        fileName = input("how many stars in your galaxy ?: ")
        #try:
        Planets_Data = []
        Planets_Data = galaxy(Planets_Data,int(fileName))
        #except:
         #   print("this isn't a number")
    else:
        try:
            Planets_Data = init_file(fileName)
        except:
            print("This file dosen't exist") 

loop = True
G = 1
smoothDivision = 0.3
screen = pygame.display.set_mode((screenL, screenH))
pygame.display.set_caption("planets")

delay = pygame.time.Clock()
pygame.key.set_repeat(10,10)

while (loop):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if(event.type == pygame.KEYDOWN):
            
            if(event.key == pygame.K_z):
                DeltaTime += 0.01
            if(event.key == pygame.K_s):
                DeltaTime -= 0.01
            if(event.key == pygame.K_e):
                DeltaTime += 0.0001
            if(event.key == pygame.K_d):
                DeltaTime -= 0.0001
            if(event.key == pygame.K_r):
                DeltaTime += 0.00001
            if(event.key == pygame.K_f):
                DeltaTime -= 0.00001

    calculate_pos(Planets_Data,G,DeltaTime,smoothDivision)
    pygame.draw.rect(screen, (0,0,0), (0,0,screenL,screenH))
    drawPlanets(Planets_Data)

    pygame.display.update()

pygame.quit