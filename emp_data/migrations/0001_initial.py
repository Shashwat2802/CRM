# Generated by Django 4.2.3 on 2023-07-24 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "cName",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("cEmail", models.EmailField(max_length=254, null=True)),
                ("cUrl", models.CharField(max_length=50, null=True)),
            ],
            options={
                "db_table": "customer",
            },
        ),
        migrations.CreateModel(
            name="Customer_Requirements",
            fields=[
                (
                    "Customer_Requirement_id",
                    models.CharField(max_length=100, null=True),
                ),
                ("Required_skills", models.TextField()),
                ("Job_Description", models.TextField()),
                ("Required_Experience", models.FloatField(default=0)),
                ("Open_positions", models.IntegerField(default=0)),
                ("remain_positions", models.IntegerField(default=0)),
                ("Position_Status", models.CharField(max_length=10)),
                ("Sales_Incharge", models.CharField(max_length=50, null=True)),
                ("Bu_head", models.CharField(max_length=50, null=True)),
                ("history", models.TextField(default="")),
                ("reqIdPK", models.AutoField(primary_key=True, serialize=False)),
                ("priority", models.IntegerField(default=1)),
                (
                    "customers",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="emp_data.customer",
                    ),
                ),
            ],
            options={
                "db_table": "customer_requirements",
            },
        ),
        migrations.CreateModel(
            name="EmpExperienceHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("e_id", models.CharField(max_length=5)),
                ("refer_customer", models.CharField(max_length=100, null=True)),
                ("customer_start_date", models.DateField(null=True)),
                ("customer_end_date", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "e_id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("eFname", models.CharField(max_length=50, null=True)),
                ("eLname", models.CharField(max_length=50, null=True)),
                ("BU", models.CharField(max_length=50, null=True)),
                ("BUH", models.CharField(max_length=50, null=True)),
                ("Manager", models.CharField(max_length=100, null=True)),
                ("eEmail", models.EmailField(max_length=200, null=True)),
                ("ePhone", models.CharField(max_length=50, unique=True)),
                ("eExperience", models.IntegerField(default=0, null=True)),
                ("eskills", models.CharField(max_length=100, null=True)),
                ("estatus", models.CharField(max_length=100, null=True)),
                ("leadsoc_joining_date", models.DateField(null=True)),
                ("customer_start_date", models.DateField(null=True)),
            ],
            options={
                "db_table": "employee",
            },
        ),
        migrations.CreateModel(
            name="Employee_Details",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Login",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("UserName", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=32)),
            ],
            options={
                "db_table": "login",
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "role_name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UploadFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("specifications", models.FileField(upload_to="router_specifications")),
            ],
        ),
        migrations.CreateModel(
            name="VmResource",
            fields=[
                ("position_status", models.CharField(max_length=100)),
                ("pr_date", models.DateField()),
                ("vendor_name", models.CharField(max_length=100)),
                ("candidate_source", models.CharField(max_length=100)),
                ("candidate_name", models.CharField(max_length=300)),
                ("resume", models.CharField(max_length=1000)),
                ("skillset", models.CharField(max_length=500)),
                ("experience", models.FloatField()),
                ("education", models.CharField(max_length=500)),
                ("billing_rate", models.FloatField()),
                ("bu_head", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=500)),
                ("notice_period", models.IntegerField()),
                ("reviewer_name", models.CharField(max_length=100)),
                ("remarks_panel", models.CharField(max_length=500)),
                ("vm_comment", models.CharField(max_length=1000)),
                ("client_name", models.CharField(max_length=100)),
                ("interview_schedule", models.DateField()),
                ("interview_status", models.CharField(max_length=100)),
                ("comments", models.CharField(max_length=1000)),
                ("remarks", models.CharField(max_length=1000)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.IntegerField()),
                ("mode", models.CharField(max_length=500)),
                (
                    "vmIdPK",
                    models.AutoField(default=0, primary_key=True, serialize=False),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="emp_data.employee",
                    ),
                ),
            ],
            options={
                "db_table": "VmResource",
            },
        ),
        migrations.CreateModel(
            name="TA_Resource",
            fields=[
                (
                    "ta_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("archived", models.CharField(max_length=100)),
                ("date", models.DateField()),
                ("name", models.CharField(max_length=300)),
                ("resume", models.CharField(max_length=1000)),
                ("BU", models.CharField(max_length=100)),
                ("Position", models.CharField(max_length=100)),
                ("skillset", models.CharField(max_length=500)),
                ("education", models.CharField(max_length=500)),
                ("experience", models.FloatField()),
                ("relevant_exp", models.FloatField()),
                ("current_org", models.CharField(max_length=500)),
                ("current_ctc", models.FloatField()),
                ("expected_ctc", models.FloatField()),
                ("actual_notice_period", models.IntegerField()),
                ("notice_period", models.IntegerField()),
                ("current_loc", models.CharField(max_length=500)),
                ("preferred_loc", models.CharField(max_length=500)),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                ("email", models.EmailField(max_length=254)),
                ("status", models.CharField(max_length=100)),
                ("BU_comments", models.CharField(max_length=1000)),
                ("TA_comments", models.CharField(max_length=1000)),
                ("T1_panel", models.CharField(max_length=100)),
                ("T1_IW_date", models.DateField()),
                ("T2_panel", models.CharField(max_length=100)),
                ("T2_IW_date", models.DateField()),
                ("source", models.CharField(max_length=500)),
                ("Rec_prime", models.CharField(max_length=500)),
                ("Domain", models.CharField(max_length=100)),
                ("T1", models.CharField(max_length=100)),
                ("T2", models.CharField(max_length=100)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="emp_data.employee",
                    ),
                ),
            ],
            options={
                "db_table": "TA_Resource",
            },
        ),
        migrations.CreateModel(
            name="EmployeeReqMapping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, null=True)),
                ("eskills", models.CharField(max_length=100, null=True)),
                ("estatus", models.CharField(max_length=100, null=True)),
                ("empstatus", models.CharField(default="", max_length=100, null=True)),
                ("added_date", models.DateField(null=True)),
                (
                    "source",
                    models.CharField(default="LEADSOC", max_length=100, null=True),
                ),
                ("sourceid_1", models.CharField(max_length=10, null=True)),
                ("sourceid_2", models.CharField(max_length=10, null=True)),
                ("sourceid_3", models.IntegerField(default=0)),
                ("history", models.TextField(default="")),
                (
                    "req_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="emp_data.customer_requirements",
                    ),
                ),
            ],
            options={
                "db_table": "employeereqmapping",
            },
        ),
        migrations.AddField(
            model_name="employee",
            name="eRole",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="emp_data.role"
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="refer_Customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="emp_data.customer"
            ),
        ),
    ]
