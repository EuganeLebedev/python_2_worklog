import requests
from requests.auth import HTTPBasicAuth
import json
import os

from requests.models import Response


def create_worklog(*, message, duration=60, issue_id):
    """
    Create worklog for specific issue 
    """
    url = f"{os.getenv('JIRA_URL')}/rest/api/latest/issue/{issue_id}/worklog"
    # url = f"{os.getenv('JIRA_URL')}/rest/api/latest/issue/GC002SD0002-710/worklog"
    auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_PASSWORD"))
    headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
    }

    payload = json.dumps({
                    "comment": message,
                    "timeSpentSeconds": duration
                    })

    # payload = json.dumps({
    #             "comment": 'test',
    #             "started": '2021-12-13T00:00:00.000+0000',
    #             "timeSpentSeconds": 60
    #             })

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )
    print(response.status_code, response.text)

    return response 


def get_open_issues_list():
    """
    List of open issues
    """
    url = f"{os.getenv('JIRA_URL')}/rest/api/latest/search?jql=assignee=currentUser() and status in (Open, \"In Progress\")"
    auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_PASSWORD"))
    headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=auth)
    with open('results.json', 'w') as f:
        json.dump(json.loads(response.text), f, indent=4)

    return response 

def main():
    # create_worklog(message='I did some work here.', duration=60, issue_id='GC002SD0002-710')
    create_worklog(message='I did some work here.', duration=60, issue_id='GC-1479')

if __name__ == '__main__':
    main()










