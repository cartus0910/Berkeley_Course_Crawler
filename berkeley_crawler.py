# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 23:32:27 2020

@author: USER
"""
import requests
from datetime import datetime, timedelta
import json
import pandas as pd
from bs4 import BeautifulSoup

def course_extract(url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    query = soup.find("div", class_="handlebarData theme_is_whitehot").attrs
    js_str = query["data-json"]
    js_dict = json.loads(js_str)
    course_num = js_dict["displayName"]
    serial_num = js_dict["id"]
    name = js_dict["course"]["title"]
    level = js_dict["course"]["academicCareer"]["description"]
    lecture = js_dict["component"]["description"]
    
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
    
    information = pd.DataFrame({
            "Course_No." : course_num,
            "Serial_NO." : serial_num,
            "Course_Name" : name,
            "Level" : level,
            "Type" : lecture,
            "Mode" : mode,
            "Instructor(s)" : instructors,
            "Units" : units,
            "Start_Time(SF_time)" : sf_start_dt,
            "End_Time(SF_time)" : sf_end_dt,
            "Start_Time(TW_time)" : tw_start_dt,
            "End_Time(TW_time)" : tw_end_dt,
            "Final_Examination" : final,
            "Description" : description}, index=[0])
    
    return information

def multiple_extract(url_list):
    import pandas as pd
    information =  pd.DataFrame({
            "Course_No." : None,
            "Serial_NO." : None,
            "Course_Name" : None,
            "Level" : None,
            "Type" : None,
            "Mode" : None,
            "Instructor(s)" : None,
            "Units" : None,
            "Start_Time(SF_time)" : None,
            "End_Time(SF_time)" : None,
            "Start_Time(TW_time)" : None,
            "End_Time(TW_time)" : None,
            "Final_Examination" : None,
            "Description" : None}, index=[0])
    for i in url_list:
        info = course_extract(i)
        information = information.append(info, ignore_index=True)
    return information.iloc[1:]

url_list = []
while True:
    multi = "yes"
    url = str(input("Please enter the link of course:"))
    multi = input("Do you wanna search for more courses?[yes/no]:")
    url_list.append(url)
    if multi == 'no':
        result = multiple_extract(url_list)
        result.to_clipboard(excel=True,sep='\t')
        print("Your result have been stored to your clipboard. You can paste it onto excel/google sheet/database.")
        break
input("Press enter to exit")
    
