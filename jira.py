import requests
from requests.auth import HTTPBasicAuth
import json
import os

def create_worklog(*, message='I did some work here.', duration=60, issue_id='GC002SD0002-710'):
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

    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    print(response.text) 


def main():
    create_worklog(message='I did some work here.', duration=60, issue_id='GC002SD0002-710')

if __name__ == '__main__':
    main()










