import csv
from ctypes import wstring_at
from io import TextIOWrapper
from pkgutil import get_data
import queue
import quopri
from emp_data.admin import EmployeeReqMappingAdmin
from django.shortcuts import render,redirect,get_object_or_404
from emp_data.models import Customer,Employee,Customer_Requirements,EmployeeReqMapping
from .resources import EmployeeResource
from emp_data.forms import CustomerForm,EmployeeForm, loginForm,UploadFileForm,Customer_RequirementForm,TA_Form, VmCandidateForm
from django.contrib import messages
from django.contrib.auth.models import auth
from emp_data.models import *
from tablib import Dataset
from .models import Customer
from django.template import loader
import xlwt
from django.http import HttpResponse
from django.db.models import Q
from datetime import date
from django.db.models import Func, F
from django.http import JsonResponse

def loginCheck(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect("/addEmployee")
        else:
            messages.info(request, 'invalid credentials')
            return redirect("/addEmployee")
    else:
        form = loginForm()
        return render(request, "regsitration/login.html")


#Home page
def home(request):
    return render(request,"home.html")

# To add Customer

def addCustomer(request):
    if request.method == "POST":

        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Company Details saved successfully')
                return redirect("/listCustomers")
            except:
                pass
    else:
        form = CustomerForm()
    return render(request, "index.html", {'form':form})


def addEmployee(request):
    form=EmployeeForm()
    if request.method == "POST":
        form=EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Details Saved !")
            return redirect("/listEmployeeFiltered/All/All/All")

        else:
            print("Error in data", form)
            return HttpResponse("mandatory params not given" )#form.errors)

    
    else:
        customerList=getCustomerList()
        rolelist=getRoleList()
        departments=getDepartmentList()
        buhList=getBUHList()
        managerList=getManagers()
        return render(request, 'addemp.html',{'departments':departments,'customerList': customerList,'rolelist':rolelist,'status':['Free','Deployed','Support Team'],"buhList":buhList,"managerList":managerList})


def addEmployeeExperience(request, e_id):
    if request.method == 'POST':
        c_name = request.POST.get('refer_customer')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        instance=EmpExperienceHistory(e_id=e_id,refer_customer=c_name,customer_start_date=start_date,customer_end_date=end_date)
        instance.save()
        return redirect('/listEmployeeFiltered/All/All/All')
    else:
        return HttpResponse("Error")
   

def deleteEmployeeExperience(request, exp_id): 
    exp_instance = EmpExperienceHistory.objects.get(id=exp_id)
    exp_instance.delete()
    return redirect('/listEmployeeFiltered/All/All/All')


def addSalesReqs(request):
    form=Customer_RequirementForm()
    if request.method == "POST":
        
        
        form=Customer_RequirementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Details Saved !')
            return redirect('/listSalesReqsFiltered/Choose/Choose/Choose')
        else:
            return HttpResponse(form.errors)

    else:
        customerList=getCustomerList()
        BUList=list(map(lambda x:x.eFname ,getBUHList()))
        SalesList=list(map(lambda x:x.eFname ,getSalesTeam()))

        return render(request, 'addcustrequirements.html',{'customerlist': customerList, 'bulist': BUList, 'saleslist' : SalesList})


def getCustomerList () :
        return list(map(lambda x:x.cName ,Customer.objects.all()))

def getRoleList () :
    return list(map(lambda x:x.role_name ,Role.objects.all()))
# To retrieve Customer details

def updateSaleReqs(request,reqIdPK):
    model_instance=Customer_Requirements.objects.get(pk=reqIdPK)
    model_instance.Required_skills=request.POST['Required_skills']
    model_instance.Job_Description=request.POST['Job_Description']
    model_instance.Required_Experience=request.POST['Required_Experience']
    model_instance.Open_positions=request.POST['Open_positions']
    model_instance.remain_positions=request.POST['Open_positions']
    model_instance.Position_Status=request.POST['Position_Status']
    model_instance.Sales_Incharge=request.POST['Sales_Incharge']
    model_instance.Bu_head = request.POST['Bu_Head']
    model_instance.priority = request.POST['priority']
    if 'history' in request.POST:
        hist=request.POST['history']
        print("hist",hist)
        model_instance.history = hist
    
    # print("history",hist)
    # model_instance.history = request.POST['history']

    model_instance.save()
    return redirect('/listSalesReqsFiltered/Choose/Choose/Choose')  
        

def listCustomers(request):
    if not request.user.is_authenticated:
        return redirect('home')
    companies = Customer.objects.all()
    return render(request, "show.html", {'companies':companies})

# To Update Customer
def updateCustomers(request, cName):
    if not request.user.is_authenticated:
        return redirect('home')
    customer = get_object_or_404(Customer,pk=cName)
    form = CustomerForm(request.POST or None, instance= customer)
    if form.is_valid():
         form.save()
         return redirect("/listCustomers")
    else:
        return HttpResponse(form.errors)
    
    # return render(request, "edit.html", {'customer': customer})

# To Delete Customer details
def deleteCustomer(request, cName):
    if not request.user.is_authenticated:
        return redirect('home')
    
    customer = Customer.objects.get(cName=cName)
    customer.delete()    
    messages.success(request,'The Selected customer'  + str(customer.cName) +  'is deleted successfully')
   
    return redirect("/listCustomers")

def getDepartmentList():
    return Department.objects.all()

def getManagers():
    return Employee.objects.filter(IsManager=True, isDeleted=False)

def getSalesTeam():
    return Employee.objects.filter((Q(eRole='SALES_STAFF')| Q(eRole='SALES_HEAD')),isDeleted=False)

def getBUHList():
    return Employee.objects.filter(eRole='BUH',isDeleted=False)


def filteredSaleReqs(request,bu,sales,st):
    if not request.user.is_authenticated:
        return redirect('home')
    
    filter_conditions={}
    if bu != 'All' and bu != 'Choose':
        filter_conditions['Bu_head'] = bu

    if sales != 'All' and sales != 'Choose':
        filter_conditions['Sales_Incharge'] = sales

    if st != 'All' and st != 'Choose':
        filter_conditions['Position_Status'] = st

    print("FIlter COndition",filter_conditions,bu,sales,st)
    customer_requirements=  Customer_Requirements.objects.filter(**filter_conditions)

    bu_head = getBUHList()
    current_user = request.user.username.title() 
    sales_incharge= getSalesTeam()
    return render(request,'show_cust_requirements.html',{'customer_requirements':customer_requirements,
                                                        'sales_incharge': sales_incharge, 'bu_head': bu_head, 
                                                        'current_user':current_user,'bu_select': bu, "sales_select": sales, 'status_select': st})

def listEmployeeFiltered(request,department,buh,manager):
    if not request.user.is_authenticated:
        return redirect('home')
    
    filter_conditions={}
    if department != 'All' and department != 'Choose':
        filter_conditions['department'] = department

    if buh != 'All' and buh != 'Choose':
        filter_conditions['BUH'] = buh

    if manager != 'All' and manager != 'Choose':
        filter_conditions['Manager'] = manager

    print("FIlter COndition",filter_conditions,department,buh,manager)
    employees=  Employee.objects.filter(**filter_conditions,isDeleted=False)
    print("Employee list",employees)
    departments =getDepartmentList()
    buhList= getBUHList()

    managerList=getManagers()
    current_user = request.user.username  
    current_emp = Employee.objects.get(eFname__icontains=current_user,isDeleted=False)     
    return render(request, "showemp.html", {'employees':employees,"department":department,"buh":buh,
                                             "manager":manager,"current_emp":current_emp,
                                              'departments':departments,'BUHList':buhList,'managerList':managerList}) 


def getEmployeeExperiances(request, employee_id):
    print("Emp id from model", employee_id)
    employee=  Employee.objects.get(e_id=employee_id,isDeleted=False)
    experiencelist = EmpExperienceHistory.objects.filter(e_id=employee_id)
    customerlist=getCustomerList()
    context = {'employee':employee,"experiencelist":experiencelist,"customerlist":customerlist}
    print("emp exp Data in view",context)
    return render(request, "empExpModal.html", context) 

def addSalesReqComment(request, reqIdPK):
    if request.method == 'POST':
        current_user = request.user.username.title()
        remark_text = request.POST.get('remark_text', '')
        today = date.today()
        salesReq = Customer_Requirements.objects.get(pk=reqIdPK)
        print("Existing Comment",salesReq.history)
        salesReq.history=today.strftime('%Y-%m-%d')+ ":"+current_user+"# "+remark_text +"\n\n"+salesReq.history
        salesReq.save()
        return redirect('/listSalesReqsFiltered/Choose/Choose/Choose')

def cust_req_dropdown(request, ref): 
    if ref[:1] == 'P':
        cust = Customer_Requirements.objects.get(pk=ref[2:3])
        if ref[1:2] == 'A': 
            cust.Position_Status = 'Active'
        elif ref[1:2] == 'H': 
            cust.Position_Status = 'Hold'
        elif ref[1:2] == 'I': 
            cust.Position_Status = 'Inactive'
    elif ref[:1] == 'S':
        cust = Customer_Requirements.objects.get(pk=ref[1:2])
        cust.Sales_Incharge = ref[2:]
    elif ref[:1] == 'B': 
        cust = Customer_Requirements.objects.get(pk=ref[1:2])
        cust.Bu_head = ref[2:]
    cust.save()
    return redirect('/listSalesReqsFiltered/Choose/Choose/Choose')
    

def salesSummary(request):
    first=getBUHList()
    second=getSalesTeam()
    saleslist=[]
    bulist=[]
    for val in first:
        bulist.append(val.eFname)
    for val in second:
        saleslist.append(val.eFname)
    final=[]
    for val in saleslist:
        firstarray=[]
        for newval in bulist:
            customercount=len(Customer_Requirements.objects.filter(Bu_head=str(newval),Sales_Incharge=str(val)))
            firstarray.append(customercount)
        firstarray.append(sum(firstarray))
        firstarray.insert(0,val)
        final.append(firstarray)
    length=len(bulist)
    context={'final':final,
             'bulist':bulist,
             'length':length}
    return render(request,'summary.html',context)


def addCommentToEmployeedReqTable(request, reqIdPK,source,sourceId):
    print("****ID",reqIdPK,source,sourceId)
    if request.method == 'POST':
        current_user = request.user.username.title()
        remark_text = request.POST.get('remark_text', '')
        today = date.today()
        mapping = EmployeeReqMapping.objects.get(req_id=reqIdPK,source=source,sourceId=sourceId)
        print("Existing mapping",mapping.req_id,mapping.eFname,mapping.sourceId)
        mapping.history=today.strftime('%Y-%m-%d')+ ":"+current_user+"# "+remark_text +"\n\n"+mapping.history
        mapping.save()
        return redirect(f'/mappedEmployeeToCustomer/{reqIdPK}')

def getOwnerList():
    return Employee.objects.filter((Q(eRole='TA_HEAD')|Q(eRole='TA_STAFF')|Q(eRole='VM_STAFF')),isDeleted=False)

def addTa(request):
    form=TA_Form()
    if request.method=='POST':
        form=TA_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/showTa')
        else:
            return HttpResponse(form.errors)
    else:
        BUList=list(map(lambda x:x.eFname ,getBUHList()))
        ownerList = list(map(lambda x:x.eFname,getOwnerList()))        
        return render(request,'addTA.html',{'BUList':BUList,'ownerList':ownerList,'status':['Select','Archived','Closed']})

def showTa(request):
    ta_instance=TA_Resource.objects.all()
    Bu_head=getBUHList()
    return render(request,'showTA.html',{'ta_instance':ta_instance,'Bu_head':Bu_head})

def filterTa(request,buhead,archive):
    filtered={}
    if buhead != 'All' :
        filtered['BU']=buhead
    if archive !='Both':
        filtered['archived']=archive
    print("Filtered Condition",filtered)
    ta_instance=TA_Resource.objects.filter(**filtered)
    Bu_head=getBUHList()
    return render(request,'showTA.html',{'ta_instance':ta_instance,'Bu_head':Bu_head,
                                         'status_select':archive,'bu_select':buhead})

def deleteTa(request,phone_number):
    instance=TA_Resource.objects.get(pk=phone_number)
    instance.delete()
    return redirect('/showTa')


def job_description(request):
    job_desc = Customer_Requirements.objects.values('Job_Description')
    return render(request,"job_description.html",{'job_desc':job_desc})




def freeFromAllSource(request,reqIdPK):
    form = Employee.objects.filter((Q(estatus ='Free')|Q(estatus='pendingProcessing')),isDeleted=False ).values()
    if request.method == "GET":   
        skills = request.GET.get('searchskill')      
        if skills != None: 
            form = Employee.objects.filter((Q(estatus ='Free')|Q(estatus='pendingProcessing')),eskills__icontains= skills,isDeleted=False)
    return render(request,'show_candidate.html',{'form':form ,'reqIdPK':reqIdPK})

def checkbox(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        if request.POST.getlist('checks'):
            
            s = request.POST.getlist('checks')
            print(s)
            for i in s:               
                savedata = EmployeeReqMapping()
                savedata.eFname = i
                savedata.save()         
            

        return redirect('/mappedEmployeeToCustomer')
    else:
        return redirect('/mappedEmployeeToCustomer')


#show added employe to customer
def mappedEmployeeToCustomer(request,reqIdPK):  
    if not request.user.is_authenticated:
        return redirect('home')
    emp_data = EmployeeReqMapping.objects.filter(req_id=reqIdPK)
    req_instance=Customer_Requirements.objects.get(pk=reqIdPK)
    position=req_instance.remain_positions
    return render(request, "showEmpToCustomer.html", {'form':emp_data,'reqIdPK':reqIdPK,'position':position,
    })



def selection_status(request, estatus,reqIdPK): 
    model_instance = EmployeeReqMapping.objects.get(name=estatus[2:])
    #model_instance = EmployeeReqMapping.objects.get(req=req_id)
    requirement_instance=Customer_Requirements.objects.get(pk=reqIdPK)

    if estatus[:2] == 'SL':
        model_instance.empstatus = 'Selected'
        requirement_instance.remain_positions-=1
        model_instance.save()
        requirement_instance.save()

    elif estatus[:2] == 'RJ': 
        model_instance.empstatus = 'Rejected'
        model_instance.save()   

    elif estatus[:2]=='BU':
        model_instance.empstatus='Shortlisted by BU'
        model_instance.save()

    elif estatus[:2]=='CL':        
        model_instance.empstatus='Shortlisted by Client'
        model_instance.save()

    elif estatus[:2]=='OP':
        model_instance.empstatus='Onboarding Progress'
        model_instance.save()

    elif estatus[:2]=='OB':
        model_instance.empstatus='Onboarded'
        model_instance.save()

    elif estatus[:2]=='RR':
        model_instance.empstatus='Resume Rejected'
        model_instance.save()
    return redirect(f'/mappedEmployeeToCustomer/{reqIdPK}')

# To display all the VM candidates 
def showVm(request):
    all_vm_candidates = VmResource.objects.all()
    ownerList = list(map(lambda x:x.eFname,getOwnerList()))  
    departments =getDepartmentList()
    buhList= getBUHList()
    return render(request, "show_vm_candidates.html", {"candidate_list":all_vm_candidates,'ownerList':ownerList,'departments':departments,'BUHList':buhList})

# Form to add only one VM candidate 
def addVm(request):
    form=VmCandidateForm()
    if request.method == "POST":
        form=VmCandidateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Details Saved !")
            return redirect("/showVm")
        else:
            return HttpResponse(form.errors)
    else:
        ownerList = list(map(lambda x:x.eFname,getOwnerList()))
        BUList=list(map(lambda x:x.eFname ,getBUHList()))
        departments=getDepartmentList()
        return render(request, "add_vm_candidates.html",{'ownerList':ownerList,'bulist':BUList,"departments":departments})

# To upload data containing VM candidates
def vmDataUpload(request): 
    if request.method == "POST":
        dataset = Dataset()
        print("Input ",request)
        new_vm = request.FILES['myfile']
        if not new_vm.name.endswith('xlsx'):
            messages.info(request, 'Wrong format of file')
            return render(request, 'upload_vm_candidates.html')
        imported_data = dataset.load(new_vm.read(), format='xlsx')
        for data in imported_data:
            dept=data[19]
            deptment=Department.objects.filter(department=dept)
            if deptment.exists():
                print("dept  exists",deptment)
            else :
                deptInstance=Department(department=dept)
                deptInstance.save()
                print("dept does not exists",deptInstance)

            value = VmResource(
                vmIdPK=data[0],
                archivalStatus=data[1],
                reqDate=data[2],
                providedDate=data[3],
                vendorName=data[4],
                resumeSource=data[5],
                candidateName=data[6],
                skillset=data[7],
                experience=data[8],
                education=data[9],
                billingRate=data[10],
                location=data[11],
                noticePeriod=data[12],
                clientName=data[13],
                email=data[14],
                mobile=data[15],
                resumeURL=data[16],
                owner=data[17],
                buh=data[18],
                department=Department(department=data[19]),
                interviewSchedule=data[20],
                resumeStatus=data[21],
                remarks=data[22],
            )
     
            print(":VM Onwer",data[16], data[5] )
            value.save()
        return redirect("/showVm")
    return render(request, "upload_vm_candidates.html")


def updateVmCandidate(request, vmIdPK): 
    if not request.user.is_authenticated:
        return redirect('home')
    vmResource = VmResource.objects.get(pk=vmIdPK)
    if request.method =='POST':
        print("BUH***",request.POST)
        vmResource.archivalStatus=request.POST['archivalStatus']
        vmResource.reqDate=request.POST['reqDate']
        vmResource.providedDate=request.POST['providedDate']
        vmResource.vendorName=request.POST['vendorName']
        vmResource.resumeSource=request.POST['resumeSource']
        vmResource.candidateName=request.POST['candidateName']
        vmResource.skillset=request.POST['skillset']
        vmResource.experience=request.POST['experience']
        vmResource.education = request.POST['education']
        vmResource.billingRate=request.POST['billingRate']
        vmResource.buh = request.POST['buh']
        vmResource.location= request.POST['location']
        vmResource.noticePeriod = request.POST['noticePeriod']
        vmResource.clientName = request.POST['clientName']
        vmResource.mobile = request.POST['mobile']
        vmResource.resumeURL = request.POST['resumeURL']
        vmResource.department = Department(department=request.POST['department'])
        vmResource.interviewSchedule = request.POST['interviewSchedule']
        vmResource.resumeStatus = request.POST['resumeStatus']
        # vmResource.remarks = request.POST['remarks']
        vmResource.email = request.POST['email']
        vmResource.owner = request.POST['owner']


        # if 'history' in request.POST:
        #     hist=request.POST['history']
        #     print("hist",hist)
        #     vmResource.history = hist

        vmResource.save()
        return redirect('/showVm')

def showTaList(request,reqIdPK):
    # form=TA_Resource.objects.filter(status='Selected').values()
    form=TA_Resource.objects.filter(archived__icontains='Active').values()

    if request.method=='GET':
        skills=request.GET.get('searchskill')
        if skills != None:
            form=TA_Resource.objects.filter(skillset__icontains=skills)
    
    return render(request,'selected_ta_list.html',{'form':form,"reqIdPK":reqIdPK})

def showVmList(request,reqIdPK):
    # form=VmResource.objects.filter(interview_status='Selected').values()
    form=VmResource.objects.filter(position_status__icontains='Active').values()

    if request.method=='GET':
        skills=request.GET.get('searchskill')
        if skills!=None:
            form=VmResource.objects.filter(skillset__icontains=skills)
    
    return render(request,'selected_vm_list.html',{'form':form,'reqIdPK':reqIdPK})

def updateTaDetails(request,ta_id):
    if not request.user.is_authenticated:
        return redirect('home')
    ta_instance = TA_Resource.objects.get(pk=ta_id)
    if request.method=='POST':      

        ta_instance.archived=request.POST['archived']
        ta_instance.date=request.POST['date']
        ta_instance.name=request.POST['name']
        ta_instance.BU=request.POST['BU']
        ta_instance.Position=request.POST['Position']
        ta_instance.skillset=request.POST['skillset']
        ta_instance.education=request.POST['education']
        ta_instance.experience=request.POST['experience']
        ta_instance.relevant_exp=request.POST['relevant_exp']
        ta_instance.current_org=request.POST['current_org']
        ta_instance.current_ctc=request.POST['current_ctc']
        ta_instance.expected_ctc=request.POST['expected_ctc']
        ta_instance.actual_notice_period=request.POST['actual_notice_period']
        ta_instance.notice_period=request.POST['notice_period']
        ta_instance.current_loc=request.POST['current_loc']
        ta_instance.preferred_loc=request.POST['preferred_loc']
        ta_instance.phone_number=request.POST['phone_number']
        ta_instance.email=request.POST['email']
        ta_instance.status=request.POST['status']
        ta_instance.T1_panel=request.POST['T1_panel']
        ta_instance.T1_IW_date=request.POST['T1_IW_date']
        ta_instance.T2_panel=request.POST['T2_panel']
        ta_instance.T2_IW_date=request.POST['T2_IW_date']
        ta_instance.source=request.POST['source']
        ta_instance.Rec_prime=request.POST['Rec_prime']
        ta_instance.Domain=request.POST['Domain']
        ta_instance.T1=request.POST['T1']
        ta_instance.T2=request.POST['T2']
        ta_instance.owner=request.POST['owner']
        ta_instance.save()

    return redirect("/showTa")

def mapEmpToReq(request,reqIdPK,choice):
    
    if request.method == 'POST':
        today = date.today()
        salesReq=Customer_Requirements.objects.get(pk=reqIdPK)
        print("Req",salesReq, salesReq.Bu_head)
        if choice=='bench':
             selectedEmpList = request.POST.getlist('empId')
             print("employee list",selectedEmpList)
             for i in selectedEmpList:
                emp=Employee.objects.get(e_id=i,isDeleted=False)
                emp.estatus='pendingProcessing'
                emp.save()
                print("Employee status updated",emp)
                final=EmployeeReqMapping(req_id=salesReq,name=emp.eFname + " " +emp.eLname,eskills=emp.eskills,  added_date=today,source='BENCH',sourceid_1=emp.e_id)
                final.save()
        if choice=='TA':
            selectedtaList = request.POST.getlist('name')
            print("Selected TA  list",selectedtaList)
            for i in selectedtaList:
                ta=TA_Resource.objects.get(name=i)
                ta.status='Selected and Mapped'
                ta.save()
                final=EmployeeReqMapping(req_id=salesReq,name=ta.name,eskills=ta.skillset,added_date=today,source='TA',empstatus='Selected',sourceid_2=ta.ta_id)
                final.save()
        if choice=='VM':
            selectedvmList = request.POST.getlist('candidate_name')
            print("Selected VM  list",selectedvmList)
            for vm_name in selectedvmList:
                vm=VmResource.objects.get(candidateName=vm_name)
                vm.interview_status='Selected and Mapped'
                vm.save()
                final=EmployeeReqMapping(req_id=salesReq,name=vm.candidateName,eskills=vm.skillset,  added_date=today,source='VM',empstatus='Selected',sourceid_3=vm.vmIdPK)
                final.save()
    return redirect(f'/mappedEmployeeToCustomer/{reqIdPK}')





#dropdown customer names
def dropDownCustomer(request):
    if request.method == "POST":
        if request.POST.get('cName'):
            savevalue = EmployeeReqMapping()
            savevalue.refer_Customer = request.POST.get('cName')
            savevalue.save()
            messages.success(request,'The Selected customer' +savevalue.refer_Customer+ 'is saved successfully')
            return redirect('/mappedEmployeeToCustomer')
        
        else:
            return render(request,'mappedEmployeeToCustomer')
        
def showDropDown(request):
    display_cust = EmployeeReqMapping.objects.all()

    return render(request,'showEmpToCustomer.html',{'display_cust':display_cust})


def deleteAppliedCandidates(request,e_id,reqIdPK):   
    req=Customer_Requirements.objects.get(pk=reqIdPK)
    if not request.user.is_authenticated:
        return redirect('home') 
    try:
        emp = EmployeeReqMapping.objects.get(e_id=e_id)
        status_instance=Employee.objects.get(eFname=e_id,isDeleted=False)
        status_instance.estatus='Free'
        status_instance.save()
        emp.delete()
        req.remain_positions+=1
        req.save()
    except EmployeeReqMapping.MultipleObjectsReturned:
        emp = EmployeeReqMapping.objects.filter(e_id=e_id)[0]
        emp.delete()
        status_instance=Employee.objects.get(e_id=e_id,isDeleted=False)[0]
        status_instance.estatus='Free'
        status_instance.save()
        req=Customer_Requirements.objects.get(pk=reqIdPK)
        req.remain_positions+=1
        req.save()

    messages.success(request,'The Selected Employee'  + emp.eFname +  'is deleted successfully')
    company=req.customers
    return redirect(f'/mappedEmployeeToCustomer/{company}/{reqIdPK}')


# To delete employee details
def deleteLeadSocEmployee(request, e_id):
    if not request.user.is_authenticated:
        return redirect('home')
    employee = Employee.objects.get(pk=e_id,isDeleted=False)
    employee.isDeleted=True
    employee.save()
    # employee.delete()
    return redirect("/listEmployeeFiltered/All/All/All")


# To update employee details
def updateLeadSocEmployee(request, e_id):
    if not request.user.is_authenticated:
        return redirect('home')
    employee = Employee.objects.get(pk=e_id,isDeleted=False)
    if request.method=='POST':
        ref_name=employee.eFname

        employee.eFname=request.POST['eFname']
        employee.eLname=request.POST['eLname']
        employee.refer_Customer=Customer(cName=request.POST['refer_Customer'])
        employee.eEmail=request.POST['eEmail']
        newval=Role(role_name=request.POST['eRole'])
        employee.department=Department(department=request.POST['department'])
        employee.eRole=newval
        employee.estatus=request.POST['estatus']
        employee.save()

    return redirect("/listEmployeeFiltered/All/All/All")

        
def save_emp_details(request): 
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        selected_employees = request.POST.getlist('employee_checkbox')
        for employee_id in selected_employees:
            employee = Employee.objects.get(id=employee_id,isDeleted=False)
            add_emp = EmployeeReqMapping(
                eFname=employee.eFname,
                eLname=employee.eLname,
                refer_Customer=request.user.customer,  # Assuming you have a logged-in user with a related customer
                eskills=employee.eskills
            )
            add_emp.save()
    return redirect("/listEmployeeFiltered/All/All/All")


# this is working upload employee data to model
def bulkUploadEmployee(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        #Employee_Resource = EmployeeResource()
        dataset = Dataset()
        new_employee = request.FILES['myfile']

        if not new_employee.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'upload.html')
        
        imported_data = dataset.load(new_employee.read(), format='xlsx')
        for data in imported_data:
            print("Customer name",data)
            roleName=data[8]
            custName=data[3]
            dept=data[12]
            cust=Customer.objects.filter(cName=custName)

            if cust.exists():
                print("Extsing Customer",cust)
            else :
                print("Customer does not exists")
                newCust=Customer(cName=custName,cEmail='test@gmail.com',cUrl="test.com")
                newCust.save()
            
            role=Role.objects.filter(role_name=roleName)
            if role.exists():
                print("Extsing role",role)
            else :
                print("role does not exists")
                newRole=Role(role_name=roleName)
                newRole.save()


            deptment=Department.objects.filter(department=dept)
            if deptment.exists():
                print("Extsing dept",deptment)
            else :
                print("dept does not exists")
                newDept=Department(department=dept)
                newDept.save()
               
            isManager=False  
            print('Managre',data[14])
            if data[14]==True:
                isManager=True 

            value = Employee(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
                data[13],
                isManager,
                data[15],


                )
            value.save()
 
        return redirect("/listEmployeeFiltered/All/All/All")
        
    return render(request,'upload.html')

# upload customer data to model
def customerDataUpload(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        #Employee_Resource = EmployeeResource()
        dataset = Dataset()
        new_customer = request.FILES['myfile']

        if not new_customer.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'upload.html')
        
        imported_data = dataset.load(new_customer.read(), format='xlsx')
        for data in imported_data:
            print(data[1])
            value = Customer(
                data[0],
                data[1],
                data[2],                           
                )
            value.save()
        return redirect("/listCustomers")
    
    return render(request,'upload.html')

# upload customer requirement data the model
def salesDataUpload(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        #Employee_Resource = EmployeeResource()
        dataset = Dataset()
        new_Requirements = request.FILES['file']

        if not new_Requirements.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'customer_requirement_data.html')
        
        imported_data = dataset.load(new_Requirements.read(), format='xlsx')
        for data in imported_data:
            print(data)
            custName=data[0]
            cust=Customer.objects.filter(cName=custName)

            if cust.exists():
                print("Extsing Customer",cust)
            else :
                print("Customer does not exists")
                newCust=Customer(cName=custName,cEmail='test@gmail.com',cUrl="test.com")
                newCust.save()
            value = Customer_Requirements(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],  
                data[10],
                data[11],                                                    
                )
            value.save()
        return redirect("/listSalesReqsFiltered/Choose/Choose/Choose")
        
    return render(request,'customer_requirement_data.html')

#TA Upload Excel File Option
def taDataUpload(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        dataset=Dataset()
        new_details=request.FILES['file']

        if not new_details.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'showTA.html')
        imported_data = dataset.load(new_details.read(), format='xlsx')
        for data in imported_data:
            value=TA_Resource(
                ta_id=data[0],
                archived=data[1],
                date=data[2],
                name=data[3],                
                BU=data[4],
                Position=data[5],
                skillset=data[6],
                education=data[7],
                experience=data[8],
                relevant_exp=data[9],
                current_org=data[10],
                current_ctc=data[11],
                expected_ctc=data[12],
                actual_notice_period=data[13],
                notice_period=data[14],
                current_loc=data[15],
                preferred_loc=data[16],
                phone_number=data[17],
                email=data[18],
                status=data[19],
                BU_comments=data[20],
                TA_comments=data[21],
                T1_panel=data[22],
                T1_IW_date=data[23],
                T2_panel=data[24],
                T2_IW_date=data[25],
                source=data[26],
                Rec_prime=data[27],
                Domain=data[28],
                T1=data[29],
                T2=data[30],                
                owner=Employee.objects.get(eFname=data[31],isDeleted=False),  
                resume=data[32]              
                )
            value.save()
        return redirect('/showTa')   

    return render(request,'TA_upload.html')




#Reset and login views

from urllib.parse import urlparse, urlunparse

from django.conf import settings

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

UserModel = get_user_model()


class RedirectURLMixin:
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url_allowed_hosts = set()

    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name)
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        raise ImproperlyConfigured("No URL to redirect to. Provide a next_page.")


