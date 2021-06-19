@@ -2,15 +2,218 @@

This crawler helps you extract more detailed information from Berkeley Course webpage. Follow the steps below, and have your excel/google sheet/database prepared. You can organize your short list of courses.


```python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 23:32:27 2020

@author: You, Bo-Xiang
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
        display(HTML(schedule.to_html().replace("\\n","<br>")))
        return schedule
```


```python
%%HTML
<style type="text/css">
table.dataframe td, table.dataframe th {
    border: 1px  black solid !important;
  color: black !important;
}
</style>
```


<style type="text/css">
table.dataframe td, table.dataframe th {
    border: 1px  black solid !important;
  color: black !important;
}
</style>



## Demonstration

### 1. Export information of course of your interest


```python
# Example for one Course: 
result = course_extract("https://classes.berkeley.edu/content/2020-fall-data-c102-001-lec-001") # put the link between ""
result
# Example for three selected Course: 
url_list = ["https://classes.berkeley.edu/content/2020-spring-geog-149b-001-lec-001",
       "https://classes.berkeley.edu/content/2020-spring-geog-167ac-001-lec-001",
       "https://classes.berkeley.edu/content/2020-spring-geog-200b-001-sem-001"]
    
result = course_info(url_list)
info = result.information
info.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
@ -18,36 +221,82 @@ result
      <th>Course_No.</th>
      <th>Serial_NO.</th>
      <th>Course_Name</th>
      <th>Location</th>
      <th>Start_Time(SF_time)</th>
      <th>End_Time(SF_time)</th>
      <th>Start_Time(TW_time)</th>
      <th>End_Time(TW_time)</th>
      <th>Level</th>
      <th>Type</th>
      <th>Mode</th>
      <th>Instructor(s)</th>
      <th>Units</th>
      <th>Start_Time(SF_time)</th>
      <th>End_Time(SF_time)</th>
      <th>Start_Time(TW_time)</th>
      <th>End_Time(TW_time)</th>
      <th>Total_Capacity</th>
      <th>Total_Enrolled</th>
      <th>Final_Examination</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>2020 Fall DATA C102 001 LEC 001</td>
      <td>33319</td>
      <td>Data, Inference, and Decisions</td>
      <th>0</th>
      <td>2020 Spring GEOG 149B 001 LEC 001</td>
      <td>31059</td>
      <td>Climate Impacts and Risk Analysis</td>
      <td>McCone 145</td>
      <td>Mon 11:00 / Wed 11:00</td>
      <td>Mon 12:30 / Wed 12:30</td>
      <td>Tue 02:00 / Thu 02:00</td>
      <td>Tue 03:30 / Thu 03:30</td>
      <td>Undergraduate</td>
      <td>Lecture</td>
      <td>Pending Reviews</td>
      <td>Norman L Miller</td>
      <td>3</td>
      <td>50</td>
      <td>39</td>
      <td>Alternative method of final assessment</td>
      <td>Climate impacts and risk analysis is the study...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020 Spring GEOG 167AC 001 LEC 001</td>
      <td>30924</td>
      <td>Border Geographies, Migration and Decolonial M...</td>
      <td>Genetics &amp; Plant Bio 100</td>
      <td>Tue 12:30 / Thu 12:30</td>
      <td>Tue 13:59 / Thu 13:59</td>
      <td>Wed 03:30 / Fri 03:30</td>
      <td>Wed 04:59 / Fri 04:59</td>
      <td>Undergraduate</td>
      <td>Lecture</td>
      <td>Pending Reviews</td>
      <td>Michael  Jordan, Jacob Noah  Steinhardt</td>
      <td>Diana M Negrin</td>
      <td>4</td>
      <td>Tue 14:00 / Thu 14:00</td>
      <td>Tue 15:29 / Thu 15:29</td>
      <td>Wed 05:00 / Fri 05:00</td>
      <td>Wed 06:29 / Fri 06:29</td>
      <td>Written final exam conducted during the schedu...</td>
      <td>This course develops the probabilistic foundat...</td>
      <td>200</td>
      <td>66</td>
      <td>Alternative method of final assessment</td>
      <td>This course examines how today’s bounded geogr...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2020 Spring GEOG 200B 001 SEM 001</td>
      <td>19853</td>
      <td>Contemporary Geographic Thought 2 (Geographica...</td>
      <td>McCone 509</td>
      <td>Wed 09:00</td>
      <td>Wed 12:00</td>
      <td>Thu 00:00</td>
      <td>Thu 03:00</td>
      <td>Graduate</td>
      <td>Seminar</td>
      <td>Pending Reviews</td>
      <td>Sharad  Chari</td>
      <td>5</td>
      <td>14</td>
      <td>6</td>
      <td>No final exam</td>
      <td>'Geographical Difference/Differentiation' is a...</td>
    </tr>
  </tbody>
</table>
@ -58,120 +307,536 @@ result

```python
# copy the result and paste it on your excel/Google Sheet/Database
result.to_clipboard(excel=True,sep='\t')
info.to_clipboard(excel=True,sep='\t')
```


```python
# or save file as .xlsx directly
multiple_results.to_excel('course_info.xlsx', na_rep=False)
```

### 2. If you wanna export a schedule of all selected courses


```python
# Example for multiple Courses:
# 1. Put all your desired course link into the list, separate them by ","
url_list = ["https://classes.berkeley.edu/content/2020-fall-data-c102-001-lec-001", "https://classes.berkeley.edu/content/2020-fall-civeng-199-001-ind-001", "https://classes.berkeley.edu/content/2020-fall-indeng-290-004-lec-004"]
# 2. Extract them as table
multiple_results = multiple_extract(url_list)
multiple_results
schedule = result.weekly_schedule(time_zone="SF")
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Course_No.</th>
      <th>Serial_NO.</th>
      <th>Course_Name</th>
      <th>Level</th>
      <th>Type</th>
      <th>Mode</th>
      <th>Instructor(s)</th>
      <th>Units</th>
      <th>Start_Time(SF_time)</th>
      <th>End_Time(SF_time)</th>
      <th>Start_Time(TW_time)</th>
      <th>End_Time(TW_time)</th>
      <th>Final_Examination</th>
      <th>Description</th>
      <th>Monday</th>
      <th>Tuesday</th>
      <th>Wednesday</th>
      <th>Thursday</th>
      <th>Friday</th>
      <th>Saturday</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2020 Fall DATA C102 001 LEC 001</td>
      <td>33319</td>
      <td>Data, Inference, and Decisions</td>
      <td>Undergraduate</td>
      <td>Lecture</td>
      <td>Pending Reviews</td>
      <td>Michael  Jordan, Jacob Noah  Steinhardt</td>
      <td>4</td>
      <td>Tue 14:00 / Thu 14:00</td>
      <td>Tue 15:29 / Thu 15:29</td>
      <td>Wed 05:00 / Fri 05:00</td>
      <td>Wed 06:29 / Fri 06:29</td>
      <td>Written final exam conducted during the schedu...</td>
      <td>This course develops the probabilistic foundat...</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2020 Fall CIVENG 199 001 IND 001</td>
      <td>16638</td>
      <td>Supervised Independent Study</td>
      <td>Undergraduate</td>
      <td>Independent Study</td>
      <td>Pending Reviews</td>
      <td>Norman A Abrahamson</td>
      <td>1 to 4</td>
      <th>00:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>No final exam</td>
      <td>Supervised independent study.</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2020 Fall INDENG 290 004 LEC 004</td>
      <td>32956</td>
      <td>Special Topics in Industrial Engineering and O...</td>
      <td>Graduate</td>
      <td>Lecture</td>
      <td>Asynchronous Instruction</td>
      <td>Barna  Saha</td>
      <td>2 to 3</td>
      <td>Tue 14:00 / Thu 14:00</td>
      <td>Tue 15:29 / Thu 15:29</td>
      <td>Wed 05:00 / Fri 05:00</td>
      <td>Wed 06:29 / Fri 06:29</td>
      <td>Written final exam conducted during the schedu...</td>
      <td>Lectures and appropriate assignments on fundam...</td>
      <th>00:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>01:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>01:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>02:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>02:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>03:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>03:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>04:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>04:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>05:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>05:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>06:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>06:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>07:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>07:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>08:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>08:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>09:00:00</th>
      <td></td>
      <td></td>
      <td><br> Contemporary Geographic Thought 2 (Geographical Difference and Differentiation)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>09:30:00</th>
      <td></td>
      <td></td>
      <td><br> Contemporary Geographic Thought 2 (Geographical Difference and Differentiation)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>10:00:00</th>
      <td></td>
      <td></td>
      <td><br> Contemporary Geographic Thought 2 (Geographical Difference and Differentiation)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>10:30:00</th>
      <td></td>
      <td></td>
      <td><br> Contemporary Geographic Thought 2 (Geographical Difference and Differentiation)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>11:00:00</th>
      <td><br> Climate Impacts and Risk Analysis</td>
      <td></td>
      <td><br> Climate Impacts and Risk Analysis <br> Contemporary Geographic Thought 2 (Geographical Difference and Differentiation)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>11:30:00</th>
      <td><br> Climate Impacts and Risk Analysis</td>
      <td></td>
      <td><br> Climate Impacts and Risk Analysis <br> Contemporary Geographic Thought 2 (Geographical Difference and Differentiation)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>12:00:00</th>
      <td><br> Climate Impacts and Risk Analysis</td>
      <td></td>
      <td><br> Climate Impacts and Risk Analysis <br> Contemporary Geographic Thought 2 (Geographical Difference and Differentiation)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>12:30:00</th>
      <td><br> Climate Impacts and Risk Analysis</td>
      <td><br> Border Geographies, Migration and Decolonial Movements of Latin America</td>
      <td><br> Climate Impacts and Risk Analysis</td>
      <td><br> Border Geographies, Migration and Decolonial Movements of Latin America</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>13:00:00</th>
      <td></td>
      <td><br> Border Geographies, Migration and Decolonial Movements of Latin America</td>
      <td></td>
      <td><br> Border Geographies, Migration and Decolonial Movements of Latin America</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>13:30:00</th>
      <td></td>
      <td><br> Border Geographies, Migration and Decolonial Movements of Latin America</td>
      <td></td>
      <td><br> Border Geographies, Migration and Decolonial Movements of Latin America</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>14:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>14:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>15:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>15:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>16:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>16:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>17:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>17:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>18:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>18:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>19:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>19:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>20:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>20:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>21:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>21:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>22:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>22:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>23:00:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>23:30:00</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>



