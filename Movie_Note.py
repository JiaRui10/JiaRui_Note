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





【中间还有待补充的东西】












6-3 	电影管理-添加电影
1）在forms.py中创建表单
from wtforms import FileField, TextAreaField, SelectField

tags = Tag.query.all()
...
class MovieForm(FlaskForm):
	title = StringField(
		label='片名',
		validators=[
			DataRequired('请输入片名！'),
		],
		description='片名',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入片名！',
		},
	),
	url = FileField(
		label='文件',
		validators=[
			DataRequired('请上传文件！'),
		],
		description='文件',
	),
	info = TextAreaField(
		label='简介',
		validators=[
			DataRequired('请输入简介！'),
		],
		description='简介',
		render_kw={
			'class': 'form-control',
			'rows': 10,
		},
	),
	logo = FileField(
		label='封面',
		validators=[
			DataRequired('请上传封面！'),
		],
		description='封面',
	),
	star = SelectField(
		label='星级',
		validators=[
			DataRequired('请选择星级！'),
		],
		description='星级',
		render_kw={
			'class': 'form-control',
		},
		coerce=int,
		choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
	),
	tag_id = SelectField(
		label='标签',
		validators=[
			DataRequired('请选择标签！'),
		],
		coerce=int,
		choices=[(v.id, v.name) for v in tags],
		description='标签',
		render_kw={
			'class': 'form-control',
		}
	),
	area = StringField(
		label='地区',
		validators=[
			DataRequired('请输入地区！'),
		],
		description='地区',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入地区！',
		},
	),
	length = StringField(
		label='片长',
		validators=[
			DataRequired('请输入片长！'),
		],
		description='片长',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入片长！',
		},
	),
	release_time = StringField(
		label='上映时间',
		validators=[
			DataRequired('请选择上映时间！'),
		],
		description='上映时间',
		render_kw={
			'class': 'form-control',
			'placeholder': '请选择上映时间！',
			'id': 'input_release_time',
		},
	),
	submit = SubmitField(
		'编辑',
		render_kw={
			'class': 'btn btn-primary',
		},
	),
2）在views.py中。
...
@admin.route('/movie/add/', methods=['GET', 'POST'])
def movie_add():
	form = MovieForm()
	return render_template('admin/movie_add.html', form=form)	
3）在movie_add.html中。
	# enctype是为了让表单支持文件上传
	<form method="post" enctype="multipart/form-data">

	{{ form.title.label }}
	{{ form.title }}

	{{ form.url.label }}
	{{ form.url }}

	{{ form.info.label }}
	{{ form.info }}

	{{ form.logo.label }}
	{{ form.logo }}

	{{ form.star.label }}
	# select标签全部删除
	{{ form.star }}

	{{ form.tag_id.label }}
	{{ form.tag_id }}

	{{ form.area.label }}
	{{ form.area }}

	{{ form.length.label }}
	{{ form.length }}

	{{ form.release_time.label }}
	{{ form.release_time }}

	{{ form.csrf_token }}
	{{ form.submit }}
4）运行测试
5）添加报错信息。在movie_add.html中。
...
{{ form.title }} 	/  {{ form.url }}  /  {{ form.info }}  / {{ form.logo }}  /  {{ form.star }}  /  {{ form.tag_id }}  /  {{ form.area }}  /  {{ form.length }}  / {{ form.release_time }}
{% for err in form.title.errors %}
<div class="col-md-12">
	<font style="color: red">{{ err }}</font>
</div>

{% endfor %}
6）运行测试。点击按钮【编辑】
7）编写验证逻辑。在views.py中。
	form = MovieForm()
	if form.validate_on_submit():
		data = form.data
		movie = Movie(
			title = data['title'],
			url = url,    # 需上传，无法直接获取
			info = data['info'],
			logo = logo, # 需上传，无法直接获取
			star = int(data['star']),
			playnum = 0,
			commentnum = 0,
			tag_id = int(data['tag_id']),
			area=data['area'],
			release_time=data['release_time'],
			length=data['length'],
		)
		db.session.add(movie)
		db.session.commit()
		flash('添加电影成功！', 'ok')
		return redirect(url_for('admin.movie_add'))
8）在app.__init__.py中定义文件上传保存路径。
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')
9）回到views.py中。
from werkzeug.utils import secure_filename

