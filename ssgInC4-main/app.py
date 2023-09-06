from flask import Flask
from flask import request, render_template, redirect, url_for
from flask_restful import Resource,reqparse, Api
import utils.userdao as userdao
from utils.utils import hash_password
from mymod import get_list
from os import path
import utils.utils as utils
import pymysql

static_path = path.join('.','resources/')
app = Flask(__name__,static_folder=static_path,static_url_path='/')

db = pymysql.connect(host="localhost",user="root",passwd="passwd",db="test3",charset="utf8")
cur = db.cursor()

# 회원가입 : https://luvris2.tistory.com/196

# app = Flask(__name__)
# api = Api(app)
# @app.route('/user', methods=['POST'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index_login')
def index_login():
    return render_template('index_login.html')

@app.route('/signup')
def display_user_signup_for():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def createUser():
    try:
        parser = reqparse.RequestParser()

        name = str(request.form.get('name'))
        ID = str(request.form.get('ID'))
        password = str(request.form.get('password'))
        phoneNumber = str(request.form.get('phoneNumber'))

        password_confirm = str(request.form.get('password_confirm'))
        
        args = parser.parse_args()

        if len(ID) < 4 or len(ID) > 16 or not utils.onlyalpha(ID) or not phoneNumber.isdecimal() or not name.isalpha() or password != password_confirm:
           return redirect(url_for('signup_fail'))


        hashed_password = utils.hash_password(str(password))

        user_info = [ name , ID , hashed_password, phoneNumber ]
        
        a = userdao.createUser(user_info)

        return redirect(url_for('signup_complete'))
    
    except Exception as e :
        return {'error': str(e)}

# @app.route('/register', methods=['POST'])
# def createUser():
#     try:
#         parser = reqparse.RequestParser()

#         name = request.form.get('name') 
#         ID = request.form.get('ID')
#         password = request.form.get('password')
#         phoneNumber = request.form.get('phoneNumber')

#         # password = request.form.get('password'
        
#         args = parser.parse_args()

#         # if len(data['password']) < 4 or len(data['password']) > 12 :
#         #    return { "error" : "비밀번호의 길이를 확인해주세요 (4-12자리)" }, 400


#         hashed_password = hash_password(str(password))

#         user_info = [ str(name) , str(ID) , hashed_password, str(phoneNumber) ]
        
#         return userdao.createUser(user_info)
    
#     except Exception as e :
#         return {'error': str(e)}
    
# def deleteUser

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html')

@app.route('/withdrawl')
def withdrawl():
    return render_template('withdrawl.html')

@app.route('/write')
def write():
    sql = "SELECT * from board"
    cur.execute(sql)
    data_list = cur.fetchall()
    print(data_list[0])
    print(data_list[1])
    print(data_list[2])
    return render_template('write.html')

# @app.route('/write_action', methods=['POST'])
# def write_action():

#     title = request.form.get('title')
#     writer = request.form.get('writer')
#     content = request.form.get('content')

#     sql = "INSERT INTO board (num, title, writer, content, views) VALUES (11, %s, %s, %s, 0)"
#     values = (title, writer, content)
#     cur.execute(sql, values)
#     db.commit()


#     return index()

# @app.route('/register', methods=['GET','POST'])
# def createUser():
#     try:
#         parser = reqparse.RequestParser()
#         parser.add_argument('name', required=True, type=str, help='name cannot be blank')
#         parser.add_argument('ID', required=True, type=str, help='ID cannot be blank')
#         parser.add_argument('password', required=True, type=str, help='password cannot be blank')
#         parser.add_argument('phoneNumber', required=True, type=str, help='ID cannot be blank')
#         parser.add_argument('rent', required=False, type=str)
#         args = parser.parse_args()

#         # if len(data['password']) < 4 or len(data['password']) > 12 :
#         #    return { "error" : "비밀번호의 길이를 확인해주세요 (4-12자리)" }, 400


#         hashed_password = hash_password(str(args['password']))

#         user_info = [ str(args['name']) , str(args['ID']) ,hashed_password, str(args['phoneNumber']), str(args['phoneNumber']) ]
#         return userdao.createUser(user_info)
    
#     except Exception as e :        
#         return {'error': str(e)}

@app.route('/upload',methods=['GET'])
def upload():
    files = get_list()
    return render_template("upload.html",files=files)
    # return '서비스 구동중...'

@app.route('/upload_file',methods=['POST'])
def upload_file():
    file = request.files.get("upfile", None)
    if not file:
        return "선택된 파일이 없습니다."
    file.save(path.join(static_path),file.filename)
    # file.save('.resources/',file.filename)
    return redirect(url_for("upload"))

@app.route('/board')
def board():
    sql = "SELECT * from board"
    cur.execute(sql)

    data_list = cur.fetchall() 
    return render_template('board.html', data_list=data_list)


# def create_app():
#     app = Flask(__name__)

#     @app.route('/')
#     def hello_world():
#         return 'hello world!'

#     return app



if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)