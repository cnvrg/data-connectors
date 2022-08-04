# Pulling data from Jira
## _cnvrg_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This connector extracts data from SalesForce based on user inputs.

## Input
- `username`: User name of the account. User can set the username in the environment variables with key as USER_NAME
    **Default Value -** <None>
- `api_key`: api token to access the account. User can set the api key in the environment variables with key as API_KEY
    **Default Value -** <None>
- `jira_url`: url to access jira server
    **Default Value -** <None>
-	`project_list`: List of projects to be fetched
    **Default Value -** <None>
-	`project_object_list`: List of objects in each project to be fetched
    **Default Value -** <"id,key,description,assigneeType,name,projectTypeKey,simplified,style,isPrivate,entityId,uuid,lead.accountId,lead.displayName,lead.active">
-	`issue_object_list`: List of objects in each issue to be fetched
    **Default Value -** <"id,fields.summary,fields.reporter.accountId,fields.reporter.emailAddress,fields.reporter.displayName,fields.reporter.accountType,fields.assignee.accountId,fields.assignee.emailAddress,fields.assignee.displayName,fields.assignee.accountType,fields.priority.name,fields.priority.id,fields.labels,fields.created,fields.updated,fields.resolution.description,fields.resolutiondate,fields.status.description,fields.status.name,fields.status.id,fields.aggregatetimeestimate,fields.timeestimate,fields.timespent,fields.aggregatetimespent,fields.components,fields.issuetype.description,fields.issuetype.name,fields.description,fields.environment,fields.resolution.id,fields.resolution.description,fields.resolution.name">
-	`jql_query_for_issues`: Query to filter issues
    **Default Value -** <None>
## Code Flow
- User inputs such as: **username** and  **api_key** needs to be defined in **projects->settings->environment_variables** on the cnvrg platform or the user can give them as arguments
- Access the jira api with the help of url, username and api key
- Hit jira server url
- Define projects
    - See if the length of the project_list argument is <=1 meaning no data is given in the argument
    - Make a default project list including all the projects
    - Loop on list of projects and fetch required data 
    - Filter the required project objects from the data

- Loop on all issues in a project:
    - Filter required data from issues
    - Jira Issues limit the number of issues to be fetched so to increase the limit:
        -  Go to: Administration > System > Advanced Settings.
        -  Find jira.search.views.default.max and jira.search.views.max.limit.
        -  Change the values as desired, and click update.
## Output
-   Data from issues is saved in `issue_data.csv`
-	Data from projects is saved in `project_data.csv`

## Error Handling
-   In case the code is ran successfully, the status and the logs can be checked in the experiment tab. 
-   The code prints the job status simultaneously for each task completed
    - when the data is pulled
    - when the job is completed.
-  In case of an error, the experiment fails, the code gets into debug mode and the logs display the error msg.