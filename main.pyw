import tkinter as tk
import tkinter.colorchooser as tkcol
import pygame as pg
import math
import os
import easygui
running = True
def done():
    global running
    running = False
def loadimage():
    global drawing
    draw = easygui.fileopenbox('Load image')
    print(draw.__repr__())
    drawing = pg.image.load(draw.encode())
def saveimage():
    global drawing
    draw = easygui.filesavebox('Save image as...')
    print(draw.__repr__())
    pg.image.save(drawing, draw.encode())
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", done)
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=lambda:saveimage(), accelerator="Ctrl+S")
filemenu.add_command(label="Open", command=lambda:loadimage(), accelerator="Ctrl+O")
filemenu.add_command(label="Exit", command=lambda:done(), accelerator="Esc")
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
root.resizable(False, False)
fullFrame = tk.Frame(root, width=784, height=496)
subFrame1outer = tk.Frame(fullFrame, width=128, height=496, bd=4, relief=tk.RIDGE)
subFrame1 = tk.Frame(subFrame1outer, width=128, height=496)
subFrame2 = tk.Frame(fullFrame, width=656, height=496)
embed = tk.Frame(subFrame2, width=640, height=480)
hscroll = tk.Scrollbar(subFrame2, orient=tk.HORIZONTAL, width=16)
vscroll = tk.Scrollbar(subFrame2, orient=tk.VERTICAL, width=16)
hscroll.pack(side = tk.BOTTOM, fill = tk.X)
vscroll.pack(side = tk.RIGHT, fill = tk.Y)
embed.pack(fill = tk.BOTH)
toolslabel  = tk.LabelFrame(subFrame1, text='Tools', width=128, height=64)
tool = tk.IntVar()
brushimage  = tk.PhotoImage(file=r'pics\brush.png')
brush  = tk.Radiobutton(toolslabel, bd=1, width=16, height=16, image= brushimage, variable=tool, value=0, indicatoron=False)
brush.grid(row=0,column=0)
layerslabel = tk.LabelFrame(subFrame1, text='Layers', width=128, height=64)
toolslabel.pack(fill=tk.BOTH, expand=tk.YES)
layerslabel.pack(fill=tk.BOTH, expand=tk.YES)
subFrame1.pack(fill = tk.BOTH, padx=16, pady=8)
subFrame1outer.pack(side = tk.LEFT, fill = tk.BOTH)
subFrame2.pack(side = tk.RIGHT, fill = tk.BOTH)
fullFrame.pack()
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
root.update()
pg.init()
pg.mixer.quit()
clock = pg.time.Clock()
window = pg.display.set_mode((640, 480), pg.DOUBLEBUF)
window.set_alpha(None)
window.fill((0,0,0))
drawing = pg.Surface((640, 480), pg.SRCALPHA)
window.set_alpha(0)
drawing.fill((255,255,255,0))
events = pg.event.get()
mouse_pos = pg.mouse.get_pos()
smooth_pos = mouse_pos
smooth_pos_lag = mouse_pos
smooth_size = 0
clicks = pg.mouse.get_pressed()
keys = pg.key.get_pressed()
keysold = keys
color = (0,0,0)
def changecol():
    global color
    tmp = tkcol.askcolor()[0]
    if tmp==None:
        return tmp
    color = (int(tmp[0]), int(tmp[1]), int(tmp[2]))
HOTKEYS = []
ACTIVE = []
def inside(keycomb, keys):
    return any([keys[i]==False for i in keycomb])==False
def hotkey(keycomb, func):
    HOTKEYS.append(
        (lambda keys: func() if (inside(keycomb, keys)) else None)
    )
def xor(a, b):
    return (a and not b)
hotkey([pg.K_LCTRL, pg.K_s], lambda:saveimage())
hotkey([pg.K_RCTRL, pg.K_s], lambda:saveimage())
hotkey([pg.K_LCTRL, pg.K_o], lambda:loadimage())
hotkey([pg.K_RCTRL, pg.K_o], lambda:loadimage())
hotkey([pg.K_ESCAPE], lambda:done())
hotkey([pg.K_LCTRL, pg.K_p], lambda:changecol())
hotkey([pg.K_RCTRL, pg.K_p], lambda:changecol())
trans = pg.image.load('pics\\transparent.png')
while running:
    clock.tick(60)
    dt = clock.get_time()*0.06
    events = pg.event.get()
    keys = pg.key.get_pressed()
    keystmp = [xor(keys[i],keysold[i]) for i in range(len(keys))]
    keysold = pg.key.get_pressed()
    keystmp[pg.K_RSHIFT] = keys[pg.K_RSHIFT]
    keystmp[pg.K_LSHIFT] = keys[pg.K_LSHIFT]
    keystmp[pg.K_RCTRL] = keys[pg.K_RCTRL]
    keystmp[pg.K_LCTRL] = keys[pg.K_LCTRL]
    keystmp[pg.K_RALT] = keys[pg.K_RALT]
    keystmp[pg.K_LALT] = keys[pg.K_LALT]
    keystmp[pg.K_RMETA] = keys[pg.K_RMETA]
    keystmp[pg.K_LMETA] = keys[pg.K_LMETA]
    keystmp[pg.K_RSUPER] = keys[pg.K_RSUPER]
    keystmp[pg.K_LSUPER] = keys[pg.K_LSUPER]
    keystmp[pg.K_TAB] = keys[pg.K_TAB]
    [hotkey(keystmp) for hotkey in HOTKEYS]
    mouse_pos = pg.mouse.get_pos()
    clicks = pg.mouse.get_pressed()
    smooth_pos_lag = smooth_pos
    smooth_pos = (smooth_pos[0]+(mouse_pos[0]-smooth_pos[0])/5, smooth_pos[1]+(mouse_pos[1]-smooth_pos[1])/5)
    smooth_size = math.sqrt(((mouse_pos[0]-smooth_pos[0])**2)+((mouse_pos[1]-smooth_pos[1])**2))
    smooth_size = int(smooth_size / 7 + 5)
    smooth_pos = (int(smooth_pos[0]), int(smooth_pos[1]))
    window.blit(trans, (0,0))
    if clicks[0]:
        pg.draw.line(drawing, color, smooth_pos_lag, smooth_pos, smooth_size)
        pg.draw.circle(drawing, color, smooth_pos_lag, int(smooth_size/2))
        pg.draw.circle(drawing, color, smooth_pos, int(smooth_size/2))
    window.blit(drawing, (0,0))
    pg.display.update()
    root.update_idletasks()
    root.update()
root.destroy()
pg.quit()
