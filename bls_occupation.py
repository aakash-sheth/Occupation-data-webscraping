# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:29:47 2019

@author: aakas
"""

import pandas as pd
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from pandas import ExcelWriter
from selenium.common.exceptions import NoSuchElementException

'''URL of website'''
url='https://www.bls.gov/ooh/'

#Lists to store scraped data 
occupation_list=[]
job_summary_list=[]
salary_list=[]
ed_requirement_list=[]
work_ex_list=[]
num_jobs_list=[]
job_outlook_list=[]
employment_change_list=[]
similar_occupation_list=[]



occ_group_list= ['Architecture-and-Engineering','Arts-and-Design','Building-and-Grounds-Cleaning',
                 'Business-and-Financial','Community-and-Social-Service','Computer-and-Information-Technology',
                 'Construction-and-Extraction','Education-Training-and-Library','Entertainment-and-Sports',
                 'Farming-Fishing-and-Forestry','Food-Preparation-and-Serving,','Healthcare',
                 'Installation-Maintenance-and-Repair','Legal','Life, Physical-and-Social-Science',
                 'Management','Math','Media-and-Communication','Military','Office-and-Administrative-Support',
                 'Personal-Care-and-Service','Production','Protective-Service','Sales','Transportation-and-Material-Moving']

# Start timer
Start_time= time.time()

#buetiful soup url parsing and get url

driver=webdriver.Chrome()


for i in range(len(occ_group_list)):
    occupation_gr=occ_group_list[i]
    url_add=url+str(occupation_gr)+'/'
    driver.get(url_add)
    n=1
    while True:
        print("in while")
        try:
            print("in try")
            '''job summary'''
            job_summary_xpath='//*[@id="landing-page-table"]/tbody/tr['+str(n)+']/td[3]/p'
            summary=driver.find_element_by_xpath(job_summary_xpath).text
            job_summary_list.append(summary)
            print(summary)
            
            '''Occupation Name'''
            element_xpath='//*[@id="landing-page-table"]/tbody/tr['+str(n)+']/td[2]'
            occupation=driver.find_element_by_xpath(element_xpath).text
            occupation_list.append(occupation)
            print(occupation)
            
            '''New page click'''
            driver.find_element_by_xpath(element_xpath).click()
            
            '''median Salary'''
            element_xpath='//*[@id="quickfacts"]/tbody/tr[1]/td'
            salary=driver.find_element_by_xpath(element_xpath).text
            salary_list.append(salary)
            
            '''Entry Level Education required'''
            element_xpath='//*[@id="quickfacts"]/tbody/tr[2]/td'
            required_edu=driver.find_element_by_xpath(element_xpath).text
            ed_requirement_list.append(required_edu)
            
            '''Work Ex'''
            element_xpath='//*[@id="quickfacts"]/tbody/tr[3]/td'
            work_ex=driver.find_element_by_xpath(element_xpath).text
            work_ex_list.append(work_ex)
            
            '''Job Outlook'''
            element_xpath='//*[@id="quickfacts"]/tbody/tr[6]/td'
            job_outlook=driver.find_element_by_xpath(element_xpath).text
            job_outlook_list.append(job_outlook)
            
            '''employment change'''
            element_xpath='//*[@id="quickfacts"]/tbody/tr[7]/td'
            emp_change=driver.find_element_by_xpath(element_xpath).text
            employment_change_list.append(emp_change)
            n=n+1
        
        except NoSuchElementException:
            print("Exception" + occupation )
            break
  
         
'''Consolidation of all list into pandas dataframe'''
           
df1 = pd.DataFrame(occupation_list, columns=['Occupation'])
df2=pd.DataFrame(job_summary_list, columns=['Job Summary'])
df3=pd.DataFrame(salary_list, columns=['Median Salary'])
df4=pd.DataFrame(ed_requirement_list, columns=['Entry level Education'])
df5=pd.DataFrame(work_ex_list, columns=['Work Ex'])
df6=pd.DataFrame(job_outlook_list, columns=['Job Outlook'])
df7=pd.DataFrame(employment_change_list, columns=['Employment Change'])


df_12=df1.join(df2)
df_123=df_12.join(df3)
df_1234=df_123.join(df4)
df_12345=df_1234.join(df5)
df_123456=df_12345.join(df6)
df_1234567=df_123456.join(df7)


writer = ExcelWriter('Occupation Outlook' + '.xlsx')
df_1234567.to_excel(writer, 'Sheet1', index=False)
writer.save()   


elapsed_time=time.time()- Start_time
print(elapsed_time)
        
        