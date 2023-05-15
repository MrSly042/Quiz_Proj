import time
import tkinter as tk
import tkinter.ttk as ttk
from random import shuffle
from tkinter import messagebox

from PIL import Image, ImageTk


class Quiz(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("FIRS PRACTICE QUIZ") #program window title
        self.attributes("-fullscreen", True) #set the definitions of root window
        screen_height = self.winfo_screenheight()
        screen_width = self.winfo_screenwidth()
        # self.geometry("%dx%d+0+0" % (screen_width, screen_height))

        # root window icon
        icon = ImageTk.PhotoImage(file = 'logo.jpg')
        self.iconphoto(False, icon)
        self.resizable(height=0, width=0)
        self.protocol("WM_DELETE_WINDOW", lambda: 'break')
        self.tk_focusFollowsMouse()

        #variables to get user input on login screen, needs sql & internet to complete soon
        user_value = tk.StringVar()
        Pass_value = tk.StringVar()

        #help image
        help_img = tk.PhotoImage(file = "help.png")
        sub_img = tk.PhotoImage(file = "sub.png")
        prev_img = tk.PhotoImage(file = "previous.png")
        next_img = tk.PhotoImage(file = "next.png")
        ok_img = tk.PhotoImage(file = "ok.png")
        exit_img = tk.PhotoImage(file = "exit.png")


        #displays instrructions fro how to use program
        instructions = str("The following are the instructions for this program:\n"
                        "1) The current session will last for exactly 1 hour.\n"
                        "2) A clock as well as a bar representing your time will be shown in the top right corner.\n" 
                        "3) Once the time elapses the exam will end and results will be displayed.\n"
                        "4) A help button will be displayed at the top left corner, it will contain the instructions listed here.\n"
                        "5) Each question will be displayed in the center of the screen once the exam commences and will have four multiple choice options.\n"
                        "6) A single option can be selected at a time and can be deselected if you are unsure.\n"
                        "7) At the bottom there is a toggle menu, it can be used to move quickly between questions.\n"
                        "8) The current question displayed appears as black in the minibar while unanswered questions appear red and answered green\n"
                        "9) There are a 'NEXT' and 'PREV' buttons located beneath it question, they can be used to visit the corresponding screens.\n"
                        "10) If you have finished the current session and have adequately gone through your answers, a 'Submit' button is located beside the clock.\n"
                        )

        consequence = str("WARNINGS!!!\n"
                        "a) Window cannot be closed or minimized without use of the submit button.\n"
                        "b) Elapse of time will signal end of session.\n"
                        "c) For this app's beta version, previous test scores will not be saved.\n"
                        )

        #when accepting the program parameters using GUI, make it so that
        #an answer not in the choices can't be set :)

        #parameters for quiz screen
        questions = [
            {'question': 'What is the capital of France?',
            'choices': ['Paris', 'London', 'New York'],
            'answer' : 'Paris'
            },
            
            {'question': 'What is the tallest mountain in the world?', 
            'choices': ['Mount Everest', 'Mount Kilimanjaro', 'Mount Fuji'],
            'answer' : 'Mount Everest'
            },
            
            {'question': 'What is the largest planet in the solar system?', 
            'choices': ['Jupiter', 'Mars', 'Earth'],
            'answer' : 'Jupiter'
            }
                    ]
        output = [] # list to store values "WRONG" or "CORRECT" selfd on choice
        all = {} # saves all choices made and not (not made stored as 'nil')
        current_question = 0 # Create a variable to keep track of the current screen index
        states = [] #selected and deselcted states containers for display of radiobuttons
        dice = {} #dict to store user choices selfd on screen index as key and values as values
        opt = {} #stores selection to be shown when screen is changed

        #is called when submit btn is clicked
        def ask():
            global confirm
            confirm = messagebox.askokcancel('Closure', "Continution will end this session!!!", icon="info")
            if confirm:
                stor()
                try_close()

        # called immediately testing is to begin
        def commence():
            reset_window()
            
            #update function to change time displayed with time
            def update_timer(seconds_left):
                    global update_aft
                    hours = seconds_left // 3600
                    minutes = (seconds_left // 60) % 60
                    seconds = seconds_left % 60
                    if hours > 0:
                        timer_label.config(text='{}hr {} mins {}secs'.format(hours, minutes, seconds))
                    elif minutes > 0:
                        timer_label.config(text='{}mins {}secs'.format(minutes, seconds))
                    else:
                        timer_label.config(text='{} secs'.format(seconds))
                    if seconds_left > 0:
                        update_aft = self.after(1000, update_timer, seconds_left - 1)
            
            main_cont = tk.Frame(self)
            main_cont.pack(fill='both', expand=True)
            
            main_canv = tk.Canvas(main_cont, )
            main_canv.pack(side='left', fill='both', expand=True)
            
            main_scroll_horiz = tk.Scrollbar(self, orient='horizontal',
                                        command=main_canv.xview,
                                        )
            
            main_scroll_horiz.pack(side='bottom', fill='x')
            
            main_scroll_vert = tk.Scrollbar(main_cont, command=main_canv.yview,
                                        )
            
            main_scroll_vert.pack(side='right', fill='y')
            
            main_canv.config(xscrollcommand=main_scroll_horiz.set,
                            yscrollcommand=main_scroll_vert.set,
                            )
            
            main_cont_canv = tk.Frame(main_canv, )
            main_canv.create_window((0,0), window = main_cont_canv, anchor = 'nw')
            
            def change_main(event):
                if main_canv.winfo_exists():
                    main_canv.configure(scrollregion=main_canv.bbox('all'))
                            
            main_canv.bind("<Configure>", change_main)
            
            #new frames and layout
            
            global holder, tools, hey
            holder = tk.Frame(main_cont_canv)
            holder.pack(side='left', fill='both', expand=True, 
                        )
            
            tools = tk.Frame(holder)
            tools.grid(row=0, column=0,pady=50)
            
            hey = tk.IntVar()
            hey.set(3600)
            
            # progress bar to display time value(decreasing)
            def bar():
                global cool
                if hey.get() <= 0:
                    stor()
                else:
                    hey.set(hey.get()-1)
                    cool = tools.after(1000, bar)
            
            time_bar = ttk.Progressbar(tools, orient='horizontal', variable=hey,
                                    length=600, mode = 'determinate')
            time_bar.grid(row = 0, column = 2,
                        padx = (510, 0), pady = 20, sticky='e')
            
            timer_label = tk.Label(tools, text='1hr 00mins 00secs', font=('Arial', 24))
            timer_label.grid(row = 1, column = 2, 
                            pady=3, sticky='e')
            
            #call bar func
            bar()
            
            # Start the timer with 1 hour
            update_timer(3600)
            
            #create and grid buttonns
            
            submit_btn = ttk.Button(tools, image=sub_img, 
                                    command=ask)
            submit_btn.grid(row = 0, column = 1, sticky='w', 
                            ipadx=30
                            )
            
            help_btn = ttk.Button(tools, image=help_img, 
                                command= helping, 
                                )
            help_btn.grid(row = 0, column = 0, sticky = 'w',
                        ipadx=60, ipady=30, padx=(0, 50),
                        )
            
            #shuffles items in questions lists
            shuffle(questions)
            
            #shuffles choices in choice list in respective index of questions lists
            for question in questions:
                shuffle(question['choices'])
                
            # function to check and display state of radiobtn(selected or not)
            def toggle(name, val):
                if name in states:
                    v.set(4) #if condition is met, sets the selected radiobtn out of range
                    states.remove(name) # removes from list
                    #deletes the previous choice made if btn is unselected
                    for key, item in dice.items():
                        if item == name:
                            del dice[key]
                            break
                else:
                    states.append(name) #adds to states if unselected
                ok = v.get() #gets the selected option
                opt.update({current_question:ok}) #saves option to retrieved once user navigates back to that screen

            # Create the function to display the current question and answer choices
            def display_question(index):
                question_label.config(text=questions[index]['question'], font=("comic sans ms", 30, 'bold'))
                for i, choice in enumerate(questions[index]['choices']):
                    choice_radiobuttons[i].config(text=choice)
                update_mini_bar(index)

            # Create the function for the 'previous' button
            # sets choice if a button from the screen has been selected
            # changes minibar colours selfd on whether screen have chosen options in them
            def previous_question():
                global current_question
                if current_question > 0:
                    if current_question in dice.keys():
                        mini_bar_buttons[current_question].config(bg='green')
                    else:
                        mini_bar_buttons[current_question].config(bg='red')
                    current_question -= 1
                    display_question(current_question)
                    if current_question in opt.keys():
                        chosen = opt[current_question]
                        v.set(chosen)
                    else: v.set(4)

            # Create the function for the 'next' button
            # sets choice if a button from the screen has been selected
            # changes minibar colours selfd on whether screen have chosen options in them
            def next_question():
                global current_question
                if current_question < len(questions) - 1:
                    if current_question in dice.keys():
                        mini_bar_buttons[current_question].config(bg='green')
                    else :
                        mini_bar_buttons[current_question].config(bg='red')
                    current_question += 1
                    display_question(current_question)
                    if current_question in opt.keys():
                        chosen = opt[current_question]
                        v.set(chosen)
                    else: v.set(4)
                    

            # Create a function to update the mini-bar
            def update_mini_bar(y):
                mini_bar_buttons[current_question].config(bg='black')

            # Create a function to handle selecting an answer
            # param is passed from respective radiobtn
            def select_answer(y):
                    dice.update({current_question:questions[current_question]['choices'][y]}) #update dice with respect to current screen and shuffles
                    name = dice[current_question]
                    toggle(name,y) #passes key of current screen and btn index to toggle to check the states
            
            def mini_func(i):
                if i > current_question:
                    x = 0
                    while x < i:
                        next_question()
                        x += 1
                elif i < current_question:
                    x = current_question
                    while x > i:
                        previous_question()
                        x -= 1
            
            quest_frame = tk.Frame(holder)
            question_itself = tk.Frame(quest_frame)
            choice_frame = tk.Frame(quest_frame)
            question_label = tk.Label(question_itself, text='')

            v = tk.StringVar(choice_frame, 5) #change to automatically adjust selfd on length of questions

            # declaring radiobtns using for loop
            # each call "select_ans func() using respaecting index"
            choice_radiobuttons = [tk.Radiobutton(choice_frame,value=i, variable=v,command = lambda v = i: select_answer(v)) for i in range(3)]

            nav_frame = tk.Frame(holder)
            previous_button = ttk.Button(nav_frame, image=prev_img, command=previous_question)
            next_button = ttk.Button(nav_frame, image=next_img, command=next_question)
            
            mini_bar = tk.Frame(holder)
            mini_bar_buttons = []
            for i in range(len(questions)):
                button = tk.Button(mini_bar, text=i+1, command=lambda idx=i: mini_func(idx), 
                                bg='red', fg="white")
                
                mini_bar_buttons.append(button)
                button.grid(row=1, column=i, padx=12)

            # Grid the GUI elements
            question_itself.grid(row=0,column=0, sticky='n', )
            quest_frame.grid(row=1, column=0, sticky='nsew', padx=300, pady=50)
            
            choice_frame.grid(row=1, column=0)
            nav_frame.grid(row=2, column=0, sticky='nsew', padx=100, pady=10)
            
            mini_bar.grid(row=3, column=0, sticky='nsew', )
            question_label.grid(row=0, column=0, )
            
            col = 0
            for button in choice_radiobuttons:
                button.grid(row = 0, column = col,
                            pady=50, padx=50)
                col+=1
            previous_button.grid(row=0, column=0, padx=300, 
                                pady=30, ipadx=20, ipady=10, sticky='w')
            next_button.grid(row=0, column=1, padx=300 ,pady=30, 
                            ipadx=20, ipady=10, sticky='e')
            # Display the first question
            display_question(0)
            
        #is called by "ask()" and when time bar elapses
        #displayes time used up and other parameters
        #shown once testing is completed
        def try_close():
            global other1
            reset_window()
            asserts()
            good = 0
            for word in output:
                total = len(questions)
                if word == "CORRECT":
                    good += 1
            
            #new frame for results screen      
            show_res = tk.Frame(self, bg='black')
            show_res.pack(side=TOP, fill=BOTH, expand=True)
            
            #canvas for results screen
            show_canv = tk.Canvas(show_res, )
            show_canv.pack(side=LEFT, fill=BOTH, expand=True)
            
            #scrollbars inside canvas
            show_scroll_horiz = tk.Scrollbar(self, orient='horizontal', command=show_canv.xview)
            show_scroll_horiz.pack(side=BOTTOM, fill=X)
            
            show_scroll_vert = tk.Scrollbar(show_res, command=show_canv.yview)
            show_scroll_vert.pack(side=RIGHT, fill=Y)
            
            #configure scrollbars for canvas
            show_canv.config(xscrollcommand=show_scroll_horiz.set,
                            yscrollcommand=show_scroll_vert.set)
            
            #frame/window within canvas
            cont_frame = tk.Frame(show_canv, )
            show_canv.create_window((0,0), window = cont_frame, anchor = 'nw')
            
            #function for scrollregion
            def change_show(event):
                if show_canv.winfo_exists():
                    show_canv.configure(scrollregion=show_canv.bbox('all'))
            
            #bind screen with function
            cont_frame.bind("<Configure>", change_show)
                        
            result_frame = tk.Frame(cont_frame, bg = 'black')
            self.config(bg='black')
            score_frame = tk.Frame(result_frame, bg = 'black')
            exit_frame = tk.Frame(result_frame, bg = 'black')
            others_frame = tk.Frame(result_frame, bg = 'black' )
            
            exit_btn = ttk.Button(exit_frame,image=exit_img, command=self.destroy,
                        )
            
            score_sheet = tk.Label(score_frame,text = "YOU SCORED: \n" +
                                "{}/{}".format(good, total), bg='sky blue',  font = ("Times New Roman", 18, 'bold'))
            
            other1 = tk.Label(others_frame, bg='orange',relief='sunken', bd=10,
                        font = ("Times New Roman", 18, 'bold'),)
            
            other2 = tk.Button(others_frame, text="SEE CORRECTIONS", bd=10,
                            bg = 'light green', font = ("Times New Roman", 18, 'bold'),command=corrections)
            
            result_frame.grid(row=0, column=0, sticky='nswe')
            exit_frame.grid(row=0, column=0, sticky='nswe', pady=(10, 50), )
            
            score_frame.grid(row=1, column = 0, sticky='nswe', pady = 50)
            others_frame.grid(row=2, column = 0, pady = 100, sticky = 'nswe')
            
            exit_btn.grid(row=0, column = 0, sticky='e', padx=(1450, 20), ipady=30, ipadx= 50)
            score_sheet.grid(row=0, column=0, padx=(700, 0), ipadx=100, ipady=100)
            
            other1.grid(row=0, column=0, sticky = 'w',
                        padx=500, ipadx=50, ipady=50)
            
            other2.grid(row = 0, column = 0, sticky='e',
                        ipadx=30, ipady=50,)
            
            time_used()

        #time used up
        def time_used():
            value = 3600 - hey.get()
            hours = value // 3600
            minutes = (value // 60) % 60
            seconds = value % 60
            if hours > 0:
                other1.config(text="TIME USED UP: \n" + "{}hr {} mins {}secs OUT OF 1 hour".format(hours, minutes, seconds))
            elif minutes > 0:
                other1.config(text="TIME USED UP: \n" + '{}mins {}secs OUT OF 1 hour'.format(minutes, seconds))
            else:
                other1.config(text="TIME USED UP: \n" + '{} secs OUT OF 1 hour'.format(seconds))

        #stops the updates to times
        def stor():
            data = hey.get()
            tools.after_cancel(cool)
            self.after_cancel(update_aft)

        # works in hand with correction func, used for assertion of selected choices
        def asserts():
            i = 0
            while i < len(questions):
                if i in dice.keys(): 
                    a = dice[i]
                    if a == questions[i]['answer']:
                        output.append('CORRECT')
                    else: output.append("WRONG")
                    all.update({i:dice[i]})
                else:
                    all.update({i:"Nil"})
                    output.append("WRONG")
                i += 1

        # function to display corrections once time has elapsed or submit btn is clicked
        def corrections():
            reset_window()
            corr_list = []
            to_print = []
            for x in range (len(questions)):
                corr_list.append(questions[x]['answer'])
                    
            m,n = 0,1
            for word in corr_list:
                a = "{}) You answered '{}' ({}): {}\n".format(n, all[m], output[m], word)
                to_print.append(a)
                m += 1
                n += 1
                
            show_every = ''.join(to_print)
            
            #new frame for results screen      
            corr_frame = tk.Frame(self, )
            corr_frame.pack(side=TOP, fill=BOTH, expand=True)
            
            #canvas for results screen
            corr_canv = tk.Canvas(corr_frame, bg = 'light green')
            corr_canv.pack(side=LEFT, fill=BOTH, expand=True)
            
            #scrollbars inside canvas
            corr_scroll_horiz = tk.Scrollbar(self, orient='horizontal', command=corr_canv.xview)
            corr_scroll_horiz.pack(side=BOTTOM, fill=X)
            
            corr_scroll_vert = tk.Scrollbar(corr_frame, command=corr_canv.yview)
            corr_scroll_vert.pack(side=RIGHT, fill=Y)
            
            #configure scrollbars for canvas
            corr_canv.config(xscrollcommand=corr_scroll_horiz.set,
                            yscrollcommand=corr_scroll_vert.set)
            
            #frame/window within canvas
            cont_corr = tk.Frame(corr_canv, )
            corr_canv.create_window((0,0), window = cont_corr, anchor = 'nw')
            
            #function for scrollregion
            def change_corr(event):
                if corr_canv.winfo_exists():
                    corr_canv.configure(scrollregion=corr_canv.bbox('all'))
            
            #bind screen with function
            corr_frame.bind("<Configure>", change_corr)
            
            new = Frame(cont_corr, bg = 'light green')
            
            correct_me = tk.Label(new, text=show_every, bg='light green', font = ("Comic sans ms", 15, 'bold'),
                            justify='left')
            
            leave = ttk.Button(new, image=exit_img,  
                            command = self.destroy)
            
            new.grid(row=0, column = 0, sticky='nswe', )
            correct_me.grid(row= 0, column = 0, sticky='n',
                            ipady=10)
            leave.grid(row=0, column = 1, sticky = 'e', pady = 5, padx = (800, 10),
                    ipadx=10, ipady=10)

        # called when help button on main quiz screen is clicked
        def helping():
            dis = tk.Toplevel(holder)
            dis.title("Help")
            dis.geometry("1400x600")
            dis.iconphoto(False, help_img)
            # dis.anchor('center')
            dis.resizable(height = 0, width = 0)
            dis.config(background= "cyan" )
                
            dis_frame = tk.Frame(dis, background = 'cyan')
            dis_frame.grid(row=0, column=0)
            #should include icon image
            info = tk.Label(dis_frame,text = instructions, justify='left',
                        background = 'cyan', font = ("comic sans ms", 15, 'bold'))
            help_end = ttk.Button(dis_frame, image=ok_img, command = dis.destroy,
                                width=100)

            info.grid(row=0, column=0)
            help_end.grid(row=1, column=0, padx=300)

        # function to clear screen, called when past widgets (not root) are no longer needed
        def reset_window():
            # Destroy all widgets in the root window
            for widget in self.winfo_children():
                widget.destroy()

        # displays screen after login has been verified
        def show_inst():
                    
                    #new frame to hold canvas and others
                    contain_canv_instruct = tk.Frame(self)
                    contain_canv_instruct.pack(fill='both', expand=True)
                    
                    #canvas widget
                    instruct_canvas = tk.Canvas(contain_canv_instruct, bg = 'sky blue')
                    instruct_canvas.pack(side='left', fill='both', expand=True)
                    
                    #horizontal scrollbar
                    inst_scroll_horiz = tk.Scrollbar(instruct_canvas, orient='horizontal', 
                                            command=instruct_canvas.xview,
                                            )
                    
                    inst_scroll_horiz.pack(side='bottom', fill='x')
                    
                    #vertical scrollbar
                    inst_scroll_vert = tk.Scrollbar(contain_canv_instruct, command=instruct_canvas.yview,
                                                )
                    
                    inst_scroll_vert.pack(side='right', fill='y')
                    
                    #configure the scrollbars for the canvas
                    instruct_canvas.config(xscrollcommand=inst_scroll_horiz.set,
                                        yscrollcommand=inst_scroll_vert.set,
                                        )
                    
                    instruct_cont_canv = tk.Frame(instruct_canvas, bg="sky blue")
                    instruct_canvas.create_window((0,0), window = instruct_cont_canv, anchor = 'nw')
                    
                    def change_inst(event):
                        if instruct_canvas.winfo_exists():
                            instruct_canvas.configure(scrollregion=instruct_canvas.bbox('all'))
                            
                    instruct_canvas.bind("<Configure>", change_inst)
                    
                    #frame for instructions page
                    new = tk.Frame(instruct_cont_canv, bg="sky blue", )
                    new.grid(row=0, column=0, )
                                            
                    #instructions header
                    page2_head = tk.Label(new, text = "INSTRUCTIONS", background="black",
                                        foreground="white", font = ("comic sans ms", 40, 'bold'))
                    page2_head.grid(row = 0, column = 0,
                                    ipadx=580, ipady=50)
                    #info
                    information = tk.Label(new, text = instructions, justify = "left",
                                        background = "sky blue",font=("Calibri", 15, 'bold')
                                        )
                    information.grid(row=1, column=0, sticky = "W")
                    
                    #extra info(warnings)
                    warn = tk.Label(new, text = consequence, foreground = 'red',
                                background = "sky blue",font=("Calibri", 15, "bold"),
                                justify = "left")
                    warn.grid(row = 2, column=0, sticky = "W")
                    
                    #button and its styling
                    style_start = ttk.Style()
                    style_start.configure('W.TButton', font = 
                                        ('Times New Roman', 25, 'bold'),
                                        foreground = "green",
                                        )
                    
                    start = ttk.Button(new, text = 'START', command=commence, 
                                    width=35, style = 'W.TButton')
                    start.grid(row=3, column=0)

        # function to assert input validity, will vary once sql is incorporated
        def get_input():
            user = user_value.get()
            pass_w = Pass_value.get()
            
            if user == 'Ozioma Ogu' and pass_w == '123456':
                messagebox.showinfo('Login Successful', 'Welcome to the next stage!')
                user_value.set('')
                Pass_value.set('')
                reset_window()
                show_inst()
            
            elif user == "Ezeofor Jessica" and pass_w == '123456':
                messagebox.showinfo('HI', "Welcome, sleeping beauty!!\nThis might annoy you a bit :)")
                
                screen1 = tk.Toplevel()
                screen1.geometry("350x100")
                screen1.title("Operation annoy ")
                screen1.iconphoto(False, icon)
                
                def fine():
                    for i in range(3):
                        messagebox.askyesno('Hmm', "Are you sure? ")
                    show = messagebox.showinfo('Hey', "I can't really know\ni'm just a program, \nbut i wish you a good day :)")
                    show2 = messagebox.showinfo("advance", 'You may continue')
                    user_value.set('')
                    Pass_value.set('')
                    reset_window()
                    show_inst()   
                
                def not_fine():
                    messagebox.showinfo('Joy', "Well, if it helps, anytime u feel that way\n imagine Lifechanger vibing to amapiano :)")
                    messagebox.showinfo('Joy', "I wish you a good laugh and a cure to whatever ur feeling :)")
                    messagebox.showinfo("advance", 'You may continue')
                    user_value.set('')
                    Pass_value.set('')
                    reset_window()
                    show_inst()   
            
                screen1.config(bg='brown')
                label = tk.Label(screen1, text = "How are you?", anchor='center', bg='brown')
                y = tk.Button(screen1, text='Fine', command=fine, fg='blue')
                
                n = tk.Button(screen1, text='Sad/Bored', command=not_fine, fg='blue')
                label.grid(row=0, column=0, sticky='w')
                y.grid(row=1, column = 0, sticky='e', padx = 50)
                n.grid(row=1, column = 1, sticky='e', padx = 50)
                
                screen1.mainloop()
            
            else:
                messagebox.showerror("Incorrect Login Details", 'Try Again')
                user_value.set('')
                Pass_value.set('')

        #bypass for editiing inner code, may be changed to admin privy's
        def bypass():
            answer = messagebox.askokcancel('Confirm Bypass', 
                                            "By choosing you agree that Chibuike is the Best!!!",
                                            icon = 'info')
            if answer:
                messagebox.showinfo('Login Successful', "I'm glad we think alike!!!\n" + 'Welcome to the next stage!')
                user_value.set('')
                Pass_value.set('')
                reset_window()
                show_inst()   
            else :
                messagebox.showinfo('Access Denied', 'Enter the correct login info then!')
                user_value.set('')
                Pass_value.set('')

        if __name__ == '__main__':
            container = tk.Frame(self, bg='violet')
            container.pack(side='top',fill="both", expand=True)

            #canvas for scrollbar
            canvase = tk.Canvas(container, bg='violet')
            canvase.pack(side='left', fill='both', expand=True)
            #scrollbar for login page
            login_scroll_horiz = tk.Scrollbar(canvase, orient='horizontal',command=canvase.xview,
                                        )
            login_scroll_horiz.pack(side='bottom', fill='x')

            login_scroll_vert = tk.Scrollbar(container, command=canvase.yview)
            login_scroll_vert.pack(side='right', fill='y')

            #configure canvaas with horizontal scroll
            canvase.config(xscrollcommand=login_scroll_horiz.set,
                        yscrollcommand=login_scroll_vert.set) 

            #login page frame bg and declaration
            cont_within_self = tk.Frame(canvase, bg='violet')
            #create window
            canvase.create_window((0,0), window = cont_within_self, 
                                anchor='nw', 
                                )


            #login section, nested in master frame above
            header = tk.Frame(cont_within_self, background='purple')
            header.grid(row=0, column=0,)

            login_page = tk.Label(header, background='purple', foreground='white',
                            text='PLEASE ENTER YOUR LOGIN DETAILS TO PROCEED TO THE NEXT STAGE',
                            font=('Times New Roman',20, 'bold'),
                            justify='center', height=5)

            login_page.grid(row=0, column=0, ipadx=295)

            frame = tk.Frame(cont_within_self, bg='violet')
            frame.grid(row=1, column=0, sticky='w')

            #entry segments for credentials
            username = tk.Label(frame, text='Username:', foreground='red',
                            font=('calibri', 30, 'normal'), background='violet')

            password = tk.Label(frame, text = 'Password:', foreground='red',
                            font=('Calibri', 30, 'normal'), background='violet')

            # username.pack()
            username.grid(row=1, column=0, sticky='w')
            password.grid(row=2, column=0, sticky='w')

            user_entry = tk.Entry(frame, textvariable=user_value,
                            font=('Comic Sans', 15), width=50, 
                            )
            
            user_entry.focus_force()
            
            pass_entry = tk.Entry(frame, textvariable=Pass_value,
                            show='*', font=('Comic Sans', 15), width=50
                            )

            user_entry.grid(row=1, column=1, sticky='w', padx=50)
            user_entry.focus_force() #once code runs gives focus to it
            pass_entry.grid(row=2, column=1, sticky='w', padx=50)

            #buttons for taking decisions at login screen
            sub_btn = ttk.Button(frame, text = 'Login', 
                            command = get_input)

            by_btn = ttk.Button(frame, text='Bypass',
                            command = bypass)

            end = ttk.Button(frame, text = "END",
                        command = lambda: self.destroy())


            sub_btn.grid(row=3, column=2, sticky='w', padx=10, pady=10)
            by_btn.grid(row=3, column=3, sticky='w', padx=10, pady=10)
            end.grid(row=3, column=4, sticky='w', padx=10, pady=10)

            def change(event):
                if canvase.winfo_exists():
                    canvase.configure(scrollregion=canvase.bbox('all'))
                
            cont_within_self.bind("<Configure>", change)


        # timer  still not working
        # automatically adjust deselct radiobutton selfd on number of questions
        # questions in im formats
        # maybe questions in vid formats
        # speech to questions reading(when typed)
        # databse capabilites
        # when questions in txt fromat, check if answer in choices
        # One admin will have priiledges
        
        
if __name__ == '__main__':
    App = Quiz()
    App.mainloop()