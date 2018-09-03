import pygame
import time
import random
from threading import Thread
from Utilities import SpeechRecognizer
from InputManager import ButtonInputManager as BIM, BreathInputManager as BrIM
pygame.init()

class Word:
    def __init__(self, act, varis, img):
        self.actual = act
        self.variations = varis
        self.image = img
        self.width = img.get_size()[0]
        self.label = pygame.font.SysFont("Comic Sans MS", 100).render("Say \"" + act[0].upper() + act[1:len(act)] + "\"!", 1, (255, 0, 255))
        self.label_location = (int(960 - (self.label.get_size()[0]/2)), 160)

lines = open("Words", "r").read().split("\n")
words = []
for l in range(len(lines)-1):
    line = lines[l]
    if not (line[0] == "#"):
        data = line.split(",")
        for d in range(0, len(data)):
            data[d] = data[d].lower()
        actual = data[0]
        variations = data
        image = None
        try:
            name = "./Data/" + actual[0].upper() + actual[1: len(actual)] + "/" + actual.lower() + ".jpg"
            image = pygame.image.load(name)
        except pygame.error:
            name = "./Data/" + actual[0].upper() + actual[1: len(actual)] + "/" + actual.lower() + ".png"
            image = pygame.image.load(name)
        p = image.get_size()
        k = 540 / p[1]
        image = pygame.transform.smoothscale(image, (int(k * p[0]), int(k * p[1])))
        if image is None:
            raise Exception("Couldn't load the image IDK y")
        words.append(Word(actual, variations, image))

class Card:
    def __init__(self, image, name, copy=True):
        self.name = name
        self.image = pygame.transform.smoothscale(image, (200, 200))
        self.face_up = False
        if copy:
            #print(name)
            self.copy = Card(image, name, False)
    def __str__(self):
        return str(self.name)
    def getImage(self):
        if self.face_up:
            return self.image
        else:
            return Card.face_down_image
Card.face_down_image = pygame.transform.smoothscale(pygame.image.load("CardBack.jpg"), (200, 200))

cards = []
lines = open("Cards/Cards", "r").read().split("\n")
print("Finished game 1 resources")
for l in range(len(lines)-2):
    name = lines[l]
    image = pygame.image.load("./Cards/" + name + ".jpg")
    cards.append(Card(image, name, True))

print("Finished Loading Resources!")
time.sleep(0.3)
###############################################################################

dimensions = (1920, 1080)

display = pygame.display.set_mode(dimensions)
pygame.display.set_caption("T21")

pygame.display.update()

a = time.time()


class Listener(Thread):
    def __init__(self):
        super().__init__()
        self.result = False
        self.recognizer = SpeechRecognizer()
        self.start()

    def run(self):
        self.detected_word = self.recognizer.get_word()
        self.result = True


previous_word = None
current_word = random.choice(words)
current_recognizer = Listener()

correct_label = pygame.font.SysFont("Comic Sans MS", 100).render("Nice work!", 1, (255, 255, 255))
wrong_label   = pygame.font.SysFont("Comic Sans MS", 100).render("Try again!", 1, (255, 255, 255))

