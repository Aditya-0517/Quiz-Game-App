from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import sqlite3
import threading

game_score = 0
questions_attempted = 1
player_name = ""
qualifying_score = 2

#*********************** TIMER **************************#

time_in_sec = 20

def timer():
    global time_in_sec, mylabel, button, myoptionlabel
    if(time_in_sec>0):
        minutes, seconds = divmod(time_in_sec, 60)
        time_left = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        timer_label.config(text=time_left)
        time_in_sec -= 1
        timer_label.after(1000, timer)
    else:
        mylabel.destroy()
        button.destroy()
        myoptionlabel.destroy()
        completed_session()


#*********************** TIMER **************************#

#************** DATABASE DATABASE DATABASE **************#

conn = sqlite3.connect('Database.db')

c = conn.cursor()

#c.execute('''CREATE TABLE QuizData(
#             name text,
#             score number)''')



def get_player_name(player_name):
    c.execute("SELECT * FROM QuizData WHERE name=:name", {'name':player_name})
    return c.fetchone()

def insert_player(player_name, game_score):
    with conn:
        c.execute("INSERT INTO quizData VALUES (:name, :score)", {'name': player_name, 'score': game_score})

def update_score(player_name, game_score):
    with conn:
        c.execute("""UPDATE QuizData SET score = :score
                    WHERE name = :name""",
                  {'name': player_name, 'score': game_score})

#************** DATABASE DATABASE DATABASE **************#

def show_frame(frame):
    frame.tkraise()
    
def submit_form():
    global player_name
    player_name = input_name.get().split()[0]
    player_name = player_name.lower()
    frame3.tkraise()
    timer()
    load_questions()

def load_questions():
    global questions_attempted, game_score, mylabel, button, myoptionlabel
    button = Button(frame3, image=next_btn, cursor = "hand2", borderwidth=0, bg="black", command=lambda: var.set(1))
    button.place(x=750, y= 475)
    for question in questions:
        mylabel = Label(frame3, text=question, anchor=CENTER, font =("times new roman", 18, "bold"), bg= "black", fg= "white", wraplength= 800)
        mylabel.place(x= 250 , y= 160)
        for value,key in solutions.items():
            if question == value:
                for answer in answers:
                    if key in answer:
                        random.shuffle(answer)
                        option1 = answer[0]
                        option2 = answer[1]
                        option3 = answer[2]
                        option4 = answer[3]
                        myoptionlabel = Label(frame3, bg="black")
                        myoptionlabel.place(x= 545,y= 270)
                        Radiobutton(myoptionlabel, text=option1, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option1, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option2, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option2, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option3, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option3, selectcolor="#000000").pack(pady=5, anchor="w")
                        Radiobutton(myoptionlabel, text=option4, font =("times new roman", 18, "bold"), bg="black", fg="white", variable=var2, value=option4, selectcolor="#000000").pack(pady=5, anchor="w")
                        button.wait_variable(var)
                        selected_option = var2.get()
                        if selected_option == key:
                            game_score += 1
                        questions_attempted += 1
                        if questions_attempted == 4:
                            button.destroy()
                            button = Button(frame3, image=finish_btn, cursor = "hand2", borderwidth=0, bg="black", command=lambda: var.set(1))
                            button.place(x=750, y= 475)
                        mylabel.destroy()
                        myoptionlabel.destroy()
    button.destroy()
    completed_session()

def completed_session():
    data_handling()
    messagebox.showinfo("    Quiz Game", "Quiz Has Finished\n{} you have scored {} out of 4".format(player_name, game_score))
    global qualify_bg, qualify_ok_btn, qualify_mssg, qualify_fail_mssg
    if(game_score >= qualifying_score):
        top = Toplevel()
        top.geometry("800x450")
        qualify_bg_label = Label(top, image=qualify_bg)
        qualify_bg_label.pack()
        qualify_mssg_label = Label(top, image=qualify_mssg, bg="#4e62d2")
        qualify_mssg_label.place(x=155, y=40)
        qualify_ok_button = Button(top, image=qualify_ok_btn, cursor="hand2", borderwidth=0, bg="#436fd2", command=top.destroy)
        qualify_ok_button.place(x=320, y=350)
    else:
        top = Toplevel()
        top.geometry("800x450")
        qualify_bg_label = Label(top, image=qualify_bg)
        qualify_bg_label.pack()
        qualify_mssg_label = Label(top, image=qualify_fail_mssg, bg="#4e62d2")
        qualify_mssg_label.place(x=155, y=40)
        qualify_ok_button = Button(top, image=qualify_ok_btn, cursor="hand2", borderwidth=0, bg="#436fd2", command=top.destroy)
        qualify_ok_button.place(x=320, y=350)
    show_frame(frame4)

