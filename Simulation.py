import pygame, time, random

HEIGHT = 700
WIDTH = 500

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Lift:

	def __init__(self, sec, start):
		self.__max = 5
		self.__fill = 0
		self.__sec = sec
		self.__x_pos = 225
		self.__y_pos = sec*(start-1)
		self.__width = 50
		self.__height = sec
		self.__dest = start*sec

	def room(self):
		if self.__fill < self.__max:
			return True
		return False

	def off(self):
		self.__fill -= 1

	def on(self):
		self.__fill += 1

	def get_rect(self):
		return (self.__x_pos, self.__y_pos, self.__width, self.__height)

	def goto(self, floor):
		self.__dest = floor*self.__sec

	def move(self):
		if self.__y_pos < self.__dest:
			self.__y_pos += 3
			if self.__y_pos > self.__dest:
				self.__y_pos = self.__dest
		elif self.__y_pos > self.__dest:
			self.__y_pos -= 3
			if self.__y_pos < self.__dest:
				self.__y_pos = self.__dest

	def is_open(self):
		if self.__dest == self.__y_pos:
			return True
		return False

	def floor(self):
		return self.__dest/self.__sec


class Person:

	def __init__(self, floors):
		self.__done = False
		self.__location = random.randint(1, floors)
		self.__dest = self.__location
		while self.__dest == self.__location:
			self.__dest = random.randint(1, floors)
		self.__in_lift = False
		if self.__location < self.__dest:
			self.__up = False

	def get_done(self):
		return self.__done

	def get_pos(self):
		return self.__location

	def is_on(self):
		return self.__in_lift

	def get_on(self):
		self.__in_lift = True

	def get_off(self):
		self.__in_lift = False
		self.__done = True
		self.__location = self.__dest

	def get_start(self):
		return self.__location

	def get_dest(self):
		return self.__dest


class Main:

	def __init__(self, floors):
		self.__floors = floors
		self.__sec = HEIGHT/(self.__floors+2)
		self.__lift = Lift(self.__sec, self.__floors)
		pygame.init()
		self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.__running = True
		self.__users = []
		self.__delivered = []

	def is_still(self):
		return self.__lift.is_open()

	def get_users(self):
		return self.__users

	def new_cust(self, cust):
		self.__users.append(cust)

	def l_goto(self, floor):
		self.__lift.goto(floor)

	def get_sec(self):
		return self.__sec

	def pos(self):
		return self.__lift.get_rect()[1]

	def run(self):
		if self.__running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.__runnning = False

			self.__screen.fill(BLACK)
			lift_pos = self.__lift.get_rect()
			pygame.draw.rect(self.__screen, YELLOW, pygame.Rect(lift_pos))

			for floor in range(self.__floors):
				pygame.draw.rect(self.__screen, PURPLE, pygame.Rect(100, (floor*self.__sec)+self.__sec, 100, 5))

			self.__lift.move()
			if self.__lift.is_open():
				for people in self.__users:
						if self.__lift.floor() == people.get_dest():
							people.get_off()
							self.__lift.off()
							self.__users.remove(people)
							self.__delivered.append(people)

				for people in self.__users:
					if self.__lift.floor() == people.get_start() and self.__lift.room():
						people.get_on()
						self.__lift.on()
			for people in self.__users:
				if people.is_on():
					pygame.draw.rect(self.__screen, RED, pygame.Rect(lift_pos[0], lift_pos[1], 25, self.__sec/2))
				else:
					pygame.draw.rect(self.__screen, RED, pygame.Rect(140, (people.get_pos()*self.__sec)+(self.__sec/2), 25, self.__sec/2))
			for people in self.__delivered:
				pygame.draw.rect(self.__screen, GREEN, pygame.Rect(100, (people.get_pos()*self.__sec)+(self.__sec/2), 25, self.__sec/2))


			pygame.display.flip()