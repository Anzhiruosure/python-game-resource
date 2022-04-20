import pygame 
import random
from math import*
#初始界面的创建
pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("airplane fight")
bgImg=pygame.image.load("bg.png")


#音乐添加
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1) #单曲循环

#添加射中音效
bao_sound=pygame.mixer.Sound("bullet.aiff")
#分数
score=0
font=pygame.font.Font("freesansbold.ttf",32)

#分数显示
def show_score():
    text=f"Score:{score}"
    score_render=font.render(text,True,(0,255,0))
    screen.blit(score_render,(10,10))



#飞机的位置定义
playerImg=pygame.image.load("player.png")
playerX=400
playerY=500
playerStep=0   #飞机移动速度

#添加敌人

#创建敌人类
number_of_enemies=6
class Enemy():
    def __init__(self):
        self.img=pygame.image.load("enemy.png")
        self.x=random.randint(200,600)
        self.y=random.randint(50,250)
        self.step=random.randint(1,3)
    def reset(self):
        self.x=random.randint(200,600)
        self.y=random.randint(50,250)

enemies=[]
for i in range(number_of_enemies):
    enemies.append(Enemy())


#两点之间的距离，欧式距离
def distance(bx,by,ex,ey):
    a=bx-ex
    b=by-ey
    return sqrt(a*a+b*b)

#创建子弹类
class Bullet():
    def __init__(self):
        self.img=pygame.image.load("bullet.png")
        self.x=playerX+16
        self.y=playerY+10
        self.step=6  #子弹移动速度

    def hit(self):
        global score
        for e in enemies:      
            if(distance(self.x,self.y,e.x,e.y)<30):
                bao_sound.play()
                bullets.remove(self)
                e.reset()
                score+=1
                print(score)

bullets=[] #保存现有的子弹




#显示移动子弹
def show_bullets():
    for b in bullets:
        screen.blit(b.img,(b.x,b.y))
        b.hit()
        b.y-=b.step
        #判断子弹是否出界，出界移除
        if b.y<0:
            bullets.remove(b)
#显示敌人
def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.img,(e.x,e.y))
        e.x+=e.step
        if(e.x>736 or e.x<0):
            e.step*=-1
            e.y+=40
            if e.y>450:
                is_over=True
                print("游戏结束")
                enemies.clear()

def move_player():
    global playerX
    playerX+=playerStep
    #防止飞机出界
    if playerX>736:
        playerX=736
    if playerX<0:
        playerX=0


#游戏结束
is_over=False
over_font=pygame.font.Font("freesansbold.ttf",64)
def check_is_over():
    if is_over:
        text="Game Over"
        render=over_font.render(text,True,(255,0,0))
        screen.blit(render,(200,250))


#游戏主循环，当quit时退出循环
game_running=True
while game_running:
    screen.blit(bgImg,(0,0))   #背景的绘制
    show_score()#显示分数
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_running=False
        #键盘按下
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                playerStep=5
            elif event.key==pygame.K_LEFT:
                playerStep=-5
            elif event.key==pygame.K_SPACE:
                #创建一颗子弹
                bullets.append(Bullet())
        #键盘按键弹起停止运动
        if event.type==pygame.KEYUP:
            playerStep=0
    #飞机移动
    move_player()

    screen.blit(playerImg,(playerX,playerY))
    show_enemy()
    show_bullets()
    check_is_over()
    pygame.display.update()
    