# 修改文件名称
def change_filename(filename):
	# 将文件名转化为安全的名称
	# 时间前缀+唯一字符串
	fileinfo = os.path.splitext(filename)
	filename = datatime.datatime.now().strftime('%Y%m%d%H%M%S') + (uuid.uuid4().hex) + fileinfo[-1]
	return filename

	...
	data = form.data
	file_url = secure_filename(form.url.data.filename)
	file_logo = secure_filename(form.logo.data.filename)
	# 判断目录是否存在
	if not os.path.exists(app.config['UP_DIR']):
		os.makedirs(app.config['UP_DIR'])
		os.chmod(app.config['UP_DIR'], 'rw')
	url = change_filename(file_url)
	logo = change_filename(file_logo)
	# 进行保存操作
	form.url.data.save(app.config['UP_DIR'] + url)
	form.logo.data.save(app.config['UP_DIR'] + logo)
10）体现flash消息闪现。
在tad_add.html中的消息闪现代码复制粘贴到movie_add.html中。
<div class="box-body">
	{% for msg in get_flashed_messages(category_filter=['ok']) %}
	...操作成功
11）运行测试。




--------------------------------------------这一章节的内容蛮多，蛮重要的
6-4 	电影列表-列表-删除-编辑
	列表：可以参考之前的标签列表
1）在views.py中。
@admin.route('/movie/list/<int:page>/', methods=['GET'])
@admin_login_req
def movie_list(page=None):
2）在girl.html中。
<a herf="{{ url_for('admin.movie_add') }}">
	<i class="fa fa-circle-o"></i>添加电影
</a>
3）运行测试。
4）在views.py中。
# 关联标签进行查询，用join()方法
# 单表的时候使用filter_by，多表关联的时候注意使用filter
@admin.route('/movie/list/<int:page>/', methods=['GET'])
@admin_login_req
def movie_list(page=None):
	if page is None:
		page = 1
	page_data = Movie.query.join(Tag).filter(
		Tag.id == Movie.tag_id
	).order_by(
		Movie.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/movie_list.html', page_data=page_data)
5）在movie_list.html中进行循环的遍历。
{% import "ui/admin_page.html" as pg %}
....
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.title }}</td>
	<td>{{ v.length }}分钟</td>
	<td>{{ v.tag.name }}</td>
	<td>{{ v.area }}</td>
	<td>{{ v.star }}</td>
	<td>{{ v.playnum }}</td>
	<td>{{ v.commentnum }}</td>
	<td>{{ v.addtime }}</td>
	...
