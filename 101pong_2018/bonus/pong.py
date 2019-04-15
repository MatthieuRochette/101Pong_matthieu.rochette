#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------Importations----------|

import pygame
import random
from sys import exit
import math
from pygame.locals import *

#----------Initialisation des variables----------|

pygame.init()
fenetre=pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Module Math: Pong101")
information_resolution=pygame.display.Info()
pygame.key.set_repeat(1, 1)
temps=pygame.time.Clock()
ips = 60
compteur = 0
boucle=True

# ---- Calcul angle + collisions ----
def calc_angle_with_cos(adjacent_side, hypotenuse):
	if hypotenuse != 0 :
		cos = adjacent_side / hypotenuse
		angle = math.acos(cos)
		angle = round(angle * 180 / math.pi, 2)
		return (angle)
	else:
		print("Erreur : division par zéro", file=stderr)
		pygame.quit()
		exit(0)

def calc_vect(x0, y0, z0, x1, y1, z1) :
    vect_x = x1 - x0
    vect_y = y1 - y0
    vect_z = z1 - z0
    vect = [vect_x, vect_y, vect_z]
    return (vect)

def calc_norm(vector) :
    squared_x = vector[0]**2
    squared_y = vector[1]**2
    squared_z = vector[2]**2
    norm = math.sqrt(squared_x + squared_y + squared_z)
    return (norm)


class Personnage1(pygame.sprite.Sprite):
	def __init__(self,file = ("player1.png")):
		super().__init__()
		self.image = pygame.Surface([32, 64])
		self.image = self.personnage=pygame.image.load(file).convert_alpha()
		self.rect = self.personnage.get_rect()
		self.rect.x = 14
		self.rect.y = 360 
		self.position = (self.rect.x, self.rect.y)
		self.vitesse = 10
	def haut(self):
		for i in range(self.vitesse) :
			if self.rect.y > 6:
				self.rect.y -= 1
				self.position = (self.rect.x, self.rect.y)
	def bas(self):
		for i in range(self.vitesse) :
			if self.rect.y < 648 :
				self.rect.y += 1
				self.position = (self.rect.x, self.rect.y)
	def arret(self):
		self.rect.x += 0
		self.rect.y += 0

class Personnage2(pygame.sprite.Sprite):
	def __init__(self,file = ("player2.png")):
		super().__init__()
		self.image = pygame.Surface([32, 64])
		self.image = self.personnage=pygame.image.load(file).convert_alpha()
		self.rect = self.personnage.get_rect()
		self.rect.x = 1233
		self.rect.y = 360 
		self.position = (self.rect.x, self.rect.y)
		self.vitesse = 10
	def haut(self):
		for i in range(self.vitesse) :
			if self.rect.y > 6:
				self.rect.y -= 1
				self.position = (self.rect.x, self.rect.y)
	def bas(self):
		for i in range(self.vitesse) :
			if self.rect.y < 648 :
				self.rect.y += 1
				self.position = (self.rect.x, self.rect.y)
	def arret(self):
		self.rect.x += 0
		self.rect.y += 0

class Ball(pygame.sprite.Sprite):
	def __init__(self,file = ("ball.gif")):
		super().__init__()
		self.image = pygame.Surface([32, 32])
		self.image = self.personnage=pygame.image.load(file).convert_alpha()
		self.rect = self.personnage.get_rect()
		self.rect.x = float(630)
		self.rect.y = float(340) 
		self.position = (self.rect.x, self.rect.y)
		self.vitesse = 1
		self.angle = 0
		self.wdir = random.randrange(2)
		self.hdir = 1
		self.count = 0
	def reset(self):
		self.count = 0
		self.rect.x = 630
		self.rect.y = 340
		self.vitesse = 2
		self.wdir = random.randrange(2)

#----------Groupes--------|

personnage1 = Personnage1()
personnage2 = Personnage2()
ball = Ball()
groupe_player1 = pygame.sprite.Group()
groupe_player2 = pygame.sprite.Group()
groupe_ball = pygame.sprite.Group()
groupe_player1.add(personnage1)
groupe_player2.add(personnage2)
groupe_ball.add(ball)

