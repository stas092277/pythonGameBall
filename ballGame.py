
from tkinter import *
from random import *
from time import sleep
from math import sqrt

#параметры окна
W = 800
H = 600

#глобальные переменные
colors = ['red','orange','yellow','green','blue','black','grey']
tag = "ball"

#создаём главное окно
root = Tk()
root.geometry(f'{W}x{H}')

#создаём холст, на котором будем рисовать шарики
canv = Canvas(root, width=W, height=H, bg="white")
canv.pack()

#структура шарика    
class Ball:
    def __init__(self):
        r = randint (30, 50)
        x = randint(r, W-r)
        y = randint(r, H-r)
        self.Vx = randint(-1, 1) + randint(-1,1)*random()
        self.Vy = randint(-1, 1) + randint(-1,1)*random()
        self.id = canv.create_oval(x-r, y-r, x+r, y+r, outline="white" ,fill=choice(colors), tag=tag)
    def move(self):
        leftBoard = canv.coords(self.id)[0]
        rightBoard = canv.coords(self.id)[2]
        upBoard = canv.coords(self.id)[1]
        downBoard = canv.coords(self.id)[3]
        if (leftBoard <= 0 or rightBoard >= W):
            self.Vx = -1 * self.Vx
        if (upBoard <= 0 or downBoard >= H):
            self.Vy = -1 *self.Vy
        canv.move(self.id,self.Vx,self.Vy)


GlobalBall = []
numBalls = randint(10, 30)

for i in range(numBalls):
    ball = Ball()
    GlobalBall.insert(i, ball)


def motion():
    for ballA in GlobalBall:
        leftBoard = canv.coords(ballA.id)[0]
        rightBoard = canv.coords(ballA.id)[2]
        upBoard = canv.coords(ballA.id)[1]
        downBoard = canv.coords(ballA.id)[3]
        xa = (rightBoard + leftBoard) / 2
        ya = (upBoard + downBoard) / 2
        ra = (rightBoard - leftBoard) / 2
        for ballB in GlobalBall:
            leftBoard = canv.coords(ballB.id)[0]
            rightBoard = canv.coords(ballB.id)[2]
            upBoard = canv.coords(ballB.id)[1]
            downBoard = canv.coords(ballB.id)[3]
            xb = (rightBoard + leftBoard) / 2
            yb = (upBoard + downBoard) / 2
            rb = (rightBoard - leftBoard) / 2
            if (xa != xb or ya != yb):
                R = sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
                if (R <= ra+rb):
                    ballA.Vx, ballB.Vx = ballB.Vx, ballA.Vx
                    ballA.Vy, ballB.Vy = ballB.Vy, ballA.Vy
        ballA.move()
    root.after(1,motion)

#создадим метку "количество набранных очков"
scoreStr = "score: 0"
scoreInt = 0
scoreId = canv.create_text(30, H-15, text=scoreStr)

#при попадании по шарику нужно изменить метку
def changeText(scoreId, scoreStr, scoreInt):
    tmp = scoreStr.split()
    tmp[1] = str(scoreInt)
    scoreStr = "".join(tmp)
    canv.itemconfig(scoreId, text=scoreStr)
    
#обработка клика
def click(event):
    for ballA in GlobalBall:
        xe = event.x
        ye = event.y
        leftBoard = canv.coords(ballA.id)[0]
        rightBoard = canv.coords(ballA.id)[2]
        upBoard = canv.coords(ballA.id)[1]
        downBoard = canv.coords(ballA.id)[3]
        xb = (rightBoard + leftBoard)/2
        yb = (upBoard + downBoard)/2
        rb = (rightBoard - leftBoard)/2
        R = sqrt((xe - xb) ** 2 + (ye - yb) ** 2)
        if (R <= rb):
            canv.delete(ballA.id)
            GlobalBall.remove(ballA)
            global scoreInt, scoreId, scoreStr
            scoreInt = scoreInt+1
            changeText(scoreId, scoreStr, scoreInt)
            if len(GlobalBall) == 0:
                gameEnd = canv.create_text(W/2, H/2, text='GAME OVER')
                canv.itemconfig(gameEnd)

            
canv.bind('<Button-1>', click)



motion()



#запускаем главный цикл обработки событий
root.mainloop()
