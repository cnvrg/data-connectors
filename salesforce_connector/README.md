# Pulling data from SalesForce
## _cnvrg_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This connector extracts data from SalesForce based on user inputs.

## Input
- `column_list`: It is a list of columns from salesforce that the user wants to pull.
    **Default Value -** <"Contact,Account,Order,Lead">
- `entity_definition_column_list`: List of EntityDefinition columns inside the defined columns by the user.
    **Default Value -** <"Id,Name,FirstName,LastName">
- `limit`: Limit for the number of records to be pulled.
    **Default Value -** None
-	`start_date`: This parameter is used to filter the _createdDate_ field on the basis of _start_date_
    **Default Value -** 7 days before current date
-	`end_date`: This parameter is used to filter the _createdDate_ field on the basis of _end_date_
    **Default Value -** Current date 
## Code Flow
- User inputs such as: **username**, **password** and  **security_token** needs to be defined in _projects>settings>environment on the cnvrg platform
- Bulk queries for pulling data in bulk from salesforce are initiated which pulls the data which is appended to a final dataframe
- Each iteration calls for the _data_extraction_ function:
    - In data extraction function, an _soql_ query coupled with the _bulk_ query is initiated to pull data from salesforce
    - Result is stored in a dataframe and returned from the function
- The final output dataframe is generated after the data cleaning is performed based on the _fields_to_get_ key

## Joining Tables
- User can join multiple tables according to their requirement based on following `keys`

|Account |Contact |Lead |Order | 
|---|---|---|---|
|Account - Id |Contact - AccountId |Lead - OwnerId |Order - AccountId | 
|Account - ParentId |Contact - OwnerId |Lead - ConvertedAccountId |Order - CreatedById |
|Account - OwnerId |Contact - CreatedById |Lead - ConvertedContactId | |
|Account - CreatedById | |Lead - ConvertedOpportunityId | |
|Account - ParentId | |Lead - CreatedById | |

## Output
-   Data from EntitiyDefination columns is saved in `Name_EntityDefinition_Dataframe.csv`
-	Data from columns requested by the user is saved in `Output.csv`

## Error Handling
-   In case the code is ran successfully, the status and the logs can be checked in the experiment tab. 
-   The code prints the job status simultaneously for each task completed
    - when the data is pulled
    - when the job is completed.
-  In case of an error, the experiment fails, the code gets into debug mode and the logs display the error msg.
