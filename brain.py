from Simulation import Main
from Simulation import Person
from tkinter import *
import pygame, time


class Brain:

	def __init__(self, floors):
		self.__score = 0
		self.__done = False
		self.__floors = floors
		self.__lift = Main(self.__floors)
		self.__clock = pygame.time.Clock()
		for x in range (int(round(self.__floors/3, 0))):
			self.__lift.new_cust(Person(self.__floors))
		self.run()

	def move(self):
		people = self.__lift.get_users()
		on = []
		waiting = []
		for person in people:
			if person.is_on():
				on.append(person.get_dest())
			else:
				waiting.append(person.get_start())
		nearest = self.__floors-1
		dist = 9999
		lift_pos = self.__lift.pos()/self.__lift.get_sec()
		for person in on:
			temp = person-lift_pos
			if temp < 0:
				temp -= 2*temp
			if temp < dist:
				nearest = person
				dist = temp
		for person in waiting:
			temp = person-lift_pos
			if temp < 0:
				temp -= 2*temp
			if temp <= round((dist/2), 0):
				nearest = person
				dist = temp
		if dist == 9999:
			self.__done = True
		else:
			self.__score += dist
		return nearest

	def run(self):
		while True:
			self.__clock.tick(60)
			self.__lift.run()
			if self.__lift.is_still():
				self.__lift.l_goto(self.move())
			if self.__done:
				break
		time.sleep(3)
		Score(self.__score)

class Score:

	def __init__(self, score):
		self.__root = Tk()
		self.__label = Label(self.__root, text="The score of the lift algorithm is\n %d" % (score)).pack()
		self.__button = Button(self.__root, text="END", command=self.end).pack()

		self.__root.mainloop()

	def end(self):
		raise SystemExit


class Menu():

	def __init__(self):
		self.__root = Tk()
		self.__label = Label(self.__root, text="Lift Simulation.\n\n select number of floors").pack()
		self.__var = DoubleVar()
		self.__ = Scale(self.__root, variable=self.__var, from_=0, to=20).pack()
		self.__button = Button(self.__root, text="start", command=self.start).pack()

		self.__root.mainloop()

	def start(self):
		floors = int(self.__var.get())
		self.__root.destroy()
		Brain(floors)

Menu()
