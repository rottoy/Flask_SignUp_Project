from flask import Flask , render_template , request , redirect

#flask를 구동 시키기 위한 어플리케이션 인스턴스 생성
app = Flask(__name__)

@app.route("/")
def hello():
	return "hello world!"


@app.route("/register", methods=['GET','POST'])
def register():
	if request.method=='GET':
		return render_template("register.html")
	else :
		something=request.json()
		userid = request.form.get('user_id')
		userpassword = request.form.get('user_password')
		userrepassword=request.form.get('user_re_password')
		emailaddress=request.form.get('email_address')
	
		if not (userid and userpassword and emailaddress):
			return "모두 입력해주세요"
		elif userpassword!=userrepassword:
			return "비밀번호가 일치하지 않습니다."
		else:
			#database에 삽입
			print(something)
			print(userid)
			print(userpassword)
			print(userrepassword)
			print(emailaddress)
			return "회원가입 완료"
		
		#return redirect('/')
		

if __name__ == "__main__":
	app.run()
	