from lib2to3.refactor import get_all_fix_names
import sys,random
import pygame as py
from pygame.locals import *
WHITE=(92, 120, 125);BLACK=(0,0,0);PURPLE=(55, 55, 93)
GREEN=(5,250,10)
BLUE=[(1, 81, 136),(10, 100, 142)]
DARKGREEN=(2, 41, 46)
DARK=[(0,0,0),(5, 0, 8)]       #words
GLOW=[(0, 255, 120),(22, 212, 233),(188, 234, 239)] #typed words

py.init()
size=(1080,650)
screen=py.display.set_mode(size,NOFRAME)
py.display.set_caption("Alpha Party")
time=py.time.Clock()

def sound(name): #plays a sound when the mouse hovers a button
    if name=='hover':snd=py.mixer.Sound('aud/hov.wav'); snd.play()
    elif name=='click':snd=py.mixer.Sound('aud/c.wav'); snd.play()
    elif name=='exitWindow':snd=py.mixer.Sound('aud/not.wav'); snd.play()
    elif name=='type':snd=py.mixer.Sound('aud/tap.wav'); snd.play()
    elif name=='notify':snd=py.mixer.Sound('aud/wnot.wav'); snd.play()
    elif name=='gameover':snd=py.mixer.Sound('aud/go.wav'); snd.play()
    elif name=='wrongtyping':snd=py.mixer.Sound('aud/fl.wav'); snd.play()
def play(music):
    if music=='ghetto':
        py.mixer.music.load('aud/gt.mp3'); py.mixer.music.play(-1)
    elif music=='blues':
        py.mixer.music.load('aud/b.mp3'); py.mixer.music.play(-1)




def onbutton(box): #checks whether or not the mouse is on a given button
    pos=py.mouse.get_pos()
    if (pos[0]>=box[0] and pos[0]<=box[0]+box[2]) and (pos[1]>=box[1] and pos[1]<=box[1]+box[3]): #if mouse is between button boundries
        return True
    else: return False
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