def data_handling():
    global player_name
    if(get_player_name(player_name) == None):
        insert_player(player_name, game_score)
    else:
        fetched_player = get_player_name(player_name)
        if(fetched_player[1] < game_score):
            update_score(player_name, game_score)

def load_highscores(frame):
    frame.tkraise()
    c.execute("""SELECT * FROM 'QuizData'
            ORDER BY score DESC
            LIMIT 0, 3;""")
    highscores = c.fetchall()

    const_txt = "NAME" + "\t\t\t\t" + "SCORE"
    txt_label = Label(frame5, font =("Courier New", 20,"bold"), text=const_txt, pady=25, bg="#f8f8f8")
    txt_label.place(x=475, y=75)
    
    disty = 225

    for x in range(0, 3):
        curr_player = highscores[x][0]
        curr_score = highscores[x][1]
        
        username_to_load_label = Label(frame5, font =("Courier New", 18,"bold"), text=curr_player, pady=10, bg="#f8f8f8")
        username_to_load_label.place(x=475, y=disty)
        
        userscore_to_load_label = Label(frame5, font =("Courier New", 18,"bold"), text=str(curr_score), pady=10, bg="#f8f8f8")
        userscore_to_load_label.place(x=1000, y=disty)

        disty += 90

def refresh_session():
    global player_name, game_score, time_in_sec
    player_name = ""
    var2.set(' ')
    game_score = 0
    time_in_sec = 20
    show_frame(frame1)

