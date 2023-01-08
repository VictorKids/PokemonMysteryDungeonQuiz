################################################################################################################################################################################
# Imports
################################################################################################################################################################################

from tkinter import *
from PIL import ImageTk,Image
import random
from tkinter.font import Font

################################################################################################################################################################################
# General Functions
################################################################################################################################################################################

# returns a random background for the title screen
def random_background():
    return "imgs/background" + str(random.randint(1,4)) + ".png"

# switch to the next frames/canvas of the game
def next_canvas():
    global frames, running_frame_index
    frames[running_frame_index].forget()
    if running_frame_index < len(frames) - 1:
        running_frame_index += 1
    else: # this should not happen for now
        running_frame_index = 0
    frames[running_frame_index].pack(fill="both", expand=True)
    canvas_list[running_frame_index].pack(fill="both", expand=True)

# sets the variables that stores the current text to be displayed
def get_quiz(fi):
    global question, answer1, answer2, answer3, answer4
    line = fi.readline()
    split_line = line.split("#")
    question.set(split_line[0])
    answer1.set(split_line[1])
    answer2.set(split_line[2])
    answer3.set(split_line[3])
    answer4.set(split_line[4])
    a1_val.set(split_line[5])
    a2_val.set(split_line[6])
    a3_val.set(split_line[7])
    a4_val.set(split_line[8])

# apply answer modifier to the player results list, delete objects in quiz screen and recreate it with the new texts (could be much better)
def quiz_loop(fi, f_len): 
    global file_len 
    if f_len < file_len: # check if there still more questions to be done
        f_len += 1
        global question_window, options_btn1_window, options_btn2_window, options_btn3_window, options_btn4_window, answer, Natures, goto_result_btn_window
        if answer.get() == 1:
            modifiers = a1_val.get().split(",")
            for i in range(6):
                Natures[i] += int(modifiers[i])
        elif answer.get() == 2:
            modifiers = a2_val.get().split(",")
            for i in range(6):
                Natures[i] += int(modifiers[i])
        elif answer.get() == 3:
            modifiers = a3_val.get().split(",")
            for i in range(6):
                Natures[i] += int(modifiers[i])
        elif answer.get() == 4:
            modifiers = a4_val.get().split(",")
            for i in range(6):
                Natures[i] += int(modifiers[i])
        else: # in case the player does not select any option
            return
        s2_canvas.delete(question_window)
        s2_canvas.delete(options_btn1_window)
        s2_canvas.delete(options_btn2_window)
        s2_canvas.delete(options_btn3_window)
        s2_canvas.delete(options_btn4_window)
        s2_canvas.delete(goto_result_btn_window)
        get_quiz(fi)
        # questions
        question_window = s2_canvas.create_text(640, 70, text=question.get(), font=questions_font)
        # option1
        options_btn1 = Radiobutton(s2_canvas, text=answer1.get(), variable=answer, value=1, font=answers_font, bg="#EE5061", activebackground="#EE5061")
        options_btn1_window = s2_canvas.create_window(60, 240, window=options_btn1, anchor=NW)
        # option2
        options_btn2 = Radiobutton(s2_canvas, text=answer2.get(), variable=answer, value=2, font=answers_font, bg="#EE5061", activebackground="#EE5061")
        options_btn2_window = s2_canvas.create_window(720, 240, window=options_btn2, anchor=NW)
        # option3
        options_btn3 = Radiobutton(s2_canvas, text=answer3.get(), variable=answer, value=3, font=answers_font, bg="#EE5061", activebackground="#EE5061")
        options_btn3_window = s2_canvas.create_window(60, 480, window=options_btn3, anchor=NW)
        # option4
        options_btn4 = Radiobutton(s2_canvas, text=answer4.get(), variable=answer, value=4, font=answers_font, bg="#EE5061", activebackground="#EE5061")
        options_btn4_window = s2_canvas.create_window(720, 480, window=options_btn4, anchor=NW)
        # next question btn
        goto_result_btn = Button(s2_canvas, text=s2_btn_txt.get(), padx=2, pady=1, borderwidth=5, font=("Verdana",20), command=lambda:quiz_loop(fi, f_len))
        goto_result_btn_window = s2_canvas.create_window(640, 630, window=goto_result_btn)
    
        answer.set(0)
    else:
        next_canvas()

# close the root (not sure if it is the best way to do it)
def quit_game():
    global quiz_file
    quiz_file.close()
    root.quit()

