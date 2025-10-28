# 海のプラスチックを集めるゲーム。上押すとすこし浮き上がる。魚型潜水艦。

import pyxel
import enum

FPS = 10
GAMETIME = 30

class Status(enum.Enum):
    START = 1
    PRE_MAIN = 2
    MAIN = 3
    ENDING = 4
    GAMEOVER = 5
    
class App():
    def __init__(self):
        pyxel.init(160,120, title="submarine", fps=FPS)
        pyxel.load("./assets/submarine.pyxres")
        self.umplus10 = pyxel.Font("./assets/umplus_j10r.bdf")
        self.umplus12 = pyxel.Font("./assets/umplus_j12r.bdf")

        self.status = Status.START
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if self.status == Status.START:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.gamecountdown = FPS*GAMETIME -1
                self.precountdown = FPS*3
                self.life = 3
                self.point = 0
                self.player_x = 15
                self.player_y = 40
                self.player_dy = 0
                self.status = Status.PRE_MAIN
            
                self.trush = [
                    (50, pyxel.rndi(0, 104), pyxel.rndi(0,2), True),
                    (100, pyxel.rndi(0, 104), pyxel.rndi(0,2), True),
                    (150, pyxel.rndi(0, 104), pyxel.rndi(0,2), True)
                ]

                self.fish = [ # x,cnter_y, y, kind, is_alive
                    (65, pyxel.rndi(30,90), 0, pyxel.rndi(0,2),True),
                    (125, pyxel.rndi(30,90), 0, pyxel.rndi(0,2),True),
                    (190, pyxel.rndi(30,90), 0, pyxel.rndi(0,2),True)
                ]
                for i, (x,center_y,y,kind,is_alive) in enumerate(self.fish):
                    self.fish[i] = (x, center_y, center_y, kind, is_alive) #yの値をコピー

        elif self.status == Status.PRE_MAIN:
            if self.precountdown == FPS*3:
                pyxel.play(1,4)
            elif self.precountdown < 1:
                self.status = Status.MAIN
                
            self.precountdown -= 1

        elif self.status == Status.MAIN:
            # カウントダウン
            self.gamecountdown -= 1
            if self.gamecountdown == FPS*3:
                pyxel.play(1,2)
            
            # 終了判定
            if self.life < 1:
                self.status = Status.GAMEOVER
                pyxel.play(1,3)
            elif self.gamecountdown < 1:
                self.status = Status.ENDING

            # 更新処理
            self.update_player()

            for i, v in enumerate(self.trush):
                self.trush[i] = self.update_trush(*v)

            for i,v in enumerate(self.fish):
                self.fish[i] = self.update_fish(*v)

        elif self.status == Status.ENDING:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.status = Status.START
                
        elif self.status == Status.GAMEOVER:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.status = Status.START

    def update_player(self):
        # 左右、下はいける
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width -16)
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(0, self.player_x -2)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player_y += 2 
            

        # 上はブースト
        if pyxel.btnp(pyxel.KEY_UP, 1, 3) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP, 1, 3):
            self.player_dy =  -6#5
            
        self.player_dy = min(self.player_dy+1, 1)

        self.player_y += self.player_dy
        self.player_y = min(self.player_y, pyxel.height-16)
        self.player_y = max(self.player_y, 0)

    def collide(self, x, y):
        if x > self.player_x-8 and x < self.player_x + 16+8 and y+8 > self.player_y-8 and y+8 < self.player_y+16+8:
            return True
        else:
            return False
    def update_trush(self, x,y, kind,is_alive):
        if is_alive and self.collide(x,y):
            self.point += 10*(kind+1)
            is_alive = False
            pyxel.play(0, 0)
        
        x = x - 2

        if x < -40:
            x += 200
            y = pyxel.rndi(0,104)
            kind = pyxel.rndi(0,2)
            is_alive = True
        return (x,y,kind, is_alive)
        
    def update_fish(self, x,center_y,y,kind,is_alive):
        if is_alive and self.collide(x,y):
            self.life += -1
            is_alive = False
            pyxel.play(0, 1)

        x = x - 4

        if x < -40:
            x += 200
            center_y = pyxel.rndi(30,90)
            kind = pyxel.rndi(0,2)
            is_alive = True

