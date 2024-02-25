from jira import JIRA
import csv
import yaml

def fetch_issues(jira, project_key, fix_version, fields):
    jql_query = f'project = {project_key} AND fixVersion = {fix_version}'
    issues = jira.search_issues(jql_query, fields=fields, maxResults=False)
    return issues

def write_to_csv(issues, csv_file_path, fieldnames):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for issue in issues:
            writer.writerow({field: getattr(issue.fields, field, '') for field in fieldnames})

def main():
    # Load configuration from YAML file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Jira server credentials
    JIRA_SERVER = config['jira']['server']
    JIRA_API_TOKEN = config['jira']['api_token']
    JIRA_USERNAME = config['jira']['username']

    # Initialize Jira client
    jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

    # Project details
    project_key = config['project']['key']
    fix_version = config['project']['fix_version']

    # Fields to fetch from Jira
    fields = config['fields']

    # Fetch issues
    issues = fetch_issues(jira, project_key, fix_version, fields)

    # CSV file path
    csv_file_path = 'jira_issues.csv'

    # Write issues to CSV
    write_to_csv(issues, csv_file_path, fields)

    print(f'Jira issues exported to {csv_file_path}')

if __name__ == "__main__":
    main()
