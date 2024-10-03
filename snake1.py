import pygame
from pygame.math import Vector2
from pygame import Rect
import os
import random 

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Unit():
    def __init__(self,state,position,tile=None, color=(255,255,255), father=None, prevpos=None, childs=[]):
        self.state = state
        self.position = position
        self.tile = tile
        self.color = color
        self.father = father
        self.childs = childs
        self.prevpos = prevpos

    def move(self,moveVector):
        pass

class Snake(Unit):
    
    def move(self, moveVector):
        self.prevpos=self.position
        newPos = self.position + moveVector

        # Don't allow positions outside the world
        if newPos.x < 0 or newPos.x >= self.state.worldWidth \
        or newPos.y < 0 or newPos.y >= self.state.worldHeight:
            return
        
        # Eat apple 
        for unit in self.state.units:
            if newPos == unit.position and type(unit) == Apple :
                if len(self.childs)==0:
                    self.childs.append(SnakeChild(self.state,self.prevpos,color=(0,255,255), father=self))
                    self.state.units.append(self.childs[-1])
                    
                else:
                    self.childs.append(SnakeChild(self.state,self.childs[-1].prevpos,color=(0,255,255), father=self.childs[-1]))
                    self.state.units.append(self.childs[-1])
                self.state.apples.position=newpos([x.position for x in self.state.units])
                print(self.state.apples.position)
                
            elif newPos == unit.position and type(unit) == SnakeChild:
                newPos=self.position


        self.position = newPos
    
class SnakeChild(Snake):
    
    def move(self, moveVector): 
        self.prevpos = self.position
        newPos = self.father.prevpos

        for unit in self.state.units:
            if newPos == unit.position and type(unit) in (Snake, SnakeChild) :
                newPos= self.position
                

        

        # # Don't allow positions outside the world
        # if newPos.x < 0 or newPos.x >= self.state.worldWidth \
        # or newPos.y < 0 or newPos.y >= self.state.worldHeight:
        #     return
        
        # # Eat apple 
        # for unit in self.state.units:
        #     if newPos == unit.position:
        #         return
        
        self.position = newPos   

    



class Apple(Unit):
    def move(self, moveVector):
        raise RuntimeError("Apple can't move")

class GameState():
    def __init__(self):
        self.worldSize = Vector2(30,30)
        misnake=Snake(self,Vector2(5,4),color=(0,0,255))
        firstchild=SnakeChild(self,Vector2(5,3),color=(0,255,255), father=misnake)
        secondchild=SnakeChild(self,Vector2(5,2),color=(0,255,255), father=firstchild)
        misnake.childs=[firstchild,secondchild]
        self.apples=Apple(self,Vector2(10,3))
        self.units=[
            misnake,
            self.apples,
            misnake.childs[0],
            misnake.childs[1]
        ]
        
    @property
    def worldWidth(self):
        return int(self.worldSize.x)

    @property
    def worldHeight(self):
        return int(self.worldSize.y)

    def update(self,moveSnakeCommand):
        for unit in self.units:
            if type(unit) in (Snake, SnakeChild):
              unit.move(moveSnakeCommand)


class UserInterface():
    def __init__(self):
        pygame.init()
        
        # Game state
        self.gameState = GameState()


        # Rendering properties
        self.cellSize = Vector2(15,15)
        
        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Discover Python & Patterns")
        # pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveSnakeCommand=Vector2(0,0)
        self.prevmoveSnakeCommand=Vector2(10,10)
        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True
        self.KeyList=["A"]
    
    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
       
            #It manages key pressing: it is when a key goes from unpressed to pressed. It is different from holding or releasing a key.
            elif event.type == pygame.KEYDOWN:
                #The Espace key quit the game (like the pygame.QUIT event).
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                
                elif event.key == pygame.K_RIGHT or pygame.K_LEFT or pygame.K_DOWN or pygame.K_UP:
                    self.moveSnakeCommand = Vector2(0,0)
                    # The arrow keys change the x and y coordinates of the rectangle.
                    if event.key == pygame.K_RIGHT:
                        if self. KeyList[-1]=="L":
                            self.moveSnakeCommand.x=-1
                        else:
                            self.moveSnakeCommand.x = 1
                            self. KeyList=[]
                            self. KeyList.append("R")
                    elif event.key == pygame.K_LEFT:
                        if self. KeyList[-1]=="R":
                            self.moveSnakeCommand.x=1
                        else:
                            self.moveSnakeCommand.x = -1
                            self. KeyList=[]
                            self. KeyList.append("L")
                    elif event.key == pygame.K_DOWN:
                        if self. KeyList[-1]=="U":
                            self.moveSnakeCommand.y=-1
                        else:
                            self.moveSnakeCommand.y = 1
                            self. KeyList=[]
                            self. KeyList.append("D")
                    elif event.key == pygame.K_UP:
                        if self. KeyList[-1]=="D":
                            self.moveSnakeCommand.y = 1
                        else:
                            self.moveSnakeCommand.y = -1
                            self. KeyList=[]
                            self. KeyList.append("U")

                    

    def update(self): 
        if self.moveSnakeCommand != self.prevmoveSnakeCommand and self.moveSnakeCommand!=Vector2(0,0):
            
            self.prevmoveSnakeCommand=self.moveSnakeCommand
            
                  
        if (self.moveSnakeCommand.x == -self.prevmoveSnakeCommand.x and self.moveSnakeCommand.y==0) or (self.moveSnakeCommand.y == -self.prevmoveSnakeCommand.y and self.moveSnakeCommand.x==0):
            print(self.prevmoveSnakeCommand)
            print(self.moveSnakeCommand)
            self.gameState.update(self.moveSnakeCommand)

        else:    
            self.gameState.update(self.moveSnakeCommand)

        
        
    
    def renderGround(self,position,tile):
        # Location on screen
        #spritePoint = position.elementwise()*self.cellSize
    
        # Texture
        #texturePoint = tile.elementwise()*self.cellSize
        #textureRect = Rect(int(texturePoint.x), int(texturePoint.y), self.cellWidth,self.cellHeight)
        #self.window.blit(self.groundTexture,spritePoint,textureRect)    
        pass


    def renderUnit(self,unit):
        # Location on screen
        spritePoint = unit.position.elementwise()*self.cellSize

        pygame.draw.rect(self.window,unit.color,(spritePoint.x,spritePoint.y,self.cellWidth,self.cellHeight))
    


    def render(self):
        #... Render game state ...
        self.window.fill((0,0,0))
        
      # Units
        for unit in self.gameState.units:
            self.renderUnit(unit)
        
        pygame.display.update()  

    def run(self):    
        while self.running:
            self.processInput()
            self.update()
            self.render()        
            self.clock.tick(15)
    
def newpos(lista:list):
    inf_lim=0
    sup_lim=29
    vector=Vector2(random.randint(inf_lim,sup_lim),random.randint(inf_lim,sup_lim))
    while any([x == vector for x in lista]):
        vector=Vector2(random.randint(inf_lim,sup_lim),random.randint(inf_lim,sup_lim))
    return vector


        



userInterface = UserInterface()
userInterface.run()
pygame.quit()