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
import sys

import pygame
from pygame.locals import *

# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
# ---------------------------------------------------------------------

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

def main():
    #Creo la ventana
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #Sete el titulo de la ventana
    pygame.display.set_caption("PingPong")

    #Seteo el fondo
    imagen_fondo = load_image('imagenes/fondo.jpg')
    screen.blit(imagen_fondo, (0, 0))

    #Bucle principal
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        #actualiza todas las pantallas
        pygame.display.flip()

    return 0

if __name__ == '__main__':
    pygame.init()
    main()






