import requests
from requests.auth import HTTPBasicAuth
import json
import os

from requests.models import Response


def create_worklog(*, message='I did some work here.', duration=60, issue_id='GC002SD0002-710'):
    """
    Create worklog for specific issue
    """
    url = f"http://192.168.213.40:8080/rest/api/latest/issue/{issue_id}/worklog"
    auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_PASSWORD"))
    headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
    }

    payload = json.dumps({
                    "comment": message,
                    "timeSpentSeconds": duration
                    })

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )

    return response 


def get_open_issues_list():
    """
    List of open issues
    """
    url = f"http://192.168.213.40:8080/rest/api/latest/search?jql=assignee=currentUser() and status in (Open, \"In Progress\")"
    auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_PASSWORD"))
    headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=auth)

    with open('tasks.json', 'w') as f:
        json.dump(response.json(), f, indent=4)

    for issue in response.json().get("issues"):
        print(issue['key'])
    return response 

def main():
    # create_worklog(message='I did some work here.', duration=60, issue_id='GC002SD0002-710')
    get_open_issues_list()

if __name__ == '__main__':
    main()










