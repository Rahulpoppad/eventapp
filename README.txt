Deploying the application

Prerequisites:
    - AWS account
    - Access Key ID and Access Key Secret and Default Region configured via the aws command line interface.
    - Python3.11 

Step 1: Setup an RDS database and note the connections credentials:
    - host name
    - port
    - database user
    - databse name
    - database password

    Insert the above values in settings.py in the following fields of DATBASES settings. Replace with the existing sqlite3 database settings:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'database name',
                'USER': 'databse user',
                'PASSWORD': 'database password',
                'HOST': 'host name',
                'PORT': '5432',
            }
        }

    Note the subnet and security group ids for the RDS instance and insert them as follows in a zapp_settings.json
        "vpc_config": {
            "SubnetIds": [
                "subnet-id1",
                "subnet-id2",
                "subnet-id3"
            ],
            "SecurityGroupIds": [
                "sg-security-group-id"
            ]
        }

Step 2: Create an S3 bucket with ACLs allowed and ensure you allow public access as well. add the following cors policy to its permissions.

    [
        {
            "AllowedHeaders": [
                "Authorization"
            ],
            "AllowedMethods": [
                "GET",
                "PUT",
                "POST"
            ],
            "AllowedOrigins": [
                "*"
            ],
            "ExposeHeaders": [],
            "MaxAgeSeconds": 3000
        }
    ]

    Also append the following to the settings.py file and replace the bucket-name with your S3 bucket's name:

        AWS_S3_BUCKET = "bucket-name"

        STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
        AWS_S3_BUCKET_NAME_STATIC = AWS_S3_BUCKET

        # These next two lines will serve the static files directly 
        # from the s3 bucket
        AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_S3_BUCKET
        STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

Step 3: Setting up gmail SMTP server:
        Visit and create an app and note the password and fill it in the EMAIL_HOST_PASSWORD field. Change EMAIL_HOST_USER's value to your google account's email address

            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            EMAIL_HOST = 'smtp.gmail.com'
            EMAIL_USE_TLS = True
            EMAIL_PORT = 587
            EMAIL_HOST_USER = 'youremailaddress@gmail.com'
            EMAIL_HOST_PASSWORD = 'replace_with_your_app_password'

Step 4: Setup a virtual environment in your app and install all the dependencies:
    install zappa with pip
    i.e pip install zappa

    'zappa init' initalizes the zappa_setting.json file follow the prompts corrctly.


Step 5: Deploy:
    zappa deploy dev

    On success, a link is provided to the app, click to verify the app is up and running.

Step 6: Create migrations and push the updated code.

        python manage.py makemigrations
        zappa update dev

    Now you invoke the zappa manage command to migrate and write table to the database:

        zappa manage dev migrate

    Create a superuser:

        zappa invoke --raw dev "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@yourdomain.com', 'admin', 'admin', 'password')"