#!/usr/bin/env python3
# import numpy as np
import pandas as pd

def convertattendance(attendance, output): # this function makes the data pretty :3
	attendance = pd.read_csv(filepath)
	attendance = attendance.sort_values(by=["Student summary"])
	attendance = attendance.groupby("Student summary", group_keys=False).apply(lambda x: x)
	attendance = attendance[["Student summary", "Attendance date", "Course", "Reason"]]
	attendance.to_csv(output, "	", index=False, date_format="%d/%m/%Y")
