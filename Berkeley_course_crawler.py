# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 13:12:23 2021

@author: USER
"""

import requests
from datetime import datetime, timedelta
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
from IPython.display import display, HTML
import calendar

class course_info():
    def __init__(self, url_list):
        
        # if the input is not a list, convert it to list
        if type(url_list) is not list:
            url_list = [url_list]
        
        self.information = pd.DataFrame(columns=["Course_No.","Serial_NO.","Course_Name","Location",
                                                 "Start_Time(SF_time)","End_Time(SF_time)","Start_Time(TW_time)",
                                                 "End_Time(TW_time)","Level","Type","Mode","Instructor(s)",
                                                 "Units","Total_Capacity","Total_Enrolled",
                                                 "Final_Examination","Description"])
        for url in url_list:
            self.course_extract(url)
            time.sleep(0.8);
    
    # Method 1: 
    def course_extract(self, url):
        
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            query = soup.find("div", class_="handlebarData theme_is_whitehot").attrs
            js_str = query["data-json"]
            js_dict = json.loads(js_str)
            course_num = js_dict["displayName"]
            serial_num = js_dict["id"]
            name = js_dict["course"]["title"]
            location = js_dict["meetings"][0]["location"]["description"]
            level = js_dict["course"]["academicCareer"]["description"]
            lecture = js_dict["component"]["description"]
            capacity = js_dict["enrollmentStatus"]["maxEnroll"]
            enrolled = js_dict["enrollmentStatus"]["enrolledCount"]
            
            try:
                special_title = js_dict["attributes"]["NOTE"]["special-title"]["value"]["formalDescription"]
                name = name + " : " + special_title
            except KeyError:
                name = name
        
            try:
                mode = js_dict["attributes"]["WEB"][0]["value"]["formalDescription"]
            except KeyError:
                mode = "Pending Reviews"
                
            try:
                instructor = js_dict["meetings"][0]["assignedInstructors"]
                instructors = ', '.join([str(i["instructor"]["names"][1]["formattedName"]) for i in instructor])
            except KeyError:
                instructors = "None"
            
            try:
                units = js_dict["course"]["credit"]["value"]["fixed"]["units"]
            except KeyError:
                units = ' to '.join([str(js_dict["course"]["credit"]["value"]["range"]["minUnits"]), str(js_dict["course"]["credit"]["value"]["range"]["maxUnits"])])
                
            # date process
            fake_date = []
            if js_dict["meetings"][0]["meetsMonday"]:
                fake_date.append(datetime(2020,7,6).date())
            if js_dict["meetings"][0]["meetsTuesday"]:
                fake_date.append(datetime(2020,7,7).date())
            if js_dict["meetings"][0]["meetsWednesday"]:
                fake_date.append(datetime(2020,7,8).date())
            if js_dict["meetings"][0]["meetsThursday"]:
                fake_date.append(datetime(2020,7,9).date())
            if js_dict["meetings"][0]["meetsFriday"]:
                fake_date.append(datetime(2020,7,10).date())
            fake_starttime = datetime.strptime(js_dict["meetings"][0]["startTime"], '%H:%M:%S').time()
            fake_endtime = datetime.strptime(js_dict["meetings"][0]["endTime"], '%H:%M:%S').time()
            fake_start_dt = [datetime.combine(i, fake_starttime) for i in fake_date]
            fake_end_dt = [datetime.combine(i, fake_endtime) for i in fake_date]
            
            sf_start_dt = " / ".join([str(i.strftime("%a %H:%M")) for i in fake_start_dt])
            sf_end_dt = " / ".join([str(i.strftime("%a %H:%M")) for i in fake_end_dt])
            
            tw_start_dt = " / ".join([str((i + timedelta(hours=15)).strftime("%a %H:%M")) for i in fake_start_dt])
            tw_end_dt = " / ".join([str((i + timedelta(hours=15)).strftime("%a %H:%M")) for i in fake_end_dt])
            
            description = js_dict["course"]["description"]
            final = js_dict["course"]["finalExam"]["description"]
            
            self.information = self.information.append({
                    "Course_No." : course_num,
                    "Serial_NO." : serial_num,
                    "Course_Name" : name,
                    "Location" : location,
                    "Start_Time(SF_time)" : sf_start_dt,
                    "End_Time(SF_time)" : sf_end_dt,
                    "Start_Time(TW_time)" : tw_start_dt,
                    "End_Time(TW_time)" : tw_end_dt,
                    "Level" : level,
                    "Type" : lecture,
                    "Mode" : mode,
                    "Instructor(s)" : instructors,
                    "Units" : units,
                    "Total_Capacity" : capacity,
                    "Total_Enrolled" : enrolled,
                    "Final_Examination" : final,
                    "Description" : description}, ignore_index=True, sort=False)
    # method 2:
    def weekly_schedule(self, time_zone="SF"):
        info = self.information
        # define time zone
        if time_zone == "SF":
            start_col = "Start_Time(SF_time)"
            end_col = "End_Time(SF_time)"
        
        elif time_zone == "TW":
            start_col = "Start_Time(TW_time)"
            end_col = "End_Time(TW_time)"
        
        else:
            print('Error: time_zone must be "SF" or "TW".')
            return 

        schedule = pd.DataFrame({
                "Monday": "",
                "Tuesday": "",
                "Wednesday": "",
                "Thursday": "",
                "Friday": "",
                "Saturday": ""},
                index = pd.date_range("00:00", "23:30", freq="30min").time)
        
        for i in range(0, info.shape[0]):

            str_time = info.loc[i, start_col].split(" / ")
            end_time = info.loc[i, end_col].split(" / ")
            course_name = info.loc[i, "Course_Name"]
            for t in range(0, len(str_time)):
                str_formatted = datetime(*time.strptime(str_time[t], "%a %H:%M")[:7])
                end_formatted = datetime(*time.strptime(end_time[t], "%a %H:%M")[:7])
                DoW = calendar.day_name[time.strptime(str_time[t], "%a %H:%M")[6]]
                str_point = str_formatted.strftime("%H:%M")
                end_point = end_formatted.strftime("%H:%M")
                period = pd.date_range(str_point, end_point, freq="30min").time
                schedule.loc[period, DoW] = schedule.loc[period, DoW] + " \n " + course_name
        return schedule


url_list = []
while True:
    multi = "yes"
    url = str(input("Please enter the link of course:"))
    multi = input("Do you wanna add more courses?[yes/no]:")
    url_list.append(url)
    if multi == 'no':
        result = course_info(url_list)
        print(result.information)
        save_info = input("Do you wanna save the info of selected courses to excel?[yes/no]:")
        if save_info == 'yes':
            result.information.to_excel('Documents/course_info.xlsx', na_rep=False)
            print("Your result have been stored to Document of your PC, Please check on the directory.")
        schdl = input("Do you wanna schedule these selected courses?[yes/no]:")
        if save_info == 'yes':
            schedule = result.weekly_schedule(time_zone="SF")
            print(schedule)
            save_schdl = input("Do you wanna save the schedule of selected courses to excel?[yes/no]:")
            if save_schdl == 'yes':
                schedule.to_excel('Documents/course_schedule.xlsx', na_rep=False)
        break
input("Press enter to exit")

