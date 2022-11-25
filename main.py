#!/usr/bin/env python3
import os, sys, subprocess
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

def convertdate(frame):
	frame["Attendance date"] = pd.to_datetime(frame["Attendance date"])
	frame["Attendance date"] = frame["Attendance date"].dt.strftime('%m/%d/%Y')
	return frame


def convertattendance(attendance):
	attendance = attendance.sort_values(["Student summary", "Course"])
	attendance = convertdate(attendance)
	attendance = attendance[["Student summary", "Attendance date", "Course", "Reason"]]
	return attendance

def attendance_delta(old, new):
	return new.merge(old, indicator=True, how="outer").query("_merge=='left_only'").drop("_merge", axis=1)

def loadsheet(name):
	if name.endswith(".xlsx"):
		return pd.read_excel(name)
	return pd.read_csv(name)

def replace_last(s, old, new):
	reverse_removal = old[::-1]
	reverse_replacement = new[::-1]
	return s[::-1].replace(reverse_removal, reverse_replacement, 1)[::-1]


a = None
o = None
p = None

root = tk.Tk()
root.title("Magic Attendance App")
root.resizable(True, True)
root.geometry("400x300")


input_buttontext = tk.StringVar()
input_file = tk.StringVar()

output_buttontext = tk.StringVar()
output_file = tk.StringVar()

delta_buttontext = tk.StringVar()
delta_file = tk.StringVar()

should_open = tk.BooleanVar()
delta = tk.BooleanVar()


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
	input_file.set("In: " + f.split("/")[-1])
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
	output_file.set("Out: " + f.split("/")[-1])
	output_buttontext.set("Clear")
	maybe_enable_button()

def pick_delta():
	global p, delta_file, delta_buttontext
	if p != None:
		p = None
		delta_buttontext.set("Pick a File")
		delta_file.set("Previous report (optional):")
		return
	# file type
	filetypes = (
		('CSV Files', '*.csv'),
		('Excel files', '*.xlsx')
	)

	# show the open file dialog
	f = fd.askopenfilename(filetypes=filetypes)
	p = f
	delta_file.set("Previous: " + f.split("/")[-1])
	delta_buttontext.set("Clear")
	maybe_enable_button()


def domagic():
	attendance = loadsheet(a)
	attendance = convertattendance(attendance)

	previous = pd.DataFrame()
	if p != None:
		previous = loadsheet(p)

	adelta = pd.DataFrame()

	if not previous.empty:
		previous = convertdate(previous)
		adelta = attendance_delta(previous, attendance)
	delta_file = replace_last(o, ".", "_delta.")

	if o.endswith(".xlsx"):
		attendance.to_excel(o, index=False, sheet_name="Attendance")
		if not adelta.empty:
			adelta.to_excel(delta_file, index=False, sheet_name="Attendance Delta")
	else:
		attendance.to_csv(o, "	", index=False, date_format="%d/%m/%Y")
		if not adelta.empty:
			adelta.to_csv(delta_file, "	", index=False, date_format="%d/%m/%Y")

	if should_open.get():
		open_file(o)
		if not adelta.empty:
			open_file(delta_file)



inlabel = ttk.Label(root, textvariable=input_file)
inlabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

input_button = ttk.Button(root, textvariable=input_buttontext, command=pick_in)
input_button.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

input_file.set("Raw attendance data:")
input_buttontext.set("Pick a File")

deltalabel = ttk.Label(root, textvariable=delta_file)
deltalabel.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

delta_button = ttk.Button(root, textvariable=delta_buttontext, command=pick_delta)
delta_button.grid(column=1, row=1, sticky=tk.W, padx=10, pady=10)

delta_file.set("Previous report (optional):")
delta_buttontext.set("Pick a File")

outlabel = ttk.Label(root, textvariable=output_file)
outlabel.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

output_button = ttk.Button(root, textvariable=output_buttontext, command=pick_out)
output_button.grid(column=1, row=2, sticky=tk.W, padx=10, pady=10)

output_file.set("Output file:")
output_buttontext.set("Pick a File")

op = ttk.Checkbutton(root, text="Open on success", variable=should_open, onvalue=True, offvalue=False)
op.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)
should_open.set(True)

gobutton = ttk.Button(root, text="Do Magic!", command=domagic)
gobutton.grid(column=1, row=4, sticky="w", padx=10, pady=10)
gobutton["state"] = "disabled"

root.mainloop()
