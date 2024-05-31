import sys,random
import pygame as py
from pygame.locals import *

from AlphaParty import Ballon
from Demo import mainMenu
WHITE=(0,0,0)
GREEN=(5,250,10)
BLUE=[(1, 81, 136),(10, 100, 142)]
DARKGREEN=(2, 41, 46)
DARK=[(30, 30, 30),(5, 0, 8)]       #words
GLOW=[(0, 255, 120),(22, 212, 233),(188, 234, 239)] #typed words
py.init()
size=(1080,650)
screen=py.display.set_mode(size,NOFRAME)
py.display.set_caption("Alpha Party")
time=py.time.Clock()
def message(word,xy,size,color,writing):
    font=py.font.SysFont(writing,size,False)
    msg=font.render(str(word),True,color)
    screen.blit(msg,xy)
def load(name):
    return py.image.load(name)
def resize(image_obj,size):
    return py.transform.scale(image_obj,size)
class Cloud:
    def __init__(self,pos,type,speed,front):
        self.pos=pos
        self.size=[100,50]
        self.type=type #3 types of clouds will exist 
        self.speed=speed
        self.exist=True
        self.frontCloud=front

    def keeptrack(self):
        self.pos[0]-=self.speed
        if self.pos[0]+400<=0: self.exist=False
    def show_FrontClouds(self):
        if self.exist and self.frontCloud:
            screen.blit(game.CloudImg[self.type],self.pos)
            #py.draw.rect(screen,(255, 251, 231),[self.pos[0],self.pos[1],self.size[0],self.size[1]])
    def show_BackgroundClouds(self):
        if self.exist and not self.frontCloud:
            screen.blit(game.CloudImg[self.type],self.pos)
            #py.draw.rect(screen,(255, 251, 231),[self.pos[0],self.pos[1],self.size[0],self.size[1]])

def onbutton(box): #checks whether or not the mouse is on a given button
    pos=py.mouse.get_pos()
    if (pos[0]>=box[0] and pos[0]<=box[0]+box[2]) and (pos[1]>=box[1] and pos[1]<=box[1]+box[3]): #if mouse is between button boundries
        return True
    else: return False