def add_questions():
    global input_question, input_options, input_correct_option
    top = Toplevel()
    top.geometry("1100x650")
    my_canvas = Canvas(top)
    my_canvas.pack(fill="both", expand=True)
    my_canvas.create_image(0, 0, image=add_questions_bg, anchor="nw")
    my_canvas.create_text(153, 70, text= "Add Question :", font= ("Helvetica", 18,"bold"), fill="#ffffff", anchor="nw")
    input_question = Entry(top)
    my_canvas.create_window(150, 100, window=input_question, width=750, anchor="nw")
    input_question.config(font= ("Helvetica", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5, highlightbackground="#74159d", highlightcolor="#74159d")
    #Options
    my_canvas.create_text(153, 180, text= "Enter Options :", font= ("Helvetica", 18,"bold"), fill="#ffffff", anchor="nw")
    input_options = Entry(top)
    input_options.config( font= ("Helvetica", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5, highlightbackground="#74159d", highlightcolor="#74159d")
    my_canvas.create_window(150, 210, window=input_options, width=750, anchor="nw")
    #Guide
    my_canvas.create_text(153, 255, text= "**Enter 4 Options Above", font= ("Helvetica", 10,"bold"), fill="#e31313", anchor="nw")
    my_canvas.create_text(153, 273, text= "**Enter Comma Seperated values", font= ("Helvetica", 10,"bold"), fill="#e31313", anchor="nw")
    #Correct Answers
    my_canvas.create_text(153, 330, text= "Correct Option :", font= ("Helvetica", 18,"bold"), fill="#ffffff", anchor="nw")
    input_correct_option = Entry(top)
    input_correct_option.config( font= ("Helvetica", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5, highlightbackground="#74159d", highlightcolor="#74159d")
    my_canvas.create_window(153, 360, window=input_correct_option,width=750, anchor="nw")
    my_canvas.create_text(153, 405, text= "*ENTER THE CORRECT ANSWER ABOVE(Note: It Must Be Present In The Enter Options Row **CASE SENSITIVE ", font= ("Helvetica", 10,"bold"), fill="#e31313", anchor="nw")
    #Submit Button
    submit_btn = Button(my_canvas, image=submit_btn_img, border=0, relief=FLAT, bg="#5f4bd1", cursor="hand2", command=handle_questions_options)
    submit_btn_window = my_canvas.create_window(450, 500, anchor="nw", window=submit_btn)
    #Exit Button
    form_exit_button = Button(my_canvas, image=form_exit_btn, cursor = "hand2", borderwidth=0, bg="#683ed2", command=top.destroy)
    exit_btn_window = my_canvas.create_window(1025, 10, anchor="nw", window=form_exit_button)

def handle_questions_options():
    global get_question, get_options, get_correct_option
    get_question = input_question.get()
    get_options = input_options.get().split(",")
    get_correct_option = input_correct_option.get()
    for option in get_options:
        formatted_option = option.strip()
        formatted_options_list.append(formatted_option)
    get_correct_option = get_correct_option.strip()

    temp_error_evaluator = validate_questions_options_data()
    if(temp_error_evaluator):
        submit_btn.wait_variable(err_var)
        handle_questions_options()
    
    #CONTINUE FROM HERE - TO FORWARD THE DATA TO RESPECTIVE LISTS AND DICTIONARY AND CLEAR THE PREVIOUS FETCHED DATA
    questions.append(get_question)
    answers.append(formatted_options_list)
    solutions[get_question] = get_correct_option
    
def validate_questions_options_data():
    global get_options, get_correct_option

    def error_validator():
        err_var.set(1)
        top2.destroy()
        return True

    if(len(get_options) != 4):
        top2 = Toplevel()
        top2.geometry("750x325")
        error_canvas = Canvas(top2)
        error_canvas.pack(fill="both", expand=True)
        error_canvas.create_image(50, 60, image=error_img, anchor="nw")
        error_canvas.create_text(120, 70, text= "Please Add Correct Number Of Options As Instructed", font= ("Helvetica", 18,"bold"), fill="#e31313", anchor="nw")
        ok_button = Button(error_canvas, image=ok_btn, cursor = "hand2", borderwidth=0, command=error_validator)
        ok_btn_window = error_canvas.create_window(315, 220, anchor="nw", window=ok_button)
    
    elif(get_correct_option not in formatted_options_list):
        top2 = Toplevel()
        top2.geometry("925x325")
        error_canvas = Canvas(top2)
        error_canvas.pack(fill="both", expand=True)
        error_canvas.create_image(50, 60, image=error_img, anchor="nw")
        error_canvas.create_text(120, 70, text= "Please Check If Correct Option Is Present In Both The Input Rows", font= ("Helvetica", 18,"bold"), fill="#e31313", anchor="nw")
        ok_button = Button(error_canvas, image=ok_btn, cursor = "hand2", borderwidth=0, command=error_validator)
        ok_btn_window = error_canvas.create_window(375, 220, anchor="nw", window=ok_button)

    else:
        return False

window = Tk()

window.state('zoomed')

window.title("    Quiz Game")

#window.iconbitmap('images\quiz.ico')

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
frame1 = Frame(window)
frame2 = Frame(window)
frame3 = Frame(window)
frame4 = Frame(window)
frame5 = Frame(window)

for frame in (frame1, frame2, frame3, frame4, frame5):
    frame.grid(row=0,column=0,sticky='nsew')

#============================================== FRAME 1 ==================================================#

bg_img = PhotoImage(file="images/bghome.png")
my_label =  Label(frame1, image=bg_img)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

start_btn = PhotoImage(file='images/bgFormplay.png')
play_button = Button(frame1, image=start_btn, cursor = "hand2", borderwidth=0, bg="#5f4bd1", command=lambda:show_frame(frame2))
play_button.pack(side="bottom", pady=50)

exit_btn = PhotoImage(file='images/exitForm.png')
exit_button = Button(frame1, image=exit_btn, cursor = "hand2", borderwidth=0, bg="#683ed2", command=window.destroy)
exit_button.pack(padx=30, pady=30, anchor="ne")

add_questions_btn = PhotoImage(file="images/addQuestionsbtn10.png")
add_questions_button = Button(frame1, image=add_questions_btn, cursor = "hand2", borderwidth=0, bg="#9400d4", command=add_questions)
add_questions_button.place(x= 900, y= 525)

error_img = PhotoImage(file="images/error2.png")
ok_btn = PhotoImage(file="images/okbtn.png")
#============================================== FRAME 2 ==================================================#
# #4a66d3
bg2_img = PhotoImage(file='images/bgbgbg.png')
my_label2 = Label(frame2, image=bg2_img)
my_label2.place(x=0, y=0, relwidth=1, relheight=1)

form = PhotoImage(file="images/bgForm3.png")
form_label = Label(frame2, image=form)
form_label.place(x=420, y=170, width=135, height=180)

title = Label (frame2, text= "Player Details", font= ("times new roman", 20,"bold"), bg="#3683d1", fg="#ffffff").place(x=625, y=90)

# First Row
name = Label (frame2, text= "Player Name", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=575, y=175)
input_name = Entry(frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5)
input_name.config(highlightbackground="#74159d", highlightcolor="#74159d")
input_name.place(x=575, y=205, width=270)

form_exit_btn = PhotoImage(file="images/exitForm.png")
form_exit_button = Button(frame2, image=form_exit_btn, cursor = "hand2", borderwidth=0, bg="#683ed2", command=lambda:show_frame(frame1))
form_exit_button.pack(padx=30, pady=30, anchor="ne")

# Second Row
mail = Label (frame2, text= "Email Id", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=575, y=260)
txt_mail = Entry (frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5)
txt_mail.config(highlightbackground="#74159d", highlightcolor="#74159d")
txt_mail.place(x=575, y=290, width=270)

# Third Row
contact = Label (frame2, text= "Contact Number", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff").place(x=575, y=345)
txt_contact = Entry (frame2, font= ("times new roman", 14),bg="#8319d3", fg="#ffffff", highlightthickness=5)
txt_contact.config(highlightbackground="#74159d", highlightcolor="#74159d")
txt_contact.place(x=575, y=375, width=270)

# Fourth Row
Stream = Label (frame2, text= "Stream", font= ("times new roman", 14,"bold"),bg ="#4273d2", fg="#ffffff", highlightthickness=5).place(x=575, y=430)

combo_stream = ttk.Combobox (frame2, font=("times new roman", 14), state='readonly', justify=CENTER)
combo_stream['values'] = ("Select your Stream", "Comps", "IT", "Extc", "Mechanical", "Civil")
combo_stream.place(x=575, y=460, width=270)
combo_stream.current(0)

form_start_btn = PhotoImage(file="images/bgFormplay.png")

form_start_button = Button(frame2, image=form_start_btn, cursor = "hand2", borderwidth=0, bg="#5f4bd1", command=submit_form)
form_start_button.pack(side="bottom", pady=50)

#============================================== FRAME 3 ==================================================#

quiz_bg_img = PhotoImage(file="images/Frame3.png")
img_label = Label(frame3, image=quiz_bg_img)
img_label.place(x=0, y=0, height=650,width=1300)

# NEXT BUTTON & FINISH BUTTON
next_btn = PhotoImage(file="images/nextF3.png")
finish_btn = PhotoImage(file="images/finishF2.png")

# Label for Questions
mylabel = Label()

# Label for Options
myoptionlabel = Label()

# Button for Next/Finish
button = Button()

# Label for Timer
timer_label = Label(frame3, font="times 50", fg="#FFFFFF", bg="#000000")
timer_label.place(x=900, y=80)

input_answer = StringVar()
var = IntVar()
var2 = StringVar()
var2.set(' ')

questions = ["The ratio of width of our National flag to its length is",
             "The words 'Satyameva Jayate' inscribed below the base plate of the emblem of India are taken from",
             "'Kathakali' is a folk dance prevalent in which state",
             "The last Mahakumbh of the 20th century was held at"]

solutions = {"The ratio of width of our National flag to its length is": "2:3",
             "The words 'Satyameva Jayate' inscribed below the base plate of the emblem of India are taken from": "Mundak Upanishad",
             "'Kathakali' is a folk dance prevalent in which state": "Karnataka",
             "The last Mahakumbh of the 20th century was held at": "Haridwar"}

answers = [["3:5", "2:3", "2:4", "3:4"],["Rigveda", "Satpath Brahmana", "Mundak Upanishad", "Ramayana"],
            ["Karnataka", "Orissa", "Kerala", "Manipur"],["Nasik", "Ujjain", "Allahabad", "Haridwar"]]

random.shuffle(questions)

#============================================== FRAME 4 ==================================================#

score_bg_img = PhotoImage(file="images/quizscorebg.png")

score_img_label = Label(frame4, image=score_bg_img, width=1920)
score_img_label.place(x=0, y=0, relheight=1,relwidth=1)

bact_to_home_btn = PhotoImage(file="images/backtohome.png")
bact_to_home_button = Button(frame4, image=bact_to_home_btn, cursor = "hand2", borderwidth=0, command=refresh_session)
bact_to_home_button.place(x=575 , y=200)

view_highscore_btn = PhotoImage(file="images/Highscore.png")
view_highscore_button = Button(frame4, image=view_highscore_btn, cursor = "hand2", borderwidth=0, command=lambda:load_highscores(frame5))
view_highscore_button.place(x=575 , y=475)

#============================================== FRAME 5 ==================================================#

last_page_bg = PhotoImage(file="images/quizscorebg.png")
last_page_bg_label = Label(frame5, image=last_page_bg, width=1920)
last_page_bg_label.place(x=0, y=0, relheight=1,relwidth=1)

highscore_exit_btn = PhotoImage(file="images/bg1exit.png")
highscore_exit_button = Button(frame5, image=highscore_exit_btn, cursor = "hand2", borderwidth=0, bg="white", command=refresh_session)
highscore_exit_button.pack(padx=30, pady=30, anchor="ne")

#============================================== FRAME 6 ==================================================#

qualify_bg = PhotoImage(file="images/qualify_background.png")
qualify_ok_btn = PhotoImage(file="images/qualify_btn7.png")
qualify_mssg = PhotoImage(file="images/qualify_mssg.png")
qualify_fail_mssg = PhotoImage(file="images/qualify_failmssg.png")

#============================================== ADD QUESTION CANVAS ==================================================#
add_questions_bg = PhotoImage(file="images/addQuestionbg.png")
submit_btn_img = PhotoImage(file="images/submitbtn.png")

submit_btn = Button()

my_canvas = Canvas(width=1100, height=650)

get_question = ""
get_options = ""
get_correct_option = ""

input_question = Entry()
input_options = Entry()
input_correct_option = Entry()

formatted_options_list = []

err_var = IntVar()

show_frame(frame1)

window.mainloop()

conn.close()