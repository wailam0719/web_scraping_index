import requests
import re
from bs4 import BeautifulSoup
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pickle
import os.path


class Index():
    sched = BackgroundScheduler()

    @classmethod
    def CPI_Index(cls):
        CPI_url = "https://www.censtatd.gov.hk/hkstat/sub/so270.jsp"
        CPI_page = requests.get(CPI_url)
        CPI_soup = BeautifulSoup(CPI_page.content,'html.parser')
        cls.CPI = CPI_soup.findAll("a", class_="noul")[0].text
        cls.Storage('CPI',cls.CPI)
    
    @classmethod
    def HSI_Index(cls):
        HSI_url = "https://hk.finance.yahoo.com/quote/%5Ehsi?ltr=1"
        HSI_page = requests.get(HSI_url)
        HSI_soup = BeautifulSoup(HSI_page.content,'html.parser')
        cls.HSI = HSI_soup.find("span",class_="Trsdu(0.3s) ").text
        cls.Storage('HSI',cls.HSI)

    @classmethod
    def RunClass(cls):
        if os.path.isfile('./HSI.pickle') == False or os.path.isfile('./CPI.pickle') == False:
            cls.HSI_Index()
            cls.CPI_Index()
            cls.sched.add_job(cls.HSI_Index, 'cron', id = 'HSI', hour = 9, minute = 35)
            cls.sched.add_job(cls.CPI_Index, 'cron', id = 'CPI', month = '1-12', day = 25)
            cls.sched.start()
        
        else:
            cls.sched.add_job(cls.HSI_Index, 'cron', id = 'HSI', hour = 9, minute = 35)
            cls.sched.add_job(cls.CPI_Index, 'cron', id = 'CPI', month = '1-12', day = 25)
            cls.sched.start()

    @classmethod
    def Storage(cls,filename,obj):
        file = open('{}.pickle'.format(filename),'wb')
        pickle.dump(obj,file)

    @classmethod
    def fetchHSI(cls):
        with open('HSI.pickle', 'rb') as file:
            cls.HSI = pickle.load(file)
        return cls.HSI

    @classmethod
    def fetchCPI(cls):
        with open('CPI.pickle','rb') as file:
            cls.CPI = pickle.load(file)
        return cls.CPI

    @classmethod
    def ShutDown(cls):
        cls.sched.shutdown()
    
    @classmethod
    def RemoveJob(cls,id):
        cls.sched.remove_job(id)
    
    @classmethod
    def RemoveAllJobs(cls):
        cls.sched.remove_all_jobs()

    @classmethod
    def GetJobs(cls):
        cls.sched.get_jobs()

    @classmethod
    def PauseJob(cls,id):
        cls.sched.pause_job(id)
    
    @classmethod
    def ResumeJob(cls,id):
        cls.sched.resume_job(id)


