#!/usr/bin/env python3
import os, sys, subprocess
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

def convertattendance(attendance):
	attendance = attendance.sort_values(["Student summary", "Course"])
	attendance["Attendance date"] = attendance["Attendance date"].dt.strftime('%m/%d/%Y')
	attendance = attendance[["Student summary", "Attendance date", "Course", "Reason"]]
	return attendance

a = None
o = None

root = tk.Tk()
root.title("Magic Attendance App")
root.resizable(True, True)
root.geometry("400x300")


input_buttontext = tk.StringVar()
input_file = tk.StringVar()

output_buttontext = tk.StringVar()
output_file = tk.StringVar()

should_open = tk.BooleanVar()


def open_file(filename):
	if sys.platform == "win32":
		os.startfile(filename)
	else:
		opener = "open" if sys.platform == "darwin" else "xdg-open"
		subprocess.call([opener, filename])

def maybe_enable_button():
	if a != None and o != None:
		gobutton["state"] = "enabled"

def pick_in():
	global a, input_file, input_buttontext, gobutton
	if a != None:
		a = None
		input_buttontext.set("Pick a File")
		input_file.set("Raw attendance data:")
		gobutton["state"] = "disabled"
		return
	# file type
	filetypes = (
		('CSV Files', '*.csv'),
		('Excel files', '*.xlsx')
	)

	# show the open file dialog
	f = fd.askopenfilename(filetypes=filetypes)
	a = f
	input_file.set("In: " + f)
	input_buttontext.set("Clear")
	maybe_enable_button()

def pick_out():
	global o, output_file, output_buttontext, gobutton
	if o != None:
		o = None
		output_buttontext.set("Pick a File")
		output_file.set("Output file:")
		gobutton["state"] = "disabled"
		return
	# file type
	filetypes = (
		('CSV Files', '*.csv'),
		('Excel files', '*.xlsx')
	)

	# show the open file dialog
	f = fd.asksaveasfilename(filetypes=filetypes)
	o = f
	output_file.set("Out: " + f)
	output_buttontext.set("Clear")
	maybe_enable_button()

def domagic():
	attendance = pd.DataFrame()
	if a.endswith(".xlsx"):
		attendance = pd.read_excel(a)
	else:
		attendance = pd.read_csv(a)

	attendance = convertattendance(attendance)
	if o.endswith(".xlsx"):
		attendance.to_excel(o, index=False, sheet_name="Attendance")
	else:
		attendance.to_csv(o, "	", index=False, date_format="%d/%m/%Y")

	if should_open.get():
		open_file(o)



inlabel = ttk.Label(root, textvariable=input_file)
inlabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

input_button = ttk.Button(root, textvariable=input_buttontext, command=pick_in)
input_button.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

input_file.set("Raw attendance data:")
input_buttontext.set("Pick a File")

outlabel = ttk.Label(root, textvariable=output_file)
outlabel.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

output_button = ttk.Button(root, textvariable=output_buttontext, command=pick_out)
output_button.grid(column=1, row=1, sticky=tk.W, padx=10, pady=10)

output_file.set("Output file:")
output_buttontext.set("Pick a File")

op = ttk.Checkbutton(root, text="Open on success", variable=should_open, onvalue=True, offvalue=False)
op.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)
should_open.set(True)

gobutton = ttk.Button(root, text="Do Magic!", command=domagic)
gobutton.grid(column=1, row=3, sticky="w", padx=10, pady=10)
gobutton["state"] = "disabled"

root.mainloop()
