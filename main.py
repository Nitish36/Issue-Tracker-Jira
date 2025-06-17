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

def read_write():
    # Link= https://drive.google.com/file/d/11jlteTm-QzYHt105qe3mdlWfJ1xC2K7w/view?usp=sharing
    url = "https://drive.google.com/uc?export=download&id=11jlteTm-QzYHt105qe3mdlWfJ1xC2K7w"
    dataset = pd.read_csv(url)
    dataset.columns = dataset.columns.str.strip()
    print("Columns:", dataset.columns.tolist())

    # Select the relevant columns
    data = {
        "Jira Issue Key": dataset["Jira Issue Key"],
        "Jira Ticket Type": dataset["Jira Ticket Type"],
        "Description": dataset["Description"],
        "Client ID": dataset["Client ID"],
        "City": dataset["City"],
        "Status": dataset["Status"],
        "Issue Dateonly": dataset["Issue Dateonly"],
        "Priority": dataset["Priority"],
        "Assigned Person": dataset["Assigned Person"],
        "Escalation Needed": dataset["Escalation Needed"],
        "Escalation Reason": dataset["Escalation Reason"],
        "Issue Resolved": dataset["Issue Resolved"],
        "Issue Resolved Date": dataset["Issue Resolved Date"],
        "Issue Raised Week": dataset["Issue Raised Week"],
        "Issue Resolved Week": dataset["Issue Resolved Week"],
        "Resolution Ageing": dataset["Resolution Ageing"],
        "Resolution TAT": dataset["Resolution TAT"],
        "Resolution TAT <=2": dataset["Resolution TAT <=2"],
        "Current Date": dataset["Current Date"],
        "Issue Raised MY": dataset["Issue Raised MY"],
        "Issue Resolved MY": dataset["Issue Resolved MY"],
    }
    final_data = pd.DataFrame(data)
    final_data['Issue Dateonly'] = pd.to_datetime(final_data['Issue Dateonly'], errors='coerce')
    final_data['Issue Resolved Date'] = pd.to_datetime(final_data['Issue Resolved Date'], errors='coerce')
    final_data['Current Date'] = pd.to_datetime(final_data['Current Date'], errors='coerce')

    GSHEET_NAME = 'Issue Tracker'
    TAB_NAME = 'Issue'
    gsheet_secret = os.getenv("GSHEET_SECRET_KEY")
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
        set_with_dataframe(worksheet, final_data)
        print("Data loaded successfully!! Have fun!!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(credentialsPath):
            os.remove(credentialsPath)

write_df()
read_write()
