import pyautogui as pygui
import pyperclip
import time
import chessboard_detection
import game_state_classes
import ml_model
secondsWaitNewGame = 60
refreshX = 95
refreshY = 119
findmatchX = 1249
findmatchY = 755
findmatchY2 = 916
linkX = 690
linkY = 118
copyX = 755
copyY = 209
randomX = 1761
randomY = 713
def refreshBrowser():
	time.sleep(5)
	#launchNewGameSearch()
	pygui.click(refreshX, refreshY)
	time.sleep(10)

def launchNewGameSearch():
	time.sleep(1)
	# pygui.click(findmatchX, findmatchY)
	pygui.click(findmatchX, findmatchY2)
	time.sleep(0.1)
	
def checkNewGameFound(previouslink):
	print("checking new game found")
	start = time.time()
	newlink = previouslink
	while newlink == previouslink and (time.time() - start) < 60:
		newlink = getLink()
	if (time.time() - start) > secondsWaitNewGame:
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





