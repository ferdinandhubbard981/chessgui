import pyautogui as pygui
import pyperclip
import time
import chessboard_detection
import game_state_classes
import ml_model
refreshX = 103
refreshY = 65
findmatchX = 1516
findmatchY = 665
findmatchY2 = 911
linkX = 559
linkY = 68
copyX = 623
copyY = 135
randomX = 1813
randomY = 937
def refreshBrowser():
	time.sleep(5)
	#launchNewGameSearch()
	pygui.click(refreshX, refreshY)
	time.sleep(10)

def launchNewGameSearch():
	time.sleep(1)
	pygui.click(findmatchX, findmatchY)
	pygui.click(findmatchX, findmatchY2)
	time.sleep(0.1)
	
def checkNewGameFound(previouslink):
	start = time.time()
	newlink = previouslink
	while newlink == previouslink and (time.time() - start) < 60:
		newlink = getLink()
	if (time.time() - start) > 60:
		return False
	
	else:
		for i in range(100):
			print("Found")
		return True
	

def getLink():
	time.sleep(0.3)
	pygui.click(randomX, randomY)
	time.sleep(0.1)
	pygui.click(randomX, randomY)
	time.sleep(0.1)
	pygui.click(linkX, linkY, button='right')
	time.sleep(0.1)
	pygui.click(copyX, copyY)
	link = pyperclip.paste()
	return link
	
	
def checkColour():
	#ml_model.init_binary()
	#ml_model.init_class()
	game_state = game_state_classes.Game_state()
	found, game_state.board_position_on_screen = chessboard_detection.find_chessboard()
	side = game_state_classes.our_side(game_state)
	return side

def checkIfOpponentPlayed():
	#ml_model.init_binary()
	#ml_model.init_class()
	game_state = game_state_classes.Game_state()
	found, game_state.board_position_on_screen = chessboard_detection.find_chessboard()
	fen_str, vis_glob = game_state_classes.build_fen_check(game_state)
	#print(fen_str)
	#print(vis_glob)
	if fen_str == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1":
		return False
	else:
		return True #opponent has played





