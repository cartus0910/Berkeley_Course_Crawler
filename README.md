# Berkeley Course Crawler

This crawler helps you extract more detailed information from Berkeley Course webpage. Follow the steps below, and have your excel/google sheet/database prepared. You can organize your short list of courses.




## Demonstration


```python
# Example for one Course: 
result = course_extract("https://classes.berkeley.edu/content/2020-fall-data-c102-001-lec-001") # put the link between ""
result
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
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
  </tbody>
</table>
</div>




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
    </tr>
  </tbody>
</table>
</div>




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

Or You can just process through online environment here
Just follow the instructions.
<iframe height="400px" width="100%" src="https://repl.it/@cartus0910/TrimOrchidBootstrapping-2?lite=true" scrolling="no" frameborder="no" allowtransparency="true" allowfullscreen="true" sandbox="allow-forms allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-modals"></iframe>
