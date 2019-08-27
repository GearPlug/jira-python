# jira-python

jira-python is an API wrapper for Jira Software written in Python.

This library uses API version 2 and Basic Authentication for requests.

If you are looking for Jira Software Cloud using OAuth 2.0 (3LO) and the latest API version: https://github.com/ingmferrer/jira-cloud-python

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

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.
#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/GearPlug/jira-python/issues).
#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/GearPlug/jira-python )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
