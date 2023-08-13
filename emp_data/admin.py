from import_export.admin import ImportExportModelAdmin 
from django.contrib import admin
from emp_data import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(models.UploadFile)

@admin.register(models.CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    list_display = ['username', 'email', 'role', 'emp_id','user_permissions']

@admin.register(models.Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('cName','cEmail','cUrl')
    search_fields = ['cName']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    

@admin.register(models.Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('e_id','eFname','eLname','refer_Customer','eEmail','ePhone','eExperience','eskills','eRole','estatus','leadsoc_joining_date','customer_start_date','Manager','IsManager','BUH','isDeleted')
    search_fields = ['eFname','eLname','eEmail','ePhone','eMP_Type','eRole','estatus','eskills','Manager','BUH']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(models.Customer_Requirements)
class Customer_RequirementsAdmin(ImportExportModelAdmin):
    list_display = ('reqIdPK','customers','CustReqId','RequiredSkills','JD','minExp','openPositions','reqStatus','SalesIncharge','buHead','history')
    search_fields = ['JD','RequiredSkills','SalesIncharge','buHead']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(models.EmployeeReqMapping)
class EmployeeReqMappingAdmin(ImportExportModelAdmin):
    list_display = ('req_id','name','source','department','BU','eskills')
    search_fields = ['name','eskills','department','BU']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    


@admin.register(models.EmpExperienceHistory) #CHANGING CLASS NAME
class Emp_ExperienceAdmin(ImportExportModelAdmin):
    list_display=('e_id','refer_customer','customer_start_date','customer_end_date')



@admin.register(models.TA_Resource)
class Ta_ResourceAdmin(ImportExportModelAdmin):
    list_display=('ta_id','name','skillset','education','phone_number','email')

#admin.site.register(models.VmResource)
@admin.register(models.VmResource)
class VmResourceAdmin(ImportExportModelAdmin):
    list_display=('archivalStatus','candidateName','skillset','education','mobile','email','resumeStatus','department')


admin.site.register(models.Role)
admin.site.register(models.Department)



# admin.site.register(CustomUser, CustomUserAdmin)