# ---- Calcul du vecteur et de l'angle pour la balle ----
def generate_angle(ball) :
	ball.angle = 1.0 + random.uniform(0, 1)
	vect_hypo = calc_vect(ball.rect.x, 0, ball.rect.y, ball.rect.x + ball.vitesse, 0, float(ball.rect.y + ball.angle))
	vect_proj = [vect_hypo[0], vect_hypo[1], 0]

	norm_vect_hypo = calc_norm(vect_hypo)
	norm_vect_proj = calc_norm(vect_proj)

	angle = calc_angle_with_cos(norm_vect_proj, norm_vect_hypo)
	print("angle =", angle/20)
	return (angle / 20)

ball.angle = generate_angle(ball)

#----------Boucle du jeu----------|

while boucle == True:
	temps.tick(ips)
#----------Affichages-----------|
	fond=pygame.image.load("map_pong.png").convert()
	fenetre.blit(pygame.transform.scale(fond, (1280, 720)), (0,0))
	groupe_player1.draw(fenetre)
	groupe_player2.draw(fenetre)
	groupe_ball.draw(fenetre)
	pygame.display.flip()

	#On s'occupe des évènements lorsqu'il y a une collision:
	for i in range(5) :
		if ball.wdir == 0:
			ball.rect.x += ball.vitesse
			if ball.hdir == 0:
				ball.rect.y += ball.angle
			else:
				ball.rect.y -= ball.angle
			if ball.rect.y <= 6 or ball.rect.y >= 680:
				print ("collision :", ball.hdir, " et y =", ball.rect.y)
				if ball.hdir != 0:
					ball.hdir = 0
					ball.rect.y = 7
				else:
					ball.hdir = 1
					ball.rect.y = 679
				print ("y =", ball.rect.y)
			if ball.rect.x <= 14 or ball.rect.x >= 1234:
				print ("BUUUUUUUUUUUUT!!")
				ball.angle = generate_angle(ball)
				ball.reset()
			if ball.rect.x <= 48 or ball.rect.x >= 1202 :
				if personnage2.rect.y <= ball.rect.y <= personnage2.rect.y + 64 or personnage2.rect.y <= ball.rect.y + 32 <= personnage2.rect.y + 64:
					ball.wdir = 1
					ball.count += 1
					if ball.count % 10 == 9:
						ball.vitesse += 1
		else:
			ball.rect.x -= ball.vitesse
			if ball.hdir == 0:
				ball.rect.y += ball.angle
			else:
				ball.rect.y -= ball.angle
			if ball.rect.y <= 6 or ball.rect.y >= 680:
				print ("collision :", ball.hdir, " et y =", ball.rect.y)
				if ball.hdir != 0:
					ball.hdir = 0
					ball.rect.y = 7
				else:
					ball.hdir = 1
					ball.rect.y = 679
				print ("y =", ball.rect.y)
			if ball.rect.x <= 14 or ball.rect.x >= 1234:
				print ("BUUUUUUUUUUUUT!!")
				ball.angle = generate_angle(ball)
				ball.reset()
			if ball.rect.x <= 48 or ball.rect.x >= 1202 :
				if personnage1.rect.y <= ball.rect.y <= personnage1.rect.y + 64 or personnage1.rect.y <= ball.rect.y + 32 <= personnage1.rect.y + 64:
					ball.wdir = 0
					ball.angle += random.uniform(-0.05, 0.05)
					ball.count += 1
					if ball.count % 10 == 9:
						ball.vitesse += 1

	#Mise en place du temps: le signe // permet d'avoir le résultat sous forme d'entier de la division.
	secondes_totales = compteur // ips
	secondes = secondes_totales % 60
	minutes = secondes_totales//60
	heures = secondes_totales//3600
	pygame.display.set_caption("Temps de jeu: {}:{}:{} IPS: {}".format(heures,minutes,secondes, str(int(temps.get_fps()))))
#----------Gestion des touches----------|

	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.display.quit()
			pygame.quit()
			exit()
	keys=pygame.key.get_pressed()
	if keys[pygame.K_UP]:#Si le joueur appuie sur la flèche du haut:
		personnage2.haut()
	if keys[pygame.K_DOWN]:#Si le joueur appuie sur la flèche du bas:
		personnage2.bas()
	if keys[K_z]:
		personnage1.haut()
	if keys[K_s]:
		personnage1.bas()
	compteur += 1#On augmente de 1 la valeur pour le compteur.

	pygame.display.flip()#raffraichissement
exit()
