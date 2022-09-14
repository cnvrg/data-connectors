# Jira Connector (Library)
The Jira Connector is a library that utilizes a Jira account to extract data based on user inputs. The library then stores this data as a CSV file and provides it as input to existing inference and batch predict blueprints. A Jira account, its credentials, and its security access token are required to use this library.

Click [here](https://github.com/cnvrg/data-connectors/tree/master/jira_connector) for more information on this connector.

## Connector Flow
The following list provides this connector's high-level flow:
- The user provides inputs such as `username` and  `api_key` through cnvrg Projects > Settings > Environment.
- The user accesses and connects to the Jira API using the URL, username, and API key.
- The user completes the following to define the projects:
  - Determine whether the length of the `project_list` argument is ≤1, meaning no data is given in the argument.
  - Create a default project list including all the projects.
  - Loop on the list of projects and fetch the required data.
- The user completes the following to loop on all a project's issues:
  - Filter the required data from issues.
  - Limit the number of Jira issues to be fetched so to increase the limit:
    - Select **Administration** > **System** > **Advanced Settings**.
    - Locate `jira.search.views.default.max` and `jira.search.views.max.limit`.
    - Change the values, as required, and click **Update**.
- The connector outputs data from issues and projects and saves it in `issue_data.csv` and `project_data.csv`, respectively.

## Inputs
This library assumes the user has an existing Jira account. The Jira Connector requires the following inputs:
- `username` - Provide the account username. Select **Projects** > **Settings** > **Environment** to set the Key `USER_NAME` with the Value according to the username. Default Value: `None`.
- `api_key` - Provide the API token to access the account. Select **Projects** > **Settings** > **Environment** to set the Key `API_KEY` with the Value according to the API key. Default Value: `None`.
- `jira_url` - Provide the URL to access the Jira server. Default Value: `None`.
- `project_list`- List the projects to be fetched. Default Value: `None`.
- `project_object_list`: List the objects in each project to be fetched. Default Value: `id,key,description,assigneeType,name,projectTypeKey,simplified,style,isPrivate,entityId,uuid,lead.accountId,lead.displayName,lead.active`.
- `issue_object_list`- List the objects in each issue to be fetched. Default Value: `id,fields.summary,fields.reporter.accountId,fields.reporter.emailAddress,fields.reporter.displayName,fields.reporter.accountType,fields.assignee.accountId,fields.assignee.emailAddress,fields.assignee.displayName,fields.assignee.accountType,fields.priority.name,fields.priority.id,fields.labels,fields.created,fields.updated,fields.resolution.description,fields.resolutiondate,fields.status.description,fields.status.name,fields.status.id,fields.aggregatetimeestimate,fields.timeestimate,fields.timespent,fields.aggregatetimespent,fields.components,fields.issuetype.description,fields.issuetype.name,fields.description,fields.environment,fields.resolution.id,fields.resolution.description,fields.resolution.name`.
- `jql_query_for_issues` - Set the query to filter issues. Default Value: `None`.

## Outputs
- The connector outputs data from issues and saves it in `issue_data.csv`.
- The connector outputs data from projects and saves in `project_data.csv`.

## Troubleshooting
Complete one or more of the following steps to troubleshoot issues that may be encountered with this connector:
- Confirm the `api_key` and other parameters are valid.
- Confirm the code prints the job status simultaneously for each task completed: when the data is pulled and when the job is completed.
- Check the Experiments > Artifacts section to confirm this connector has generated the output CSV files.
- Check the logs (in the Experiments tab) for an error message. If the experiment fails, an error code displays and cnvrg enters its Debug mode, which allows limited time to review the logs and resolve the problem.

## Related Blueprints
The Jira Connector can be used with the following blueprints:
- [Task Prioritization Batch](https://metacloud.staging-cloud.cnvrg.io/marketplace/blueprints/task-prioritization-batch)
- [Document Classification Inference](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/document-classification)

