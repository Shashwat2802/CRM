# employee-Company-management-Sytem-using-Django

0.1 : Create Virtual Env
python3 -m venv myenv

0.2 : source /Users/raghuvallikkat/Desktop/LEADSOC_CODE/myenv/bin/activate

0.3: python -m pip install --upgrade pip

0.4 pip install django-admin

0.5 : pip install pip-tools

0.6 : pip install django-import_export

0.7 : pip install django-bootstrap-v5

0.8 : pip install pymysql

0.9 : pip install pandas



steps to Run This Poject
-------------------------

1. open VS code create you own directory,create virtual environment and
Run "Git pull origin master"

Creating all the table for database
--------------------------------
2. python manage.py makemigrations emp_data

3. python manage.py migrate

Create superuser
----------------
4. python manage.py createsuperuser
Please enter username, password,confirm password
To run the project
------------------

5. python manage.py runserver
6. copy generated IP Adress and paste into the browser, output will be visible. 



# To remove all entries in a table
python manage.py shell -c "from emp_data.models  import Customer_Requirements; Customer_Requirements.objects.all().delete()"
python manage.py shell -c "from emp_data.models  import employeeReqMapping; employeeReqMapping.objects.all().delete()"