class LoginView(RedirectURLMixin, FormView):
    """
    Display the login form and handle the login action.
    """

    form_class = AuthenticationForm
    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
            }
        )
        return context


class LogoutView(RedirectURLMixin, TemplateView):
    http_method_names = ["post", "options"]
    template_name = "registration/logged_out.html"
    extra_context = None

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            return resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                "site": current_site,
                "site_name": current_site.name,
                "title": _("Logged out"),
                "subtitle": None,
                **(self.extra_context or {}),
            }
        )
        return context


def logout_then_login(request, login_url=None):
    """
    Log out the user if they are logged in. Then redirect to the login page.
    """
    login_url = resolve_url(login_url or settings.LOGIN_URL)
    return LogoutView.as_view(next_page=login_url)(request)


def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect the user to the login page, passing the given 'next' page.
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe="/")

    return HttpResponseRedirect(urlunparse(login_url_parts))


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "/password_reset_done.html"
    title = _("Password reset sent")


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("password_reset_complete")
    template_name = "password_reset/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    #success_url = reverse_lazy("password_change_done")
    #template_name = "registration/password_change_form.html"
    #template_name = "password_reset/password_change.html"
    title = _("Password change")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    #template_name = "password_reset/password_change_done.html"
    template_name = "home.html"
    title = _("Password Change Successful")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)