class Game:
    def __init__(self):
        self.FPS=60
        self.Exit=False
        self.field=[0,0,1080,650]
        self.fX,self.fY,self.fLength,self.fWigth=0,0,1080,650
        self.lineWidth=5
        self.b_count=0
        self.count_range=0 #could be able to use the same comp
        self.score=0
        self.letterPressed=''
        self.keydown=False

        #LEVEL VARIABLES
        self.Level=1 #the game level it's self
        self.family="town"#alpha, syllabus , town , jazz , nature
        self.wordList=[]#depending on the family, a list of words will be attributed to the level
        self.wordColor=BLUE
        self.typedColor=WHITE
        self.backgroundImage=None# Background image(town, grasses, jazzInstruments, etc..)
        self.sky='indigo' #This is the color of the sky in the background
        self.goal=10
        self.bar_img=load('loading_bar.png')
        self.max_time=[1,0] #mins seconds

        self.ballonSpeed=0 #This is the average speed of the ballons.This speed shall be summed to the normal speed of each word. it will vary with the level

        #Ballon Variables
        self.ballon=[[],[],[]] #Green , blue and black ballons(there shall be three different kinds for each category)
        #self.ballonType="green"# green, blue , black etc..
        self.max_ballon_on_screen=10
        self.ballon_on_screen=[]
        self.ballon_generation_rate=50
        self.ballon_size=[[100,123],[108,121],[70,86]]
        self.ballons_generated=0
        self.least_ballon_number=2 #this represents the least number of ballons that should be on the screen
        #self.ballon=[load('b1.png').convert_alpha(),load('b2.png').convert_alpha(),load('b3.png').convert_alpha(),load('r.png')]
        self.ballon_Type=0
        

        nature=load('nature2.png');blueSky=load('blueSky.png')
        self.environment={'nature':nature,'blueSky':blueSky}
        self.ballon=[load('b1.png'),load('b2.png'),load('b3.png'),load('r.png')]
        
        #cloud variables
        self.CloudImg=[load('cloud1.png'),load('cloud2.png'),load('cloud3.png')]
        self.cloud=[]

        #clock_variables
        self.second=0
        self.minute=0
        self.clock_timer=0
        self.clock_sec=0
        self.clock_img=load('time.png')
        
        #button_variables
        self.exit_rect=[1040,5,35,35]
        self.exit_img=load('close.png')
        self.mouse_clicked=False


    def exit_win(self):
        sound("exitWindow")
        out=False;n=[(40, 141, 49),(40, 141, 199)]
        while not out:
            if onbutton([390,350,80,25]):b1=1
            else:b1=0
            if onbutton([530,350,80,25]):b2=1
            else:b2=0
            screen.fill((76, 74, 74))
            game.Generate_and_Destroy_Clouds()
            game.Cloudtrack()
            game.FrontClouds()
        
            py.draw.rect(screen,(40, 41, 49),[350,250,300,150])#main window
            message("Are you sure you want to leave?",[370,300],20,(146, 194, 226),"Impact")#exit message
            py.draw.rect(screen,n[b1],[390,350,80,25])#Cancel button
            message("Cancel",[393,352],20,(0,0,5),"Impact")#Cancel label
            py.draw.rect(screen,n[b2],[530,350,80,25])#Leave button
            message("Leave",[540,352],20,(0,0,5),"Impact")#Leave label
            
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    if b1==1:out=True;sound("click") #if user clicks on cancel button then window exits and game continues
                    if b2==1:sys.exit() #if user clicks on leave button then game exits automatically
            py.display.update()
            time.tick(game.FPS)

    def clock(self):
        self.clock_timer+=1
        if self.clock_timer%game.FPS==0:
            self.clock_sec+=1;self.clock_timer=0
        self.minute=str(self.clock_sec // 60); self.second=str(self.clock_sec%60)
        if len(self.minute)==1:self.minute='0'+self.minute
        if len(self.second)==1:self.second='0'+self.second
        message(self.minute +' : '+ self.second,[50,80],40,(0, 0, 0),'Forte')
        screen.blit(self.clock_img,[5,84])
    
    def ballon_bar(self):
        screen.blit(self.bar_img,[7,10])
        #py.draw.rect(screen,(0,12,0),[70,20,300,35],3)
        length=(self.score/self.goal)*300
        py.draw.rect(screen,(15, 153, 186),[70,20,length,33])
    
    def check_button(self):
        #print(game.mouse_clicked,onbutton(self.exit_rect))
        if onbutton(self.exit_rect):
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN or event.type==MOUSEBUTTONDOWN : 
                    print("EXIT WINDOW");game.exit_win();sound("click")
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN or event.type==MOUSEBUTTONDOWN : 
                    print("EXIT WINDOW");game.exit_win();sound("click");break
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
                self.cloud.pop(i);break;
    def Cloudtrack(self):
        for i in range(len(self.cloud)):
            self.cloud[i].keeptrack()
    def BackgroundClouds(self):
        for i in range(len(self.cloud)):
            self.cloud[i].show_BackgroundClouds()
    def FrontClouds(self):
        for i in range(len(self.cloud)):
            self.cloud[i].show_FrontClouds()
    
    def show_background(self):
        screen.blit(self.environment['nature'],[0,0])
    def show_Sky(self):
        screen.blit(self.environment['blueSky'],[0,0])

    def make(self,family,goal,speed,rate,maxb,least,wcol,tcol,time):
        self.family=family;self.goal=goal;self.ballonSpeed=speed;self.ballon_generation_rate=rate
        self.max_ballon_on_screen=maxb;self.least_ballon_number=least;self.wordColor=wcol;self.typedColor=tcol
        self.max_time=time #1min:0seconds
    
    def setLevel(self):
        print("SETTED"); self.clock_sec=0;self.score=0;game.ballon_on_screen=[]
        if self.Level==1: self.make("alpha",20,0,40,3,2,DARK[0],GLOW[0],[1,8])
        if self.Level==2:self.make("alpha",30,1,40,3,2,DARK[0],GLOW[0],[1,0])
        elif self.Level==3:self.make("alpha",40,1,45,4,3,DARK[0],GLOW[0],[1,0])
        elif self.Level==4:self.make("alpha",50,2,45,4,3,DARK[0],GLOW[0],[1,0])
        elif self.Level==5:self.make("alpha",60,3,50,5,4,DARK[0],GLOW[0],[1,0])
        elif self.Level==4:self.make("town",10,0,10,2,1,DARK[0],GLOW[0],[1,0])
        elif self.Level==6:self.make("town",20,0.5,45,2,1,DARK[0],GLOW[0],[1,0])
        elif self.Level==7:self.make("town",30,1,45,3,1,DARK[0],GLOW[0],[2,0])
        elif self.Level==8:self.make("town",40,1,45,3,2,DARK[0],GLOW[0],[2,0])
        elif self.Level==9:self.make("town",60,1.5,5,45,3,3,DARK[0],GLOW[0],[2,30])
        elif self.Level==10:self.make("town",70,2,50,4,2,DARK[0],GLOW[0],[3,0])
        
    
        self.wordList=word.list[self.family] #fetching the corresponding wordList from the list of words of the wordclass and assigning it the the wordlist of the current game
        
    #def check_state(self):
    #    if self.minute>=self.max_time[0] and self.second>=self.max_time[1]:



    def show(self):
        message('LEVEL '+str(self.Level),[880,50],20,(255,255,255),'Arial Black')
    
    def check_state(self):
        if int(self.minute)>=self.max_time[0] and int(self.second)>=self.max_time[1]:
            self.result_window('backtomenu',"Time Over","You lose")
        elif self.score>=self.goal:
            self.result_window('continue',"Congrates","You win")

    def result_window(self,state,line1,line2):
        out=False;n=[(40, 141, 49),(40, 141, 199)]
        if state=='backtomenu':sound("gameover")
        else:sound("notify")
        
        while not out:
            Sky('indigo')

            self.BackgroundClouds()
            self.FrontClouds()
        
            py.draw.rect(screen,(40, 41, 49),[350,250,300,150])#main window      
            if onbutton([420,350,150,35]):b1=1
            else:b1=0
            py.draw.rect(screen,n[b1],[420,350,150,35])#Empty button
            if state=='backtomenu':
                message(line1,[370,255],20,(210, 194, 226),"Impact")#exit message
                message(line2+' at Level'+str(self.Level),[370,300],20,(146, 194, 226),"Impact")#exit message
                message("MainMenu",[460,355],20,(0,0,5),"Impact")#Cancel label on button
            if state=='continue':
                message(line1,[370,255],20,(10, 184, 156),"Impact")#exit message
                message(line2 +'  Level '+str(self.Level),[370,300],20,(146, 194, 226),"Impact")#exit message
                message("Continue",[460,355],20,(0,0,5),"Impact")#Cancel label on button
            #print  
            keys=py.key.get_pressed()
            for event in py.event.get():
                if event.type==MOUSEBUTTONDOWN or keys[K_RETURN]:
                    if b1==1:
                        if state=="backtomenu":
                            out=True;game.Exit=True
                        elif state=="continue":
                            game.Level+=1; game.setLevel();print("Continue Selected LEVEL: ",game.Level)
                            out=True; self.score=0
            if keys[K_RETURN]:
                if state=="backtomenu":
                    out=True;game.Exit=True
                elif state=="continue":
                    game.Level+=1; game.setLevel();print("Continue Selected LEVEL: ",game.Level)
                    out=True; self.score=0

                            
            game.Cloudtrack()
            game.BackgroundClouds()
            py.display.update()
            time.tick(game.FPS)
        
        

    def generate_ballon(self):
        if len(self.ballon_on_screen)<self.max_ballon_on_screen : #new ballons can only be generated if the ballons existing on the screen are less than the maximun ballons_on_the_screen for that level
            result=random.randrange(self.ballon_generation_rate)
            if result==1 or len(self.ballon_on_screen)<self.least_ballon_number : #probability of 1/ballon_generation_rate for a ballon to be generated  or there is no existing ball on the field 
                #type_=random.randrange(3);size=self.ballon_size[type_]#randomizing the ballon type
                x=random.randrange(self.fX+10,self.fLength-100) #100 represents the size of the ballon(inorder for the ballon not to exceed the screen boundries)
                word_ID=random.randrange(len(self.wordList));word=self.wordList[word_ID] #getting a random word from actual wordlist
                typeOfballon=random.randrange(len(game.ballon)-1)#if there are three ballons the we will randomize from one to two. there by excluding the last image which is the ballon rope
                if (len(word))<5:speed=1
                elif (len(word))>=5 and (len(word))<9: speed=1.5
                elif (len(word))>=9 and (len(word))<13: speed=1.5
                elif (len(word))>=13 and (len(word))<17: speed=2
                else: speed=3
                self.ballon_on_screen.append(Ballon(typeOfballon,x,word,speed,game.wordColor,game.typedColor))# creating the new ballong #random type,x_cordinate,size,word,speed
              
                #print("CREATED")

    def keeptrack(self):
        for i in range(len(self.ballon_on_screen)):
            if self.ballon_on_screen[i].exist==True: #if the ballon does not exist again for a reason or another()we pop it from the list
                #print("hey i'm keeping track: {0} postion {1} ",i,self.ballon_on_screen[i].pos[1])
                stop=self.ballon_on_screen[i].keeptrack()
                self.ballon_on_screen[i].check_collider()
                self.ballon_on_screen[i].show()
            else: self.ballon_on_screen.pop(i); break
    
        #print("Size: ",len(self.ballon_on_screen))
    
    #def scan_keys(self):
    #    event=py.event.get()
    #    if event.type==KEYDOWN:


class Ballon:
    def __init__(self,type,x,word,speed,wordColor,typedColor):
        self.type="" #green, blue , black , white , violet
        self.img=game.ballon[type] #image type
        self.size=self.img.get_size()
        self.pos=[x,(game.fX+game.fWigth)]
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        self.exist=True
        self.speed=speed
        self.word=word
        self.currentPosition=0
        self.currentLetter=word[self.currentPosition]
        self.wordSize=len(self.word) #this will later be updated
        self.typingComplete=False #when the player types correctly the word on the ballon, this variable is set to true
        self.typedWord=""
        self.wordColor=wordColor
        self.typedColor=typedColor

    #def Sound. "pfff" a sound should be heard every time a new ballon is created

    def show(self):
        #py.draw.rect(screen,(24, 209, 240),(self.pos[0],self.pos[1],100,75))
        message(self.word,[self.pos[0],self.pos[1]-24],20,self.wordColor,'Arial Black')
        message(self.typedWord,[self.pos[0],self.pos[1]-24],20,self.typedColor,'Arial Black')
        screen.blit(self.img,[self.pos[0],self.pos[1]])
        screen.blit(game.ballon[-1],[self.pos[0]+(self.size[0]/2)-2,self.pos[1]+self.size[1]])#The rope
        

    def keeptrack(self):
        #making ballon climb
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]#may be used later... but not now
        if not (self.typingComplete): #if the word on the ballon is not yet typed or the ballon has not the limit up, then we can continue keeping track of it
            self.pos[1]-=(self.speed+game.ballonSpeed)# the ballon climbs by it's normal speed plus that influenced by the level in the game class       
            if game.keydown and game.letterPressed==self.currentLetter: #if the button is a letter and is equal to the currentLetter of the balloon,..
                sound("type")
                self.typedWord+=game.letterPressed #we color that letter(Transparency).
                if self.typedWord!=self.word: #if the word is not completed, we increment the current letter index by one
                    self.currentPosition+=1
                    self.currentLetter=self.word[self.currentPosition]
                else: #else we eliminate that balloon(since it's word has been typed) and increase the score by 1
                    self.typingComplete=True
                    game.score+=1 #;print('SCORE :'+str(game.score))
                    self.exist=False

                game.letterPressed='' #Resetting letterPressed for it not to match with the next letter of a possible upcomming word
            else:
                if game.keydown and game.letterPressed!='' and game.letterPressed!=self.currentLetter:
                    sound("wrongtyping")
            
            #print('Word :'+self.typedWord)

        #Checking if 
        
            
  
    def check_collider(self):
        if self.pos[1]<=game.fY+game.lineWidth:
            self.exist=False
            
    


