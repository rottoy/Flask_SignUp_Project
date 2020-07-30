import pymysql
from datetime import datetime

"""
table 미리 작성안해놓으면 시망이였다 ㅠㅠㅠ

"""
def connect_mysql():
	return pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='111111',
                     db='userinformation',
                     charset='utf8')


def create_schema(schema_name):
    try:
	    db= connect_mysql()
	    with db.cursor() as cursor:
		    sql= """CREATE SCHEMA `%s` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;""" % (schema_name)
		    cursor.execute(sql)
		    db.commit()
    finally:
	    db.close()

def create_table(table_name):
    try:
        db= connect_mysql()
        with db.cursor() as cursor:
            if table_name=='users':
                sql= """CREATE TABLE `userinformation`.`%s` (
                    `user_index` INT NOT NULL AUTO_INCREMENT,
                    `user_id` VARCHAR(45) NULL,
                    `user_pwd` VARCHAR(45) NULL,
                    `user_email` VARCHAR(45) NULL,
                    PRIMARY KEY (`user_index`));
                    """ % (table_name)
                cursor.execute(sql)
                db.commit()
            elif table_name=='boards':
                sql="""CREATE TABLE `userinformation`.`%s` (
                `board_idx` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                 `board_title` VARCHAR(45) NULL,
                 `board_contents` VARCHAR(300) NULL,
                 `board_writer` VARCHAR(45) NULL,
                 `board_writtentime` DATETIME NULL,
                  PRIMARY KEY (`board_idx`));
                """   % (table_name)
            else:
                return
            cursor.execute(sql)
            db.commit()
    finally:
	    db.close()

def user_insert(user_id,user_pwd,user_email):
    try:
	    db= connect_mysql()
	    with db.cursor() as cursor:
		    sql= """INSERT INTO users(user_id, user_pwd,user_email)
         VALUES('%s', '%s','%s'); """ % (user_id, user_pwd,user_email) 
		    cursor.execute(sql)
		    db.commit()
    finally:
	    db.close()

def user_select_unique(user_id):
    try:
	    db= connect_mysql()
	    with db.cursor() as cursor:
		    sql= """SELECT * FROM userinformation.users where user_id='%s'; """ % (user_id)
		    cursor.execute(sql)
		    data = cursor.fetchall()
		    return data
    finally:
	    db.close()

def board_insert(board_title,board_contents,board_writer,board_writtentime):
    try:
	    db= connect_mysql()
	    with db.cursor() as cursor:
		    sql="""INSERT INTO boards(board_title,board_contents,board_writer,board_writtentime)
							VALUES('%s','%s','%s','%s')""" % (board_title,
							board_contents,
							board_writer,
							board_writtentime)
		    cursor.execute(sql)
		    db.commit()
    finally:
	    db.close()
   
def board_select_unique(index):
    try:
	    db= connect_mysql()
	    with db.cursor() as cursor:
		    sql= """SELECT SQL_NO_CACHE * FROM userinformation.boards where board_idx='$s';""" % (index)
		    cursor.execute(sql)
		    data = cursor.fetchall()
		    return data
    finally:
	    db.close()
    
#create_table('boards')
board_insert('제목123입니다','내용입12321323니다','wnsgur9609',str(datetime.today().strftime('%Y/%m/%d %H:%M:%S')))
#user_insert('wnsgur9609','123','wnsgur9609@naver.com')