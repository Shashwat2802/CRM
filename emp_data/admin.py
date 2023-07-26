from import_export.admin import ImportExportModelAdmin 
from django.contrib import admin
from emp_data import models

admin.site.register(models.UploadFile)

@admin.register(models.Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('cName','cEmail','cUrl')
    search_fields = ['cName']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    

@admin.register(models.Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('e_id','eFname','eLname','refer_Customer','eEmail','ePhone','eExperience','eskills','eRole','estatus','leadsoc_joining_date','customer_start_date','Manager','IsManager','BUH')
    search_fields = ['eFname','eLname','eEmail','ePhone','eMP_Type','eRole','estatus','eskills','Manager','BUH']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(models.Customer_Requirements)
class Customer_RequirementsAdmin(ImportExportModelAdmin):
    list_display = ('reqIdPK','customers','Customer_Requirement_id','Required_skills','Job_Description','Required_Experience','Open_positions','Position_Status','Sales_Incharge','Bu_head','history')
    search_fields = ['Job_Description','Required_skills','history']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(models.EmployeeReqMapping)
class EmployeeReqMappingAdmin(ImportExportModelAdmin):
    list_display = ('id','req_id','name','eskills')
    search_fields = ['eFname','eLname','eskills']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    


@admin.register(models.EmpExperienceHistory) #CHANGING CLASS NAME
class Emp_ExperienceAdmin(ImportExportModelAdmin):
    list_display=('e_id','refer_customer','customer_start_date','customer_end_date')



@admin.register(models.TA_Resource)
class Ta_ResourceAdmin(ImportExportModelAdmin):
    list_display=('ta_id','name','skillset','education','phone_number','email')

admin.site.register(models.VmResource)

admin.site.register(models.Role)
admin.site.register(models.Department)

@admin.register(models.Mappedempremarks)
class Mappedremarksadmin(ImportExportModelAdmin):
    list_display=('remark_id','remark')

