import asyncio
from datetime import datetime, timedelta
from okta.client import Client as OktaClient
from os import getenv
from pathlib import Path

config = {
    'orgUrl': 'https://dev-45433294.okta.com',
    'token': getenv('OKTA_TOKEN')
}
client = OktaClient(config)
app_name = "Test-app"
file_path = Path(r"reports/unassigned_users_report.txt")
list_unassigned_users = []

async def get_app_id(client, app_name):
    """Get the id of an application by its name.

    Args:
        client: An instance of the Client class that provides methods to interact with the API.
        app_name: A string representing the name of the application.

    Returns:
        An integer representing the id of the application, or None if no such application exists.
    """
    apps, resp, err = await client.list_applications()
    for app in apps:
        if app.label == app_name:
            id = app.id
            print(f"The Test-app id is {id}")
            break
    return id

def get_days_since_last_login(user):
    """Return the number of days since the user's last login.

    Args:
        user: A user object with a last_login attribute.

    Returns:
        A timedelta object representing the difference between the current time and the user's last login time.
    """
    last_login = datetime.fromisoformat(user.last_login.replace("Z", ""))
    now = datetime.utcnow()
    diff = now - last_login
    return diff

def make_report(lines):
    """Write a list of strings to a text file.

    Args:
        lines: A list of strings to write to the file.
    """
    with open (file_path ,'w') as f:
       for line in lines:
        f.write(f"{line}\n")

async def check_last_login(app_id, app_users_list, all_users_list, list_unassigned_users):
    """Check the last login date of each user in the app and unassign them if they are inactive.

    Args:
        app_id: A string representing the id of the application
        app_users_list: A list of user objects that are assigned to the app.
        all_users_list: A list of all user objects in okta.
        list_unassigned_users: An empty list to store the unassigned users.

    Returns:
        None
    """
    for app_user in app_users_list:
        print(f'The name of the user is {app_user.profile["name"]} and the ID of the user is {app_user.id} ')
        for user in all_users_list:
            if app_user.id == user.id:
                if user.last_login is not None:
                    diff = get_days_since_last_login(user)
                    print(f'last login is before {diff}')

                    # Unassign the user if the user was inactive for more than 30 days and the user is not part of test-team                
                    if diff > timedelta(days=30) and user.profile.team != 'test-team':
                        resp, err = await client.delete_application_user(app_id, user.id)
                        list_element = f'{user.profile.firstName} {user.profile.lastName} - {user.profile.email}'
                        list_unassigned_users.append(list_element)
                else:
                    print(f'user {user.profile.first_name} has not logged into the system')
                    
    make_report(list_unassigned_users)

async def main():
    """Perform tasks related to user management and reporting.

    Args:
        None
    """
    app_id = await get_app_id(client, app_name)    
    app_users_list, resp, err = await client.list_application_users(app_id)
    all_users_list, resp, err = await client.list_users()

    await check_last_login(app_id, app_users_list, all_users_list, list_unassigned_users)                    
    make_report(list_unassigned_users)

# Run the main function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