correct_counter = 0
bim = BIM()
def card_game():
    bim.clear()
    CARD_QUIT = False
    cards_copy = []
    for card in cards:
        cards_copy.append(card)
    set_of_current_cards = []
    for a in range(8):
        choice = random.randint(0, len(cards_copy)-1)
        set_of_current_cards.append(cards_copy.pop(choice))
        set_of_current_cards.append(set_of_current_cards[-1].copy)
        set_of_current_cards[-1].face_up = False
        set_of_current_cards[-2].face_up = False
        
    random.shuffle(set_of_current_cards)
    list_of_current_cards = set_of_current_cards
    current_face_up = None
    number_of_correct = 0
    move_count = 0
    while not (number_of_correct == 16):
        display.fill((200,200,0))
        for i in range(4):
            for j in range(4):
                display.blit(list_of_current_cards[(4*j)+i].getImage(), ((i*220) + 460, (j*220) + 20))
        display.blit(pygame.font.SysFont("Comic Sans MS", 100).render("Moves: " + str(move_count), 1, (255, 255, 255)), (1350, 200))
        pygame.display.update()
        if(len(bim.queue) > 0):
            chosen_card = bim.queue[0]
            bim.clear()
            if not list_of_current_cards[chosen_card-1].face_up:
                list_of_current_cards[chosen_card-1].face_up = True
                if current_face_up is None:
                    current_face_up = list_of_current_cards[chosen_card-1]
                else:
                    move_count += 1
                    card_time = time.time()
                    display.fill((200,200,0))
                    while(time.time() - card_time < 1):
                        for i in range(4):
                            for j in range(4):
                                display.blit(list_of_current_cards[(4*j)+i].getImage(), ((i*220) + 460, (j*220) + 20))
                        display.blit(pygame.font.SysFont("Comic Sans MS", 100).render("Moves: " + str(move_count), 1, (255, 255, 255)), (1350, 200))
                        pygame.display.update()
                    if current_face_up.name == list_of_current_cards[chosen_card-1].name:
                        card_time = time.time()
                        display.fill((0,255,0))
                        while(time.time() - card_time < 1):
                            for i in range(4):
                                for j in range(4):
                                    display.blit(list_of_current_cards[(4*j)+i].getImage(), ((i*220) + 460, (j*220) + 20))
                            display.blit(pygame.font.SysFont("Comic Sans MS", 100).render("Moves: " + str(move_count), 1, (255, 255, 255)), (1350, 200))
                            pygame.display.update()
                        current_face_up = None
                        number_of_correct += 2
                    else:
                        card_time = time.time()
                        display.fill((255,0,0))
                        while(time.time() - card_time < 1):
                            for i in range(4):
                                for j in range(4):
                                    display.blit(list_of_current_cards[(4*j)+i].getImage(), ((i*220) + 460, (j*220) + 20))
                            display.blit(pygame.font.SysFont("Comic Sans MS", 100).render("Moves: " + str(move_count), 1, (255, 255, 255)), (1350, 200))
                            pygame.display.update()
                        current_face_up.face_up = False
                        current_face_up = None
                        list_of_current_cards[chosen_card-1].face_up = False
            bim.clear()
    #blow_game(move_count)

brim = BrIM()

def blow_game(moves):
    blows = 0
    if moves < 10:
        blows = 1
    elif moves < 15:
        blows = 2
    elif moves < 20:
        blows = 3
    elif moves < 25:
        blows = 4
    elif moves < 30:
        blows = 5
    elif moves < 35:
        blows = 6
    elif moves < 40:
        blows = 7
    elif blows < 45:
        blows = 8
    else:
        blows = 9
    # 1880/n is width of each panel
    width_of_panel = 1880/blows
    blown = 0
    brim.clear()
    while len(brim.queue) <= blows:
        display.fill((0, 0, 0))
        for xyz in range(blows):
            color = (200, 200, 50) if xyz < len(brim.queue) else (10,10,10)
            pygame.draw.rect(display, color, (20 + (xyz*width_of_panel), 20, width, 1040))
        pygame.display.update()


QUIT = False
while not QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT = True

    display.fill((50, 200, 50))
    if current_recognizer.result:
        print(current_recognizer.detected_word)
        a = time.time()
        boolean = False
        detected_words = current_recognizer.detected_word.split()
        for detected_word in detected_words:
            if detected_word in current_word.variations:
                boolean = True
                break
        if boolean:
            print("correct")
            while time.time() - a < 1.5:
                display.fill((0, 255, 0))
                display.blit(correct_label, (650, 400))
                pygame.display.update()
            current_word = random.choice(words)
            correct_counter += 1
            if correct_counter == 5:
                card_game()
                correct_counter = 0
        else:
            print("try again")
            while time.time() - a < 1.5:
                display.fill((255, 0, 0))
                display.blit(wrong_label, (650, 400))
                pygame.display.update()
        current_recognizer = Listener()
    elif current_recognizer.recognizer.is_fetching:
        display.fill((0, 128, 0))

    display.blit(current_word.label, current_word.label_location)
    display.blit(current_word.image, (960 - (current_word.width/2), 360))

    pygame.display.update()

pygame.quit()
quit()
