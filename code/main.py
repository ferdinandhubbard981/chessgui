import restartgame
import tkinter as tk
from tkinter import ttk
import chessboard_detection
import board_basics
from game_state_classes import Game_state
from tkinter.simpledialog import askstring
import ml_model
import chess
from PIL import ImageTk, Image
import cv2
import numpy as np
import time
import sys
import os
from game_state_classes import PositionChanged,NoValidPosition
import tensorflow as tf
import time
timeinmin = 10
function_parser = ""
sess = tf.InteractiveSession()

auto_is_white = True
keep_going = False
def resetgame():
    global auto_is_white
    global keep_going
    previouslink = restartgame.getLink()
    restartgame.refreshBrowser()
    restartgame.launchNewGameSearch()
    gamefound = restartgame.checkNewGameFound(previouslink)
    if gamefound == False:
        return False
    colour = "unsure"
    start = time.time()
    while colour == "unsure" and (time.time() - start) < 25:
        colour = restartgame.checkColour()
    if colour == "white":
        keep_going = True
        auto_is_white = True
    elif colour == "black":
        firstmoveplayed = False
        while firstmoveplayed == False and (time.time() - start) < 25:
            firstmoveplayed = restartgame.checkIfOpponentPlayed()
            time.sleep(0.2)
    
        keep_going = True
        auto_is_white = False
    if (time.time() - start) >= 25:
        return False
    else:
        return True
            
def clear_logs(logs_text):
    logs_text.delete('1.0', tk.END)
    #add_log("Logs have been cleared:")

def add_log(logs_text,log):
    logs_text.insert(tk.END,log + "\n")

def stop_playing():
    print('stop playing')
    global running
    global slider_str
    global slider_var
    running = False
    button_start = ttk.Button(tab1, text="Start playing", command=start_playing)
    button_start2 = ttk.Button(tab2, text="Start playing", command=puzzel_rush)

    button_start.grid(column=0, row=1, pady=10, columnspan=2)
    button_start2.grid(column=0, row=0, pady=10)
    slider_str.config(state=tk.ACTIVE)
    slider_var.config(state=tk.ACTIVE)
    successfulreset = False
    while successfulreset == False:
        successfulreset = resetgame()
    # raise SystemExit

def start_playing():
    start = time.time()
    global function_parser
    global running
    global slider_str
    global slider_var
    running = True
    strength = slider_str.get()+1
    variance = slider_var.get()+1
    slider_str.config(state=tk.DISABLED)
    slider_var.config(state=tk.DISABLED)
    game_state = Game_state()
    add_log(logs_text,"Looking for a chessboard...")

    found_chessboard, position  = chessboard_detection.find_chessboard()

    if found_chessboard:
        add_log(logs_text,"Found the chessboard " + position.print_custom())
        game_state.board_position_on_screen = position
    else:
        add_log(logs_text,"Could not find the chessboard")
        add_log(logs_text,"Please try again when the board is open on the screen\n")
        return
    

    button_start = ttk.Button(tab1,text="Stop playing", command =stop_playing)
    button_start.grid(column=0,row = 1,pady=10,columnspan=2)



    # add_log(logs_text,"Checking if we are black or white...")
    resized_chessboard = chessboard_detection.get_chessboard(game_state)

    game_state.previous_chessboard_image = resized_chessboard

    we_are_white = v.get()
    if keep_going == True:
        we_are_white = auto_is_white
    game_state.we_play_white = we_are_white
    fen_str,detected_board = game_state.build_fen(we_are_white)
    try:
        game_state.board.set_fen(fen_str)
    except Exception as e:
        print(e)
        stop_playing()
        return
    # print(game_state.get_castling_rights())

    while running:

        window.update()
        if (time.time() - start) > (timeinmin * 60 / 2):
            stop_playing()
            return

        timeleft = ((timeinmin * 60) - (time.time() - start)) / 2
        # if timeleft < 600:
        #     variance = 12000
        # if timeleft < 300:
        #     variance = 8000
        # if timeleft < 180:
        #     variance = 2500
        # if timeleft < 60:
        #     variance = 700
        # if timeleft < 40:
        #     variance = 600
        # if timeleft < 30:
        #     variance = 300
        # if timeleft < 10:
        #     variance = 50
        # if timeleft < 5:
        #     variance = 5
            
        if game_state.moves_to_detect_before_use_engine == 0:
            #add_log("Our turn to play:")

            score,move_time = game_state.play_next_move(position.factor,strength,variance)

            position_eval = ttk.Label(tab1,text=f"Score: {score} \t move_time: {move_time}",anchor="e", wraplength = 300)
            position_eval.grid(column =0,row = 9,columnspan=2)
            #add_log("We are done playing")
        found_move=False
        try:

            found_move, move,img_boards = game_state.register_move_if_needed()

            if found_move:
                v.set(not v.get())
                diff = abs(img_boards[0] - img_boards[1])
                numpy_horizontal = np.vstack((img_boards[0], img_boards[1], diff))
                image = cv2.resize(numpy_horizontal, (200, 600),interpolation=cv2.INTER_CUBIC)
                img = ImageTk.PhotoImage(Image.fromarray(np.uint8(image)))
                imglabel = tk.Label(tab1, image=img).grid(row=2, column=2, rowspan=100)

        except Exception as e:
            print(e)
            stop_playing()
            return

        
        if function_parser:
            move = function_parser
            function_parser=""
            new_board = chessboard_detection.get_chessboard(game_state)
            valid_move_UCI = chess.Move.from_uci(move)
            valid_move_registered = game_state.register_move(valid_move_UCI, new_board)

        if found_move:
            clear_logs(logs_text)
            add_log(logs_text,"The board :\n" + str(game_state.board) + "\n")
            add_log(logs_text,"\nAll moves :\n" + str(game_state.executed_moves))

    
