import os
import mysql.connector
import pandas as pd
import argparse

def table_creation_unfiltered(databases, tables_split, filter_col_names_table, j, i, host, user, password):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=databases[i]
    )
    cursor = mydb.cursor(buffered=True)
    individual_table = tables_split[j]
    query = "select * from "+databases[i]+'.'+tables_split[j]
    cursor.execute(query)
    mydb.commit()
    table = cursor.fetchall()
    field_names = [cnter[0] for cnter in cursor.description]
    cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
    filename = os.path.join(cnvrg_workdir, 'Table_'+individual_table+'.csv')
    final_frame = pd.DataFrame(table, columns=field_names)
    print('checkpint')
    print(filter_col_names_table)
    if filter_col_names_table != 'None':
        columns_to_filter = filter_col_names_table.split('|')
        filter_col_names = columns_to_filter[j].split(',')
        filter_col_names = [x.replace('"', '') for x in filter_col_names]
        final_frame_last = final_frame[filter_col_names]
    final_frame_last = final_frame
    cursor.close()
    return final_frame_last, filename

def table_creation_filtered(databases, tables_split, pre_table_filters, j, individual_table_cols, i, filter_col_names_table, host, user, password):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=databases[i]
    )
    cursor = mydb.cursor(buffered=True)
    individual_table = tables_split[j]
    # columns of first table in string format
    col_split = individual_table_cols[j]
    query = "select * from " + databases[i] + '.' + tables_split[j]
    table_filters = pre_table_filters[j].split('!')
    for m in range(len(table_filters)):
        print(m)
        if ('>' in table_filters[m]) or ('<' in table_filters[m]):
            value_column = col_split.split(',')[m]
            base_condition = ''
            if len(table_filters[m].split(',')) > 0:
                for k in range(len(table_filters[m].split(','))-1):
                    print(k)
                    col_filter = table_filters[m].split(
                        ',')[k].replace('"', '')
                    temp_cond = col_filter[0] + " '" + col_filter[1:] + "'"
                    if k == 0:
                        condition = base_condition + value_column + ' ' + temp_cond
                    else:
                        condition = condition + ' ' + \
                            table_filters[m].split(
                                ',')[2] + ' ' + value_column + ' ' + temp_cond
                condition = '('+condition+')'
            else:
                condition = base_condition + value_column + ' ' + temp_cond
            if m != 0:
                query = query + " and " + condition
                print(query)
            else:
                query = query + " where " + condition
                print(query)
        else:
            value_column = col_split.split(',')[m]
            temp_cond = ','.join(
                ['"'+x+'"' for x in table_filters[m].split(',')])
            condition = value_column + ' in (' + temp_cond + ')'
            if m != 0:
                query = query + " and " + condition
            else:
                query = query + ' where ' + condition
    cursor.execute(query)
    mydb.commit()
    table = cursor.fetchall()
    field_names = [cnter[0] for cnter in cursor.description]
    cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
    filename = os.path.join(cnvrg_workdir, 'Table_'+individual_table+'.csv')
    print('Lohgarh')
    print(filename)
    if filter_col_names_table != 'None':
        print('Khalsae')
        columns_to_filter = filter_col_names_table.split('|')    
        final_frame = pd.DataFrame(table, columns=[field_names])
        filter_col_names = columns_to_filter[j].split(',')
        filter_col_names = [x.replace('"', '') for x in filter_col_names]
        final_frame_last = final_frame[filter_col_names]
        print(final_frame_last)
    else:
        final_frame_last = final_frame
    cursor.close()
    return final_frame_last, filename


def custom_function(custom_query, database, i, host, user, password):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database[i]
    )
    cursor = mydb.cursor(buffered=True)
    query = custom_query
    cursor.execute(query)
    mydb.commit()
    table = cursor.fetchall()
    field_names = [cnter[0] for cnter in cursor.description]
    final_frame = pd.DataFrame(table, columns=[field_names])
    cursor.close()
    return final_frame

