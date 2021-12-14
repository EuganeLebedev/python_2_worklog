import requests
from requests.auth import HTTPBasicAuth
import json
import os

from requests.models import Response


def create_worklog(*, comment, duration=60, issue_id):
    """
    Create worklog for specific issue 
    """
    url = f"{os.getenv('JIRA_URL')}/rest/api/latest/issue/{issue_id}/worklog"
    auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_PASSWORD"))
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "comment": comment,
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
    url = f"{os.getenv('JIRA_URL')}/rest/api/latest/search?jql=assignee = currentUser() AND status in (Open, \"In Progress\") and project != \"Гросвер Груп. 2019-12. SAP B1\""
    auth = HTTPBasicAuth(os.getenv("JIRA_USER"), os.getenv("JIRA_PASSWORD"))
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=auth)
    with open('results.json', 'w') as f:
        json.dump(json.loads(response.text), f, indent=4)

    return response


def get_typical_issues_list():
    """
    List of typical issues
    """
    url = f"{os.getenv('JIRA_URL')}/rest/api/latest/search?jql=project = GC AND issuetype = \"Typical task\" and status != Close"
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
    create_worklog(comment='I did some work here.',
                   duration=60, issue_id='GC-1479')


if __name__ == '__main__':
    main()
