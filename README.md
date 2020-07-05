# Berkeley Course Crawler

This crawler helps you extract more detailed information from Berkeley Course webpage. Follow the steps below, and have your excel/google sheet/database prepared. You can organize your short list of courses.


```python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 23:32:27 2020

@author: You, Bo-Xiang
"""


def course_extract(url):
    
    import requests
    from datetime import datetime, timedelta
    import json
    import pandas as pd
    from bs4 import BeautifulSoup
    
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
    
    instructor = js_dict["meetings"][0]["assignedInstructors"]
    instructors = ', '.join([str(i["instructor"]["names"][1]["formattedName"]) for i in instructor])
    
    try:
        units = js_dict["course"]["credit"]["value"]["fixed"]["units"]
    except KeyError:
        units = ' to '.join([str(js_dict["course"]["credit"]["value"]["range"]["minUnits"]), str(js_dict["course"]["credit"]["value"]["range"]["maxUnits"])])
    
    # date-time process
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
    
    tw_start_dt = " / ".join([str((i + timedelta(hours=9)).strftime("%a %H:%M")) for i in fake_start_dt])
    tw_end_dt = " / ".join([str((i + timedelta(hours=9)).strftime("%a %H:%M")) for i in fake_end_dt])
    
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

## Demonstration


```python
# Example for one Course: 
result = course_extract("https://classes.berkeley.edu/content/2020-fall-data-c102-001-lec-001") # put the link between ""
result
```


```python
# copy the result and paste it on your excel/Google Sheet/Database
result.to_clipboard(excel=True,sep='\t')
```


```python
# Example for multiple Courses:
# 1. Put all your desired course link into the list, separate them by ","
url_list = ["https://classes.berkeley.edu/content/2020-fall-data-c102-001-lec-001", "https://classes.berkeley.edu/content/2020-fall-civeng-199-001-ind-001", "https://classes.berkeley.edu/content/2020-fall-indeng-290-004-lec-004"]
# 2. Extract them as table
multiple_results = multiple_extract(url_list)
multiple_results
```


```python
# 3. use this action to copy the result and paste it on your excel/Google Sheet/Database
multiple_results.to_clipboard(excel=True,sep='\t')
```

## Search for the courses that interest you


```python
# NOW, Try it on your own for one link!
result = course_extract("") # insert link
result.to_clipboard(excel=True,sep='\t') # copy the result, so you can paste it elsewhere
#check the result
result
```


```python
# NOW, Try it on your own for multiple link!
url_list = ["", "", ""] # insert links, you can add as more links as you want
multiple_results = multiple_extract(url_list)
multiple_results.to_clipboard(excel=True,sep='\t') # copy the result, so you can paste it elsewhere
#check the result
multiple_results
```
