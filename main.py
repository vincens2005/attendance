#!/usr/bin/env python3
import numpy as np
import pandas as pd

attendance = pd.read_csv("attendance.csv")
attendance = attendance.sort_values(by=["Student summary"])
attendance = attendance.groupby("Student summary", group_keys=False).apply(lambda x: x)
attendance = attendance[["Student summary", "Attendance date", "Course", "Reason"]]
attendance.to_csv("processed.csv", "	", index=False, date_format="%d/%m/%Y")