# uses player answers to create a string that works as a index in the dex dictionary
def calc_char():
    global Natures, top_finalmsg, final_btn_window, dex, _pkm
    s3_canvas.delete(pokemon)
    s3_canvas.delete(top_finalmsg)
    s3_canvas.delete(final_btn_window)
    img_name = ""
    for value in Natures:
        if value < 0:
            img_name = img_name + "0"
        elif value > 0:
            img_name = img_name + "1"
        else:
            img_name = img_name + str(random.randint(0,1))
    poke_name = s3_canvas.create_text(640, 470, text=dex[img_name], font=questions_font)
    o_pkm = Image.open("imgs/"+ dex[img_name] + ".png")
    r_pkm = o_pkm.resize((80,80), Image.LANCZOS)
    _pkm = ImageTk.PhotoImage(r_pkm)
    s3_canvas.create_image(645, 350, image=_pkm)
    quit_btn = Button(s3_canvas, text="Sair", padx=2, pady=1, borderwidth=4, bg="white", font=("Verdana",20), command=quit_game)
    quit_btn_window = s3_canvas.create_window(640, 650, window=quit_btn)

################################################################################################################################################################################
# Tkinter Initial Definitions
################################################################################################################################################################################

# screens basic
root = Tk()
root.title("Pokémon Mystery Dungeon Character Selection v1.0")
root.iconbitmap("favicon.ico")
root.geometry("1280x720")
root.resizable(0,0)
# each game section main frame
s1_frame  = Frame(root, width=1280, height=720)
s2_frame  = Frame(root, width=1280, height=720)
s3_frame  = Frame(root, width=1280, height=720)
s1_canvas = Canvas(s1_frame, width=1280, height=720)
s2_canvas = Canvas(s2_frame, width=1280, height=720)
s3_canvas = Canvas(s3_frame, width=1280, height=720)
frames = [s1_frame, s2_frame, s3_frame]
canvas_list = [s1_canvas, s2_canvas, s3_canvas]
running_frame_index = 0
Natures = [0,0,0,0,0,0] # Bom/Good, Corajoso/Brave, Inteligente/Smart, Social/Social, Cuidadoso/Careful, Carismatico/Charismatic
dex = { # All 64 possible results
    "000000": "Feebas",  "000001": "Goomy",    "000010": "Ditto",   "000011": "Stufful",  "000100": "Grookey", "000101": "Cubchoo",   "000110": "Chespin",  "000111": "Skitty",
    "001000": "Tinkatin","001001": "Torchic",  "001010": "Pumpkaboo","001011": "Fennikin","001100": "Sinistea","001101": "Gothita",   "001110": "Klink",    "001111": "Meowth",
    "010000": "Grimer",  "010001": "Chimchar", "010010": "Turtwig",  "010011": "Cubone",  "010100": "Mankey",  "010101": "Totodile",  "010110": "Timburr",  "010111": "Oshawott",
    "011000": "Bagon",   "011001": "Litten",   "011010": "Snivy",    "011011": "Zorua",   "011100": "Beldum",  "011101": "Scorbunny", "011110": "Porygon",  "011111": "Sprigatito",
    "100000": "Lechonk", "100001": "Togepi",   "100010": "Snom",     "100011": "Rowlet",  "100100": "Mareep",  "100101": "Wooloo",    "100110": "Chikorita","100111": "Bidoof",
    "101000": "Ralts",   "101001": "Cyndaquil","101010": "Yamask",   "101011": "Sooble",  "101100": "Piplup",  "101101": "Eevee",     "101110": "Flabebe",  "101111": "Clefairy",
    "110000": "Munchlax","110001": "Fuecoco",  "110010": "Larvitar", "110011": "Quaxly",  "110100": "Slakoth", "110101": "Charmander","110110": "Popplio",  "110111": "Tepig",
    "111000": "Treecko", "111001": "Mudkip",   "111010": "Riolu",    "111011": "Froakie", "111100": "Rockruff","111101": "Squirtle",  "111110": "Bulbasaur","111111": "Pikachu"    
}

################################################################################################################################################################################
# Title Section
################################################################################################################################################################################

