# MySQL Connector (Library)
This connector library extracts user-filtered data from the MySQL databases. The extracted data requires further processing to make it suitable for attaching alongside other blueprints, like [Churn Detection](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/churn-detection-train) or [Sentiment Analysis](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/sentiment-analysis-train), depending on the type of database pinged.

Click [here](https://github.com/cnvrg/data-connectors/tree/mysql/mysql_connector) for more information on this connector.

## Connector Flow
The following list provides this connector's high-level flow:
- The user defines his/her credentials in cnvrg Projects > Settings > Environment.
- The user specifies in a custom query whether to join two different tables.
- The connector run supports both tables and views as well as data filtering.
- The connector outputs a separate CSV for each table.

## Inputs
This library assumes the user has an existing MySQL account. The user's MySQL credentials (to pull data from) are required as input, which can be obtained from the user's MySQL account.
The MySQL Connector requires the following inputs:
- `credentials` (comma separated string) − Provide the host name, user name, and password. Default: `host,user,password`.
- `databases` (comma separated string) − Provide the database names to ping for data. Default: `database1,database2`.
- `tables_views` (comma/exclamation-mark separated string) − Define the table names and view names, using a comma to separate tables and views and an exclamation mark to separate tables from views. Default: `"Employees,Mentors"!"temp_employee"`.
- `tables_views_columns` − Provide a list of columns to apply the filtering, with the columns of the same table or view separated by a comma, the columns of two tables separted by a pipe, and the columns of tables and views separated from each other by exclamation mark. Default: `"name,dept,salary"|“mentorid”!"dept,joindate"`.
NOTE: If default data is desired, specify this field as `None`.
- `tables_columns_filters` − List the values to filter for the columns specified in the `tables_views_columns` field. The same separations apply as the above field. Default: `“Geralt,Irenicus,Marine,Ranger”!“Maths,Biology”!"">“1000,”<“2000,AND”|“1,2”`.
- `views_columns_filters` − List the values to filter for the columns specified in the `tables_views_columns` field. The same separations apply as the above field, except now it is for views rather than tables. Default: `“Chemistry”!""<“1984-01-01,”>“1985-01-01”`.
- `custom_query` − Run a custom query, as desired, to join two tables. Default: `“select a.* from table a inner join table b on a.col1 = b.col2”`.
- `columns_to_filter` − Define the columns to appear in the final CSV files, with columns of the same table separated by comma, columns of multiple tables separated by pipe, and view columns separated from table columns by exclamation mark. Default: `“id,salary”|“mentordept,mentorid”!“id,joindate”`.

## Run Instructions
The code requires [Python 3](https://www.python.org/) installed on your system to run. Run the following example command:

```
python3 mysql_connector.py --credentials yourcreds --databases sql9578677 --tables_views Employees,Mentors"!"temp_employee --tables_views_columns name,dept,salary"|"mentorid"!"dept,joindate --tables_columns_filters Geralt,Irenicus,Marine,Ranger"!"Maths,Biology"!"">"1000,"<"2000,AND"|"1,2 --views_columns_filters Chemistry"!""<"1984-01-01,">"1985-01-01 --custom_query "select a.id, a.name, a.dept, a.salary, a.mentorid, a.isdisabled, a.joindate, b.mentordept, b.mentorexp from Employees a inner join Mentors b on a.mentorid = b.mentorid" --columns_to_filter id,salary"|"mentordept,mentorid"!"id,joindate
```

## Outputs
The connector outputs the following three CSV files:
- `‘Table_’+table_name+’.csv’`
- `‘View_’+view_name+’.csv’`
- `‘custom_table.csv’`

## Troubleshooting
Complete one or more of the following steps to troubleshoot issues that may be encountered with this connector:
- Confirm the MySQL account credentials are valid.
- Check the job status, which cnvrg displays simultaneously for each task completed: when the data is pulled and when the job is completed.
- Check the Experiments > Artifacts section to confirm this connector has generated the output CSV files.
- Check for an error code, which displays if the experiment fails and cnvrg enters Debug mode, which allows limited time to check the logs in the Experiments tab to resolve the problem.

## Tables and Views in MySQL Workbench
Follow the instructions below to create tables and views in MySQL Workbench: 
```
Go to Terminal and type the following:
1. 'sudo apt install mysql-server'
2. 'sudo snap connect mysql-workbench-community:password-manager-service :password-manager-service'
3. 'sudo mysql'
4. ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pwd'

Then, open MySQL Workbench and connect to database. Use the following data listed:
- Stored Connection: Local Instance 3306
- Connection Method: Standard TCP/IP
- Hostname = localhost
- Port: 3308
- Username: root
- Password: whatever provided in the previous step 4 (in this case it's root)

Now, create a schema and some tables by opening Python and running the following commands:
1. pip install mysql-connector-python
2. mydb = mysql.connector.connect(
     host="localhost",
  	 user="root",
  	 password="root",
  	 database="Testing"
   )
3. cursor = mydb.cursor()
4. query2 = "select * from Employees"
5. cursor.execute(query2)
6. table = cursor.fetchall()
7. mydb.commit() ]only to be run in case of creation queries rather than fetching queries]
```

## Related Blueprints
The MySQL Connector can be used with the following blueprints:
- [Churn Detection Train](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/churn-detection-train)
- [Sentiment Analysis Train](https://metacloud.cloud.cnvrg.io/marketplace/blueprints/sentiment-analysis-train)

## References
- [MySQL Workbench Guide](https://www.mysql.com/products/workbench/)
- [MySQL Query Guide](https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/examples.html)
- [MySQL Python Connector Library)](https://pypi.org/project/mysql-connector-python/)
