#coding=utf-8

import pygame
import time
from pygame.locals import * 
import random


class Bullet(object):
	def __init__(self, screen, x, y, image):
		self.x = x 
		self.y = y
		self.image = pygame.image.load(image)
		self.screen = screen

	def blit(self): 				#放置玩家飞机的子弹图片
		self.screen.blit(self.image, (self.x, self.y))	 


class userBullet(Bullet):
	def __init__(self, screen, x, y):
		Bullet.__init__(self, screen, x + 40, y - 20, "./feiji/bullet.png")

	def blit(self): 				#放置玩家飞机的子弹图片
		Bullet.blit(self)	   

	def move(self):
		self.y -= 15

	def judge(self):				#判断子弹是否越界
		if self.y < -50:
			return False
		else:
			return True


class enemyBullet(Bullet):
	def __init__(self, screen, x, y):
		Bullet.__init__(self, screen, x + 22, y + 35, "./feiji/bullet1.png")

	def blit(self): 				#放置玩家飞机的子弹图片
		Bullet.blit(self)

	def move(self):					#敌机移动
		self.y += 15

	def judge(self):				#判断子弹是否越界
		if self.y > 800:
			return False
		else:
			return True


class Plane(object):
	def __init__(self, screen, x, y, image):
		self.x = x
		self.y = y
		self.image = pygame.image.load(image)      #导入玩家飞机图片
		self.screen = screen
		self.bullet_list = []

	def blit(self):			#放置玩家飞机方法         Notice：飞机发射的炸弹，所以fire()以后在飞机的blit中调用并且移动
		self.screen.blit(self.image, (self.x, self.y))	
		for bullet in self.bullet_list:
			bullet.blit() 
			bullet.move()
			if not bullet.judge():
				self.bullet_list.remove(bullet)



class user_Plane(Plane):
	def __init__(self, screen):
		Plane.__init__(self,  screen, 190, 700, "./feiji/hero1.png")

	def blit(self):			#放置玩家飞机方法         Notice：飞机发射的炸弹，所以fire()以后在飞机的blit中调用并且移动
		Plane.blit(self)

	def fire(self):			#玩家开火
		self.bullet_list.append(userBullet(self.screen, self.x, self.y))


class enemy_Plane(Plane):
	def __init__(self, screen):
		Plane.__init__(self, screen, 190, 0, "./feiji/enemy0.png")
		self.times = 0

	def blit(self):			#放置玩家飞机方法         Notice：飞机发射的炸弹，所以fire()以后在飞机的blit中调用并且移动
		Plane.blit(self)
		
	def fire(self):			#让敌机自动开火
		random_num =  random.randint(0,100)
		random_list = [10,20,30,40,50,60,70,80,90]
		if random_num in random_list:
			self.bullet_list.append(enemyBullet(self.screen, self.x, self.y))
	
	def move(self):		#让敌机自动移动
		if self.times % 2 == 0:
			self.x += 5
		else:
			self.x -= 5
		if self.x >= 430 or self.x <= 0:
			self.times += 1


def monitor_keyboard(userplane):    #监测键盘以及鼠标点击
	for event in pygame.event.get():   
		if event.type == QUIT:
				exit()
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:    		#检测左键
				userplane.x -= 10
			elif event.key == K_RIGHT:   	#检测右键
				userplane.x += 10
			elif event.key == K_DOWN:		#检测下键
				userplane.y += 10
			elif event.key == K_UP:			#检测上键
				userplane.y -= 10
			elif event.key == K_SPACE:		#检测空格键
				userplane.fire()
			elif event.key == K_ESCAPE:		#检测退出键
				exit()


def main():
	screen = pygame.display.set_mode((480, 852), 0, 32)    		#创建一个480*852尺寸的窗口
	background = pygame.image.load("./feiji/background.png")    #导入背景图片
	user_plane = user_Plane(screen)   	#创建玩家飞机
	enemy_plane = enemy_Plane(screen)	#创建敌机

	
	while True:
		screen.blit(background, (0, 0))    #将背景图片贴到窗口上，对齐点是(0,0)点处对齐贴

		user_plane.blit()		   #显示玩家飞机并且显示移动的子弹

		enemy_plane.blit()         #显示敌机

		enemy_plane.move()		   #敌机自动移动调用

		enemy_plane.fire()		   #敌机发射子弹

		pygame.display.update()    #贴完以后不会显示，必须调用update函数更新后才会显示新图

		monitor_keyboard(user_plane)		#监测键盘

		time.sleep(0.01)

main()