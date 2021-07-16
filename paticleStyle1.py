import pygame as pg
import random
import sys


class Particle:
    def __init__(self):
        self.particle_list = []

    def emit(self):
        self.delete()
        if self.particle_list:
            for particle in self.particle_list:
                particle[0][1] += particle[2][1]
                particle[0][0] += particle[2][0]
                particle[1] -= 0.2
                pg.draw.circle(screen, particle[3], particle[0], particle[1])

    def add_particle(self):
        px = pg.mouse.get_pos()[0]
        py = pg.mouse.get_pos()[1]
        radius = 10
        direction_y = random.randint(-3, 3)
        direction_x = random.randint(-3, 3)
        # added by me
        cr = random.randint(0, 255)
        cg = random.randint(0, 255)
        cb = random.randint(0, 255)
        color = (cr, cg, cb)
        par_circle = [[px, py], radius, [direction_x, direction_y], color]
        self.particle_list.append(par_circle)

    def delete(self):
        particle_copy = [particle for particle in self.particle_list if particle[1] > 0]
        self.particle_list = particle_copy


width, height = 500, 500

screen = pg.display.set_mode((width, height))
pg.display.set_caption("particle effect 1")
clock = pg.time.Clock()

particle_event = pg.USEREVENT + 1
pg.time.set_timer(particle_event, 50)


particle1 = Particle()


while True:
    screen.fill((30, 30, 30))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == particle_event:
            particle1.add_particle()

    particle1.emit()
    pg.display.update()
    clock.tick(120)
