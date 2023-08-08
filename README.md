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

nohup python manage.py runserver 0.0.0.0:8000 &
gunicorn emp_data.wsgi:application --bind 0.0.0.0:8000

source /home/ec2-user/venv/bin/activate

# How to create requiremnet.txt





<!-- Note : here wsgi.py is inside management folder. Thats why management.wsgi:application is given -->

# Set up nginx
sudo yum install nginx

# new learnings for deployment

# Starting services on AWS
sudo nano /etc/systemd/system/crm.service
content below
====================
[Unit]
Description=gunicorn daemon for Your Project Name
After=network.target

[Service]
User=ec2-user  # Replace with your username
Group=ec2-user    # Replace with your user's group
WorkingDirectory=/home/ec2-user/CRM1.0
ExecStart=/home/ec2-user/venv/bin/gunicorn management.wsgi:application --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
=======================


# Commands to start service
sudo systemctl daemon-reload
sudo systemctl start crm
sudo systemctl stop crm
sudo systemctl enable crm
sudo systemctl status crm



# To remove all entries in a table
python manage.py shell -c "from emp_data.models  import Customer_Requirements; Customer_Requirements.objects.all().delete()"
python manage.py shell -c "from emp_data.models  import employeeReqMapping; employeeReqMapping.objects.all().delete()"


# To remove from git repo
git rm -r --cached path/to/folder/
git rm --cached path/to/file.ext

# To Delete branch from Git repo
git push origin --delete <branch-name>


.......

AWS Deployment
==============

sudo yum install python3 python3-pip python3-devel gcc
python3 -m venv venv
source ../venv/bin/activate


python -m pip install --upgrade pip
pip install django-admin
pip install pip-tools
pip install django-import_export
pip install django-bootstrap-v5
pip install pymysql
pip install pandas
pip install gunicorn
pip install whitenoise

pip freeze > requirements.txt
pip install -r requirements.txt
python manage.py collectstatic

gunicorn management.wsgi:application --bind 0.0.0.0:8000  --workers 4 --threads 2





