# Flow Files

## Purpose
This application will load Meter Readings flow files of ElectraLink Data Transfer Catalogue (DTC), and displays the data in Django's admin site. 

## Assumptions
- Developed with: Python version 3.8, Django version 3.2
- Disregarded a scenario where more than one record with "028" (Meter/Reading Types) associated with one "026" (MPAN Core)

---
## Instructions
Follow the steps below to setup environment, ingest sample data, log in, and view the data.

### Set up environment
Necessary environment can be set up by running the following commands.
1. python -m venv <VENV_NAME>
2. cd <VENV_NAME>
3. source bin/activate
4. git clone https://github.com/kttyo/flow_files.git
5. pip install -r flow_files/requirements.txt

### Ingest sample data file
Set up database and ingest the sample data file by running the following commands.
1. cd flow_files
2. python manage.py migrate
3. python manage.py file_ingestion DTC5259515123502080915D0010.uff

### Log in
Create a super user account and log in to the application by running the following commands.
1. python manage.py createsuperuser
2. (Instruction) Set up the following information
- Username (ex. 'test_user')
- Email address (ex. 'test_user@example.com')
- Password (ex. 'testpassword')
3. python manage.py runserver

### View Reading Data
Log in to the application and view the data by following the steps below.
1. Access http://127.0.0.1:8000 in a web browser
2. Enter the credentials created in the previous step to log in
3. Click on "Register_readings" on the left side of the screen
4. Enter MPAN or Meter Serial Number into the search field

### Other Commands
- Run "python manage.py refresh_db_tables" to delete all data from database and move files back from "ingested_files".
- Run "python manage.py file_ingestion" to ingest all .uff files in the "file_inbox" folder. (I created a dummy file named "DMY5259515123502080915D0010.uff" so it can be ingested with this command)

---
## To do
### Very quick
- Display some kind of message when a file name is already present in the files table -> **Done**
- Fix the repeating "s" at the end of model names in admin site -> **Done**
- Set an appropriate time zone -> **Done**
- Modify namings of variables, functions, etc -> **Done**
- Add try-except clause for file opener and object creation -> **Done**

### May take some time
- Fix the bug that 1 record is falsely missing in the register_reading table (solution displayed in 'cleaner_code.jpg') -> **Done**
- Simplify the for-loop in file_ingestion.py (solution displayed in 'cleaner_code.jpg') **-> Done**
- Write an automated test to compare the records loaded to the register_readings table and the number of records with '030' -> **Done**
- Add logging configuration -> **Done**
- Handle the warnings for naive datetime -> **Done**
- Add a function to move the loaded file to a separate folder -> **Done**
- Add a command and function to bulk ingest multiple files in the inbox folder -> **Done**
- Make adjustments for records other than '026', '028', or '030' that might be included in the D0010 file
---
## Ideas for Improvement
- When a file path is not passed to "file_ingestion" command, all the files present in the file_inbox folder gets processed -> **Done**
- If more functionality is needed in the admin site, (separate search fields, filtering by date and time) , we can consider creating a view
- Footer record in the D0010 file seems to have record count information, so it might become useful in data validation
- Depending on how we would like implement REST interface, we can move some parts of the "file_ingestion" function to some other module, so the view can use the same module
