#!/usr/bin/env python3
# import numpy as np
import pandas as pd

def convertattendance(filepath, output): # this function makes the data pretty :3
	attendance = pd.read_csv(filepath)
	attendance = attendance.sort_values(["Student summary", "Course"])
	# attendance = attendance.groupby(["Course", "Student summary"], group_keys=False).apply(lambda x: x)
	# attendance["Attendance date"] = attendance["Attendance date"].dt.strftime('%m/%d/%Y')
	attendance = attendance[["Student summary", "Attendance date", "Course", "Reason"]]
	attendance.to_csv(output, "	", index=False, date_format="%d/%m/%Y")

convertattendance("attendance.csv", "processed.csv")
