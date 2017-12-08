virtualenv的使用：
1）创建虚拟环境：virtualenv venv
2）激活虚拟环境：source venv/bin/activate
3）退出虚拟环境：deactivate

==========

flask的安装：
1）检测：pip freeze
2）安装：pip3 install -i http://pypi.douban.com/simple/  --trusted-host  pypi.douban.com  flask的安装：

==========

前台/后台（home/admin）：
	数据模型：models.py
	表单处理：home（admin）/forms.py
	模板目录：templates/admin（admin）
	静态目录：static
（前台和后台的表单处理和模板目录是独立的）

==========

前后台项目目录分析：
manage.py 					入口启动脚本
app						项目APP
	__init__.py 				初始化文件
	models.py 				数据模型文件
	static 					静态目录 
	home/admin 				前台/后台模块
		__init__.py 			初始化脚本
		views.py 			视图处理文件
		forms.py 			表单处理文件
	templates 				模板目录 
		home/admin 			前台/后台模板


==========

使用蓝图构建项目目录
1、定义蓝图（app/admin/__init__.py）	
from flask import Blueprint
admin = Blueprint('admin', __name__)
from . import views
2、注册蓝图（app/__init__.py）
from admin import admin as admin_blueprint
...
app.register_blueprint(admin_blueprint, url_prefix='admin')
3、调用蓝图（app/admin/views.py）
from . import admin
@admin.route('/')

==========

【数据模型设计】
flask-sqlalchemy通过面向对象的思想去操作数据库。避免我们使用sql去进行重复操作。
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/movie'
# sqlite地址写法：sqlite:///D:/M-LITTER/movie
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 电影
class Movie(db.Model):
	__tablename__ = 'movie'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True)
	url = db.Column(db.String(255), unique=True)
	info = db.Column(db.Text)
	logo = db.Column(db.String(255), unique=True)
	star = db.Column(db.SmallInteger)
	playnum = db.Column(db.BigInteger)
	commentnum = db.Column(db.BigInteger)
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id')) 	# 所属标签id
	area = db.Column(db.String(255))
	release_time = db.Column(db.Date)
	length = db.Column(db.String(100))
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)
	comments = db.relationship('Comment', backref='movie') 	# 外键关系关联
	def __repr__(self):
		return '<Movie {}>'.format(self.title)

Userlog模型里面的user_id字段，需要关联User模型的id字段，操作如下：
1、user_id会员，这里要定义关联外键，指向【user表的id字段】
user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 	# 所属会员
2、user表也要进行关系的关联。【外键关系关联】
userlogs = db.relationship('Userlog', backref='user') 	# 外键关系关联

==========

如何把上面的数据模型生成数据表？
if __name__ == '__main__':
	db.create_all()
运行。
可能会报错：没有mysql模型。
解决方法：安装PyMySQL
import PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/movie'

==========

如何插入测试数据？
if __name__ == '__main__':
	role = Role(
		name='超级管理员',
		auths='',
	)
	db.session.add(role)
	db.session.commit()

if __name__ == '__main__':
	from werkzeug.security import generate_password_hash
	admin = Admin(
		name='jiarui',
		pwd='123456',
		is_super=0,
		role_id=1,
	)
	db.session.add(admin)
	db.session.commit()