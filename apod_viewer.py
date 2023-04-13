from tkinter import ttk
from tkinter import *
import inspect
import os
import apod_desktop
import image_lib
import apod_api
import ctypes
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime
import sqlite3


# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
root = Tk()
root.geometry('600x400')
root.title("NASA APOD Viewer")

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.NASAAPODViewer')
icon_path = os.path.join(script_dir, 'nasa_logo.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frm_top = ttk.Frame(root)
frm_top.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky=NSEW)


frm_btm_left = ttk.LabelFrame(root, text='View Cached Image')
frm_btm_left.grid(row=1, column=0, sticky=NSEW)


frm_btm_right = ttk.LabelFrame(root, text='Get MMore')
frm_btm_right.grid(row=1, column=1, sticky=NSEW)


lbl_image = ttk.LabelFrame(frm_btm_left, text='View Cached Image')
lbl_image.grid(row=1, column=0)

lbl_cal = ttk.LabelFrame(frm_btm_right, text='Get More Images')
lbl_cal.grid(row=1, column=1)


img_nasa = PhotoImage(file=os.path.join(script_dir, 'logo.png'))
lbl_nasa = ttk.Label(frm_top, image=img_nasa)
lbl_nasa.grid(row=0, column=0, sticky=NSEW)



lbl_title = ttk.Label(frm_btm_left, text='Select image')
lbl_title.grid(row=1, column=1, padx=10, pady=10)

desktop_names_list = apod_desktop.get_all_apod_titles()
nasa_names = ttk.Combobox(frm_btm_left, values=desktop_names_list, width=50, state='readonly')
nasa_names.set("Select an image")
nasa_names.grid(row=1, column=2, padx=10, pady=10)

def handle_img_sel(event):
    global image_path
    user_pick = nasa_names.get()
    image_db = apod_desktop.image_cache_db
    con = sqlite3.connect(image_db)
    cur = con.cursor()
    title_query = f"""
    SELECT explanation, path FROM image_cache
    WHERE title='{user_pick}'
    """
    cur.execute(title_query)
    query_result = cur.fetchone()
    con.close()
 
    image_path = query_result[1]
    explanation = query_result[0]
    
    if image_path is not None:
        img_nasa['file'] = image_path
        btn_down.state(['!disabled'])



nasa_names.bind('<<ComboboxSelected>>', handle_img_sel)


lbl_cal = ttk.Label(frm_btm_right, text='Select Date')
lbl_cal.grid(row=1, column=1, padx=10, pady=10)




today = date.today()
lower = date(1995, 6, 16)
calen = DateEntry(frm_btm_right, maxdate=today, mindate=lower)
calen.grid(row=1, column=2, padx=10, pady=10)


def handle_date_sel():

    date_sel = calen.get_date()
    format_date = date_sel.strftime('%Y-%m-%d')
    info = apod_desktop.add_apod_to_cache(format_date)
    apod_dict = apod_desktop.get_apod_info(info)
    

def image_change():
    global image_path
    image_lib.set_desktop_background_image(image_path)




btn_date = ttk.Button(frm_btm_right, text='Download image',command=handle_date_sel)
btn_date.grid(row=1, column=3, padx=10, pady=10)




btn_down = ttk.Button(frm_btm_left, text='Set as Desktop',command=image_change, state=DISABLED)
btn_down.grid(row=1, column=3, padx=10, pady=10)


root.mainloop()