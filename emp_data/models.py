from django.db import models
from datetime import datetime

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
    customers = models.ForeignKey(Customer, on_delete = models.CASCADE)
    Customer_Requirement_id = models.CharField(max_length=100,null=True)
    Required_skills = models.TextField()
    Job_Description = models.TextField()
    Required_Experience = models.FloatField(default=0)
    Open_positions = models.IntegerField(default=0)
    remain_positions = models.IntegerField(default=0)
    Position_Status = models.CharField(max_length=10) # active or closed        
    Sales_Incharge = models.CharField(max_length=50,null=True)# name of the person
    Bu_head=models.CharField(max_length=50,null=True)
    history = models.TextField(default="")
    priority = models.IntegerField(default=1)
    reqIdPK = models.AutoField(primary_key=True)


    class Meta:
        db_table = "customer_requirements"

    def __str__(self):
        return str(self.customers)
    

'''
class EmployeeReqMapping(models.Model):
    # req_id=models.IntegerField(default=0) #Model name change: Employee requirement 

    req_id=models.ForeignKey(Customer_Requirements, on_delete = models.CASCADE) #Model name change: Employee requirement 
    eFname = models.CharField(max_length=100,null=True)
    eLname = models.CharField(max_length=100, null=True)
    eskills = models.CharField(max_length=100,null=True)
    estatus = models.CharField(max_length=100,null=True)
    empstatus = models.CharField(max_length=100,null=True, default='')
    added_date = models.DateField(null=True)
    source = models.CharField(max_length=100,null=True, default='BENCH')
    sourceId = models.CharField(max_length=100,null=True,default='') # Can We  give foriegn key from 3 different table, like VM,TA, employee
    history = models.TextField(default="")

    class Meta:
        db_table = "employeereqmapping"

    def __str__(self):
        return str(self.req_id)
        '''

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

    class Meta:
        db_table = "employeereqmapping"

    def __str__(self):
        return str(self.req_id)


# model for VM candidates 
class VmResource(models.Model):
    position_status = models.CharField(max_length=100,null=True) #whether active or closed
    pr_date = models.DateField()
    vendor_name = models.CharField(max_length=100,null=True)
    candidate_source = models.CharField(max_length=100,null=True) #whether from bench or market
    candidate_name = models.CharField(max_length=300,null=True)    
    skillset = models.CharField(max_length=500,null=True)
    experience = models.FloatField()
    education = models.CharField(max_length=500,null=True)
    billing_rate = models.FloatField()
    bu_head = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=500,null=True)
    notice_period = models.IntegerField()
    reviewer_name = models.CharField(max_length=100,null=True)
    remarks_panel = models.CharField(max_length=500,null=True)
    vm_comment = models.CharField(max_length=1000,null=True)
    client_name = models.CharField(max_length=100,null=True)  
    interview_schedule = models.DateField()
    interview_status = models.CharField(max_length=100,null=True) 
    comments = models.CharField(max_length=1000,null=True)
    remarks = models.CharField(max_length=1000,null=True)   
    email = models.EmailField()
    phone_number = models.IntegerField()
    mode = models.CharField(max_length=500,null=True)
    vmIdPK = models.AutoField(primary_key=True,default=0)
    # owner = models.ForeignKey(Employee, on_delete = models.CASCADE)
    resume = models.CharField(max_length=1000,null=True)
    owner = models.CharField(max_length=1000,null=True)

    class Meta:
        db_table = "VmResource"
    def __str__(self):
        return str(self.candidate_name)
   
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
    BU = models.CharField(max_length=100)
    Position = models.CharField(max_length=100)
    skillset = models.CharField(max_length=500)
    education = models.CharField(max_length=500)
    experience = models.FloatField()
    relevant_exp = models.FloatField()
    current_org = models.CharField(max_length=500)
    current_ctc = models.FloatField()
    expected_ctc = models.FloatField()
    actual_notice_period = models.IntegerField()
    notice_period = models.IntegerField()
    current_loc = models.CharField(max_length=500)
    preferred_loc = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=15,unique=True)
    email = models.EmailField()
    status = models.CharField(max_length=100)
    BU_comments = models.CharField(max_length=1000)
    TA_comments = models.CharField(max_length=1000)    
    T1_panel = models.CharField(max_length=100)
    T1_IW_date = models.DateField()
    T2_panel = models.CharField(max_length=100)
    T2_IW_date = models.DateField()
    source = models.CharField(max_length=500)
    Rec_prime = models.CharField(max_length=500)
    Domain = models.CharField(max_length=100)
    T1 = models.CharField(max_length=100)
    T2 = models.CharField(max_length=100)
    owner = models.ForeignKey(Employee, on_delete = models.CASCADE)
    resume = models.CharField(max_length=1000)

    class Meta:
        db_table = "TA_Resource"
    def __str__(self):
        return str(self.name)

