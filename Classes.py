from random import shuffle
import time
from pygame import mixer
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
#import mfrc522.SimpleMFRC522 as SimpleMFRC522
#import RPi.GPIO as GPIO  
# from gpiozero import 


button_pins = [2,21,20,16,26]
but_pin = 2
led_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(but_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin,GPIO.OUT)
curs = [0,0,0,0,0]
prevs = [0,0,0,0,0]
class Question():
    
    def __init__ (self, q_id: str, num_ans:int):
        self._main_path_ = "/media/pi/3362-3231/"
        self._generic_succsses = self._main_path_ + "succsess_sound.wav"
        self._generic_fail = self._main_path_ + "fail_sound.wav"
        self._question_path_ = self._main_path_ + "/" + q_id
        self._correct_ans_ = self._question_path_ + "/" + "correct_answer.wav"
        list1 = []
        for i in range(num_ans - 1):
            list1.append(self._quesion_path_+ "/" + "incorrect_answer" + str((i+1))+ ".wav")   
        self._incorrect_answers_ = list1
        self._all_answers = list1.append(self._correct_ans_)
        self._question_data =  self._question_path_ + "/" + "question_data.wav" 
        self._correct_ans_index = self._all_answers.index(self._correct_ans_)
        # self._explained_ans = 

    # def shuffle(self):
    #     self._all_answers = shuffle(self._all_answers)
    #     self._correct_ans_index = self._all_answers.index(self._correct_ans_)

    def get_all_answers(self):
        return self._all_answers

    def get_correct_index(self):
        return self._correct_ans_index

# when we add diff -> class card
# user? 
# take card after 20 second 
class Game():
    def __init__ (self):
        self.mixer = mixer.init()
        self.reader = SimpleMFRC522()
        self.cur_question
    
    def _start_game (self):
        while (not self.cur_question):
            id = self.get_uuid()
    
        self.cur_question = Question(id,4) # TODO change to fixed nAns
        self.play()
        # try
        # find folder if T -> ok else -> err
        # restart all lights 
    
    def get_uuid(self):
        id = None
        while id == None:
            id = self.reader.read()[0]
       
        return id
        
    def play(self):
        self.mixer.Sound(self.cur_question.question_data).play()
        timer.sleep(.5)
        self.play_answers()
        while self.play_success_or_fail() == -1:
            pass


    def button_pressed(self):
        for i in range(4):
            curs[i] = GPIO.input(button_pins[i])
            if (curs[i] == 1) and (prevs[i] == 0):
                return i
            
            prevs[i] = curs[i]
        return -1
        # button_pressed = (input from button)

    def play_answers(self):
        ans = self.cur_question.get_all_answers()
        for i in range(len(ans)):
            self.mixer.Sound(ans[i]).play()
        
        #   light on 
        #   play(ans)
        #   light off

    def play_success_or_fail(self):
        bIndex = self.button_pressed()
        if bIndex == -1:
            return -1
        if self.cur_question.get_correct_index() == bIndex:
            self.mixer.Sound(self.cur_question._generic_succsses).play()
            self.cur_question = None
            return 1
        else:
            self.mixer.Sound(self.cur_question._generic_fail).play()
            return 0