```python
# copy the schedule and paste it on your excel/Google Sheet/Database
schedule.to_clipboard(excel=True, sep='\t')
```


```python
# 3. use this action to copy the result and paste it on your excel/Google Sheet/Database
multiple_results.to_clipboard(excel=True,sep='\t')
# or save file as .xlsx directly
schedule.to_excel('course_schedule.xlsx', na_rep=False)
```

## Search for the courses that interest you


```python
# NOW, Try it on your own for one link!
result = course_extract("") # insert link
result.to_clipboard(excel=True,sep='\t') # copy the result, so you can paste it elsewhere
#check the result
result
# NOW, Try it on your own with course of your interest!
url_list = ["",
            "",
            "",
            "",
            ""] # insert links, you can add as more links as you want
result = course_info(url_list)
info = result.information
info.head()
# copy the result and paste it on your excel/Google Sheet/Database
info.to_clipboard(excel=True,sep='\t')

```


```python
# NOW, Try it on your own for multiple link!
url_list = ["", "", ""] # insert links, you can add as more links as you want
multiple_results = multiple_extract(url_list)
multiple_results.to_clipboard(excel=True,sep='\t') # copy the result, so you can paste it elsewhere
#check the result
multiple_results
```
***

## For non-python environmnet

You can just process through online environment here.
<iframe height="400px" width="100%" src="https://replit.com/@cartus0910/Berkeley-Course-Crawler?lite=true" scrolling="no" frameborder="no" allowtransparency="true" allowfullscreen="true" sandbox="allow-forms allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-modals">
</iframe>

Take this course for example, you can copy the link of whatever course you want:
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/webpage.png)

1. Click the "run" button directly.
*  Note: it may takes a few minutes do download all the required packages.
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/step1.png)

2. If all the packages have been downloaded. The right side will show an instruction that asks you to enter a link of course.
*  Note: ctrl+v may not work in the section, please right click and paste the link instead.
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/step2.png)

3. Follow the instruction, if you have more courses to add, type in "yes".
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/step3.png)

4. Once you are done with all desired courses, just type in "no".
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/step4.png)

5. If you wanna export the result as excel(.xlsx) file, type in  "yes". Otherwise, type in "no".
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/step5.png)

6. If you wanna organize your selected courses in a weely schedule, please enter "yes". Otherwise, type in "no".
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/step6.png)

7. If you wanna  wanna export the result as excel(.xlsx) file, type in  "yes". Otherwise, type in "no".
![image](https://github.com/cartus0910/Berkeley_Course_Crawler/blob/master/Steps_img/step7.png)

8. The result would be saved to excel file(.xlsx) in the "code" panel. Just download the whole file as .zip