#        y = center_y + pyxel.sin((self.gamecountdown%80)*360/80) * (kind+1)*10
        y = center_y + pyxel.sin(((FPS*GAMETIME -self.gamecountdown)%80)*360/80) * (kind+1)*10
#        y = center_y + pyxel.sin((pyxel.frame_count%80)*360/80) * (kind+1)*10
        return (x,center_y,y,kind, is_alive)
        
    def draw(self):
        if self.status in [Status.MAIN, Status.PRE_MAIN]:
            pyxel.cls(6)
            # draw bg
#            pyxel.bltm(0,0, 0, 0,0, 160,120)
            offset = (self.gamecountdown//3)%pyxel.width
            pyxel.bltm(offset,0, 0, 0,0, 160,120)
            pyxel.bltm(-pyxel.width+offset,0, 0, 0,0, 160,120)
            pyxel.blt(offset, pyxel.height-16, 1, 0,16, 160,16, 6)
            pyxel.blt(-pyxel.width+offset, pyxel.height-16, 1, 0,16, 160,16, 6)
 
            # draw player
            pyxel.blt(self.player_x,self.player_y, 0, 0,0, 16,16, 6, scale=2.0)

            # draw fish
            for (x,center_y, y,kind,is_alive) in self.fish:
                if is_alive:
                    pyxel.blt(x,y, 0, (kind)*16, 16, 16,16, 6)
        
            # draw trush
            for (x,y,kind,is_alive) in self.trush:
                if is_alive:
                    pyxel.blt(x,y, 0, (1+kind)*16, 0, 16,16, 6)

            # draw point
            s = f"POINT {self.point:>4}"
            pyxel.text(5,5, s, 12)
            pyxel.text(4,5, s, 0)

            # draw time
            s = f"TIME {self.gamecountdown//FPS + 1: >2}"
            pyxel.text(130,5, s, 12)
            pyxel.text(129,5, s, 0)
            
            # draw life
            for i in range(self.life, 0, -1):
                pyxel.blt(90+10*i, 5, 0, 4,37, 10,10, 6)

            # mainの前のカウントダウン3,2,1
            if self.status == Status.PRE_MAIN:
                pyxel.blt(75,40, 0,  16*(self.precountdown//FPS + 1)-16, 48, 16,16, 6, scale=3.0)  
#                s = f"{self.precountdown//FPS + 1}"
#                pyxel.text(65,40, s, 12, self.umplus12)
#                pyxel.text(64,39, s, 0 ,self.umplus12)
                

        elif self.status == Status.START:
            pyxel.cls(0)
            pyxel.blt(65,80, 0, 0,0, 16,16, 6, scale=3.0)

            s = "MISSION:\n海のプラスチックごみを集めて\nいきものを まもれ！"
            if pyxel.frame_count%(FPS*2) > 2:
                pyxel.text(10, 10, s, 10, self.umplus10)
            
            s = f"press A to start"
            pyxel.text(40,110,s, 10)
        elif self.status == Status.ENDING:
            pyxel.cls(0)
            
#            s = f"POINT\n\n{self.point:>4} +   100 x {self.life:>1} = {self.point + 100* self.life :>4}"
#            pyxel.text(30,30, s, 8)
#            pyxel.text(29,30, s, 10)
#            pyxel.blt(57,42, 0, 4,37, 10,10, 6)

            s = f" POINT\n{self.point:>4} +  100 x {self.life:>1} = {self.point + 100* self.life :>4}"
            pyxel.text(5,30, s, 10,self.umplus10)
            pyxel.blt(45,46, 0, 4,37, 10,10, 6)

            s = f"Thank you for playing!"
            pyxel.text(40,90,s, pyxel.frame_count%16)
            s = f"press A to restart"
            pyxel.text(40,110,s, 10)
            
        elif self.status == Status.GAMEOVER:
            pyxel.cls(0)

#            s = f"POINT {self.point:>4}"
#            pyxel.text(60,40, s, 8)
#            pyxel.text(59,40, s, 10)
            s = f" POINT\n{self.point:>4} +  100 x {self.life:>1} = {self.point + 100* self.life :>4}"
            pyxel.text(5,30, s, 10,self.umplus10)

            s = f"GAME OVER!"
            pyxel.text(60,90, s, pyxel.frame_count%16)
            s = f"press A to restart"
            pyxel.text(40,110, s, 10)            
            
App()
    