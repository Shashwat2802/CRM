from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    role = models.CharField(max_length=100, default='user')
    emp_id = models.CharField(max_length=100, default='LS111')
    user_permissions=models.IntegerField(default=0xFFFFFFFFFFF)


class Customer(models.Model):
    cName = models.CharField(max_length=50,primary_key=True)
    cEmail = models.EmailField(null=True)
    cUrl = models.CharField(max_length=50,null=True)
    
    class Meta:     
        db_table = "customer"

    def __str__(self):
        return str(self.cName)
    

class Role(models.Model):
    role_name=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.role_name
    
class Department(models.Model):
    department=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.department

class Employee(models.Model):
    e_id=models.CharField(max_length=100,primary_key=True)
    eFname = models.CharField(max_length=50,null=True)
    eLname = models.CharField(max_length=50,null=True)
    refer_Customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    eEmail = models.EmailField(max_length=200,null=True)
    ePhone = models.CharField(max_length=50)
    eExperience = models.IntegerField(default=0,null=True)
    eskills = models.CharField(max_length=100,null=True)
    eRole = models.ForeignKey(Role,on_delete=models.CASCADE) # designation
    estatus = models.CharField(max_length=100,null=True) # either free or deployed
    leadsoc_joining_date = models.DateField(null=True)
    customer_start_date = models.DateField(null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE) # designation
    Manager = models.CharField(max_length=100,null=True)
    IsManager = models.BooleanField(default=False)
    BUH= models.CharField(max_length=50,null=True)
    isDeleted=models.BooleanField(default=False)
    class Meta:
        db_table = "employee"

    def __str__(self):
        return str(self.eFname)
         
from datetime import datetime

class EmpExperienceHistory(models.Model):
    e_id=models.CharField(max_length=5)
    refer_customer=models.CharField(max_length=100,null=True)
    customer_start_date=models.DateField(null=True)
    customer_end_date=models.DateField(null=True)
    
    @property
    def duration(self):
        return (self.customer_end_date-self.customer_start_date).days

        

class Customer_Requirements(models.Model):
# ReqDate	Customer	CustomeRequirmentID	JobTitle	JobDescription	RequiredSkills	MinExp	MaxExp	OpenPositions	filled	lapsed	Remaining 	Status	ReqClosedDate	SalesIncharge	BuHead	Remarks	priority	FullFillment	ACtiveSubmissionCount	ActiveResumeList
    reqIdPK = models.AutoField(primary_key=True)
    ReqDate=models.DateField()
    customers = models.ForeignKey(Customer, on_delete = models.CASCADE)
    CustReqId = models.CharField(max_length=100,null=True)
    jobTitle = models.CharField(max_length=100,null=True)
    JD = models.TextField()
    RequiredSkills = models.TextField()
    minExp = models.FloatField(default=3)
    maxExp = models.FloatField(default=10)
    openPositions = models.IntegerField(default=0)
    filledPositions = models.IntegerField(default=0)
    lapsedPositions = models.IntegerField(default=0)
    remainPositions = models.IntegerField(default=0)
    reqStatus = models.CharField(max_length=10) # active,hold or closed  
    ReqClosedDate=models.DateField(null=True)
      
    SalesIncharge = models.CharField(max_length=50,null=True)# name of the person
    buHead=models.CharField(max_length=50,null=True)
    history = models.TextField(default="")
    priority = models.IntegerField(default=1)
    fulfillThru = models.CharField(max_length=10,default='BENCH')
    ActiveSubmissionCount = models.IntegerField(default=0)
# ActiveResumeList  == This is only for Excel sheet 


    class Meta:
        db_table = "customer_requirements"

    def __str__(self):
        return str(self.customers)
    

class EmployeeReqMapping(models.Model):
    # req_id=models.IntegerField(default=0) #Model name change: Employee requirement 

    req_id=models.ForeignKey(Customer_Requirements, on_delete = models.CASCADE) #Model name change: Employee requirement 
    name = models.CharField(max_length=100,null=True)
    eskills = models.CharField(max_length=100,null=True)
    estatus = models.CharField(max_length=100,null=True)
    empstatus = models.CharField(max_length=100,null=True, default='')
    added_date = models.DateField(null=True)
    source = models.CharField(max_length=100,null=True, default='BENCH')
    sourceid_1 = models.CharField(max_length=10,null=True) # Can We  give foriegn key from 3 different table, like VM,TA, employee
    sourceid_2=models.CharField(max_length=10,null=True)
    sourceid_3=models.IntegerField(default=0)
    history = models.TextField(default="")
    resumeURL = models.CharField(max_length=1000,null=True)

    class Meta:
        db_table = "employeereqmapping"

    def __str__(self):
        return str(self.req_id)


# model for VM candidates 
class VmResource(models.Model):

    vmIdPK = models.AutoField(primary_key=True,default=0)
    archivalStatus = models.CharField(max_length=100,default='Active') #whether active or closed
    reqDate = models.DateField()
    providedDate = models.DateField()
    vendorName = models.CharField(max_length=100)
    resumeSource = models.CharField(max_length=100) #whether from bench or market
    candidateName = models.CharField(max_length=300)    
    skillset = models.CharField(max_length=500)
    experience = models.FloatField()
    education = models.CharField(max_length=500)
    billingRate = models.FloatField()
    location = models.CharField(max_length=500)
    noticePeriod = models.IntegerField()
    clientName = models.CharField(max_length=100)   
    email = models.EmailField()
    mobile = models.IntegerField()
    resumeURL = models.CharField(max_length=1000,null=True)
    owner = models.CharField(max_length=1000)
    buh = models.CharField(max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE) # designation
    interviewSchedule = models.DateField(null=True)
    resumeStatus = models.CharField(max_length=100,default='ScreeningPending') 
    remarks = models.CharField(max_length=1000)


    class Meta:
        db_table = "VmResource"
    def __str__(self):
        return str(self.candidateName)
   
class Employee_Details(models.Model):
    pass

class UploadFile(models.Model):
    specifications = models.FileField(upload_to='router_specifications')
    
class Login(models.Model):
    UserName = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    
    class Meta:
        db_table = "login"

class TA_Resource(models.Model): # TA_resource contain 33 records
    ta_id = models.CharField(max_length=10,primary_key=True)
    archived = models.CharField(max_length=100)
    date = models.DateField()
    name = models.CharField(max_length=300)  
    department = models.ForeignKey(Department,on_delete=models.CASCADE)    
    BU = models.CharField(max_length=100)
    Position = models.CharField(max_length=100)
    skillset = models.CharField(max_length=500)
    education = models.CharField(max_length=500)
    experience = models.FloatField(default=0)
    relevant_exp = models.FloatField(default=0)
    current_org = models.CharField(max_length=500)
    current_ctc = models.FloatField(default=0)
    expected_ctc = models.FloatField(default=0)
    actual_notice_period = models.IntegerField(default=0)
    notice_period = models.IntegerField(default=0)
    current_loc = models.CharField(max_length=500)
    preferred_loc = models.CharField(max_length=500)
    phone_number = models.IntegerField(default=0)
    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100,default='ScreeningPending')        
    T1_panel = models.CharField(max_length=100)
    T1_IW_date = models.DateField(null=True)
    T2_panel = models.CharField(max_length=100)
    T2_IW_date = models.DateField(null=True)
    source = models.CharField(max_length=500)      
    owner = models.CharField(max_length=100)
    resume = models.URLField(null=True,blank=True)
    remarks = models.CharField(max_length=1000)

    class Meta:
        db_table = "TA_Resource"
    def __str__(self):
        return str(self.name)

