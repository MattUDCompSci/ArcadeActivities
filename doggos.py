'''
Animals have a name, energy level, hunger level, and mood
    eat
    sleep

Dogs have breeds
    play

Cats have coat color
    hunt
'''

class Dog:
    name: str
    energy: int
    hungry: bool
    mood: str

    def __init__ (self, the_name:str):
        self.name = the_name
        self.energy = 0
        self.hungry = False
        self.mood = "happy"

    def feed(self):
        self.hungry = False

    def play_with_my_dog(self):
        self.mood = "happy"
        self.hungry = True
        self.energy -= 1

    def rest(self, length_of_time):
        self.energy += length_of_time

ada = Dog("Ada")
babbage = Dog("Babbage")
ada.feed()