def new_move():
    global function_parser
    window.attributes('-topmost', 0)
    new_move = askstring('Missed Move', 'What is the next move')
    window.attributes('-topmost', 1)
    function_parser = new_move
    window.attributes('-topmost', 1)
    print(new_move)
    # curr_pos = game_state.build_fen()




def puzzel_rush():
    global function_parser
    global running
    global slider_str2
    global slider_var2
    running = True
    strength2 = slider_str2.get() + 1
    variance2 = slider_var2.get() + 1
    slider_str2.config(state=tk.DISABLED)
    slider_var2.config(state=tk.DISABLED)
    game_state = Game_state()


    found_chessboard, position = chessboard_detection.find_chessboard()

    if found_chessboard:
        game_state.board_position_on_screen = position
    else:
        print('no board on screen')
        return

    button_start2 = ttk.Button(tab2, text="Stop playing", command=stop_playing)
    button_start2.grid(column=0, row=0, pady=10)

    resized_chessboard = chessboard_detection.get_chessboard(game_state)
    game_state.previous_chessboard_image = resized_chessboard

    we_are_white, fen_str, detected_board = game_state.build_fen_guess_side()
    compare = cv2.resize(resized_chessboard,(200,200),interpolation=cv2.INTER_CUBIC)
    detected_board = cv2.resize(detected_board, (200,200),interpolation=cv2.INTER_CUBIC)[...,0]
    numpy_horizontal = np.vstack((compare,detected_board))

    detected_board = ImageTk.PhotoImage(Image.fromarray(np.uint8(numpy_horizontal)))

    imglabel = tk.Label(tab2, image=detected_board).grid(row=7, column=0, columnspan=2)

    try:
        game_state.board.set_fen(fen_str)
    except:
        stop_playing()


    while running:
        window.update()

        if game_state.moves_to_detect_before_use_engine == 0:
            game_state.play_next_move(position.factor, strength2, variance2)
           

        found_move = False
        move = "no move"
        img_boards = (game_state.previous_chessboard_image, game_state.previous_chessboard_image)
        try:
            found_move, move, img_boards = game_state.register_move_if_needed()
        except PositionChanged:
            print('postionchanged')
            time.sleep(2)
           
            we_are_white,fen_str,detected_board = game_state.build_fen_guess_side()
            try:
                game_state.board.set_fen(fen_str)
            except:
                stop_playing()
            curr_board = chessboard_detection.get_chessboard(game_state, (200, 200))

            detected_board = cv2.resize(detected_board, (200, 200),interpolation=cv2.INTER_CUBIC)[..., 0]
            numpy_horizontal = np.vstack((curr_board, detected_board))

            detected_board = ImageTk.PhotoImage(Image.fromarray(np.uint8(numpy_horizontal)))

            imglabel = tk.Label(tab2, image=detected_board).grid(row=7, column=0, columnspan=2)

            continue

        if found_move:
            imglabel = tk.Label(tab2, image=detected_board).grid(row=7, column=0,columnspan=2)

        if function_parser:
            move = function_parser
            function_parser = ""
            new_board = chessboard_detection.get_chessboard(game_state)
            valid_move_UCI = chess.Move.from_uci(move)
            valid_move_registered = game_state.register_move(valid_move_UCI, new_board)



ml_model.init_binary()
ml_model.init_class()

window = tk.Tk()


window.wm_attributes("-topmost", 1)
window.geometry('%dx%d+%d+%d' % (590,730, 1000, 100))
window.title("ChessVisionBot")

label_title = tk.Label(window,text="Computer Vision based Chessbot",anchor="e", wraplength = 300)
label_title.grid(column = 0,row = 0,columnspan=2,pady=5)

