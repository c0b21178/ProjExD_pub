"""逃げるな！こうかとん！
左右に動いて逃げるこうかとんを捕まえるゲーム。
マウスの動きに合わせて腕が動き、クリックしたら腕が振り下ろされる。
腕が当たったらこうかとんがびっくりして回転し、腕が当たらなかったらミスになる。
また、腕が当たるとこうかとんの動くスピードがランダムだ変わる。
こうかとんに10回腕を振り下ろすか、残機が0になったらゲームが終了。
"""

#moduleのインポート
import os
import pygame as pg
import random

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


"""関数の作成"""
def load_image(name, colorkey = None, scale = 1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound


"""クラスの作成"""
class Fist(pg.sprite.Sprite):
    
    """腕の画像の貼り付け"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("fist.png", -1, 0.75)
        self.fist_offset = (-235, -80)
        self.punching = False

    """マウスと連動"""
    def update(self):
        pos = pg.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    """マウスが押された時の処理"""
    def punch(self, target):
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    """マウスから離れた時の処理"""
    def unpunch(self):
        self.punching = False


class Bird(pg.sprite.Sprite):

    """こうかとんが画面上を動き回り、パンチされたら回転して速さがランダムで変わる。"""
    def __init__(self):
        global x
        x= random.randint(0,9)
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(f"{x}.png", -1, 1) #木下宗一郎
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.centerx = random.randint(0, 1200) #初期位置をランダムに
        self.rect.centery = random.randint(0, 600)
        self.movex = 3 #最初の速さ
        self.movey = 3
        self.dizzy = False

    """走り回るか、叩かれて一回転するか"""
    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._run()

    """こうかとんが走り回る"""
    def _run(self):
        newpos = self.rect.move((self.movex, self.movey))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.movex = -self.movex
                newpos = self.rect.move((self.movex, self.movey))
                self.image = pg.transform.flip(self.image, True, False)
            if self.rect.top > self.area.top or self.rect.bottom < self.area.bottom:
                self.movey = -self.movey
                newpos = self.rect.move((self.movex, self.movey))
        self.rect = newpos

    """こうかとんが回転して速さがランダムになる処理"""
    def _spin(self):
        speed = random.randint(1, 20) #当たったら速さがランダムに
        center = self.rect.center
        self.dizzy = self.dizzy + 18
        if self.dizzy >= 720:
            self.dizzy = False
            self.image = self.original
            self.movex = speed
            self.movey = speed
            global x
            x = random.randint(0,9)
            self.image, self.rect = load_image(f"{x}.png", -1) #木下　宗一郎
            screen = pg.display.get_surface()
            self.area = screen.get_rect()
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    """回り始める"""
    def punched(self):
        if not self.dizzy:
            self.dizzy = True
            self.original = self.image


def main():
    #画面などの設定
    pg.init()
    screen = pg.display.set_mode((1200, 600), pg.SCALED)
    pg.display.set_caption("逃げるな!こうかとん！")
    pg.mouse.set_visible(False)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background = pg.image.load("rensyu06\data\koka.png")#木下　宗一郎
    #background.fill((255, 255, 0))

    if pg.font:
        font = pg.font.Font("rensyu06\IPAexfont00401\ipaexg.ttf", 64)
        text = font.render("こうかとんを10回叩け!", True, (10, 10, 10))
        textpos = text.get_rect(centerx = background.get_width() / 2, y = 10)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pg.display.flip()

    #準備
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    bird = Bird()
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((bird, fist))
    clock = pg.time.Clock()
    count = 9   #残機
    score = 0    #得点

    going = True
    while going:
        clock.tick(60)

        #eventが起こったら
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN: #mouseを押したら
                if fist.punch(bird):
                    punch_sound.play()  # punch
                    bird.punched()
                    score += 1
                else:
                    whiff_sound.play()  # miss
                    count -= 1
            elif event.type == pg.MOUSEBUTTONUP: #mouseから離れたら
                fist.unpunch()

        if count == 0: #5回missしたら
            font = pg.font.Font("rensyu06\IPAexfont00401\ipaexg.ttf", 64)
            text = font.render("Game Over…", True, (255, 0, 0), (10, 10, 10))
            textpos = text.get_rect(centerx = background.get_width() / 2,
                                    centery = 150)
            background.blit(text, textpos)
            
        elif score == 10: #10点になったら
            font = pg.font.Font("rensyu06\IPAexfont00401\ipaexg.ttf", 64)
            text = font.render("Clear!", True, (255, 0, 0), (255,255,255))
            textpos = text.get_rect(centerx = background.get_width() / 2,
                                    centery = 150)
            background.blit(text, textpos)

        font = pg.font.Font("rensyu06\IPAexfont00401\ipaexg.ttf", 25)
        text = font.render("残機：" + str(count), True, (10, 10, 10), (255, 255, 0)) #残機の表示
        textpos = text.get_rect(x = 0, y = 575)
        text2 = font.render("得点：" + str(score), True, (10, 10, 10), (255, 255, 0)) #得点の表示
        textpos2 = text.get_rect(x = 0, y = 550)
        allsprites.update()
        background.blit(text, textpos)
        background.blit(text2, textpos2)

        allsprites.update()
        

        #描画
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.update()

        """countが0、scoreが10になったら5秒後に終了"""
        if count == 0:
            pg.time.wait(2000)
            return
        elif score == 10:
            pg.time.wait(5000)
            return


    pg.quit()


# Game Over


if __name__ == "__main__":
    main()