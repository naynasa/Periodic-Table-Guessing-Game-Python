"""TAKEAWAYS:
*use lambda to not call the function no initialization
*create_button in order to not have to repeat a ton of code
*use ["feature"] or .config to update tkinter widgets
*Menus in tkinter are confusing
*Classes, self, (inheritance)
"""
from tkinter import *
import random
from tkinter import messagebox
#inheritence from Frame class in tkinter
class Gui(Frame):
    def __init__(self, master = None):
        #inherit from Frame to be able to use all tkinter functions
        #like importing variables, or functions but with a class (everything is included without code)
        
        #master = None means this is the main window
        #init is called on initialisation and creates the "global" variales need as well as the buttons and the data (answer_list)
        Frame.__init__(self, master)
        self.master = master

        # Change the title of the window and pack
        self.master.title("Periodiska Systemet")
        self.pack(fill=BOTH, expand=1)

        # Define variables, button_list, answer_list
        #answer_list are all the buttons and corresponding elements not yet answered
        self.button_list = []
        self.answer_list = []
        self.correctly_guessed = []

        # Create a list of positions in the first 3 rows and iterate over it
        row_list = [[0, 17], [0, 1, 12, 13, 14, 15, 16, 17], [0, 1, 12, 13, 14, 15, 16, 17]]
        counter = 0
        for list in row_list:
            for item in list:
                self.create_button(80 * item, 10+ 70 * counter)
            counter += 1

        # Create rest of normal elements
        for row in range(3, 7):
            for col in range(0, 18):
                self.create_button(80 * col, 10+ 70 * row)

        # Lantanides and Actinides
        for row in range(8, 10):
            for col in range(3, 17):
                self.create_button(80 * col, 10 +70 * row)
        #Support label to show where lantanides and actinides start
        arrow = Label(self, text="", relief="flat", height=22, width=1, bg="Black",bd=1)
        arrow.place(x=2.75*80, y=5*70+10)

        # Import and clean the data in list format
        self.data_list = self.import_data()
        self.data_list.sort(key=lambda x: x[1])

        #index data_list = atomic number +1
        #swap the elements that are not in order (the table is not ordered by weight but by atomic number)
        self.data_list[51], self.data_list[52] = self.data_list[52], self.data_list[51]
        self.data_list[83], self.data_list[84] = self.data_list[84], self.data_list[83]
        self.data_list[89], self.data_list[90] = self.data_list[90], self.data_list[89]
        self.data_list[91], self.data_list[92] = self.data_list[92], self.data_list[91]


        #Create the menu
        self.create_menu()
        self.create_game()
    def create_menu(self):
        #Menu
        main_menu = Menu(self.master)
        self.master.config(menu=main_menu)
        #-Game
        game = Menu(main_menu)
        main_menu.add_cascade(label="Game", menu=game)  # adds the Game symbol to the top left

        #-Game-New
        new_menu = Menu(game)
        game.add_cascade(label="New", menu=new_menu)
        new_menu.add_command(label="New Element", command=lambda : self.play())

        game.add_command(label="Show answers", command=lambda : self.show_answers())
        game.add_command(label="Exit", command=lambda: exit())
    def create_button(self, x, y): #function for creating a button, plotting it at the x,y coordinates and saving it to button_list
        button = Checkbutton(self,text="",relief="flat", height=5, width=5, command=lambda: self.element_guess(button),indicatoron=0, bd=1)
        button.place(x=x, y=y)
        self.button_list.append(button)
    def import_data(self): #imports data from peridiska_data.txt and returns it as data_list
        data_list = []
        f = open("periodiska_data.txt", "r")
        for n in f:
            n = n.split(" ")
            if len(n) == 3:
                n.remove(n[1])
            n = [i.split('\n')[0] for i in n] #removes all /n characters

            data_list.append(n)
        f.close()
        #make all the numbers integers
        for n in range(0, len(data_list)):
            num = int(float(data_list[n][1]))
            data_list[n][1] = int(num)
        return data_list
    def show_answers(self): #shows all elements on the corresponding buttons as well as the correct answer in purple
        for i in range(0,len(self.answer_list)):
            self.answer_list[i][0].config(text=self.answer_list[i][1][0])
        self.answer_list[self.random_number][0].config(bg="purple2")
    def clear_answers(self,complete):
        #if complete is true set all buttons to white and remove text
        #else set all but the correctly guessed buttons to
        if complete == True:
            for button in self.button_list:
                button.config(text="")
                button.config(highlightbackground="White", bg="White")
                button.deselect()
        else:
            for lst in self.answer_list:
                if lst[0]["background"] != "green" or "yellow":
                    lst[0].config(text="")
                    lst[0].config(highlightbackground="White", bg="White")
                    lst[0].deselect()
    def create_answer_list(self):
        # Create a list of what button corresponds with what elements and what weight

        # first 56 elements
        for i in range(0, 57):
            adder_list = self.button_list[i], self.data_list[i]
            self.answer_list.append(adder_list)

        # Lantanides with correcsponding buttons
        counter = 57
        for z in range(90, 104):
            adder_list = self.button_list[z], self.data_list[counter]
            self.answer_list.append(adder_list)
            counter += 1

        # between Actinides and lantanides
        for z in range(57, 75):
            adder_list = self.button_list[z], self.data_list[counter]
            self.answer_list.append(adder_list)
            counter += 1
        # Actinides
        for z in range(104, 118):
            adder_list = self.button_list[z], self.data_list[counter]
            self.answer_list.append(adder_list)
            counter += 1

        # Last part of the table
        for z in range(75, 90):
            adder_list = self.button_list[z], ["",0]
            self.answer_list.append(adder_list)
            counter += 1
    def create_game(self):
        #function is called when a new game is created
        self.create_answer_list()
        self.clear_answers(True)
        self.attempts_total = 1
        self.attempts_current = 1
        self.play()
    def play(self):
        #function for choosing one element and then another when that one is correctly guessed
        #ending if all the elements that should be guessed are guessed
        if len(self.answer_list) == 0:
            msg_box = messagebox.askquestion("All elements correct! Total guesses {}".format(self.attempts_total), "Play again?")
            if msg_box == "yes":
                self.create_game()
            else:
                exit()

        self.clear_answers(False)

        #choose a correct answer
        self.random_number = random.randrange(0,len(self.answer_list)-16) #16 are for the last empty boxes (100-116)
        self.chosen_element = self.answer_list[self.random_number][1][0]
        #create the text label
        self.question_display = Label(self, font = ("Georgia", 18),text = "This is a periodic table training game please click on: {}. Guesses: {}   ".format(self.chosen_element, self.attempts_total))
        self.question_display.place(x=5*80,y=0)

    def element_guess(self, guess_button):
        #If guess is correct
        if self.answer_list[self.random_number][0] == guess_button:
            if self.attempts_current <= 1:
                guess_button.config(bg="green", text=self.chosen_element)
            elif self.attempts_current < 4:
                guess_button.config(bg="yellow", text=self.chosen_element)
            elif self.attempts_current >= 4:
                guess_button.config(bg="orange", text=self.chosen_element)
            guess_button.deselect()
            self.attempts_current = 1
            self.attempts_total += 1
            self.answer_list.remove(self.answer_list[self.random_number])
            self.play()

        else:
            self.attempts_total += 1
            self.question_display["text"] = "Wrong Guess, please click on: {}, current attempts: {}, total guesses {}      ".format(self.chosen_element,self.attempts_current,self.attempts_total)
            self.attempts_current += 1
            if guess_button["background"] != "green" or "yellow":
                guess_button.config(background="red")
                guess_button.config(highlightbackground="green")
        #print(guess_button["text"])

#define the list in which every button is stored and list of correct button element cominations
root = Tk()
app = Gui(root)
root.geometry("1900x1000")
root.mainloop()