# just a bunch of visual stuffs
background_img = PhotoImage(file=random_background()) 
s1_canvas.create_image(0, 0, image=background_img, anchor="nw")
# these 2 pokemon fonts must be downloaded aside (i think..)
title_font_e = Font(family="Pokemon Hollow", size=65, weight="bold")
title_font_i = Font(family="Pokemon Solid", size=65, weight="bold")
subtitle_font = Font(family="Magneto", size=50, weight="bold")
m_t_i1 = s1_canvas.create_text(240, 195, text="Pokémon", font=title_font_i, fill='yellow')
m_t_e1 = s1_canvas.create_text(240, 195, text="Pokémon", font=title_font_e, fill='blue')
m_t_i2 = s1_canvas.create_text(640, 150, text="Mystery", font=title_font_i, fill='yellow')
m_t_e2 = s1_canvas.create_text(640, 150, text="Mystery", font=title_font_e, fill='blue')
m_t_i3 = s1_canvas.create_text(1025, 200, text="Dungeon", font=title_font_i, fill='yellow')
m_t_e3 = s1_canvas.create_text(1025, 200, text="Dungeon", font=title_font_e, fill='blue')
s1_canvas.itemconfig(m_t_i1, angle=10)
s1_canvas.itemconfig(m_t_e1, angle=10)
s1_canvas.itemconfig(m_t_i3, angle=-10)
s1_canvas.itemconfig(m_t_e3, angle=-10)
s1_canvas.create_text(640, 320, text="- Char Selection -", font=subtitle_font)
s1_canvas.create_text(1180, 705, text="v1.0 - 05/01/23 - Victor Vieira", font=("Helvetica",10))
start_btn = Button(s1_canvas, text="INICIAR", padx=2, pady=1, borderwidth=5, font=("Verdana",20), command=next_canvas)
start_btn_window = s1_canvas.create_window(640, 500, window=start_btn)

################################################################################################################################################################################
# Questions Section
################################################################################################################################################################################

# background
background_img2 = PhotoImage(file="imgs/quizbg3.png")
s2_canvas.create_image(0,0,image=background_img2, anchor="nw")
# fonts
questions_font = Font(family="Arial", size=25, weight="bold")
answers_font = Font(family="Arial", size=15, weight="bold")
# file and variables
quiz_file = open("quiz.txt", "r", encoding="utf-8")
file_len  = int(quiz_file.readline())
question  = StringVar()
answer1   = StringVar()
answer2   = StringVar()
answer3   = StringVar()
answer4   = StringVar()
a1_val    = StringVar()
a2_val    = StringVar()
a3_val    = StringVar()
a4_val    = StringVar()
# answer check
answer = IntVar()
# next question button text
s2_btn_txt = StringVar()
s2_btn_txt.set("Seguir")
# initial question values (could be better done)
get_quiz(quiz_file)
question_window = s2_canvas.create_text(640, 70, text=question.get(), font=questions_font)
options_btn1 = Radiobutton(s2_canvas, text=answer1.get(), variable=answer, value=1, font=answers_font, bg="#EE5061", activebackground="#EE5061")
options_btn1_window = s2_canvas.create_window(60, 240, window=options_btn1, anchor=NW)
options_btn2 = Radiobutton(s2_canvas, text=answer2.get(), variable=answer, value=2, font=answers_font, bg="#EE5061", activebackground="#EE5061")
options_btn2_window = s2_canvas.create_window(720, 240, window=options_btn2, anchor=NW)
options_btn3 = Radiobutton(s2_canvas, text=answer3.get(), variable=answer, value=3, font=answers_font, bg="#EE5061", activebackground="#EE5061")
options_btn3_window = s2_canvas.create_window(60, 480, window=options_btn3, anchor=NW)
options_btn4 = Radiobutton(s2_canvas, text=answer4.get(), variable=answer, value=4, font=answers_font, bg="#EE5061", activebackground="#EE5061")
options_btn4_window = s2_canvas.create_window(720, 480, window=options_btn4, anchor=NW)
goto_result_btn = Button(s2_canvas, text=s2_btn_txt.get(), padx=2, pady=1, borderwidth=5, font=("Verdana",20), command=lambda:quiz_loop(quiz_file, 1))
goto_result_btn_window = s2_canvas.create_window(640, 630, window=goto_result_btn)

################################################################################################################################################################################
# Result Section
################################################################################################################################################################################

# just visual stuffs
background_img3 = PhotoImage(file="imgs/finalbg.png")
s3_canvas.create_image(0,0,image=background_img3, anchor="nw")
pkm = PhotoImage(file="imgs/missingno.png")
pokemon = s3_canvas.create_image(645, 350, image=pkm)
top_finalmsg = s3_canvas.create_text(640, 220, text="Hmm... Você parece ser...", font=questions_font)
final_btn = Button(s3_canvas, text="Revelar", padx=2, pady=1, borderwidth=4, bg="white", font=("Verdana",20), command=calc_char)
final_btn_window = s3_canvas.create_window(640, 500, window=final_btn)


################################################################################################################################################################################
# Main Loop
################################################################################################################################################################################

frames[running_frame_index].pack(fill="both", expand=True)
canvas_list[running_frame_index].pack(fill="both", expand=True)
root.mainloop()
