# jira-python

jira-python is an API wrapper for JIRA written in Python

## Installing
```
pip install jira-python
```

## Usage
```
from jira.client import Client

client = Client('HOST', 'USER', 'PASSWORD') # Host must have trailing slash
```

Get user permissions
```
response = client.get_permissions()
```

Get all projects
```
response = client.get_all_projects()
```

Get an issue
```
response = client.get_issue('ISSUE_ID)
```

Create an issue
```
data = {'fields':
             {'description': 'Issue description',
              'reporter': {'name': 'ingmferrer'},
              'assignee': {'name': 'ingmferrer'},
              'project': {'id': '10400'},
              'issuetype': {'id': '10002'},
              'summary': 'Issue summary'}}

response = client.create_issue(data)
```

Delete an issue
```
response = client.delete_issue('ISSUE_ID')
```

Get metadata for issues
```
response = client.get_create_issue_meta()
```

Get metadata for issues
```
response = client.get_create_issue_meta()
```


### Webhooks
Get a webhook
```
response = client.get_webhook('WEBHOOK_ID')
```

Get all webhooks
```
response = client.get_all_webhooks()
```

Get all webhooks
```
data = {
    "name": "Webhook",
    "url": "https://mywebsite.com/notification_url/",
    "events": [
        "jira:issue_created"
    ],
    "jqlFilter": "Project = KEY", #Change KEY to your project key. Project key != project id
    "excludeIssueDetails": False
}
response = client.create_webhook(data)
```

Delete a webhook
```
response = client.delete_webhook()
```
