import sys
sys.setrecursionlimit(100000)
import pygame
import sys
import math
import random
import time

#增加积分功能
#增加排行榜
# class 
class Grid:
    cellWidth=30
    grid=[]
    default=0
    maxX=0
    maxY=0
    snake=None
    food=None
    foods=[]
    foodcounter=0
    frameindex=0
    framenum=60
    frame= pygame.USEREVENT
    bg=pygame.image.load('ground.jpeg')
    # bg=None
    # bgpos=bg.get_rect()
    # bgsprit_rect=pygame.Rect(0,0,130,130)
    tile=None
    ball=None
    score=None
    bgmap=None
    # @profile
    def __init__(self,size):
        
        # self.bgpos=(size[0]/2,size[1]/2)
        self.ball=Ball()
        self.score=Score()
        self.size=size
        self.maxX=math.ceil(size[0]/self.ball.size[0])
        self.maxY=math.ceil(size[1]/self.ball.size[1])
        self.initGrid()
        self.addFood()
        self.addSnake()
        # self.bg.set_clip(0,0,130,130)
        # pygame.Surface.blit()
        # self.bg.blit()
        # self.tile=self.bg.subsurface((0,264,133,132))
        self.fillBg()
        # self.bgmap.blit(self.bg,(133,0,133,132),(0,0,133,132))
        pygame.time.set_timer(self.frame,math.ceil(1000/self.framenum))
    def fillBg(self):
        self.bgmap=pygame.Surface(self.size)
        imagesize=(130,128)
        maxX=math.ceil(self.size[0]/imagesize[0])
        maxY=math.ceil(self.size[1]/imagesize[1])
        for x in range(maxX):
            for y in range(maxY):
                self.bgmap.blit(self.bg,(x*imagesize[0],y*imagesize[1],imagesize[0],imagesize[1]),(1,265,imagesize[0],imagesize[1]))

    def initGrid(self):
        self.grid=[]
        for i in range(self.maxX):
            self.grid.append([])
            for j in range(self.maxY):
                self.grid[i].append(self.default)
    def addSnake(self):
        self.snake=Snake(5,self)
    def addFood(self):
        self.food=Food(self)
    def listenEvent(self,keycode,callback=None):
        self.snake.setSnakeFace(keycode)
    def render(self,screen,event,callback=None):
        if(event.type==pygame.KEYDOWN):
            self.listenEvent(event.key,callback)
        if(event.type==self.frame):
            self.frameindex=(self.frameindex+1)%self.framenum
            
        if(self.frameindex%self.snake.speed==0):
            screen.blit(pygame.transform.scale(self.bgmap, self.size),(0,0))
            # screen.blit(self.tile,(0,0))
            self.ball.setScreen(screen)
            self.snake.go(callback)
            self.food.addToGrid()
            snakedata=self.snake.data()
            length=len(snakedata['snake'])
            for index in range(length):
                self.ball.draw(snakedata['snake'][index][0],snakedata['snake'][index][1],snakedata['snakeObj'][index])
            for food in self.food.foods:
                self.ball.draw(food[0],food[1],food[2])
            self.score.draw(screen)
            pygame.display.flip()
            # t2=time.perf_counter()
            # print(t2-t1)
    
class Score:
    score=0
    font=None
    def __init__(self):
        self.score=0
        self.font=pygame.font.Font("STHeiti Medium.ttc",24)
    def add(self,num):
        self.score=self.score+num
    def draw(self,screen):
        scoretext = self.font.render("分数:"+str(self.score), True, (255, 0, 0), (0, 0, 255))
        textRectObj3 = scoretext.get_rect()
        textRectObj3.center = (10, 10)
        screen.blit(scoretext, textRectObj3)
        # self.font.render_to(screen,(10,10),"分数:"+str(self.score),fgcolor=GOLD,bgcolor=BLACK,)
        # screen.blit()

