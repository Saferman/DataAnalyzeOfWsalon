# encoding:utf8
import sys
import pymysql
import xlsxwriter

reload(sys)
sys.setdefaultencoding('utf-8')


class DBHandle(object):
    def __init__(self,host="localhost",user="root",password="new_password",database="wsalon",debug=0):
        db = pymysql.connect(host,user,password,database,charset="utf8")
        self.db = db

    def execute_sql(self,sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def dbclose(self):
        self.db.close()

def main():
    dbh = DBHandle()
    try:
        results = dbh.execute_sql("select id,name from app_tag order by id asc")
        workbook = xlsxwriter.Workbook('tag.xlsx')
        worksheet = workbook.add_worksheet("salon_tag_name")
        # Start from the first cell below the headers.
        row = 1
        col = 0
        for item in results:
            name = item[1]
            worksheet.write(row,col,name);
            row += 1
        workbook.close()
    finally:
        dbh.dbclose()



if __name__ == '__main__':
    main()
