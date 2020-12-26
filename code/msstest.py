from mss import mss
with mss() as sct:
        monitor = {'top': y1+1, 'left': x1+1, 'width': x2-x1-2 , 'height': (y2-y1)}
        img = np.array(sct.grab(monitor))
