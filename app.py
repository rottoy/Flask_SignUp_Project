from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import pymysql
from datetime import datetime
#flask를 구동 시키기 위한 어플리케이션 인스턴스 생성
app = Flask(__name__)

app.secret_key = 'i am preventing unauthorized user'

#parameter 'db' : schema name



def connect_mysql():
	return pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='401230',
                     db='userinformation',
                     charset='utf8')
db= connect_mysql()

@app.route("/")
def hello():
	return render_template('intro.html')

@app.route("/register", methods=['GET','POST'])
def register():
	if request.method=='GET':
		return render_template("register.html")
	else :

		userid = request.form.get('user_id')
		userpassword = request.form.get('user_password')
		userrepassword=request.form.get('user_re_password')
		emailaddress=request.form.get('email_address')
	
		if not (userid and userpassword and emailaddress):
			return "모두 입력해주세요"
		elif userpassword!=userrepassword:
			return "비밀번호가 일치하지 않습니다."
		else:
			try:
				db= connect_mysql()
				with db.cursor() as cursor:
					sql= """INSERT INTO users(user_id, user_pwd,user_email)
         VALUES('%s', '%s','%s'); """ % (userid, userpassword,emailaddress) 
					cursor.execute(sql)
					db.commit()
			finally:
				db.close()

				print(userid)
				print(userpassword)
				print(userrepassword)
				print(emailaddress)
				return "회원가입 완료!"
		
		return "회원가입에 실패함! db에 들어가지 않음!"
		#return redirect('/')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('login.html')
	else :
		user_id = request.form['user_id']
		user_password = request.form['user_password']
		try:
			db= connect_mysql()
			with db.cursor() as cursor:
				sql ="""SELECT * FROM userinformation.users where user_id='%s'; """ % (user_id)
				cursor.execute(sql)
				
				data = cursor.fetchall()
				print(data)
				if len(data)>0:
					if data[0][2]==user_password:
						session['users'] = user_id
						return redirect('/main')
					else:
						return render_template('error.html',error='Wrong password!')
				else:
					return render_template('error.html',error='아이디가 존재하지 않습니다!')
		except Exception as e:
			return render_template('error.html',error=str(e))	
		finally:
			db.close()

	return "실패!"

#Session Needed URL
@app.route('/main')
def main_page():
	if session.get('users'):
		try:
			db= connect_mysql()
			with db.cursor() as cursor:
				sql ="""SELECT SQL_NO_CACHE board_title, board_contents, board_writer, board_writtentime FROM userinformation.boards;"""
				
				cursor.execute(sql)
				boards=cursor.fetchall()
				
				cursor.close()
				for board in boards:
					print(str(board))
				
				return render_template('main_page.html', boards=boards)
		except Exception as e:
			return render_template('error.html',error=str(e))
		finally:
			db.close()
		
		
	else:
		return render_template('error.html',error='유효하지 않은 접근입니다.')



if __name__ == "__main__":
	app.run()
	
#TODO
	#sql 질의로 response반환 - 성공
	#파싱을 하는데 json으로 하는게 아니네? 이것도 나중에 알아보자.
				
	#사용자가 임의로 mainPage에 접근을 못하게 막아야함!

	#try , finally안에서 return 하면 finally 실행안되지 않음? =>네!
	#db를 언제 열고 언제 닫는게 좋습니까?
	#받아온 데이터 형이tuple인데 어떻게 파싱합니끼?
	#세션은 서버가 들고있는 스택같은 개념이군요?
	#근데 서버가 꺼졌다 켜져도 세션이 유지되는 원리가 무엇인가요?
	
	#html에 있는 {{}} 라던가 {% for %} 이런 문법은 어디에서 나오는 것인가요?
	#서버와 클라이언트 간은 form으로 데이터를 교환해서 파싱하기가 쉬운데,
	#데이터베이스에서 데이터를 파싱하려면 그냥 [0][1] 이렇게 요소 인덱스로 파싱해야되나요? 너무 주먹구구인데

	#내부에서 갱신하려면 백엔드가 아닌 프론트에서 작업해야 하는데, 이는 귀찮음.
	
