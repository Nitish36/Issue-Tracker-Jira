import requests
from requests.auth import HTTPBasicAuth
import gspread
from gspread_dataframe import set_with_dataframe
import os
import pandas as pd
import json

def push_data():
    email = 'nitish.pkv@gmail.com'
    api_token = os.getenv("JIRA_SECRET")  # Get Jira API token from secret
    server = 'https://nitish36.atlassian.net'

    jql = 'project = "IT" AND created >= -30d'

    url = f"{server}/rest/api/3/search"

    params = {
        "jql": jql,
        "maxResults": 100,
        "fields": "key,issuetype,customfield_10071,customfield_10073,statusCategory,created,priority,assignee,summary,labels"
    }

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        auth=HTTPBasicAuth(email, api_token)
    )

    data = response.json()

    issues = []
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    for issue in data["issues"]:
        fields = issue["fields"]
        print(json.dumps(issue["fields"], indent=5))
        issues.append({
            "Jira Issue Key": issue["key"],
            "Jira Ticket Type": fields["issuetype"]["name"],
            "Description": fields["summary"],
            "Client ID": fields["customfield_10071"],
            "City": fields["customfield_10073"]["value"] if fields["customfield_10073"] else "",
            "Status": fields["statusCategory"]["name"],
            "Issue Date": fields["created"],
            "Priority": fields["priority"]["name"],
            "Label": fields["labels"],
            "Assigned Person": fields["assignee"]["emailAddress"] if fields["assignee"] else "",
        })

    return issues

def write_df():
    issues = push_data()
    df = pd.DataFrame(issues)
    GSHEET_NAME = 'Issue Tracker Jira'
    TAB_NAME = 'Dump'

    # Get Google credentials JSON string from env and parse
    gsheet_secret = os.getenv("GSHEET_SECRET")
    if not gsheet_secret:
        print("Google Sheets secret not found in environment.")
        return

    # Write the JSON to a temporary file
    credentialsPath = "temp_gsheet_credentials.json"
    with open(credentialsPath, "w") as f:
        f.write(gsheet_secret)

    try:
        gc = gspread.service_account(filename=credentialsPath)
        sh = gc.open(GSHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)
        set_with_dataframe(worksheet, df)
        print("Data loaded successfully!! Have fun!!")
        print(df)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(credentialsPath):
            os.remove(credentialsPath)

write_df()
