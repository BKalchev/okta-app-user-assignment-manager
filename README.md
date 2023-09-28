## User Management and Reporting
This is a Python project that uses the Okta API to perform tasks related to user management and reporting. 
### It can:

- Check the last login date of each user assigned to a specific application
- Unassign the users who have been inactive for more than 30 days and are not part of a certain team
- Generate a report of the unassigned users and save it to a text file

## Installation
To run this project, you need:

- Python 3.7 or higher
- An Okta account and an API token
- The Okta SDK for Python, which you can install with:

```sh
pip install okta
```

## Usage
To use this project, you need to:

- Set the OKTA_TOKEN environment variable to your API token value
- Modify the config dictionary in the code to match your Okta organization URL
- Modify the app_name variable in the code to match the name of the 
application you want to check
- Modify the file_path variable in the code to specify the path and name of the text file where you want to save the report
- Run the code with:

```sh
python3 unassign_user.py
```
The code will print some information to the console and write the report to the text file. You can open the text file to see the names and emails of the unassigned users.

## Schedule
This project can also run in a scheduled workflow every Friday using GitHub Actions. The workflow file **action.yml** contains a schedule event that triggers the workflow at 00:00 UTC every Friday. The workflow will perform the same tasks as described in the Usage section. It will save the report as an artifact with a name **unassigned_users_report** containing the *unassigned_users_report.txt* file. 

You can modify the cron expression in the schedule event to change the frequency or time of the schedule.
