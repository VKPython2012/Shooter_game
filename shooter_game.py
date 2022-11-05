#Create your own shooter

from pygame import *
from random import randint

live, lost, hits = 5, 0, 0

num_shots, reload_time = 0, 0

class Player(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 90))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and player.rect.x > 5:
            player.rect.x -= player.speed
        if keys_pressed[K_RIGHT] and player.rect.x < 595:
            player.rect.x += player.speed
        window.blit(self.image, (self.rect.x, self.rect.y))
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5)
        bullets_group.add(bullet)
        
class Monsters(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
        self.monsters = sprite.Group()

    def update(self):
        while len(self.monsters) < 5:
            monster = sprite.Sprite()
            monster.image = self.image
            monster.rect = monster.image.get_rect()
            monster.rect.x = randint(5, 620)
            monster.rect.y = randint(5, 80)

            self.monsters.add(monster)
        
        for monsters in self.monsters:
            monsters.rect.y += self.speed

            if monsters.rect.y > 420:
                global lost
                lost += 1
                monsters.rect.x = randint(5, 620)
                monsters.rect.y = randint(5, 80)
        self.monsters.draw(window)

class Asteroids(sprite.Sprite):
    def __init__(self, player_image,  player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        
        self.group = sprite.Group()

    def update(self):
        while len(self.group) < 3:
            asteroid = sprite.Sprite()
            asteroid.image = self.image
            asteroid.rect = asteroid.image.get_rect()
            asteroid.rect.x = randint(5, 620)
            asteroid.rect.y = randint(5, 80)

            self.group.add(asteroid)
        
        for asteroid in self.group:
            asteroid.rect.y += self.speed

            if asteroid.rect.y > 420:
                asteroid.rect.x = randint(5, 620)
                asteroid.rect.y = randint(5, 80)
        self.group.draw(window)

class Bullet(sprite.Sprite):
    def __init__(self, bullet_image, bullet_x, bullet_y, bullet_speed):
        super().__init__()
        self.image = transform.scale(image.load(bullet_image), (20, 35))
        self.speed = bullet_speed
        self.rect = self.image.get_rect()
        self.rect.x = bullet_x
        self.rect.y = bullet_y
    def update(self):
        if self.rect.y == 0: self.kill()
        if self.rect.y > 0: self.rect.y -= self.speed
        window.blit(self.image, (self.rect.x, self.rect.y))

window = display.set_mode((700, 500))
display.set_caption("Shooter game")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

player = Player('rocket.png', 295, 410, 2)
monsters = Monsters('ufo.png', 0, 0, 1)
asteroids = Asteroids('asteroid.png', 1)

monsters_group = sprite.Group()
bullets_group = sprite.Group()
asteroid_group = sprite.Group()

# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
lost = 0
hits = 0

font.init()
text = font.Font(None, 45)
Lose = text.render('YOU LOSE!', True, (255, 0, 0))
Win = text.render('YOU WIN!', True, (0, 255, 0))



finish = False
clock = time.Clock()
FPS = 30

reload_pause_time = None
elapsed_time = 750
game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))
        player.update()

        keys_pressed = key.get_pressed()

        if keys_pressed[K_SPACE]: 
            if not reload_pause_time:
                player.fire()
                num_shots += 1

        if num_shots >= 5: 
            reload_time = True
            reload_pause_time = time.get_ticks()
            num_shots = 0       

        elapsed_time = time.get_ticks() - reload_pause_time if reload_pause_time else 750

        if reload_time: 
            if elapsed_time < 750:
                font.init()
                text = font.Font(None, 30)
                reload_text = text.render('WAIT, RELOAD...', True, (255, 255, 255))
                window.blit(reload_text, (200, 470))
            else:
                reload_text = text.render('WAIT, RELOAD...', False, (255, 255, 255))
                reload_pause_time = None
                reload_time = False


        

        bullets_group.update()
        monsters.update()
        asteroids.update()

        sprite_list = sprite.spritecollide(player, monsters.monsters, True)
        bullet_hits = sprite.groupcollide(bullets_group, monsters.monsters, True, True)
        asteroid_hit = sprite.spritecollide(player, asteroids.group, True)
        hits += len(bullet_hits)

        win = hits >= 5
        lose_life = lost >= 3 or len(sprite_list) > 0 or len(asteroid_hit) > 0
        if lose_life: 
            live -= 1
            lost = 0
            sprite_list = None
            asteroid_hit = None
        lose = live == 0 
        if lose or win:
            finish = True
            print(sprite_list)

        lost_count = text.render(('Missed: ' + str(lost)), 1, (255, 255, 255))
        life_count = text.render(('Life left: ' + str(lost)), 1, (255, 255, 255))
        kill_count = text.render(('Killed: ' + str(hits)), 1, (255, 255, 255))


        window.blit(lost_count, (0, 0))
        window.blit(life_count, (0, 70))
        window.blit(kill_count, (0, 35))
        
    else:
        if lose:
            window.blit(Lose, (265, 215))
        elif win:
            window.blit(Win, (265, 215))
    display.update()