class Ball:
    size=(30,30)
    screen=None
    head=None
    def __init__(self):
        self.head=pygame.image.load('head.jpg')

    def setScreen(self,screen):
        self.screen=screen
    def draw(self,x,y,type):
        radius=math.ceil(self.size[0]/2)
        if(type==-1 or type==1):
            pygame.draw.circle(self.screen,[255,255,255],self.__getPosXY(x,y),radius,0)
        if(type==-2 or type==2):
            pygame.draw.circle(self.screen,[255,0,0],self.__getPosXY(x,y),radius,0)
        if(type==-3 or type==3):
            pygame.draw.circle(self.screen,[0,255,0],self.__getPosXY(x,y),radius,0)
        if(type==-4 or type==4):
            pygame.draw.circle(self.screen,[0,0,255],self.__getPosXY(x,y),radius,0)
        if(type==9):
            postuple=self.__getPosXY(x,y)
            pos=[
                math.ceil(postuple[0]-self.size[0]/2),
                math.ceil(postuple[1]-self.size[1]/2)
            ]
            self.screen.blit(pygame.transform.scale(self.head, (self.size[0],self.size[1])),pos)
    def __getPosXY(self,x,y):
        x=math.ceil(x*self.size[0]+self.size[0]/2)
        y=math.ceil(y*self.size[1]+self.size[1]/2)
        return (x,y)
class Snake:
    minlength=3
    x=0
    y=0
    snake=[]
    defaultdirection='r'#u向上d向下l向左r向右
    face='r'
    isDead=False
    maxX=0
    maxY=0
    grid=[]
    snakeobj=[]
    food=None
    throughWall=True
    #帧数
    speed=10
    def __init__(self,length,grid):
        self.maxX=grid.maxX
        self.maxY=grid.maxY
        self.grid=grid.grid
        self.food=grid.food
        self.snakeobj=[]
        self.snake=[]
        self.score=grid.score
        self.append([self.x+length-1,0],9)
        for i in range(1,length):
            self.isDead=False
            self.append([self.x+length-i-1,0],-1)
    
    def pop(self,n=-1):
        self.snakeobj.pop(n)
        self.snake.pop(n)
    
    def insert(self,n,pos,val):
        self.snakeobj.append(val)
        self.snake.insert(n,pos)

    def append(self,pos,val):
        self.snakeobj.append(val)
        self.snake.append(pos)

    def canGoPos(self,x,y):
        if(self.throughWall!=True):
            if(x<0 or x>=self.maxX):
                return False
            if(y<0 or y>=self.maxY):
                return False
        for pos in self.snake:
            if(pos==[x,y]):
                return False
        return True

    def checkDead(self,callback):
        if(self.isDead==True):
            callback('end')
            return True
        return False
    #todo: 再增加2项超能力 天降食物 限时穿墙
    def activePower(self):
        length=len(self.snakeobj)
        a=length-1
        b=length-2
        c=length-3
        if(length>=3):
            if(self.snakeobj[a]==self.snakeobj[b] and self.snakeobj[a]==self.snakeobj[c]):
                if(self.snakeobj[a]==-2):
                    self.speedUp()
                    return
                if(self.snakeobj[a]==-3):
                    self.speedDown()
                    return
                if(self.snakeobj[a]==-4):
                    self.shorter(6)
                    return
    #加速超能力
    def speedUp(self):
        self.speed=self.speed-1
        if(self.speed<=0):
            self.speed=1
        self.shorter(3)
    #减速超能力
    def speedDown(self):
        self.speed=self.speed+1
        if(self.speed>=60):
            self.speed=60
        self.shorter(3)
    #缩短超能力
    def shorter(self,n):
        length=len(self.snakeobj)
        if(length-self.minlength-n<0):
            n=length-self.minlength
        for i in range(n):
            self.pop()

    def getNextPos(self,currentpos,direction):
        nextX=0
        nextY=0
        if(direction=='r'):
            nextX=currentpos[0]+1
            nextY=currentpos[1]
        if(direction=='l'):
            nextX=currentpos[0]-1
            nextY=currentpos[1]
            newpos=[currentpos[0]-1,currentpos[1]]
        if(direction=='u'):
            nextX=currentpos[0]
            nextY=currentpos[1]-1
            newpos=[currentpos[0],currentpos[1]-1]
        if(direction=='d'):
            nextX=currentpos[0]
            nextY=currentpos[1]+1
        if(self.throughWall==True):
            if(nextX<0):
                nextX=self.maxX-1
            if(nextX>=self.maxX):
                nextX=0
            if(nextY<0):
                nextY=self.maxY-1
            if(nextY>=self.maxY):
                nextY=0
            # nextX=
        newpos=[nextX,nextY]
        return newpos

    def goNext(self,direction):
        nextPos=self.getNextPos(self.snake[0],direction)
        if(self.canGoPos(nextPos[0],nextPos[1])):
            if(self.canEat(nextPos[0],nextPos[1])==False):
                self.snake.pop()
                self.snake.insert(0,nextPos)
            else:
                type=self.food.getFoodType(nextPos[0],nextPos[1])
                self.food.removeFromGrid(nextPos[0],nextPos[1])
                self.insert(0,nextPos,-1*type)
                self.score.add(1)
                self.activePower()
        else:
            self.isDead=True

    def canEat(self,x,y):
        if(self.grid[x][y]>0):
            return True
        return False
    def go(self,callback):
        if(self.checkDead(callback)==False):
            self.goNext(self.face)

    def setSnakeFace(self,keycode):
        oldface=self.face
        if(keycode==119 and self.face!='d'):
            self.face='u'
        if(keycode==115 and self.face!='u'):
            self.face='d'
        if(keycode==97 and self.face!='r'):
            self.face='l'
        if(keycode==100 and self.face!='l'):
            self.face='r'
        nextpos=self.getNextPos(self.snake[0],self.face)
        if(self.snake[1]==nextpos):
            self.face=oldface

    def data(self):
        data={'snake':self.snake,'snakeObj':self.snakeobj}
        # print(data)
        return data
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple py2app

