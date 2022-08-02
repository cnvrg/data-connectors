# Pulling data from hubspot
## _cnvrg_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This connector extracts data from hubspot based on user inputs.

## Input
- `object_list`: It is a list of objects from hubspot that the user wants to pull.
    **Default Value -** <"deals,Companies,contacts,Feedback_submissions,Line_items,products,tickets,quotes,calls,emails,meetings,notes.tasks">
- `access_token`: List of EntityDefinition columns inside the defined columns by the user.
    **Default Value -** cnvrg connector app token
- `count`: Limit for the number of records to be pulled.
    **Default Value -** 500
- `association_id_list`: list of id's to be assiciated.
    **Default Value -** None
- `object_type`: Object to be associated.
    **Default Value -** None
- `to_object_type`: Object to be associated with.
    **Default Value -** None
## Code Flow
- User inputs such as: **access_token** needs to be defined in _projects>settings>secrets_ on the cnvrg platform.
- Bulk queries for pulling data in bulk from hubspot are initiated which pulls the data which is appended to multiple dataframes according to their objects.
- Each iteration hits object specific api in the user defined app:
    - user needs to create an app to access objects and generate an api.
    - to create an app follow integrations -> Private Apps -> Create a private app -> Scopes -> CRM -> check the objects you want to fetch -> generate api
    - copy the generated api and provide it as an argument for access_token.
- Each iteration calls the api and fetches data for the objects specified in the list.
- Seperate dataframes as csv for each objects is created.

## Joining Tables
- User can join multiple tables according to their requirement based on associations.

## Output
-   Data from multiple objects is saved in object named dataframes `{object}.csv`
-   Data from associated objects is saved in dataframe names `ObjectType_toObjectType.csv`

## Error Handling
-   In case the code is ran successfully, the status and the logs can be checked in the experiment tab. 
-   The code prints the job status simultaneously for each task completed:
    - when the data is pulled.
    - when the job is completed.
-  In case of an error, the experiment fails, the code gets into debug mode and the logs display the error msg.