class Word:
    def __init__(self):
        self.family="alpha"
        self.alpha=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        #self.syllabus=random_letters. 
        self.town=["Building","Car","Tower","Traffic","Street","Town","Junction","Police","Snackbar","Yaounde","Douala","Buea",
                   "Office","Restaurant","Night club","Street light","Eneo","Nkolmesseng","Mbouda","Kumba","Limbe","Bamenda",
                   "Infrastructure","Camwater","Network","Shopping","Technology","Employement","Bridge","Companies","Industry","Zebra crossing"
                   ,"Vehicles","Bank","Buisiness","Love","Restaurant","Acid jazz","Sensational","Modes","Disorder","Acidity","Nineteen sixties","Oldies","Sorrow"
                    ,"Jazz","Funk","Bossa nova","Bebop","funky","soul","Composer","jazz man","Afrobeat","trap","jazz up","Country","Boogie","rap"
                    ,"Jazzist","folk","rumba","lento","Conga","Glee","Calypso","Billie holiday","presto","Surf rock","Fitzgerald","Ella",
                    "Apple","Orange","Fruit","Tree","Leaf","Mango","Pear","River","Lake","Animals","Waterfall","Stars","Day","Night",
                    "Air","Ozone","Football","Handball","Ball","Kick","Refree","Halftime","Victory","Running","Jump","Reward","Defeated","Indomittable","Olembe",
                    "Efforts","Motivation","Fitness"]
        
        

        self.list={"alpha":self.alpha,"town":self.town}

