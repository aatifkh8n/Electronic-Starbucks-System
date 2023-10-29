import random
import string

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def order_now():
    print("ordered successful")

def generate_random_string(lenght=None):
    if lenght:
        rand = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=lenght))
    else:
        rand = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits))
    return rand