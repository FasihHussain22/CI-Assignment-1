import random
import copy
import numpy as np
from PIL import Image, ImageDraw

temp = Image.open('Mona Lisa.png')
# temp.show()
imgRef = Image.new("RGB", temp.size, (255, 255, 255))
imgRef.paste(temp, mask=temp.split()[3])
# imgRef.show()

class Individual:

    def __init__(self, polygons, vertices):
        self.polygonCount = polygons
        self.vertexCount = vertices
        self.polygons = []
        self.color = [random.randint(0,255), random.randint(0,255), random.randint(0,255), 0]
        self.fitness = -1
        self.imgOut = None
        for x in range(polygons):
            self.polygons.append({'points':[], 'color':[random.randint(0,255), random.randint(0,255), random.randint(0,255), 0]})
            for y in range(vertices):
                self.polygons[-1]['points'].append([random.randint(0,imgRef.width-1), random.randint(0,imgRef.height-1)])
    
    def updateFitness(self):
        self.imgOut = Image.new('RGB', imgRef.size, (255, 255, 255))
        draw = ImageDraw.Draw(self.imgOut, 'RGBA')
        draw.polygon([(0,0), (0,imgRef.height), (imgRef.width,imgRef.height), (imgRef.width, 0)], (255, 255, 255, 255))
        for x in self.polygons:
            draw.polygon([tuple(a) for a in x['points']], tuple(x['color']))
        del draw
        self.fitness = np.sum((np.array(imgRef).reshape(-1) - np.array(self.imgOut).reshape(-1))**2)**0.5
    
    def getFitness(self):
        if self.fitness == -1:
            self.updateFitness()
        return round(self.fitness, 2)
    
    def copy(self):
        child = Individual(0, 0)
        child.polygonCount = self.polygonCount
        child.vertexCount = self.vertexCount
        child.polygons = copy.deepcopy(self.polygons)
        return child
    
    def mutate(self):
        randomNumber = random.randint(0,6)
        # print(self.polygonCount)
        if randomNumber == 0:
            # update x of a random point
            polygon = random.randint(0,self.polygonCount-1)
            vertex = random.randint(0,self.vertexCount-1)
            self.polygons[polygon]['points'][vertex][0] = min(max(0, self.polygons[polygon]['points'][vertex][0] + random.randint(0,imgRef.width)//2 - imgRef.width//4),imgRef.width)
        elif randomNumber == 1:
            # update y of a random point
            polygon = random.randint(0,self.polygonCount-1)
            vertex = random.randint(0,self.vertexCount-1)
            self.polygons[polygon]['points'][vertex][1] = min(max(0, self.polygons[polygon]['points'][vertex][1] + random.randint(0,imgRef.height)//2 - imgRef.height//4),imgRef.height)
        elif randomNumber == 2:
            # update r of a random point
            polygon = random.randint(0,self.polygonCount-1)
            self.polygons[polygon]['color'][0] = min(max(0, self.polygons[polygon]['color'][0] + random.randint(0,255)//2 - 255//4),255)
        elif randomNumber == 3:
            # update g of a random point
            polygon = random.randint(0,self.polygonCount-1)
            self.polygons[polygon]['color'][1] = min(max(0, self.polygons[polygon]['color'][1] + random.randint(0,255)//2 - 255//4),255)
        elif randomNumber == 4:
            # update b of a random point
            polygon = random.randint(0,self.polygonCount-1)
            self.polygons[polygon]['color'][2] = min(max(0, self.polygons[polygon]['color'][2] + random.randint(0,255)//2 - 255//4),255)
        elif randomNumber == 5:
            # update alpha of a random point
            polygon = random.randint(0,self.polygonCount-1)
            self.polygons[polygon]['color'][3] = min(max(0, self.polygons[polygon]['color'][3] + random.randint(0,255)//2 - 255//4),255)
            # print('Alpha updated to',self.polygons[polygon]['color'][3])
        elif randomNumber == 6:
            # swap 2 random points in the array to change height
            polygon1 = random.randint(0,self.polygonCount-1)
            polygon2 = random.randint(0,self.polygonCount-1)
            self.polygons[polygon1], self.polygons[polygon2] = self.polygons[polygon2], self.polygons[polygon1]
    
    def show(self):
        self.imgOut.show()

def train(polygons, vertices, generations):
    parent = Individual(polygons, vertices)
    print("Generation No.: 0\t\tFitness:", parent.getFitness())
    for x in range(generations):
        child = parent.copy()
        child.mutate()
        if child.getFitness() < parent.getFitness():
            parent = child
        print("Generation No.:",x+1,"\t\tFitness:", parent.getFitness())
    parent.show()

# a=Individual(0,0)
# print(a.getFitness())

train(15,4,1000000)