word=Word()      

def Sky(n):
    Col={"blue":(28, 121, 190),"brown":(89, 57, 74),"indigo":(153, 105, 168),"black":(12, 14, 17)}
    if n!="black":
        x=screen.get_size(); width=20;#print(x[0]/width)
        for i in range(35):
            py.draw.rect(screen,(Col[n][0]+i+1,Col[n][1]+i+1,Col[n][2]),[0,i*width,x[0],50])
    else:
        screen.fill(Col[n])        
  
game=Game()
def mainMenu():
    play("blues");py.mixer.music.set_volume(0.5)
    out=False;n=[(10, 184, 156),(27, 244, 160)]
    while not out :
        screen.fill((38, 38, 38))
        if onbutton([410,300,200,50]):b1=1
        else:b1=0
        if onbutton([410,390,200,50]):b2=1
        else:b2=0

        game.Generate_and_Destroy_Clouds()
        game.Cloudtrack()
        game.FrontClouds()
    
        #py.draw.rect(screen,(40, 41, 49),[350,250,300,150])#main window
        message("Alpha Party",[310,100],90,(146, 194, 226),"Impact")#exit message
        py.draw.rect(screen,n[b1],[410,300,200,50])#Cancel button
        message("Play Demo",[428,305],30,(0,0,5),"Arial Black")#Cancel label
        py.draw.rect(screen,n[b2],[410,390,200,50])#Leave button
        message("Exit",[480,395],35,(0,0,5),"Impact")#Leave label
        
        message("(c) Copyright 2022 GreenLeafStudio",[750,600],20,(69, 68, 68),"Impact")#exit message
        
        for event in py.event.get():
            if event.type==MOUSEBUTTONDOWN:
                if b1==1:game.Exit=False; sound("click"); game.Level=1;game.setLevel();main() #if user clicks on cancel button then window exits and game continues
                if b2==1:sys.exit() #if user clicks on leave button then game exits automatically
        py.display.update()
        time.tick(160)


def main():
    play("ghetto")
    game.setLevel()
    while not game.Exit:
        #screen.fill((38, 141, 210))
        Sky("indigo")
        pressed=False
        for event in py.event.get():
            if event.type==KEYDOWN or event.type==KEYDOWN:
                game.letterPressed=event.unicode;pressed=True    
        for event in py.event.get():
            if event.type==KEYDOWN or event.type==KEYDOWN:
                game.letterPressed=event.unicode;pressed=True
        game.keydown=pressed
            
                #print('Letter :'+game.letterPressed)
                  
        keys=py.key.get_pressed()
        if keys[K_ESCAPE]:game.exit_win()
        
        game.show()
        game.Generate_and_Destroy_Clouds()
        game.Cloudtrack()
        
        game.FrontClouds()

        game.clock()
        game.ballon_bar()
        game.check_button()
        game.check_state()
        
        

        game.generate_ballon()
        game.keeptrack()

        
        

        py.display.update()
        time.tick(game.FPS)
    play("blues")



if __name__=="__main__":
    mainMenu()
    sys.exit()