class Food:
    x=-1
    y=-1
    maxX=0
    maxY=0
    maxFoodNum=20
    counter=0
    foods=[]
    griddata=[]
    def __init__(self,grid):
        self.maxX=grid.maxX
        self.maxY=grid.maxY
        self.grid=grid
        self.counter=0
        self.foods=[]
    def addToGrid(self):
        if(len(self.foods)<self.maxFoodNum):
            self.x=random.randint(0,self.maxX-1)
            self.y=random.randint(0,self.maxY-1)
            self.griddata=self.grid.grid
            if(self.griddata[self.x][self.y]==0):
                type=random.randint(1,4)
                self.griddata[self.x][self.y]=type
                self.foods.append([self.x,self.y,type])
    def removeFromGrid(self,x,y):
        for i in range(len(self.foods)):
            if(self.foods[i][0]==x and self.foods[i][1]==y):
                self.foods.pop(i)
                self.griddata[x][y]=0
                break;
    
    def getFoodType(self,x,y):
        return self.griddata[x][y]

class RetroSnaker:
    startbtn=pygame.image.load('start_game.png')
    status='wait' #wait start end
    size=None
    screen=None
    statusPage=None
    def __init__(self,width,height):
        pygame.init()
        self.size = width, height   # 设置窗口大小
        self.screen = pygame.display.set_mode(self.size)  # 显示窗口
        pygame.display.set_caption("贪吃蛇")
        self.wait()
        pygame.display.flip()
    def wait(self):
        self.statusPage=None
        self.statusPage=StartPage(self.size)
    def start(self):
        self.statusPage=None
        self.statusPage=Grid(self.size)
    def end(self):
        self.statusPage=None
        self.statusPage=EndPage(self.size)
    def render(self):
        while True:  # 死循环确保窗口一直显示
            for event in pygame.event.get():  # 遍历所有事件
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    sys.exit()
                self.statusPage.render(self.screen,event,self.changeStatus)
    def changeStatus(self,status):
        self.status=status
        if self.status=='wait'  :
            self.wait()
        if self.status=='start':
            self.start() 
        if self.status=='end':
            self.end()              

class StartPage:
    bg=pygame.image.load('start.jpg')
    size=None
    isShow=False
    def __init__(self,size):
        self.size=size
        self.isShow=False
    def render(self,screen,event,callback=None):
        if self.isShow==False:
            screen.blit(pygame.transform.scale(self.bg, self.size),(0,0))
            pygame.display.flip()
            self.isShow=True
        if event.type==pygame.KEYDOWN:
            self.listenEvent(event.key,callback)

    def listenEvent(self,keycode,callback=None):
        if keycode==32:
            if callback!=None :
                callback('start')

class EndPage:
    bg=pygame.image.load('end.jpg')
    size=None
    isShow=False
    def __init__(self,size):
        self.size=size
        self.isShow=False
    def render(self,screen,event,callback=None):
        if self.isShow==False:
            screen.blit(pygame.transform.scale(self.bg, self.size),(0,0))
            pygame.display.flip()
            self.isShow=True
        if event.type==pygame.KEYDOWN:
            self.listenEvent(event.key,callback)
        

    def listenEvent(self,keycode,callback=None):
        if keycode==32:
            if callback!=None :
                callback('start')

retroSnake=RetroSnaker(600,600)
retroSnake.render()
