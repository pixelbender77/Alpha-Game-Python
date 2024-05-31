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
        self.FPS=40
        self.Exit=False
        self.field=[0,0,1080,650]
        self.fX,self.fY,self.fLength,self.fWigth=0,0,1080,650
        self.lineWidth=5
        self.b_count=0
        self.count_range=0 #could be able to use the same comp
        self.score=0
        self.letterPressed=''

        #LEVEL VARIABLES
        self.Level=1 #the game level it's self
        self.family="town"#alpha, syllabus , town , jazz , nature
        self.wordList=[]#depending on the family, a list of words will be attributed to the level
        self.wordColor=BLUE
        self.typedColor=WHITE
        self.backgroundImage=None# Background image(town, grasses, jazzInstruments, etc..)
        self.sky='blue' #This is the color of the sky in the background

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


    def setLevel(self):
        self.ballons_generated=0
        self.wordList=word.list[self.family] #fetching the corresponding wordList from the list of words of the wordclass and assigning it the the wordlist of the current game
        if self.family=="alpha":
            self.wordColor=DARK[0];self.typedColor=GLOW[0]
            if self.Level==1:
                self.ballonSpeed=0
                self.max_ballon_on_screen=5

        if self.family=="town":
            self.wordColor=DARK[0];self.typedColor=GLOW[0]
            if self.Level==1:
                self.max_ballon_on_screen=2

        if self.family=="jazz":
            self.wordColor=DARK[0];self.typedColor=GLOW[0]
        
            if self.Level==1:
                self.max_ballon_on_screen=3

        if self.family=="nature":
            self.wordColor=DARK[0];self.typedColor=GLOW[0]
            
            if self.Level==1:
                self.max_ballon_on_screen=3

    def drawField(self):
        #py.draw.rect(screen,BLUE[0],self.field,self.lineWidth)#external box|| down is the internal box
        py.draw.rect(screen,BLACK,[self.fX+self.lineWidth-1,self.fY+self.lineWidth-1,self.fLength-(self.lineWidth*2-2),self.fWigth-(self.lineWidth*2-2)],3)
    
    def show(self):
        message('SCORE :'+str(self.score),[880,50],20,(255,255,255),'Arial Black')
        
        

    def generate_ballon(self):
        if len(self.ballon_on_screen)<self.max_ballon_on_screen : #new ballons can only be generated if the ballons existing on the screen are less than the maximun ballons_on_the_screen for that level
            result=random.randrange(self.ballon_generation_rate)
            if result==1 or len(self.ballon_on_screen)<self.least_ballon_number : #probability of 1/ballon_generation_rate for a ballon to be generated  or there is no existing ball on the field 
                #type_=random.randrange(3);size=self.ballon_size[type_]#randomizing the ballon type
                x=random.randrange(self.fX+10,self.fLength-100) #100 represents the size of the ballon(inorder for the ballon not to exceed the screen boundries)
                word_ID=random.randrange(len(self.wordList));word=self.wordList[word_ID] #getting a random word from actual wordlist
                typeOfballon=random.randrange(len(game.ballon)-1)#if there are three ballons the we will randomize from one to two. there by excluding the last image which is the ballon rope
                if (len(word))<5:speed=5
                elif (len(word))>=5 and (len(word))<9: speed=2.5
                elif (len(word))>=9 and (len(word))<13: speed=2.5
                elif (len(word))>=13 and (len(word))<17: speed=3.5
                else: speed=5.5
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
            if game.letterPressed==self.currentLetter: #if the button is a letter and is equal to the currentLetter of the balloon,..
                self.typedWord+=game.letterPressed #we color that letter(Transparency).
                if self.typedWord!=self.word: #if the word is not completed, we increment the current letter index by one
                    self.currentPosition+=1
                    self.currentLetter=self.word[self.currentPosition]
                else: #else we eliminate that balloon(since it's word has been typed) and increase the score by 1
                    self.typingComplete=True
                    game.score+=1 #;print('SCORE :'+str(game.score))
                    self.exist=False

                game.letterPressed=''#Resetting letterPressed for it not to match with the next letter of a possible upcomming word

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
                   "Infrastructure","Camwater","Network","Shopping","Technology","Employement","Bridge","Campanies","Industry","Zebra crossing"
                   ,"Vehicles","Bank","Buisiness"]
        
        self.sport=["Football","Handball","Ball","Kick","Refree","Halftime","Victory","Running","Jump","Reward","Defeated","Indomittable","Olembe",
                    "Efforts","Motivation","Fitness","Encouragements","Muscles","Competition","Prize","Practice","Energy","Power","Race","Hockey"
                    ,"Voleyball","","",""]
        
        self.animal=["Lion","Snail","Eagle","Monkey","Owl","Snake","Frog","Rat","Cat","Dog","Tiger","Zebra","","","","","","","","","","","",""
                      ,"Rabbit","Mouse","Cat","Lizard","Goat","Cow","Tilapia","Bear","","","","","Giraffe"
                      ,"Domestic","Elephant","Hipopotamus","Crocodile","Dinosor","","","","","","","","","","","","",""]

        self.jazz=["Ella Fitzgerald","Piano","Jazz Band","Drum","Jazz brush","Louis Amstrong","John Coltrane","Miles Davis",
                    "Count Basie","Cycle of fiths","Two five one","Saxophone","Depression","Swing","Waltz","Smooth","Trombone"
                    ,"Love","Restaurant","Acid jazz","Sensational","Modes","Disorder","Acidity","Nineteen sixties","Oldies","Sorrow"
                    ,"Jazz","Funk","Bossa nova","Bebop","funky","soul","Composer","jazz man","Afrobeat","trap","jazz up","Country","Boogie","rap"
                    ,"Jazzist","folk","rumba","lento","Conga","Glee","Calypso","Billie holiday","presto","Surf rock","Fitzgerald","Ella"
                    ,"pedal","free","Infinite","Solist","concert","Minor","Major","Musicallity","Unaccompanied","samba","tonality"
                    ,"Modality","Sixth","Seventh","Eleventh","Thirteenth","Jazzification","Vocalist","Musically","Music","Organ"
                    ,"Trumpet","Partition","Lovers","conga","Alex","Anderson","Metaphor","Old","Cloudy","Reharmonization"]

        self.base=["is","on","and","for","you","me","then","after","before","learn","of","no","yes","again","but","even","odd","far","here"
                  ,"none","can","Qi","Jis","zen","often","out","long","still","take","fail","win","take","go","man","leave","make","day"
                  ,"walk","inner","outer","layer","edge","King","Queen","it","him","her","his","over"]

        self.nature=["Apple","Orange","Fruit","Tree","Leaf","Mango","Pear","River","Lake","Animals","Waterfall","Stars","Day","Night",
                    "Air","Ozone","Sky","Clouds","Earth","Soil","Water","Sun","Wind","Oxygen","Gases"]


        self.list={"alpha":self.alpha,"town":self.town,"jazz":self.jazz,"nature":self.nature,"sport":self.sport}