class Game:
    def __init__(self):
        self.FPS=25
        self.Exit=False
        self.field=[10,10,850,625]
        self.fX,self.fY,self.fLength,self.fWigth=10,10,850,625
        self.lineWidth=5
        self.b_count=0
        self.count_range=0 #could be able to use the same comp

        #LEVEL VARIABLES
        self.Level=1 #the game level it's self
        self.family="alpha"#alpha, syllabus , town , jazz , nature
        self.wordList=[]#depending on the family, a list of words will be attributed to the level
        self.wordColor=BLUE
        self.typedColor=WHITE
        self.backgroundImage=None# Background image(town, grasses, jazzInstruments, etc..)
        self.backgroundMark=None#This is a corresponding moving image in the background such as cloud
        self.ballonSpeed=0 #This is the average speed of the ballons.This speed shall be summed to the normal speed of each word. it will vary with the level

        #Ballon Variables
        self.ballon=[[],[],[]] #Green , blue and black ballons(there shall be three different kinds for each category)
        self.ballonType="green"# green, blue , black etc..
        self.max_ballon_on_screen=10
        self.ballon_on_screen=[]
        self.ballon_generation_rate=50
        #self.ballon_size={1:[30,90],2:[40,100],3:[50,110]}
        self.ballons_generated=0
        self.least_ballon_number=2 #this represents the least number of ballons that should be on the screen
        
        #Design Test variables
        self.text='Text'
        nature=load('nature2.png');blueSky=load('blueSky.png')
        self.environment={'nature':nature,'blueSky':blueSky}
        self.ballon=[load('b1.png'),load('b2.png'),load('r.png')]

        #cloud variables
        self.CloudImg=[load('cloud1.png'),load('cloud2.png'),load('cloud3.png')]
        self.cloud=[]

        #clock_variables
        self.clock_timer=0
        self.clock_sec=0
        self.clock_img=load('time.png')

        #bar variables
        self.score=0
        self.goal=60
        self.bar_img=load('loading_bar.png')

        #buttons
        self.exit_rect=[1040,5,35,35]
        self.exit_img=load('close.png')
        self.mouse_clicked=False

    def exit_win(self):
        out=False;n=[(40, 141, 49),(40, 141, 199)]
        while not out:
            if onbutton([390,350,80,25]):b1=1
            else:b1=0
            if onbutton([530,350,80,25]):b2=1
            else:b2=0
            screen.fill((76, 74, 74))
            game.Cloudtrack()
            game.BackgroundClouds()
        
            py.draw.rect(screen,(40, 41, 49),[350,250,300,150])#main window
            message("Are you sure you want to leave?",[370,300],20,(146, 194, 226),"Impact")#exit message
            py.draw.rect(screen,n[b1],[390,350,80,25])#Cancel button
            message("Cancel",[393,352],20,(0,0,5),"Impact")#Cancel label
            py.draw.rect(screen,n[b2],[530,350,80,25])#Leave button
            message("Leave",[540,352],20,(0,0,5),"Impact")#Leave label
            
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    if b1==1:out=True #if user clicks on cancel button then window exits and game continues
                    if b2==1:sys.exit() #if user clicks on leave button then game exits automatically
            py.display.update()
            time.tick(game.FPS)
            
    def result_window(self,state,line1,line2):
        out=False;n=[(40, 141, 49),(40, 141, 199)]
        while not out:
            py.draw.rect(screen,(40, 41, 49),[350,250,300,150])#main window
            message(line2,[370,255],20,(210, 194, 226),"Impact")#exit message
            message(line2,[370,300],20,(146, 194, 226),"Impact")#exit message      
            if onbutton([390,350,80,25]):b1=1
            else:b1=0

            if state=='backtomenu':
                message(line2,[370,255],20,(210, 194, 226),"Impact")#exit message
                message(line2,[370,300],20,(146, 194, 226),"Impact")#exit message
                message("MainMenu",[390,352],20,(0,0,5),"Impact")#Cancel label on button
            if state=='continue':
                message(line2,[370,255],20,(183, 194, 226),"Impact")#exit message
                message(line2,[370,300],20,(146, 194, 226),"Impact")#exit message
                message("Continue",[390,352],20,(0,0,5),"Impact")#Cancel label on button

                

            
            py.draw.rect(screen,n[b1],[390,350,80,25])#Empty button
            message("Leave",[540,352],20,(0,0,5),"Impact")#Leave label
            
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    if b1==1:
                        if state=="backtomenu":
                            game.Exit=True
                        elif state=="continue":
                            self.Level+=1;self.ballon=[];
                            
            game.Cloudtrack()
            game.BackgroundClouds()
            py.display.update()
            time.tick(game.FPS)
    def mainMenu(self):
        out=False;n=[(40, 141, 49),(40, 141, 199)]
        while not out :
            game.Cloudtrack()
            game.show_Sky()
            game.BackgroundClouds()
            game.show_background()
            game.FrontClouds()
            
        
            keys=py.key.get_pressed()
            if keys[K_ESCAPE]:game.exit_win()
        
            py.display.update()
            time.tick(game.FPS)
            

    def clock(self):
        self.clock_timer+=1
        if self.clock_timer%game.FPS==0:
            self.clock_sec+=1;self.clock_timer=0
        hour=str(self.clock_sec // 60); minute=str(self.clock_sec%60)
        if len(hour)==1:hour='0'+hour
        if len(minute)==1:minute='0'+minute
        message(hour +' : '+ minute,[50,80],40,(0, 0, 0),'Forte')
        screen.blit(self.clock_img,[5,84])


    def ballon_bar(self):
        screen.blit(self.bar_img,[7,10])
        #py.draw.rect(screen,(0,12,0),[70,20,300,35],3)
        length=(self.score/self.goal)*288
        py.draw.rect(screen,(15, 153, 186),[70,20,length,33])
        #print('Length :',length, 'Score :',self.score)
        
    


    def check_button(self):
        #print(game.mouse_clicked,onbutton(self.exit_rect))
        if onbutton(self.exit_rect):
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN or event.type==MOUSEBUTTONDOWN : 
                    print("EXIT WINDOW");game.exit_win()
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN or event.type==MOUSEBUTTONDOWN : 
                    print("EXIT WINDOW");game.exit_win();break
            

        #py.draw.rect(screen,(0,12,55),[1040,10,35,35])
        screen.blit(self.exit_img,[self.exit_rect[0],self.exit_rect[1]])
        




    

    def Generate_and_Destroy_Clouds(self):
        result=random.randrange(100)
        if result==1:
            y=random.randrange(2,104); type_=random.randrange(3);speed=random.randrange(1,4);ran=random.randrange(2)
            if ran==0:front=True
            else:front=False
            self.cloud.append(Cloud([1080,y],type_,speed,front))

        for i in range(len(self.cloud)):
            if self.cloud[i].exist==False:
                self.cloud.pop(i);break
    def Cloudtrack(self):
        for i in range(len(self.cloud)):
            self.cloud[i].keeptrack()
    def BackgroundClouds(self):
        for i in range(len(self.cloud)):
            self.cloud[i].show_BackgroundClouds()
    def FrontClouds(self):
        for i in range(len(self.cloud)):
            self.cloud[i].show_FrontClouds()



    def display_text(self):
        pos=py.mouse.get_pos()
        #message(self.text,[200,100],30,(28, 44, 50),"Arial Black")
        message(str(pos),[700,0],30,(255,255,255),"Arial Black")

    
    def show_background(self):
        screen.blit(self.environment['nature'],[0,0])
    def show_Sky(self):
        screen.blit(self.environment['blueSky'],[0,0])



    #def scan_keys(self):
    #    event=py.event.get()
    #    if event.type==KEYDOWN:
        
class Ennemy:
    def __init__(self):
        self.pos=[570,510] #sprite's position
        self.timer=0 #used in animations to difine the time for each frame of sub animation
        self.exist=False #initialy ennemy doesn't exist. Ennemy will only start existing after the appear animation
        self.count=0
        self.exFace=0
        self.eyFace=0
        self.exEye=0
        self.eyEye=0
        self.exLimit=3
        self.adFace=[1,3]
        self.adEye=[1,1]
        face=load('face.png');red_face=load('red_face.png');eye1=load('Y1.png');eye2=load('closed_eye.png');eye3=load('red_eye.png');fire=load('fire.png')
        smile=load('smile.png');large_smile=load('largeMouth.png');shadow=load('shadow.png');light=load('light.png');dis=load('disapear.png');laser=load('laser.png')
        self.samy={'face':[face,red_face],'eye':[eye1,eye2,eye3],'mouth':[smile,large_smile],'shadow':shadow,'light':light,'disapear':dis,'fire':fire,'laser':laser}
        self.state='appear' #idle , appear , attack
        

    def showIdle(self,face,eye,mouth):
        screen.blit(resize(self.samy['face'][face],[75-self.exFace,123+self.eyFace]),[self.pos[0],self.pos[1]-self.eyFace])
        screen.blit(resize(self.samy['eye'][eye],[55-self.exEye,14+self.eyEye]),[(self.pos[0]+8),self.pos[1]+80-self.eyEye])
        screen.blit(resize(self.samy['mouth'][mouth],[40-self.exEye,12+self.eyEye]),[self.pos[0]+17,self.pos[1]+100-self.eyEye])
        screen.blit(resize(self.samy['shadow'],[87-self.exEye,13-self.eyEye]),[self.pos[0]-5,self.pos[1]+121])
        if self.state=='attack':screen.blit(resize(self.samy['fire'],[85-self.exFace,149+self.eyFace]),[self.pos[0]-5,self.pos[1]-self.eyFace-20])
        
        if self.count%3==0:
            self.exFace+=self.adFace[0];self.eyFace+=self.adFace[1]
            if self.exFace>=self.exLimit or self.exFace<=-self.exLimit:
                self.adFace[0]*=-1;self.adFace[1]*=-1

        if self.count%5==0:
            self.exEye+=self.adEye[0];self.eyEye+=self.adEye[1]
            if self.exEye>=2 or self.exFace<=-2:
                self.adEye[0]*=-1;self.adEye[1]*=-1


    def animate(self):
        if self.state=='idle':
            screen.blit(resize(self.samy['face'][0],[75-self.exFace,123+self.eyFace]),[self.pos[0],self.pos[1]-self.eyFace])
            screen.blit(resize(self.samy['eye'][1],[55-self.exEye,14+self.eyEye]),[(self.pos[0]+8),self.pos[1]+80-self.eyEye])
            screen.blit(resize(self.samy['mouth'][0],[40-self.exEye,12+self.eyEye]),[self.pos[0]+17,self.pos[1]+100-self.eyEye])
            screen.blit(resize(self.samy['shadow'],[87-self.exEye,13-self.eyEye]),[self.pos[0]-5,self.pos[1]+121])    
            if self.count%3==0:
                self.exFace+=self.adFace[0];self.eyFace+=self.adFace[1]
                if self.exFace>=self.exLimit or self.exFace<=-self.exLimit:
                    self.adFace[0]*=-1;self.adFace[1]*=-1
            if self.count%5==0:
                self.exEye+=self.adEye[0];self.eyEye+=self.adEye[1]
                if self.exEye>=2 or self.exFace<=-2:
                    self.adEye[0]*=-1;self.adEye[1]*=-1
            if self.count>100:self.count=0 #This is simply to avoid big numbers in memory


            #screen.blit(self.samy['disapear'],self.pos)
        elif self.state=='appear': #appearing animation
            if self.timer<30: # we start by showing the light
                if self.timer%4!=0  : #The light blinks
                    screen.blit(self.samy['light'],[self.pos[0]-22,self.pos[1]-33])
            else:
                if self.timer>30 : #face and shadow appear first
                    screen.blit(resize(self.samy['face'][0],[75-self.exFace,123+self.eyFace]),[self.pos[0],self.pos[1]-self.eyFace])
                    screen.blit(resize(self.samy['shadow'],[87-self.exEye,13-self.eyEye]),[self.pos[0]-5,self.pos[1]+121])
                if self.timer>40 : #blue Eye
                    screen.blit(resize(self.samy['eye'][0],[55-self.exEye,14+self.eyEye]),[(self.pos[0]+8),self.pos[1]+80-self.eyEye])
                if self.timer>50: #Mouth
                    screen.blit(resize(self.samy['mouth'][1],[40-self.exEye,12+self.eyEye]),[self.pos[0]+17,self.pos[1]+100-self.eyEye])
                screen.blit(self.samy['light'],[self.pos[0]-22,self.pos[1]-33]) #light stops blinking and remains
                if self.timer>60: #Stop animation
                    self.state='idle'
                    self.init_animation();self.exist=True
            
        elif self.state=='attack': #attack animation
            if self.timer>10 and self.timer<70:screen.blit(self.samy['laser'],[self.pos[0]-10,self.pos[1]-207-self.eyFace])#laser shot
            
            if self.timer<10:self.showIdle(0,2,1);#print("BLUE FACE") #blue face,red eyes and normal mouth
            elif self.timer>=10 and self.timer<40: self.showIdle(1,2,1)#red face,red eyes and large mouth
            elif self.timer>=40 and self.timer<50: self.showIdle(1,1,1)#red face, blue eye, large mouth
            elif self.timer>=50 and self.timer<80: self.showIdle(0,1,1)#blue face, blue eye, large mouth
            else:self.state='idle';self.init_animation()

        #elif self.state=='disappear':
            

            
            

            #screen.blit(self.samy['fire'],[self.pos[0],self.pos[1]]) #light stops blinking and remains
                
        self.timer+=1
        #print('State: ',self.state,self.timer)
        #print('Speed:',self.showIdle())


    
    def init_animation(self):
        self.timer=0;self.exFace=0;self.eyFace=0;self.exEye=0
        self.eyEye=0;self.exLimit=3;self.adFace=[1,3];self.adEye=[1,1]
        #self.state='appear'
        
    
en=Ennemy()

game=Game()
def Sky(n):
    Col={"blue":(28, 121, 190),"brown":(89, 57, 74),"indigo":(153, 105, 168),"black":(12, 14, 17)}
    if n!="black":
        x=screen.get_size(); width=20;#print(x[0]/width)
        for i in range(35):
            py.draw.rect(screen,(Col[n][0]+i+1,Col[n][1]+i+1,Col[n][2]),[0,i*width,x[0],50])
    else:
        screen.fill(Col[n]) 

def main():
    
    while not game.Exit:
        #screen.fill((89, 57, 74))
        Sky("indigo")
        for event in py.event.get():
            if event.type==QUIT:
                game.Exit=True
            if event.type==KEYDOWN:
                game.text+=event.unicode
            if event.type==MOUSEBUTTONDOWN:
                game.mouse_clicked==True
            #else: game.mouse_clicked=False
        
        keys=py.key.get_pressed()
        if keys[K_ESCAPE]:sys.exit();game.exit_win()
        if keys[K_RETURN]:en.init_animation(); en.state='attack';game.score+=1 ;print("SCORED!!")
        if keys[K_LEFT]:en.pos[0]-=3
        if keys[K_RIGHT]:en.pos[0]+=3
        
        game.Generate_and_Destroy_Clouds()
        game.Cloudtrack()
        #game.show_Sky()
        game.BackgroundClouds()
        #game.show_background()
        #game.FrontClouds()
        game.display_text()
        #en.animate()
        

        screen.blit(game.ballon[0],[350,400])
        screen.blit(game.ballon[-1],[395,520])
        game.clock()
        game.ballon_bar()
        game.check_button()
        
        py.display.update()
        time.tick(game.FPS)



if __name__=="__main__":
    mainMenu()
    sys.exit()
