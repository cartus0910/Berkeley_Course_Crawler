
# Berkeley Course Crawler

This crawler helps you extract more detailed information from Berkeley Course webpage. Follow the steps below, and have your excel/google sheet/database prepared. You can organize your short list of courses.

***


## Demonstration

### 1. Export information of course of your interest


```python
# Example for three selected Course: 
url_list = ["https://classes.berkeley.edu/content/2020-spring-geog-149b-001-lec-001",
       "https://classes.berkeley.edu/content/2020-spring-geog-167ac-001-lec-001",
       "https://classes.berkeley.edu/content/2020-spring-geog-200b-001-sem-001"]
    
result = course_info(url_list)
info = result.information
info.head()
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
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
      <th>Total_Capacity</th>
      <th>Total_Enrolled</th>
      <th>Final_Examination</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
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
      <td>Diana M Negrin</td>
      <td>4</td>
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
</div>




```python
# copy the result and paste it on your excel/Google Sheet/Database
info.to_clipboard(excel=True,sep='\t')
```


```python
# or save file as .xlsx directly
multiple_results.to_excel('course_info.xlsx', na_rep=False)
```

### 2. If you wanna export a schedule of all selected courses


```python
schedule = result.weekly_schedule(time_zone="SF")
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
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
  </tbody>
</table>



```python
# copy the schedule and paste it on your excel/Google Sheet/Database
schedule.to_clipboard(excel=True, sep='\t')
```


```python
# or save file as .xlsx directly
schedule.to_excel('course_schedule.xlsx', na_rep=False)
```

## Search for the courses that interest you


```python
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

## For non-python environmnet

If you don't have a python environment, welcome to use **[the service from my webiste](http://homepage.ntu.edu.tw/~b06208002/service/replit.html)** via replit.

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