word=Word()      
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
            
            if self.timer<10:self.showIdle(0,2,1);print("BLUE FACE") #blue face,red eyes and normal mouth
            elif self.timer>=10 and self.timer<40: self.showIdle(1,2,1)#red face,red eyes and large mouth
            elif self.timer>=40 and self.timer<50: self.showIdle(1,1,1)#red face, blue eye, large mouth
            elif self.timer>=50 and self.timer<80: self.showIdle(0,1,1)#blue face, blue eye, large mouth
            else:self.state='idle';self.init_animation()

        #elif self.state=='disappear': 
            #screen.blit(self.samy['fire'],[self.pos[0],self.pos[1]]) #light stops blinking and remains
                
        self.timer+=1
        print('State: ',self.state,self.timer)
    
    def init_animation(self):
        self.timer=0;self.exFace=0;self.eyFace=0;self.exEye=0
        self.eyEye=0;self.exLimit=3;self.adFace=[1,3];self.adEye=[1,1]
        #self.state='appear'
player=Ennemy()
def Sky(n):
    Col={"blue":(28, 121, 190),"brown":(89, 57, 74),"indigo":(153, 105, 168),"black":(12, 14, 17)}
    if n!="black":
        x=screen.get_size(); width=20;print(x[0]/width)
        for i in range(35):
            py.draw.rect(screen,(Col[n][0]+i+1,Col[n][1]+i+1,Col[n][2]),[0,i*width,x[0],50])
    else:
        screen.fill(Col[n])        
  
game=Game()
def main():
    game.setLevel()
    while not game.Exit:
        #screen.fill((38, 141, 210))
        Sky("blue")

        for event in py.event.get():
            if event.type==KEYDOWN or event.type==KEYDOWN:
                game.letterPressed=event.unicode         
        for event in py.event.get():
            if event.type==KEYDOWN or event.type==KEYDOWN:
                game.letterPressed=event.unicode
            
            
                #print('Letter :'+game.letterPressed)
             
           
        keys=py.key.get_pressed()
        if keys[K_SPACE]:player.state='attack'
        if keys[K_ESCAPE]:game.Exit=True
        game.drawField()
        game.show()
        game.Generate_and_Destroy_Clouds()
        game.Cloudtrack()
        #game.show_Sky()
        #game.BackgroundClouds()
        #game.show_background()
        game.FrontClouds()
        game.display_text()
        

        game.generate_ballon()
        game.keeptrack()
        player.animate()
        
        

        py.display.update()
        time.tick(game.FPS)
    



if __name__=="__main__":
    main()
    sys.exit()
