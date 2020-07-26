from flask import Flask , render_template , request , redirect
import pymysql
#flask를 구동 시키기 위한 어플리케이션 인스턴스 생성
app = Flask(__name__)

#parameter 'db' : schema name
db= pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='401230',
                     db='userinformation',
                     charset='utf8')


@app.route("/")
def hello():
	return "hello world!"

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
			with db.cursor() as cursor:
				sql ="""SELECT * FROM userinformation.users where user_id='%s'; """ % (user_id)
				cursor.execute(sql)
				
				data = cursor.fetchall()
				print(data)
				if len(data)>0:
					if data[0][2]==user_password:
						return redirect('/main')
					else:
						return render_template('error.html',error='Wrong password!')
				else:
					return render_template('error.html',error='아이디가 존재하지 않습니다!')
			
		except Exception as e:
			db.close()
			return render_template('error.html',error=str(e))

		return "실패!"

@app.route('/main')
def main_page():
	return render_template('main_page.html')

if __name__ == "__main__":
	app.run()
	
#TODO
	#sql 질의로 response반환 - 성공
	#파싱을 하는데 json으로 하는게 아니네? 이것도 나중에 알아보자.
				
	#사용자가 임의로 mainPage에 접근을 못하게 막아야함!

	#try , finally안에서 return 하면 finally 실행안되지 않음? =>네!
	#db를 언제 열고 언제 닫는게 좋습니까?
	#받아온 데이터 형이tuple인데 어떻게 파싱합니끼?