def mysql_main():
    
    parser = argparse.ArgumentParser(description="""Creator""")
    parser.add_argument(
        "-f",
        "--credentials",
        action="store",
        dest="credentials",
        default="localhost,root,root",
        required=True,
        help="""host,user,password""",
    )
    parser.add_argument(
        "--databases",
        action="store",
        dest="databases",
        default="Testing",
        required=True,
        help="""Databases which you want to hit""",
    )
    parser.add_argument(
        "--tables_views",
        action="store",
        dest="tables_views",
        default="Employees,Mentors!temp_employee",
        required=True,
        help="""the names of tables and views whose data you want to extract""",
    )
    parser.add_argument(
        "--tables_views_columns",
        action="store",
        dest="tables_views_columns",
        default="name,dept,salary:mentorid!dept,joindate",
        required=True,
        help="""The columns of those tables which need to be subset""",
    )
    parser.add_argument(
        "--tables_columns_filters",
        action="store",
        dest="tables_columns_filters",
        default="Geralt,Irenicus,Marine,Ranger!Maths,Biology!1,2",
        required=True,
        help="""the column values whose data is supposed to be extracted""",
    )
    parser.add_argument(
        "--views_columns_filters",
        action="store",
        dest="views_columns_filters",
        default="Chemistry!<1984-01-01",
        required=True,
        help="""the column values whose data is supposed to be extracted""",
    )
    parser.add_argument(
        "--custom_query",
        action="store",
        dest="custom_query",
        default="SELECT * FROM Testing.Employees where dept = Chemistry",
        required=True,
        help="""the column values whose data is supposed to be extracted""",
    )
    parser.add_argument(
        "--columns_to_filter",
        action="store",
        dest="columns_to_filter",
        default="id,salary:mentordept,mentorid!id,joindate",
        required=True,
        help="""the columns on which the data will be filtered on""",
    )
    
    args = parser.parse_args()
    databases = args.databases.split(',')
    views = args.tables_views.split('!')[1]
    tables = args.tables_views.split('!')[0]
    table_columns = args.tables_views_columns.split('!')[0]
    try:
        view_columns = args.tables_views_columns.split('!')[1]
    except:
        view_columns = args.tables_views_columns.split('!')[0]
    pre_table_filters = args.tables_columns_filters.split('|')
    view_filters = args.views_columns_filters.split('!')
    custom_query = args.custom_query
    filter_col_names_table = args.columns_to_filter.split('!')[0]
    filter_col_names_view = args.columns_to_filter.split('!')[1]
    cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")
    print('comparison')
    print(args.tables_views.split('!'))
    if os.environ.get('host') != 'None':
        print('Using Env Variables')
        host = os.environ['host']
        user = os.environ['user']
        password = os.environ["pwd"]
        print(host)
        print('host')
        print(user)
        print('user')
        print(password)
        print('password')
    else:
        print('Using Argument Parser Variables')
        host = args.credentials[0]
        user = args.credentials[1]
        password = args.credentials[2]

    if args.custom_query == 'None':
        for i in range(len(databases)):
            if tables != 'None':
                print('Moh')
                print(table_columns)
                print('Maya')
                print(pre_table_filters)
                if table_columns == 'None' or pre_table_filters == 'None':
                    tables_split = tables.split(',')
                    for j in range(len(tables_split)):
                        print('Torture')
                        print(tables_split)
                        final_frame_last, filename = table_creation_unfiltered( databases, tables_split, filter_col_names_table, j, i, host, user, password)
                        final_frame_last.to_csv(filename)
                else:
                    tables_split = tables.split(',')
                    individual_table_cols = table_columns.split('|')
                    for j in range(len(tables_split)):
                        print('Goku')
                        print(tables_split[j])
                        print('Gohan')
                        print(individual_table_cols[j])
                        print('Seven')
                        final_frame_last, filename = table_creation_filtered(databases, tables_split, pre_table_filters, j, individual_table_cols, i, filter_col_names_table, host, user, password)
                        final_frame_last.to_csv(filename)

            if views != 'None':
                if view_columns == 'None' or view_filters == 'None':
                    views_split = views.split(',')
                    for jj in range(len(views_split)):
                        final_view_last, viewname = table_creation_unfiltered( databases, views_split, filter_col_names_view, jj, i, host, user, password)
                        final_view_last.to_csv(viewname)
                else:
                    views_split = views.split(',')
                    individual_view_cols = view_columns.split('|')
                    for j in range(len(views_split)):
                        final_view_last, viewname = table_creation_filtered(
databases, views_split, view_filters, j, individual_view_cols, i, filter_col_names_view, host, user, password)
                        final_view_last.to_csv(viewname)
    else:
        for i in range(len(databases)):
            final_frame = custom_function(args.custom_query, databases, i, host, user, password)
            final_frame.to_csv('/cnvrg/custom_table.csv')

if __name__ == '__main__':
    mysql_main()
    
#https://ofa-beijing.oss-cn-beijing.aliyuncs.com/checkpoints/caption_base_best.pt