note = ttk.Notebook(window)
tab1 = ttk.Frame(note)
tab2 = ttk.Frame(note)
tab3 = ttk.Frame(note)
note.add(tab1, text='Computer')
note.add(tab2, text='Puzzelrush')
note.add(tab3, text='Analysis')
note.grid(column = 0,row = 1,padx=10)


button_start = ttk.Button(tab1,text="Start playing", command =start_playing)
button_start.grid(column=0,row = 1,pady=10,columnspan=2)

button_enter_move=ttk.Button(tab1,text="Missed Move",command=new_move)
button_enter_move.grid(column=2,row = 1,pady=10)
v = tk.BooleanVar()
v.set(1)

ttk.Label(tab1, 
      text="To Move:",
      justify = tk.LEFT).grid(row=2, column=0)
ttk.Radiobutton(tab1, 
            text="White",
            # indicatoron = 0,
            # padx = 20, 
            variable=v, 
            value=True).grid(row=3, column=0)
ttk.Radiobutton(tab1, 
            text="Black",
            # indicatoron = 0,
            # padx = 20, 
            variable=v, 
            value=False).grid(row=3, column=1)


strength = tk.IntVar()
slider_str = tk.Scale(tab1, from_= 0, to=2000,tickinterval=500, 
                    orient=tk.HORIZONTAL,sliderlength=10,length=250,
                    resolution=10,label="Time to think/strength [ms]",variable=strength)
slider_str.set(100)

slider_str.grid(column = 0,row = 5,padx=10, pady=10,columnspan=2)
variance = tk.IntVar()
slider_var = tk.Scale(tab1, from_= 0, to=6000,tickinterval=500, 
                    orient=tk.HORIZONTAL,sliderlength=10,length=250,
                    resolution=10,label="Maximum move delay variance [ms]",variable=variance)
slider_var.set(50)

slider_var.grid(column = 0,row = 6,padx=10, pady=10,columnspan=2)
logs_text = tk.Text(tab1,width=45,height=15,background='gray')
logs_text.grid(column = 0,row = 7,padx=10, pady=10,columnspan=2)
gui_image=np.zeros((600,200), dtype=int)
img = ImageTk.PhotoImage(Image.fromarray(np.uint8(gui_image)))
imglabel = tk.Label(tab1, image=img).grid(row=2, column=2,rowspan = 100) 





tab2.grid_columnconfigure(0, weight=1)
tab2.grid_columnconfigure(1, weight=1)
# tab2.grid_rowconfigure(0, weight=1)
button_start2 = ttk.Button(tab2,text="Start playing", command =puzzel_rush)
button_start2.grid(column=0,row = 0,pady=10)

button_enter_move2=ttk.Button(tab2,text="Missed Move",command=new_move)
button_enter_move2.grid(column=1,row = 0,pady=10)
# v2 = tk.BooleanVar()
# v2.set(1)
#
# ttk.Label(tab2,
#       text="To Move:",
#       justify = tk.LEFT).grid(row=2, column=0)
# ttk.Radiobutton(tab2,
#             text="White",
#             # indicatoron = 0,
#             # padx = 20,
#             variable=v2,
#             value=True).grid(row=3, column=0)
# ttk.Radiobutton(tab2,
#             text="Black",
#             # indicatoron = 0,
#             # padx = 20,
#             variable=v2,
#             value=False).grid(row=3, column=1)


strength2 = tk.IntVar()
slider_str2 = tk.Scale(tab2, from_= 0, to=2000,tickinterval=500,
                    orient=tk.HORIZONTAL,sliderlength=10,length=250,
                    resolution=10,label="Time to think [ms]",variable=strength2)
slider_str2.set(300)

slider_str2.grid(column = 0,row = 5,padx=10, pady=10,columnspan=3)
variance2 = tk.IntVar()
slider_var2 = tk.Scale(tab2, from_= 0, to=6000,tickinterval=500,
                    orient=tk.HORIZONTAL,sliderlength=10,length=250,
                    resolution=10,label="Maximum move delay variance [ms]",variable=variance2)
slider_var2.set(5000)

slider_var2.grid(column = 0,row = 6,padx=10, pady=10,columnspan=3)
# logs_text2 = tk.Text(tab2,width=45,height=15,background='gray')
# logs_text2.grid(column = 0,row = 7,padx=10, pady=10,columnspan=2)
gui_image2=np.zeros((400,200), dtype=int)
img2 = ImageTk.PhotoImage(Image.fromarray(np.uint8(gui_image2)))
imglabel2 = tk.Label(tab2, image=img2).grid(row=7, column=0,columnspan=2)



running = True
while True:
    time.sleep(0.01)
    window.update_idletasks()
    window.update()
    if keep_going == True:
        start_playing()
#window.mainloop()
