import requests
from jira.exceptions import UnknownError, InvalidIDError, NotFoundIDError, NotAuthenticatedError, PermissionError


class Client(object):
    API_URL = 'rest/api/2/'
    WEBHOOK_URL = 'rest/webhooks/1.0/'

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def get_permissions(self, params=None):
        """Returns all permissions in the system and whether the currently logged in user has them.
        You can optionally provide a specific context to get permissions for (projectKey OR projectId OR issueKey OR
        issueId)

        When no context supplied the project related permissions will return true if the user has that permission in
        ANY project.

        If a project context is provided, project related permissions will return true if the user has the permissions
        in the specified project. For permissions that are determined using issue data (e.g Current Assignee), true will
        be returned if the user meets the permission criteria in ANY issue in that project.

        If an issue context is provided, it will return whether or not the user has each permission in that specific
        issue.

        The above means that for issue-level permissions (EDIT_ISSUE for example), hasPermission may be true when no
        context is provided, or when a project context is provided, but may be false for any given (or all) issues. This
        would occur (for example) if Reporters were given the EDIT_ISSUE permission. This is because any user could be
        a reporter, except in the context of a concrete issue, where the reporter is known.

        Global permissions will still be returned for all scopes.

        Args:
            params:

        Returns:

        """
        return self._get(self.API_URL + 'mypermissions', params=params)

    def get_all_projects(self, params=None):
        """Returns all projects visible for the currently logged in user, ie. all the projects the user has either
        'Browse projects' or 'Administer projects' permission. If no user is logged in, it returns all projects that are
        visible for anonymous users.

        Args:
            params:

        Returns:

        """
        return self._get(self.API_URL + 'project', params=params)

    def get_project_issues(self, project=None, params=None):
        """Return all projects issues.
        To obtain a key for the first issue use get_project_issues("MYPROJ")[0]['key']

        Args:
            params:

        Returns:
            List of all issues that belong to a project.
        """
        all_issues = list()
        start_str=''
        while True:
            issues = self._get(self.API_URL + 'search?jql=project="' + project + '"' + start_str, params=params)
            all_issues.extend(issues['issues'])
            start_str = '&startAt='+str(int(issues['startAt']) + int(issues['maxResults']))
            if int(issues['startAt']) + int(issues['maxResults']) >= int(issues['total']): break
        #if not project
        return all_issues
    
    def get_issue(self, issue_id, params=None):
        """Returns a full representation of the issue for the given issue key.

        The issue JSON consists of the issue key and a collection of fields. Additional information like links to
        workflow transition sub-resources, or HTML rendered values of the fields supporting HTML rendering can be
        retrieved with expand request parameter specified.

        The fields request parameter accepts a comma-separated list of fields to include in the response. It can be used
        to retrieve a subset of fields. By default all fields are returned in the response. A particular field can be
        excluded from the response if prefixed with a "-" (minus) sign. Parameter can be provided multiple times on a
        single request.

        By default, all fields are returned in the response. Note: this is different from a JQL search - only navigable
        fields are returned by default (*navigable).


        Args:
            issue_id:
            params:

        Returns:

        """
        return self._get(self.API_URL + 'issue/{}'.format(issue_id), params=params)

    def get_issue_worklogs(self, issue=None, params=None):
        """Return all issue worklogs.

        Args:
            params:

        Returns:
            List of all worklogs that belong to an issue.
        """
        worklog = self._get(self.API_URL + 'issue/' + issue + '/worklog/', params=params)
        return worklog['worklogs']

    def create_issue(self, data, params=None):
        """Creates an issue or a sub-task from a JSON representation.

        You can provide two parameters in request's body: update or fields. The fields, that can be set on an issue
        create operation, can be determined using the /rest/api/2/issue/createmeta resource. If a particular field is
        not configured to appear on the issue's Create screen, then it will not be returned in the createmeta response.
        A field validation error will occur if such field is submitted in request.

        Creating a sub-task is similar to creating an issue with the following differences:
        issueType field must be set to a sub-task issue type (use /issue/createmeta to find sub-task issue types), and

        You must provide a parent field with the ID or key of the parent issue.

        Args:
            data:
            params:

        Returns:

        """
        return self._post(self.API_URL + 'issue', data=data, params=params)

    def delete_issue(self, issue_id, params=None):
        """Deletes an individual issue.

        If the issue has sub-tasks you must set the deleteSubtasks=true parameter to delete the issue. You cannot delete
        an issue without deleting its sub-tasks.

        Args:
            issue_id:
            params:

        Returns:

        """
        return self._delete(self.API_URL + 'issue/{}'.format(issue_id), params=params)

    def get_webhook(self, webhook_id, params=None):
        return self._get(self.WEBHOOK_URL + 'webhook/{}'.format(webhook_id), params=params)

    def get_all_webhooks(self, params=None):
        return self._get(self.WEBHOOK_URL + 'webhook', params=params)

    def create_webhook(self, data):
        return self._post(self.WEBHOOK_URL + 'webhook', data=data)

    def delete_webhook(self, webhook_id, params=None):
        return self._delete(self.WEBHOOK_URL + 'webhook/{}'.format(webhook_id), params=params)

    def find_assignable_users(self, params=None):
        """Returns a list of users that match the search string. This resource cannot be accessed anonymously. Please
        note that this resource should be called with an issue key when a list of assignable users is retrieved for
        editing. For create only a project key should be supplied. The list of assignable users may be incorrect if it's
        called with the project key for editing.

        Args:
            params:

        Returns:

        """
        return self._get(self.API_URL + 'user/assignable/search', params=params)

    def get_create_issue_meta(self, params=None):
        """Returns the metadata for creating issues. This includes the available projects, issue types, fields (with
        information whether those fields are required) and field types. Projects, in which the user does not have
        permission to create issues, will not be returned.

        The fields in the createmeta response correspond to the fields on the issue's Create screen for the specific
        project/issuetype. Fields hidden from the screen will not be returned in the createmeta response.

        Fields will only be returned if expand=projects.issuetypes.fields is set.

        The results can be filtered by project and/or issue type, controlled by the query parameters.

        Args:
            params:

        Returns:

        """
        return self._get(self.API_URL + 'issue/createmeta', params=params)

    def _get(self, path, params=None):
        response = requests.get(self.host + path, params=params, auth=(self.user, self.password))
        return self._parse(response)

    def _post(self, path, params=None, data=None):
        response = requests.post(self.host + path, params=params, json=data, auth=(self.user, self.password))
        return self._parse(response)

    def _delete(self, path, params=None):
        response = requests.delete(self.host + path, params=params, auth=(self.user, self.password))
        return self._parse(response)

    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            try:
                r = response.json()
            except Exception as e:
                r = None
        else:
            r = response.text
        if status_code in (200, 201):
            return r
        if status_code == 204:
            return None
        message = None
        try:
            if 'errorMessages' in r:
                message = r['errorMessages']
        except Exception:
            message = 'No error message.'
        if status_code == 400:
            raise InvalidIDError(message)
        if status_code == 401:
            raise NotAuthenticatedError(message)
        if status_code == 403:
            raise PermissionError(message)
        if status_code == 404:
            raise NotFoundIDError(message)
        raise UnknownError(message)
