import requests
from requests.auth import HTTPBasicAuth
import json
import os
from db import get_user

from requests.models import Response


def create_worklog(*, comment, duration=60, issue_id, user_id):
    """
    Create worklog for specific issue 
    """
    JIRA_USER, JIRA_PASSWORD = get_user(user_id)
    if JIRA_USER and JIRA_PASSWORD:
        url = f"{os.getenv('JIRA_URL')}/rest/api/latest/issue/{issue_id}/worklog"
        auth = HTTPBasicAuth(JIRA_USER, JIRA_PASSWORD)
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
    return None


def get_open_issues_list(user_id):
    """
    List of open issues
    """
    JIRA_USER, JIRA_PASSWORD = get_user(user_id)
    if JIRA_USER and JIRA_PASSWORD:
        if JIRA_USER == 'e.lebedev@grosver.com':
            url = f"{os.getenv('JIRA_URL')}/rest/api/latest/search?jql=assignee = currentUser() AND status in (Open, \"In Progress\") and project != \"Гросвер Груп. 2019-12. SAP B1\""
        else:
            url = f"{os.getenv('JIRA_URL')}/rest/api/latest/search?jql=assignee = currentUser() AND status in (Open, \"In Progress\")"
        auth = HTTPBasicAuth(JIRA_USER, JIRA_PASSWORD)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.request("GET", url, headers=headers, auth=auth)

        return response
    return None


def get_typical_issues_list(user_id):
    """
    List of typical issues
    """
    JIRA_USER, JIRA_PASSWORD = get_user(user_id)
    if JIRA_USER and JIRA_PASSWORD:
        url = f"{os.getenv('JIRA_URL')}/rest/api/latest/search?jql=project = GC AND issuetype = \"Typical task\" and status != Close"
        auth = HTTPBasicAuth(JIRA_USER, JIRA_PASSWORD)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.request("GET", url, headers=headers, auth=auth)

        return response
    return None


def main():
    create_worklog(comment='I did some work here.',
                   duration=60, issue_id='GC-1479')


if __name__ == '__main__':
    main()
