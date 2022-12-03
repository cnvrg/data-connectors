# MySQL Connector

This connector extracts data from MySQL databases, filtering based on user inputs. The Data that is extracted needs further processing to make it suitable for attaching alongside other blueprints, like Churn Prediction or Sentiment Analysis, depending on the type of database pinged.

## Input
- `credentials`: comma separated string containing host name, user name and password.
    **Default Value -** 'host,user,password'
- `databases`: names of the databases that you want to ping for data, separated by comma (,).
    **Default Value -** - 'database1,database2'
- `tables_views`: comma/exclamation-mark separated string containing table names and view names. comma separates tables and views while exclamation mark separates tables from views
    **Default Value -** - 'Employees,Mentors"!"temp_employee'
-	`tables_views_columns`: list of columns, on whom the filtering needs to be applied. columns of same table or view are separated by comma, while columns of two tables are separted by pipe and columns of tables and views are separated from each other by exclamation mark. 
    _**Note :- If the user wants default data, specify this field as "None"**_
    **Default Value -** name,dept,salary"|"mentorid"!"dept,joindate
-	`tables_columns_filters`: list of values to filter, for the columns specified in the field "tables_views_columns". The separations are the same as the above field.
    **Default Value -** "Geralt,Irenicus,Marine,Ranger"!"Maths,Biology"!"">"1000,"<"2000,AND"|"1,2"
-	`views_columns_filters`: list of values to filter, for the columns specified in the field "tables_views_columns". The separations are the same as the above field. only this time, its for views than tables
    **Default Value -** "Chemistry"!""<"1984-01-01,">"1985-01-01"
-   `custom_query`: any custom query that the user wants to write in case they want to join two tables
    **Default Value -** "select a.* from table a inner join table b on a.col1 = b.col2"
-   `columns_to_filter`: the columns which will appear in the final csv files. Columns of the same table are separated by comma, while commas of multiple tables are separated by pipe. View columns are separated from table columns by exclamation mark.
    **Default Value -** "id,salary"|"mentordept,mentorid"!"id,joindate"

## Code Flow
- User inputs (**credentials**) needs to be defined in the  _environment_  tab on the cnvrg platform
- In case the user wants to join two different tables, they can specify that in the custom query
- The connector supports both tables and views as well as filtering of data
- Each table will have a separate csv in the output artifacts

## Output
-   'Table_'+table_name+'.csv'
-   'View_'+view_name+'.csv'
-   'custom_table.csv'

## How to run
```
ython3 mysql_connector.py --credentials yourcreds --databases sql9578677 --tables_views Employees,Mentors"!"temp_employee --tables_views_columns name,dept,salary"|"mentorid"!"dept,joindate --tables_columns_filters Geralt,Irenicus,Marine,Ranger"!"Maths,Biology"!"">"1000,"<"2000,AND"|"1,2 --views_columns_filters Chemistry"!""<"1984-01-01,">"1985-01-01 --custom_query "select a.id, a.name, a.dept, a.salary, a.mentorid, a.isdisabled, a.joindate, b.mentordept, b.mentorexp from Employees a inner join Mentors b on a.mentorid = b.mentorid" --columns_to_filter id,salary"|"mentordept,mentorid"!"id,joindate
```
## Creating Tables and Views in MySQL Workbench
```
Go to Terminal and type the following
1. 'sudo apt install mysql-server'
2. 'sudo snap connect mysql-workbench-community:password-manager-service :password-manager-service'
3. 'sudo mysql'
4. ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pwd'

Then Open mysql workbench and connect to database. Use the following data as show below: -
1. Stored Connection: Local Instance 3306
2. Connection Method : Standard TCP/IP
3. Hostname = localhost
4. Port : 3308
5. Username : root
6. Password : whatever you gave in the step 4 (in my case its root)

Then create a schema and some tables by following these instructions
1. Open python and write these commands 
a. pip install mysql-connector-python
b. mydb = mysql.connector.connect(
     host="localhost",
  	 user="root",
  	 password="root",
  	 database="Testing"
   )
c. cursor = mydb.cursor()
d. query2 = "select * from Employees"
e. cursor.execute(query2)
f. table = cursor.fetchall()
g. mydb.commit() ]only to be run in case of creation queries rather than fetching queries]
```
## References
[MySQL Workbench Guide](https://www.mysql.com/products/workbench/)
[MySQL Query Guide](https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/examples.html)
[MySQL Python Connector Library)](https://pypi.org/project/mysql-connector-python/)
