"""management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from emp_data import views
from django.urls import include
from django.views.generic.base import TemplateView
from django.conf import settings 
from django.conf.urls.static import static 
from emp_data.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings

# django admin customization
admin.site.site_header = "LeadSoc Admin "
admin.site.site_title = "Welcome to Admin Dashboard"
admin.site.index_title = "Welcome to LeadSoc Technologies PVT LTD."


    
urlpatterns = [   
             
    path('admin/', admin.site.urls),
    
    path('getMessagesJson/', getMessagesJson, name='getMessagesJson'),

    path("bulkUploadEmployee",views.bulkUploadEmployee),
    path("customerDataUpload",views.customerDataUpload),
    path('salesDataUpload',views.salesDataUpload),
    path("home",views.home),
    
   # customer requirements details
    path('listSalesReqsFiltered/<str:bu>/<str:sales>/<str:st>',views.filteredSaleReqs),
    path('listEmployeeFiltered/<str:department>/<str:buh>/<str:manager>',views.listEmployeeFiltered),

    path("addCommentsToVmCandidate/<int:reqIdPK>", views.addCommentsToVmCandidate),
    path("addSalesReqComment/<int:reqIdPK>", views.addSalesReqComment),
    path('getEmployeeExperiances/<str:employee_id>/', views.getEmployeeExperiances, name='getEmployeeExperiances'),

    path("cust_req_dropdown/<str:ref>", views.cust_req_dropdown),

    path("save_emp_details", views.save_emp_details, name="save_emp_details"),
    path('addSalesReqs',views.addSalesReqs),
    path('JD',views.JD),  
    path('freeFromAllSource/<int:reqIdPK>',views.freeFromAllSource),
    path('mapEmpToReq/<int:reqIdPK>/<str:choice>',views.mapEmpToReq),
    path('mappedEmployeeToCustomer/<int:reqIdPK>',views.mappedEmployeeToCustomer),
    #path("addCommentToEmployeedReqTable/<int:reqIdPK>/<str:source>/<str:sourceId>", views.addCommentToEmployeedReqTable),
    #path("addCommentToEmployeedReqTable/<int:pk>/<int:reqIdPK>",views.addCommentToEmployeedReqTable),
    path('showTaList/<int:reqIdPK>',views.showTaList),
    path('showVmList/<int:reqIdPK>',views.showVmList),
    path("addCommentToEmpReqSelect/<int:pk>/<int:reqIdPK>",views.addCommentToEmpReqSelect),    

    #path('selection_status/<str:estatus>/<int:reqIdPK>', views.selection_status),
    path('selection_status/<str:estatus>/<int:reqIdPK>/<int:pk>', views.selection_status),
    path('checkbox',views.checkbox),
    path('dropDownCustomer',views.dropDownCustomer),
    path('showDropDown',views.showDropDown),
    path('updateSaleReqs/<int:reqIdPK>',views.updateSaleReqs),
    path('deleteAppliedCandidates/<str:source>/<str:namearg>/<int:reqIdPK>', views.deleteAppliedCandidates),
    path('addResumeToMappedEmployees/<int:pk>/<int:reqIdPK>',views.addResumeToMappedEmployees),

     #Customer paths 
    path('addCustomer', views.addCustomer),
    path('listCustomers', views.listCustomers),
    path('updateCustomers/<str:cName>', views.updateCustomers),
    path('deleteCustomer/<str:cName>', views.deleteCustomer), 

    #employee paths
    path('addEmployee', views.addEmployee),
    path('deleteLeadSocEmployee/<str:e_id>', views.deleteLeadSocEmployee),
    path('updateLeadSocEmployee/<str:e_id>', views.updateLeadSocEmployee),

    #TA Path
    path('addTa',views.addTa),   
    path('taDataUpload',views.taDataUpload),
    path('deleteTa/<int:phone_number>',views.deleteTa),
    path('showTa/<str:department>/<str:buhead>/<str:archivestatus>',views.showTa),
    path('updateTaDetails/<str:ta_id>',views.updateTaDetails),
    path('taResume/<str:ta_id>',views.addTaResume),
    path('addCommentsToTaCandidate/<str:ta_id>',views.addCommentsToTaCandidate),


    path('addEmployeeExperience/<str:e_id>',views.addEmployeeExperience),
    path('deleteEmployeeExperience/<int:exp_id>', views.deleteEmployeeExperience),
    
    # employee deleted from customer
    path('deleteAppliedCandidates/<str:name>/<int:reqIdPK>', views.deleteAppliedCandidates),
    path('salesSummary',views.salesSummary),

    #For VM page
    path("showVm/<str:buh>/<str:dept>/<str:status>", views.showVm),
    path("addVm", views.addVm),
    path("vmDataUpload", views.vmDataUpload),
    path("updateVmCandidate/<int:vmIdPK>", views.updateVmCandidate),
    #Homepage path
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('PasswordChangeDoneView', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('PasswordChangeView', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_resetPasswordResetCompleteView', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('PasswordResetConfirmView/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm.html'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),

    #inbuilt login path
    path('accounts/', include('django.contrib.auth.urls')),
    
]
#for Media Storage 
if settings.DEBUG: 
        urlpatterns += static(settings.STATIC_URL,
                               document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 