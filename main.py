import pygame as pg
import random
import sys


class MyShip(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.right = False
        self.left = False

        self.image = pg.Surface((48, 48), pg.SRCALPHA)
        # self.image.fill((255, 255, 255))
        pg.draw.polygon(self.image, (230, 240, 250), ((24, 0), (48, 24), (48, 36), (36, 36), (36, 48), (12, 48),
                                                      (12, 36), (0, 36), (0, 24)))
        self.rect = self.image.get_rect()

        self.rect.x = 150
        self.rect.y = 450

    def update(self, *args, **kwargs):
        if self.left:
            self.rect.x -= 20
            if self.rect.x < 0:
                self.rect.x = 0
            self.left = False
        if self.right:
            self.rect.x += 20
            if self.rect.x >= width - 48:
                self.rect.x = width - 48
            self.right = False

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        bullet_list.add(bullet)


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super(Bullet, self).__init__()

        self.image = pg.Surface((10, 20))
        self.image.fill((240, 50, 0))
        self.rect = self.image.get_rect()

        self.rect.x = pos_x + 14
        self.rect.y = pos_y + 14

    def update(self, *args, **kwargs):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.kill()


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # for color variations
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.color = (r, g, b)

        self.random_shape = random.randint(1, 5)

        self.image = pg.Surface((30, 30), pg.SRCALPHA)
        if self.random_shape == 1:
            pg.draw.circle(self.image, self.color, (15, 15), 15)
        elif self.random_shape == 2:
            pg.draw.rect(self.image, self.color, (0, 0, 30, 30))
        elif self.random_shape == 3:
            pg.draw.polygon(self.image, self.color, ((0, 15), (15, 30), (30, 15), (15, 0)))
        elif self.random_shape == 4:
            pg.draw.polygon(self.image, self.color, ((10, 0), (20, 0), (30, 10), (30, 20), (20, 30),
                                                     (10, 30), (0, 20), (0, 10)))
        else:
            pg.draw.polygon(self.image, self.color, ((15, 0), (15, 30), (30, 15), (0, 15)))

        self.rect = self.image.get_rect()

        ex = random.randint(0, width - 32)
        ey = random.randint(-600, 0)

        self.rect.x = ex
        self.rect.y = ey

    def update(self, *args, **kwargs):
        self.rect.y += 1
        if self.rect.y > height:
            self.kill()
            enemy_list.add(Enemy())


class ParticleEffect:
    def __init__(self):
        super().__init__()
        self.particle_list = []

    def emit(self):
        if len(self.particle_list) > 0:
            self.delete()
            for particle in self.particle_list:
                particle[0][0] += particle[2][0]
                particle[0][1] += particle[2][1]
                particle[1] -= 0.2
                pg.draw.circle(screen, particle[3], particle[0], particle[1])

    def add_particle(self, pos_x, pos_y, color):
        px = pos_x
        py = pos_y
        radius = 5
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        color = color
        par_circle = [[px, py], radius, [direction_x, direction_y], color]

        self.particle_list.append(par_circle)

    def delete(self):
        particle_copy = [particle for particle in self.particle_list if particle[1] > 0]
        self.particle_list = particle_copy


def game_over():
    pg.quit()
    sys.exit()

# ---------------------------------- Main Game ----------------------------------- #


pg.init()

width, height = 350, 550

screen = pg.display.set_mode((width, height))
pg.display.set_caption("games")
clock = pg.time.Clock()

# Player initialization
player = MyShip()
my_ships = pg.sprite.Group()
my_ships.add(player)

# Bullet
bullet_list = pg.sprite.Group()

# enemy list
enemy_list = pg.sprite.Group()
for i in range(20):
    enemy = Enemy()
    enemy_list.add(enemy)

# score and lives
score = 0
live = 100

# fonts
fonts = pg.font.SysFont('arial', 20, True)

particle = ParticleEffect()


while True:
    screen.fill((30, 30, 30))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player.left = True
            if event.key == pg.K_RIGHT:
                player.right = True
            if event.key == pg.K_SPACE:
                player.shoot()

    # group collision
    coll_1 = pg.sprite.groupcollide(enemy_list, bullet_list, True, True)
    if coll_1:
        for enem, bulle in coll_1.items():
            enemy_list.add(Enemy())
            for _ in range(10):
                particle.add_particle(enem.rect.x, enem.rect.y, enem.color)

            score += 10

    coll_2 = pg.sprite.groupcollide(enemy_list, my_ships, True, False)
    if coll_2:
        for enem, ship in coll_2.items():
            enemy_list.add(Enemy())
            for _ in range(10):
                particle.add_particle(enem.rect.x, enem.rect.y, enem.color)
        live -= 10
        if live <= 0:
            game_over()

    my_ships.update()
    bullet_list.update()
    enemy_list.update()
    bullet_list.draw(screen)
    enemy_list.draw(screen)
    my_ships.draw(screen)

    particle.emit()

    # for score and lives
    pg.draw.rect(screen, (100, 200, 50), (0, height-49, width, 49))
    pg.draw.line(screen, (100, 255, 50), (0, height-50), (width, height-50))

    # score and live
    score_text = fonts.render(f'SCORE: {score}', True, (20, 20, 200))
    live_text = fonts.render(f'LIVE: {live}', True, (20, 10, 200))
    screen.blit(score_text, (10, 510))
    screen.blit(live_text, (250, 510))

    pg.display.update()
    clock.tick(60)