</tr>
{% endfor %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.movie_list') }}
</div>
6）运行测试。

	【删除】按钮
1）在views.py中。
@admin.route('/movie/del/')
@admin_login_req
def movie_del(id=None):
	movie = Movie.query.get_or_404(int(id))
	#因为标签和评论记录之类，都是和电影关联的。所以删除电影的时候要注意解绑关联
	db.session.delete(movie)
	db.session.commit()
	flash('删除电影成功！', 'ok')
	return redirect(url_for('admin.movie_list', page=1))
2）在movie_list.html中加入flash消息闪现删除提示。还有定义删除按钮。
<div class="box-body table-responsive no-padding">
	{% for msg in get_flashed_messages(category_filter=['ok']) %}
	...操作成功

<a href="{{ url_for('admin.movie_del', id=v.id) }}"  class="label label-danger">删除</a>
3）运行测试。



	【编辑】按钮
1）在views.py中。
@admin.route('/movie/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def movie_edit(id=None):
	# 查询到记录之后，再进行修改
	form = MovieForm()
	movie = Movie.query.get_or_404(int(id))	
	if form.validate_on_submit():
		data = form.data
		flash('修改电影成功！', 'ok')
		return redirect(url_for('admin.movie_edit', id=movie.id))
	# 将movie传递进去，用于设置表单的初始值
	return render_template('admin/movie_edit.html', form=form, movie=movie)
2）创建movie_edit.html。
将movie_add.html的代码拷贝进来。
添加电影   →   修改电影
{{ form.title(value=movie.title) }}
{{ form.url }}
{{ form.info }}     # 注意这个不一样
<img src="{{ url_for('static', filename='uploads/{}'+movie.logo) }}">
{{ form.star(value=movie.star) }}
{{ form.tag_id(value=movie.tag_id) }}
{{ form.area(value=movie.area) }}
{{ form.length(value=movie.length) }}
{{ form.release_time(value=movie.release_time) }}

js代码也要替换：
file: "{{ url_for('static', filename='uploads/{}'+movie.url) }}"
title: "{{ movie.title }}"
3）设置movie_list.html中的按钮。
<a href="{{ url_for('admin.movie_edit', id=v.id) }}"  class="label label-danger">编辑</a>
4）运行测试。
5）在views.py中。
	...
	form  = MovieForm()
	# 既然url和logo已经上传到数据库，所以应该已经是存在的，不用进行过滤
	form.url.validators = []
	form.logo.validators = []
	movie = Movie.query.get_or_404(int(id))	
	# 赋予元素初始值
	if request.method == 'GET':
		form.info.data = movie.info
		form.tag_id.data = movie.tag_id
		form.star.data = movie.star
	if form.validate_on_submit():
		data = form.data
		# 注意片名是唯一的
		movie_count = Movie.query.filter_by(title=data['title']).count()
		if movie_count == 1 and movie.title != data['title']:   # 这里是!=?????
			flash('片名已经存在！', 'err')
			return redirect(url_for('admin.movie_edit', id=id))

		# 进行上传操作
		if not os.path.exists(app.config['UP_DIR']):
			os.makedirs(app.config['UP_DIR'])
			os.chmod(app.config['UP_DIR'], 'rw')
		if form.url.data.filename != '':
			file_url = secure_filename(form.url.data,filename)
			movie.url = change_filename(file_url)
			form.url.data.save(app.config['UP_DIR'] + movie.url)
		if form.logo.data.filename != '':
			file_logo = secure_filename(form.logo.data.filename)
			movie.logo = change_filename(file_logo)
			form.logo.data.save(app.config['UP_DIR'] + movie.logo)

		movie.star = data['star']
		movie.tag_id = data['tag_id']
		movie.info = data['info']
		movie.title = data['title']
		movie.area = data['area']
		movie.length = data['length']
		movie.release_time = data['release_time']
		db.session.add(movie)
		db.session.commit()
6）在movie_edit.html中添加闪现。
将代码粘贴到（ok和err两份）：
<div class="box-body">
...
7）运行测试。修改片名为已经存在的变形金刚5，正常应该会提示错误。



6-5 	预告管理
	【预告添加】
1）在forms.py中定义表单。
class PreviewForm(FlaskForm):
	title = StringField(
		label='预告标题',
		validators=[
			DataRequired('请输入预告标题！'),
		],
		description='预告标题',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入预告标题！',
		},
	),
	logo = FileField(
		label='预告封面',
		validators=[
			DataRequired('请上传预告封面！'),
		],
		description='预告封面',
	),
	submit = SubmitField(
		'编辑',
		render_kw={
			'class': 'btn btn-primary',
		},
	),
2）在views.py中。
@admin.route('/preview/add/', methods=['GET', 'POST'])
@admin_login_req
def preview_add():
	form = PreviewForm()
	if form.validate_on_submit():
		form = form.data
	return render_template('admin/preview_add.html', form=form)
3）在preview_add.html中。
	# 注意上传图片一定要跟上enctype属性
	method="post" enctype="multipart/form-data"

	# flash闪现，复制粘贴
	操作成功
	{{ form.title.label }}
	{{ form.title }}
	{% for err in form.title.errors %}
		<div class="col-md-12">
			<font style="color: red">{{ err }}</font>
		</div>
	{% endfor %}

	{{ form.logo.label }}
	{{ form.logo }}
	{% for err in form.logo.errors %}
		<div class="col-md-12">
			<font style="color: red">{{ err }}</font>
		</div>
	{% endfor %}

	{{ form.csrf_token }}
	{{ form.submit }}
4）运行测试。
5）实现逻辑。在views.py中。
@admin.route('/preview/add/', methods=['GET', 'POST'])
@admin_login_req
def preview_add():
	form = PreviewForm()
	if form.validate_on_submit():
		form = form.data
		file_logo = secure_filename(form.logo.data.filename)
		if not os.path.exists(app.config['UP_DIR']):
			os.makedirs(app.config['UP_DIR'])
			os.chmod(app.config['UP_DIR'])
		logo = change_filename(file_logo)
		form.logo.data.save(app.config['UP_DIR'] + logo)
		preview = Preview(
			title=data['title'],
			logo=logo,
		)
		db.session.add(preview)
		db.session.commit()
		flash('添加预告成功！', 'ok')
		return redirect(url_for('admin.preview_add'))
	return render_template('admin/preview_add.html', form=form)
6）运行测试。


	【列表显示】
1）在views.py中。
@admin.route('/preview/list/<int:page>', methods=['GET'])
@admin_login_req
def preivew_list(page=None):
	if page is None:
		page = 1
	page_data = Preview.query.order_by(
		preview.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/preview_list.html', page_data=page_data)
2）在preview_list.html中。
# 实现分页
{% import "ui/admin_page.html" as pg %}

{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.title }}</td>
	<td>
		<img src="{{ url_for('static', filename='uploads/' + v.logo) }}" style="width:140px" class="..." />
	</td>
	<td>{{ v.addtime }}</td>
	<td>
		<a class="...">编辑</a>
		<a class="...">删除</a>
	</td>
</tr>
{% enfor %}

<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.preview_list') }}
</div>
3）在grid.html中。
<a href="{{ url_for('admin.preview_list', page=1) }}">
	<i class="..."></i>预告列表
</a>
4）运行测试。


	【删除】按钮
1）在views.py中。
@admin.route('/preview/del/<int:id>/', methods=['GET'])
@admin_login_req
def preview_del(id=None):
	preview = Preview.query.get_or_404(int(id))
	db.session.delete(preview)
	db.session.commit()
	flash('删除预告成功！',  'ok')
	return redirect(url_for('admin.preview_list', page=1))
2）在preview_list.html中。
<a href="{{ url_for('admin.preview_del', id=v.id) }}">删除</a>

添加flash提醒：
...
<div class="box-body ...">
	操作成功
	...
3）运行测试


	【编辑】按钮
1）在views.py中。
@admin.route('/preview/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def preview_edit(id):
	form = PreviewForm()

	# 因为数据库里面，图片已经默认是有的，所以这里给个空值
	form.logo.validators = []

	preview = Preview.query.get_or_404(int(id))
	if request.method == 'GET':
		form.title.data = preview.title
	if form.validate_on_submit():
		data = form.data

		# 判断图片是否上传成功
		if form.logo.data.filename != '':
			file_logo = secure_filename(form.logo.data.filename)
			preview.logo = change_filename(file_logo)
			form.logo.data.save(app.config['UP_DIR'] + preview.logo)

		preview.title = data['title']
		db.session.add(preview)
		db.session.commit()
		flash('修改预告成功！', 'ok')
		return redirect(url_for('admin.preview_edit', id=id))
	return render_template('admin/preview_edit.html', form=form, preview=preview)
2）创建preview_edit.html。
将preview_add.html的代码拷贝进来。
添加预告  →  修改预告

# 为了显示图片，需要修改
<img  src="{{ url_for('static', filename='uploads/' + preview.logo) }}" />

3）在preview_list.html中。
<a href="{{ url_for('admin.preview_edit', id=v.id) }}">编辑</a>
4）运行测试。



6-6 	会员管理
1）在user表插入12条记录。
2）将头像拷贝到static/uploads/users目录下
3）在views.py中。
# 进行会员列表的分页
@admin.route('/user/list/<int:page>/', methods=['GET'])
@admin_login_req
def user_list(page=None):
	if page is None:
		page = 1
	page_data = User.query.order_by(
		User.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/user_list.html', page_data=page_data)
4）在user_list.html中。
# 进行分页操作
{% import "ui/admin_page.html" as pg %}
...
{% for v in page_data.items %}
                        <tr>
                            <td>{{ v.id }}</td>
                            <td>{{ v.name }}</td>
                            <td>{{ v.email }}</td>
                            <td>{{ v.phone }}</td>
                            <td>
                                <img src="{{ url_for('static', filename='uploads/users/' + v.face) }}" class="img-responsive center-block" alt="" style="width: 50px">
                            </td>
                            <td>正常/冻结</td>
                            <td>{{ v.addtime }}</td>
                            <td>
                                <a class="label label-success" href="{{ url_for('admin.user_view', id=v.id) }}">查看</a>
                                &nbsp;
                                <a class="label label-danger">删除</a>
                            </td>
                        </tr>
                        {% endfor %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.user_list') }}
</div>

5）在grid.html中。
<a href="{{ url_for('admin.user_list', page=1) }}">
	<i class="..."></i>会员列表
</a>
6）运行测试。


	【查看】按钮
1）在user_list.html中。
<a class="label label-success" href="{{ url_for('admin.user_view', id=v.id) }}">查看</a>
2）在views.py中。
@admin.route('/user/view/<int:id>', methods=['GET'])
@admin_login_req
def user_view(id=None):
	user = User.query.get_or_404(int(id))
	return render_template('admin/user_view.html', user=user)
3）在user_view.html中。
	{{ user.id }}
	{{ user.name }}
	{{ user.email }}
	{{ user.phone }}
	<img  src="{{ url_for('static', 'uploads/user/' + user.face) }}" style="width: 100px" />
	{{ user.addtime }}
	{{ user.uuid }}
	{{ user.info }}
4）运行测试。

	
	【删除】按钮
1）在user_list.html中。
<a class="label label-success" href="{{ url_for('admin.user_del', id=v.id) }}">删除</a>
2）在views.py中。
@admin.route('/user/del/<int:id>/', methods=['GET'])
@admin_login_req
def user_del(id=None):
	user = User.query.get_or_404(int(id))
	db.session.delete(user)
	db.session.commit()
	flash('删除会员成功', 'ok')
	return redirect(url_for('admin.user_list', page=1))
3）在user_list.html中添加flash消息闪现。
<div class="box-body ...">
...操作成功
4）运行测试。
