#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# copyleft © 2013 Facundo M. Acevedo <facevedo[AT]csjn[DOT]com[DOT]ar>
#
# Distributed under terms of the GPLv3+ license.

"""

"""

# Módulos
import sys, random

import pygame
from pygame.locals import *

# Constantes
WIDTH = 1024
HEIGHT = 768

#Inicializo el random con la hora
random.seed()

# Clases
# ---------------------------------------------------------------------

class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radio = 7
        self.superficie = pygame.Surface((self.radio*2, self.radio*2))
        self.color=(177,167,255)
        self.rect = pygame.draw.circle(self.superficie,self.color, (self.radio, self.radio),  self.radio,0)
        #self.rect = pygame.Rect(0,0,self.radio*2, self.radio*2)
        #self.superficie.fill((177,167,255))

        self.speed = [0.5, -0.5]


    def actualizar(self, time, pala_jug, pala_cpu, obstaculos, puntos):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time

        if self.rect.left <= 0:
            puntos[1] += 1

        if self.rect.right >= WIDTH:
            puntos[0] += 1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

        if pygame.sprite.collide_rect(self, pala_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        if pygame.sprite.collide_rect(self, pala_cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo):
                self.speed[0] = -self.speed[0]
                self.rect.centerx += self.speed[0] * time

        return puntos

class Pala(pygame.sprite.Sprite):
    def __init__(self, x):

        pygame.sprite.Sprite.__init__(self)
        self.alto= 50
        self.ancho = 15
        self.superficie = pygame.Surface((self.alto, self.ancho))
        self.rect = pygame.Rect(x,HEIGHT/2 ,self.ancho, self.alto)
        self.color=(255, 255, 255)
        self.superficie.fill(self.color)


        self.speed = 0.5
    def mover(self, time, keys):
        if self.rect.top >=0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time

    def ia(self, time, ball):
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += (self.speed-0.2) * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= (self.speed-0.2) * time

class Obstaculos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.listado = []
        self.corrida = 0

    def _crear(self):
        posX=random.randint(50,WIDTH-50)
        posY=random.randint(0,HEIGHT)
        alto=random.randint(10,50)
        ancho=random.randint(10,80)

        forma = pygame.Rect(posX, posY, alto, ancho)
        self.listado.append(forma)

    def __iter__(self):
        return iter(self.listado)

    def actualizar(self):
        if self.corrida >= random.randint(155,230):
            self.corrida = 0
            self._crear()
        self.corrida +=1
        try:
            #Desaparecer
            if random.randint(0,1000) == 5:
                indice = random.randint(0,len(self.listado)-1)
                self.listado.pop(indice)

        except:
            pass

        if len(self.listado) >0:
            #Vibrar
            indice = random.randint(0,len(self.listado)-1)
            obstaculo = self.listado[indice]
            obstaculo.centerx +=random.randint(-15,15)
            obstaculo.centery +=random.randint(-15,15)



# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------


def load_image(filename, transparent=False):
    """Carga una imagen"""

    try: imagen = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message

    imagen = imagen.convert()
    if transparent:
        #Toma el color del pixel 0,0
        color = imagen.get_at((0,0))
        #Lo define como el color de la transparencia, osea asegurate que ese color
        #no sea párte de la imagen
        imagen.set_colorkey(color, RLEACCEL)
    return imagen

def texto(texto, posx, posy, color=(255,255,255)):
    fuente = pygame.font.Font('fonts/DroidSans.ttf', 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect



def main():
    #Creo la ventana, devuelve una superficie ( pygame.Surface)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #Sete el titulo de la ventana
    pygame.display.set_caption("PingPong")

    #Creo un reloj
    clock = pygame.time.Clock()

    #Seteo el fondo
    #imagen_fondo = load_image('imagenes/fondo.jpg')

    #Creo una bola
    bola = Bola()
    #Creo la pala
    pala_jug = Pala(30)
    pala_cpu = Pala(WIDTH - 30)

    #Creo obstaculos
    obstaculos = Obstaculos()

    puntos=[0,0]

    noEpilepcia = 0
    R= random.randint(0,255)
    G= random.randint(0,255)
    B= random.randint(0,255)


    #Bucle principal
    while True:
        #La idea es:
        #    1- manejar eventos
        #    2- actualizar el estado del juego
        #    3- redibujar la pantalla

        #Manejo los eventos
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                pygame.quit()
                sys.exit(0)

        #Framerate
        tiempo = clock.tick(60)
        keys = pygame.key.get_pressed()

        obstaculos.actualizar()
        pala_jug.mover(tiempo, keys)
        pala_cpu.ia(tiempo, bola)
        p_jug, p_jug_rect = texto(str(puntos[0]), WIDTH/4, 40)
        p_cpu, p_cpu_rect = texto(str(puntos[1]), WIDTH-WIDTH/4, 40)

        #puntos = bola.actualizar(tiempo, pala_jug, pala_cpu, obstaculos, puntos)
        puntos = bola.actualizar(tiempo, pala_jug, pala_cpu,obstaculos, puntos)

        #Reposiciono las imagenes
        if puntos[0] < 5 or puntos[1] < 5:
            superficie_fondo = pygame.Surface((WIDTH, HEIGHT))
            screen.blit(superficie_fondo, (0, 0))
        else:
            if noEpilepcia >= 15:
                noEpilepcia = 0
                R= random.randint(0,255)
                G= random.randint(0,255)
                B= random.randint(0,255)
                #screen.fill((R,G,B))
            noEpilepcia +=1

        screen.blit(superficie_fondo, (0, 0))
        #screen.blit(bola.imagen, bola.rect)
        screen.blit(bola.superficie, bola.rect)
        for obstaculo in obstaculos:
            R= random.randint(0,255)
            G= random.randint(0,255)
            B= random.randint(0,255)
            pygame.draw.rect(screen,(R,G,B),obstaculo)
        pygame.draw.rect(screen,pala_jug.color, pala_jug)
        pygame.draw.rect(screen,pala_cpu.color, pala_cpu)
        #screen.blit(pala_jug.imagen, pala_jug.rect)
        #screen.blit(pala_cpu.imagen, pala_cpu.rect)
        screen.blit(p_jug, p_jug_rect)
        screen.blit(p_cpu, p_cpu_rect)


        #actualiza todas las pantallas
        pygame.display.flip()

    return 0

if __name__ == '__main__':
    pygame.init()
    main()






