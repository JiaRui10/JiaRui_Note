【Done】

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



20171211-前台布局搭建
1、静态文件引入：
{{ url_for('static', filename='文件路径') }}
2、定义路由：
{{ url_for('模块名.视图名', 变量=参数) }}
3、定义数据库：
{% block 数据块 %}...{% endblock %}
{% block content %}{% endblock %}
{% block css %}{% endblock %}
{% block js %}{% endblock %}


1、添加路由
2、编写html代码


导入代码，如左边的导航栏：{% include "home/menu.html" %}

让被选中的项目高亮：
1、将html中active的class删除
2、给每个项目添加id：m-1、m-2、m-3
3、在每个项目对应的html文件中，添加下面的js代码：
{% block js %}
<script>
$(document).ready(function(){
    $('#m-1').addClass('active');
});
</script>
{% endblock %}



6-1     管理员登录
1、app/__init__.py中创建db对象
2、app/models.py中导入db对象
3、app/admin/forms.py中定义表单验证
4、app/templates/admin/login.html中使用表单字段、信息验证、消息闪现
5、app/admin/views.py中处理登录请求、保存会话
6、app/admin/views.py中定义登录装饰器、访问控制

模型：Admin
表单：LoginForm
请求方法：GET、POST
访问控制：无

具体步骤：
1）将models.py中关于db对象创建的代码，挪到app的初始化文件__init__.py中。
2）在models.py中导入db对象。
3）在forms.py中定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    '''管理员登录表单'''
    account = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！'),
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号',
            'required': 'required',
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！'),
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'required': 'required',
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat',
        }
    )
4）将上面定义好的表单类，运用到html模板中。
a、找到views.py中的login()路由函数：
    form = LoginForm()
    return render_template('admin/login.html', form=form)
b、在login.html中，先将表单对应的html代码删除，如input标签代码。然后用下面的代码替换：
    {{ form.account }}
    {{ form.pwd }}
    {{ form.submit }}
5）直接运行。会报错：KeyError: 'A secret key is required to use CSRF.'
6）在app的初始化文件__init__.py中。
app.config['SECRET_KEY'] = 'suijizifuchuan'

在login.html中，在{{ form.submit }}前面添加：{{ form.csrf_token }}
7）视图处理。在views.py中的login()视图函数中。
if form.validate_on_submit():   # 是否验证成功
    data = form.data
8）如何在模板中显示错误信息？
{% for err form.account.errors %}
    <div class="col-md-12" id="input_user">
        <font style="color: red;">{{ err }}</font>
    </div>
{% endfor %}
注意：form元素的action属性要去掉。
9）
@admin.route('/login/', methods=['GET', 'POST'])
10）运行测试。
11）如何验证账号和密码？
（在表单里面自定义一个账号验证器）
from wtforms.validators import ValidationError
class LoginForm(FlaskForm):
    ...
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在')

a、验证哈希密码
在Admin模型下面定义方法：
def check_pwd(self, pwd):
    from werkzeug.security import check_password_hash
    return check_password_hash(self.pwd, pwd)
b、打开views.py中的login()视图函数，进行密码验证的处理。
data = form.data
admin = Admin.query.filter_by(name=data['account']).first()
if not admin.check_pwd(data['pwd']):
    flash('密码错误')
    return redirect(url_for('admin.login'))    
# 如果密码是正确的，那就要对账号进行保存
session['admin'] = data['account']
return redirect(request.args.get('next') or url_for('admin.index'))
c、用flash消息闪现显示密码错误信息
{% for msg in get_flashed_messages() %}
    <p class="login-box-msg" style="color: red;">msg</p>
{% endfor %}
12）运行测试。
13）退出系统。
@admin.route('/logout/')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))
14）访问控制：即用户未登录的情况下，不能让用户访问后台页面。
a、
（使用装饰器）
from functools import wraps

def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
b、对后台页面对应的视图函数，加上该装饰器
@admin.route('/')
@admin_login_req
15）运行测试。这时不登录就没办法访问，但如果登录了再推出，还是可以访问后台，这是因为浏览器有缓存。



6-2     标签管理
1、模型：Tag
2、表单：TagForm
3、请求方法：GET、POST
4、访问控制
@admin_login_req


1）在forms.py中定义标签表单类
class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('请输入标签！'),
        ],
        description='标签',
        render_kw={
            'class': 'form-control',
            'id': 'input_name',
            'placeholder': '请输入标签名称！'
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            'class': 'btn btn-primary'
        }
    )
2）在views.py中。
# 添加标签
@admin.route('/tag/add/')
@admin_login_req
def tag_add():
    form = TagForm()
    return render_template('admin/tag_add.html', form=form)
3）在tag_add.html中。
    {{ form.name.label }}
    {{ form.name }}

    {{ form.csrf_token }}
    {{ form.submit }}
4）运行测试。
5）如何在点击“添加”之后，让数据入库呢？
form = TagForm()
if form.validate_on_submit():
    data = form.data
    # 标签要是唯一性
    tag = Tag.query.filter_by(name=data['name']).count()
    if tag == 1:
        flash('标签已经存在！', 'err')
        return redirect(url_for('admin.tag_add'))
    # 入库
    tag = Tag(
        name=data['name'],
    )
    db.session.add(tag)
    db.session.commit()
    flash('添加标签成功', 'ok')
    return redirect(url_for('admin.tag_add'))

判断：在tag_add.html中，注意form要添加属性：method='POST'，路由也要同时允许get和post。
# 下面代码的作用：当输入为空的时候报错
{% for err in form.name.errors %}
    <div class="col-md-12" id="input_user">
        <font style="color: red;">{{ err }}</font>
    </div>
{% endfor %}

# 弹出flash
{% for msg in get_flashed_messages(category_filter=['ok']) %}
<div class="alert alert-success alert-dismissible">
    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">x</button>
    <h4><i class="icon fa fa-check"></i>操作成功</h4>
    {{ msg }}
</div>
{% endfor %}

{% for msg in get_flashed_messages(category_filter=['err']) %}
<div class="alert alert-danger alert-dismissible">
    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">x</button>
    <h4><i class="icon fa fa-ban"></i>操作失败</h4>
    {{ msg }}
</div>
{% endfor %}


【标签列表】
功能：将标签分页展示出来。
1）要给路由函数传入一个page
# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_req
def tag_list(page):
    if page is None:
        page = 1
    # 查询并分页显示
    # 不需要过滤条件，结果按时间排序
    # paginate：进行分页
    # per_page：每一页显示的页数，这里先用1测试
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=1)
    return render_template('admin/tag_list.html', page_data=page_data)
2）在tag_list.html中分页显示。
{% for v in page_data.items %}
<tr>
    <td>{{ v.id }}</td>
    <td>{{ v.name }}</td>
    <td>{{ v.addtime }}</td>
    <td>
        <a class="label label-success">编辑</a>
        &nbsp;
        <a class="label label-danger">删除</a>
    </td>
</tr>
{% endfor %}
3）打开grid.html，修改【标签列表】对应的a标签的href属性：
{{ url_for('admin.tag_list', page=1) }}
4）运行测试。此时一页就显示了一条数据。
5）创建文件：templates/ui/admin_page.html。用于保存页码。
将tag_list.html文件的下面关于页码的代码，剪切到admin_page.html中。
{% macro page(data, url) -%}
{% if data %}
<ul class="pagination pagination-sm no-margin pull-right">
    <li><a href="{{ url_for(url, page=1) }}">首页</a></li>
    {% if data.has_prev %}
        <li><a href="{{ url_for(url, page=data.prev_num) }}">上一页</a></li>
    {% else %}
        <li class="disabled"><a href="#">上一页</a></li>
    {% endif %}

    {% for v in data.iter_pages() %}
        {% if v == data.page %}
            <li class="active"><a href="#">{{ v }}</a></li>
        {% else %}
            <li><a href="{{ url_for(url, page=v) }}">{{ v }}</a></li>
        {% enif %}
    {% enfor %}

    {% if data.has_next %}
        <li><a href="{{ url_for(url, page=data.next_num) }}">下一页</a></li>
    {% else %}
        <li class="disabled"><a href="#">下一页</a></li>
    {% endif %}

    <li><a href="{{ url_for(url, page=data.pages) }}">尾页</a></li>
</ul>
{% endif %}
{%- endmacro %}
6）tag_list.html中。
{% import "ui/admin_page.html" as pg %}
<div class="box-footer clearfix">
    {{ pg.page(page_data, 'admin.tag_list') }}
</div>
7）运行测试。
8）【编辑】、【删除】按钮的逻辑
    【删除】按钮
a、
# 标签删除
@admin.route('/tag/del/<int:id>/', methods=['GET'])
@admin_login_req
def tag_del(id=None):
    # 通过主键查询
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))
b、
在tag_list.html中。添加flash消息闪现。
<a ... href="{{ url_for('admin.tag_del', id=v.id) }}">删除</a>
c、运行测试。

    【编辑】按钮
1）
# 标签编辑
@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        # 标签要是唯一性
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name == data['name'] and tag_count == 1:
            flash('标签已经存在！', 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功', 'ok')
        return redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)
2）创建tag_edit.html。
3）在tag_list.html中。
<a ... href="{{ url_for('admin.tag_edit', id=v.id) }}">编辑</a>
4）运行测试。成功。



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
<img src="{{ url_for('static', filename='uploads/'+movie.logo) }}">
{{ form.star(value=movie.star) }}
{{ form.tag_id(value=movie.tag_id) }}
{{ form.area(value=movie.area) }}
{{ form.length(value=movie.length) }}
{{ form.release_time(value=movie.release_time) }}

js代码也要替换：
file: "{{ url_for('static', filename='uploads/'+movie.url) }}"
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
		if movie_count == 1 and movie.title == data['title']:   # 这里是!=?????
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



6-7 	评论-收藏管理
			评论管理
1）先插入数据到comment表中。
2）关联movie表和user表。
3）在views.py中。
@admin.route('/comment/list/<int:page>/', methods=['GET'])
@admin_login_req
def comment_list(page=None):
	if page is None:
		page = 1
	# 用join()关联movie表和user表
	# 用filter添加过滤条件
	page_data = Comment.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == Comment.movie_id,
		User.id == Comment.user_id,
	).order_by(
		Comment.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/comment_list.html', page_data=page_data)
4）在girl.html中。
<a href="{{ url_for('admin.comment_list', page=1) }}">
	<i class="..."></i>评论列表
</a>
5）在comment_list.html中。
{% for v in page_data.items %}
<div class="box-comment">
                        <img class="img-circle img-sm"
                             src="{{ url_for('static', filename='uploads/users/' + v.user.face) }}" alt="User Image">

                        <div class="comment-text">
                                    <span class="username">
                                        {{ v.user.name }}
                                        <span class="text-muted pull-right">
                                            <i class="fa fa-calendar" aria-hidden="true"></i>
                                            &nbsp;
                                            {{ v.addtime }}
                                        </span>
                                    </span>
                            关于电影<a>《{{ v.movie.title }}》</a>的评论：{{ v.content }}
                            <br><a class="label label-danger pull-right">删除</a>
                        </div>
                    </div>
{% endfor %}
6）运行测试。
7）在comment_list.html中进行分页显示。
{% import "ui/admin_page.html" as pg %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.comment_list') }}
</div>
8）运行测试。

	【删除】按钮
1）在views.py中。
@admin.route('/comment/del/<int:id>/', methods=['GET'])
@admin_login_req
def comment_del(id=None):
	comment = Comment.query.get_or_404(int(id))
	db.session.delete(comment)
	db.session.comment()
	flash('删除评论成功', 'ok')
	return redirect(url_for('admin.comment_list', page=1))
2）在comment_list.html中。添加flash消息闪现。为按钮添加跳转。
...
<div class="box-body box-comments">
{% for msg in get_flashed_messages(category_filter=['ok']) %}
...操作成功


<a href="{{ url_for('admin.comment_del', id=v.id) }}" class="label label-danger pull-right">删除</a>
3）运行测试。



			收藏管理
1）先插入数据到movie_col表中。
2）在views.py中。
@admin.route('/moviecol/list/<int:page>/', methods=['GET'])
@admin_login_req
def moviecol_list(page=None):
	if page is None:
		page = 1
	page_data = Moviecol.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == Moviecol.movie_id
		User.id == Moviecol.user_id
	).order_by(
		Moviecol.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/moviecol_list.html', page_data=page_data)
3）在grid.html中。
<a href="{{ url_for('admin.moviecol_list', page=1) }}">
	<i class="..."></i>收藏列表
</a>
4）在moviecol_list.html中。
{% import "ui/admin_page.html" as pg %}
...
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.movie.title }}</td>
	<td>{{ v.user.name }}</td>
	<td>{{ v.addtime }}</td>
	<td>
		<a>...</a>
	</td>
</tr>
{% endfor %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.moviecol_list') }}
</div>
5）运行测试。

	【删除】按钮
1）在views.py中。
@admin.route('/moviecol/del/<int:id>/', methods=['GET'])
@admin_login_req
def moviecol_del(id=None):
	moviecol = Moviecol.query.get_or_404(int(id))
	db.session.delete(moviecol)
	db.session.commit()
	flash('删除收藏成功！', 'ok')
	return redirect(url_for('admin.moviecol_list', page=1))
2）在moviecol.list.html中添加flash消息闪现。并给按钮添加事件。
<div class="box-body ...">
{% for msg in get_flashed_messages(category_filter=['ok']) %}
...操作成功
...

<a class="..."  href="{{ url_for('admin.moviecol_del', id=v.id) }}">删除</a>
3）运行测试。


6-8 	修改密码
1）在forms.py中定义表单。
class PwdForm(FlaskForm):
	old_pwd = PasswordField(
		label='旧密码',
		validators=[
			DataRequired('请输入旧密码！')
		],
		description='旧密码',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入旧密码！',
		}
	),
	new_pwd = PasswordField(
		label='新密码',
		validators=[
			DataRequired('请输入新密码！')
		],
		description='新密码',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入新密码！',
		}
	),
	submit = SubmitField(
		'编辑',
		render_kw={
			'class': 'btn btn-primary',
		}
	)
2）在views.py中。
@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_req
def pwd():
	form = PwdForm()
	return render_template('admin/pwd.html', form=form)
3）在pwd.html中。
	method="post"	
	{{ form.old_pwd.label }}
	{{ form.old_pwd }}
	
	{{ form.new_pwd.label }}
	{{ form.new_pwd }}

	{{ form.csrf_token }}
	{{ form.submit }}
4）在pwd.html中显示错误信息。
{{ form.old_pwd }}  /  {{ form.new_pwd }} 
{% for err in form.name.errors %}
	...{{ err }}...
{% endfor %}
5）运行测试。
			定义密码验证逻辑。
1）在PwdForm中定义旧密码验证。
	def validate_old_pwd(self, field):
		from flask import session
		pwd = field.data
		name = session['admin']
		admin = Admin.query.filter_by(
			name=name
		).first()
		if not admin.check_pwd(pwd):
			raise ValidationError('旧密码错误！')
2）运行测试。
3）在views.py中。
# 进行数据库的操作
@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_req
def pwd():
	form = PwdForm()
	if form.validate_on_submit():
		data = form.data
		admin = Admin.query.filter_by(name=session['admin']).first()
		from werkzeug.security import generate_password_hash
		admin.pwd = generate_password_hash(data['new_pwd'])
		db.session.add(admin)
		db.session.commit()
		flash('修改密码成功， 请重新登录！', 'ok')    # 这份flash会在login.html中提示
		redirect(url_for('admin.logout'))
	return render_template('admin/pwd.html', form=form)
4）在login.html中。统一好两份flash提示：'ok'、'err'
5）在admin.html中。
<span class="hidden-xs">{{ session['admin'] }}</span>
...
{{ session['admin'] }}
<small>2017-06-01</small>
...
用户XXX  →   用户{{ session['admin'] }}



6-9 	日志管理
1）改变后台页面右上角的时间
在view.py中。
# 上下文应用处理器：封装全局变量
@admin.context_processor
def tpl_extra():
	data = dict(
		online_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	)
	return data
2）在admin.html中。
<small>{{ online_time }}<small>
3）运行测试。


	【操作日志列表】
1）注意登录成功之后，应该将admin_id也一同保存。退出的时候要删除
在views.py中。
...
def login():
	...
	session['admin'] = data['account']
	session['admin_id'] = admin_id
	...

def logout():
	...
	session.pop('admin_id', None)
2）当数据有改动，应该将改动写入日志
在views.py中。
...
def tag_add():
	...
	flash('添加标签成功！', 'ok')
	oplog = Oplog(
		admin_id=session['admin_id'],
		ip=request.remote_addr,
		reason='添加标签{}'.format(data['name'])
	)
	db.session.add(oplog)
	...
3）运行测试。在tag_add.html页面中添加标签。并查看数据表oplog。

4）将操作日志体现出来。
在views.py中。
@admin.route('/oplog/list/<int:page>/', methods=['GET'])
@admin_login_req
def oplog_list(page=None):
	if page is None:
		page = 1
	page_data = Oplog.query.join(
		Admin
	).filter(
		Admin.id == Oplog.admin_id,
	).order_by(
		Oplog.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/oplog_list.html', page_data=page_data)
5）在oplog_list.html进行分页显示。
{% import "ui/admin_page.html" as pg %}
...
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.admin.name }}</td>
	<td>{{ v.addtime }}</td>
	<td>{{ v.reason }}</td>
	<td>{{ v.ip }}</td>
</tr>
{% endfor %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.oplog_list') }}
</div>
6）修改grid.html。
<a href="{{ url_for('admin.oplog_list', page=1) }}">
	<i class="..."></i>操作日志列表
</a>
7）运行测试。


	【管理员登录日志列表】
1）在login()视图函数中记录管理登录情况。
def login():
	...
	session['admin_id'] = admin.id
	adminlog = Adminlog(
		admin_id=admin.id
		ip=request.remote_addr,
	)
	db.session.add(adminlog)
	db.session.commit()
2）运行测试。反复登录、退出。再查看adminlog表。
3）进行数据展示。
在views.py中。
@admin.route('/adminloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
def adminloginlog_list(page=None):
	if page is None:
		page = 1
	page_data = Adminlog.query.join(
		Admin
	).filter(
		Admin.id == Adminlog.admin_id,
	).order_by(
		Adminlog.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/adminloginlog_list.html', page_data=page_data)
4）在adminloginlog_list.html中。
{% import "ui/admin_page.html" as pg %}
...
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.admin.name }}</td>
	<td>{{ v.addtime }}</td>
	<td>{{ v.ip }}</td>
</tr>
{% endfor %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.adminloginlog_list') }}
</div>
5）修改grid.html的代码拷贝进来。
<a href="{{ url_for('admin.adminloginlog_list', page=1) }}">
	<i class="..."></i>管理员登录日志列表
</a>
6）运行测试。




	【会员登录日志列表】
1）往userlog这个表插入一些测试数据。
2）进行列表展示。
@admin.route('/userloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
def userloginlog_list(page=None):
	if page is None:
		page = 1
	page_data = Userlog.query.join(
		User
	).filter(
		User.id == Userlog.user_id,
	).order_by(
		Userlog.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/userloginlog_list.html', page_data=page_data)
3）修改grid.html的代码。
<a href="{{ url_for('admin.userloginlog_list', page=1) }}">
	<i class="..."></i>会员登录日志列表
</a>
4）在userloginlog_list.html中分页展示。
{% import "ui/admin_page.html" as pg %}
...
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.user.name }}</td>
	<td>{{ v.addtime }}</td>
	<td>{{ v.ip }}</td>
</tr>
{% endfor %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.userloginlog_list') }}
</div>
5）运行测试。




7-1 	权限管理
基于角色的访问控制
	【添加权限】
1）在forms.py中定义表单。
class AuthForm(FlaskForm):
	name = StringField(
		label='权限名称',
		validators=[
			DataRequired('请输入权限名称！'),
		],
		description='权限名称',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入权限名称！',
		},
	)
	url = StringField(
		label='权限地址',
		validators=[
			DataRequired('请输入权限地址！'),
		],
		description='权限地址',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入权限地址！',
		},
	)
	submit = SubmitField(
		'编辑',
		render_kw={
			'class': 'btn btn-primary',
		},
	)
2）在view.py中。
@admin.route('/auth/add/')
@admin_login_req
def auth_add():
	form = AuthForm()
	if form.validate_on_submit():
		data = form.data
	return render_template('admin/auth_add.html', form=form)
3）在auth_add.html中。
method="post"
	{{ form.name.label }}
	{{ form.name }}
	{% for err in form.name.errors %}
	..错误信息显示
	{% endfor %}

	{{ form.url.label }}
	{{ form.url }}
	..错误信息显示

	{{ form.csrf_token }}
	{{ form.submit }}
4）在views.py中。
@admin.route('/auth/add/'， methods=['GET', 'POST'])
@admin_login_req
def auth_add():
	form = AuthForm()
	if form.validate_on_submit():
		data = form.data
		auth = Auth(
			name=data['name'],
			url=data['url']
		)
		db.session.add(auth)
		db.session.commit()
		flash('添加权限成功！', 'ok')
	return render_template('admin/auth_add.html', form=form)
5）在auth_add.html中添加flash消息闪现。
6）运行测试。
添加标签 	/admin/tag/add/
编辑标签 	/admin/tag/edit/<int:id>/
标签列表	/admin/tag/list/<int:page>/
删除标签	/admin/tag/del/<int:id>/
然后查看数据库，检查是否添加成功。


	【权限列表】
1）在views.py中。
# 权限列表
@admin.route('/auth/list/<int:page>/', methods=['GET'])
@admin_login_req
def movie_list(page=None):
	if page is None:
		page = 1
	page_data = Auth.query.order_by(
		Movie.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/c', page_data=page_data)

# 权限删除
@admin.route('/auth/del/<int:id>/', methods=['GET'])
@admin_login_req
def auth_del(id=None):
	auth = Auth.query.fitler_by(id=id).first_or_404()
	db.session.delete(auth)
	db.session.commit()
	flash('删除标签成功！', 'ok')
	return redirect(url_for('admin.auth_list', page=1))
2）在auth_list.html中。
{% import "ui/admin_page.html" as pg %}
...
...
# 添加消息闪现
...
..
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.name }}</td>
	<td>{{ v.url }}</td>
	<td>{{ v.addtime }}</td>
	<td>
		<a class="...">编辑</a>
		<a class="..." href="{{ url_for('admin.auth_del', id=v.id) }}">删除</a>
	</td>
</tr>
{% endfor %}
...
<div class="box-footer clearfix">
	{{ pg.page(page_data, 'admin.auth_list') }}
</div>
3）在gird.html中。
<a href="{{ url_for('admin.auth_list', page=1) }}">
	<i></i>权限列表
</a>
4）运行测试。

	【编辑】按钮
1）创建auth_edit.html。将auth_add.html的代码拷贝进来。
添加权限  →  修改权限
	{{ form.name(value=auth.name) }}
	{{ form.url(value=auth.url) }}
2）在views.py中。
# 编辑权限
@admin.route('/auth/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def auth_edit(id=None):
	form = AuthForm()
	auth = Auth.query.get_or_404(id)
	if form.validate_on_submit():
		data = form.data
		auth.url = data['url']
		auth.name = data['name']
		db.session.add(auth)
		db.session.commit()
		flash('修改权限成功！', 'ok')
		redirect(url_for('admin.auth_edit', id=id))
	return render_template('admin/auth_edit.html', form=form, auth=auth)
3）在auth_list.html中。
<a class="..." href="{{ url_for('admin/auth_edit', id=v.id) }}">编辑</a>
4）运行测试。



7-2 	角色管理
1）在forms.py中定义表单。
auth_list = Auth.query.all()

class RoleForm(FlaskForm):
	name = StringField(
		label='角色名称',
		validators=[
			DataRequired('请输入角色名称！'),
		],
		description='角色名称',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入角色s名称！',
		},
	)
	auths = SelectMultipleField(
		label='权限列表',
		validators=[
			DataRequired('请选择权限列表！')
		],
		coerce=int,
		choices=[(v.id, v.name) for v in auth_list]
		description='权限列表',
		render_kw={
			'class': 'form-control',
		}
	)
	submit = SubmitField(
		'编辑',
		render_kw={
			'class': 'btn btn-primary',
		}
	)
2）在views.py中。
@admin.route('/role/add/', methods=['GET', 'POST'])
@admin_login_req
def role_add():
	form = RoleForm()
	if form.validate_on_submit():
		data = form.data
	return render_template('admin/role_add.html', form=form)
3）在role_add.html中。
将消息闪现，错误提示的代码拷贝进去。

method="post"

	{{ form.name.label }}
	{{ form.name }}

	<div class="col-md-12">
		<label>{{ form.auths.label }}</label>
	</div>
	{{ form.auths }}

	{{ form.csrf_token }}
	{{ form.submit }}
4）运行测试。
5）入库操作。
@admin.route('/role/add/', methods=['GET', 'POST'])
@admin_login_req
def role_add():
	form = RoleForm()
	if form.validate_on_submit():
		data = form.data
		role = Role(
			name=data['name'],
			auths=','.join(map(lambda v: str(v), data['auths']))
		)
		db.session.add(role)
		db.session.commit()
		flash('添加角色成功！', 'ok')
	return render_template('admin/role_add.html', form=form)


	【角色列表】
1）在views.py中。
@admin.route('/role/list/<int:page>/', methods=['GET'])
@admin_login_req
def role_list(page=None):
	if page is None:
		page = 1
	page_data = Role.query.order_by(
		Role.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/role_list.html', page_data=page_data)
2）在role_list.html中。
将消息闪现拷贝进去。

{% import "ui/admin_page.html" as pg %}
...
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.name }}</td>
	<td>{{ v.addtime }}</td>
	<td>
		<a class="...">编辑</a>
		<a class="...">删除</a>
	</td>
</tr>
{% endfor %}
...
{{ pa.page(page_data, 'admin.role_list') }}
3）在grid.html中。
<a href="{{ url_for('admin.role_list', page=1) }}">
	<i></i>角色列表
</a>
4）运行测试。

	【删除】按钮
1）在views.py中。
@admin.route('/role/del/<int:id>/', methods=['GET'])
@admin_login_req
def role_del(id=None):
	role = Role.query.filter_by(id=id).first_or_404()
	db.session.delete(role)
	db.session.commit()
	flash('删除角色成功！', 'ok')
	return redirect(url_for('admin.role_list', page=1))
2）在role_list中。
<a class="..." href="{{ url_for('admin.auth_del', id=v.id) }}">删除</a>
3）运行测试。


	【编辑】按钮
1）在views.py中。
# 编辑角色
@admin.route('/role/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def role_edit(id=None):
	form = RoleForm()
	role = Role.query.get_or_404(id)
	if form.validate_on_submit():
		data = form.data
	return render_template('admin/role_edit.html', form=form, fole=role)
2）创建role_edit.html，将role_add.html的代码拷贝进来。
添加角色  →  修改角色
	{{ form.name(value=role.name) }}
	# 注意auths是多选框，无法直接复制，所在在3中处理
3）在views.py中。
@admin.route('/role/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def role_edit(id=None):
	form = RoleForm()
	role = Role.query.get_or_404(id)

	if request.method == 'GET':
		auths = role.auths
		form.auths.data = list(map(lambda v:int(v), auths.split(',')))

	if form.validate_on_submit():
		data = form.data
	return render_template('admin/role_edit.html', form=form, fole=role)
4）在role_list.html中。
<a class="..." href="{{ url_for('admin.role_edit', id=v.id) }}">编辑</a>
5）运行测试。
6）入库操作。
@admin.route('/role/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def role_edit(id=None):
	form = RoleForm()
	role = Role.query.get_or_404(id)
	if request.method == 'GET':
		auths = role.auths
		form.auths.data = list(map(lambda v:int(v), auths.split(',')))
	if form.validate_on_submit():
		data = form.data

		role.name = data['name']
		role.auths = ','.join(map(lambda v: str(v), data['auths']))
		db.session.add(role)
		db.session.commit()
		flash('修改角色成功！', 'ok')

	return render_template('admin/role_edit.html', form=form, fole=role)


7-3 	管理员管理
	【添加管理员】
1）在forms.py中。
导入模块EqualTo，用于比较两个字段是否相等。

role_list = Role.query.all()

class AdminForm(FlaskForm):
	name = StringField(
		label='管理员名称',
		validators=[
			DataRequired('请输入管理员名称！'),
		],
		description='管理员名称',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入管理员名称！',
		},
	)
	pwd = PasswordField(
		label='管理员密码',
		validators=[
			DataRequired('请输入管理员密码！'),
		],
		description='管理员密码',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入管理员密码！',
		},
	)
	repwd = PasswordField(
		label='管理员重复密码',
		validators=[
			DataRequired('请输入管理员重复密码！'),
			EqualTo('pwd', message='两次密码不一致') 	# 注意这里
		],
		description='管理员重复密码',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入管理员重复密码！',
		},
	)
	role_id = SelectField(
		label='所属角色',
		coerce=int,
		choices=[(v.id, v.name) for v in role_list],
		render_kw={
			'class': 'form-control'
		}
	)
	submit = SubmitField(
		'编辑',
		render_kw={
			'class': 'btn btn-primary'
		}
	)
2）在views.py中。
@admin.route('/admin/add/', methods=['GET', 'POST'])
@admin_login_req
def admin_add():
	form = AdminForm()
	from werkzeug.security import generate_password_hash
	if form.validate_on_submit():
		data = form.data
		admin = Admin(
			name=data['name'],
			pwd=generate_password_hash(data['pwd']),
			role_id=data['role_id'],
			is_super=1,
		)
		db.session.add(admin)
		db.sesison.commit()
		flash('添加管理员成功！', 'ok')
	return render_template('admin/admin_add.html', form=form)
3）在admin_add.html中。
添加flash消息闪现。错误提示。

method="post"

	{{  form.name.label }}
	{{ form.name }}

	{{ form.pwd.label }}
	{{ form.pwd }}

	{{ form repwd.label }}
	{{ form.repwd }}

	{{ form role_id.label }}
	{{ form.role_id }}

	{{ form.csrf_token }}
	{{ form.submit }}
4）运行测试。

	【管理员列表】
1）在views.py中。
@admin.route('/admin/list/<int:page>/', methods=['GET'])
@admin_login_req
def admin_list(page=None):
	if page is None:
		page = 1
	# 主要需要用join进行关联查询
	page_data = Admin.query.join(
		Role
	).filter(
		Role.id == Admin.role_id
	).order_by(
		Admin.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('admin/admin_list.html', page_data=page_data)
2）在admin_list.html中。
将消息闪现拷贝进去。

{% import "ui/admin_page.html" as pg %}
...
{% for v in page_data.items %}
<tr>
	</td>{{ v.id }}</td>
	</td>{{ v.name }}</td>
	{% if v.is_super == 0 %}
		</td>超级管理员</td>
	{% else %}
		</td>普通管理员</td>
	{% endif %}
	</td>{{ v.role.name }}</td>
	</td>{{ v.addtime }}</td>
</tr>
{% endfor %}
...
{{ pg.page(page_data, 'admin.admin_list') }}
3）在grid.html中。
将管理员列表对应的a标签，加上page=1
 4）运行测试。


7-4 	访问权限控制
=====================================
# 定义权限装饰器
def admin_auth(f):
	@wraps(f)
	def decorate_function(*args, **kwargs):
		# 权限查询
		abort(404)
		return f(*args, **kwargs)
	return decorate_function

# 调用权限装饰器
@admin_auth
=====================================
管理员ID  →  角色  →  权限列表  →  能够访问的路由规则

1）在views.py中。
# 权限控制装饰器
def admin_auth(f):
	@wraps
	def decorated_function(*args, **kwargs):
		admin = Admin.query.join(
			Role
		).filter(
			Role.id == Admin.role_id,
			Admin.id == session['admin_id']
		).first()
		auths = admin.role.auths
		auths = list(map(lambda v: int(v), auths.split(',')))
		auth_list = Auth.query.all()
		urls = [v.url for v in auth_list for val in auths if val == v.id]
		rule = request.url_rule
		if str(rule) not in urls:
			abort(404)
		return f(*args, **kwargs)
2）给其他需要的路由函数加上装饰器。（登录不需要）




8-1 	会员注册
1）在home/forms.py中。
form flask_wtf import FlaskForm
from wtforms.fields import SubmitField, ...
form wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError

# 注意name、email、phone要保持唯一性，需要验证唯一性
from app.models import User

class RegistForm(FlaskForm):
	name = StringField(
		label='昵称',
		validators=[
			DataRequired('请输入昵称！'),
		],
		description='昵称',
		render_kw={
			'class': 'form-control input-lg',
			'placeholder': '请输入昵称！',
		},
	)
	email = StringField(
		label='邮箱',
		validators=[
			DataRequired('请输入邮箱！'),
			Email('邮箱格式不正确'),  	# 用于验证邮箱
		],
		description='邮箱',
		render_kw={
			'class': 'form-control input-lg',
			'placeholder': '请输入邮箱！',
		},
	)
	phone = StringField(
		label='手机',
		validators=[
			DataRequired('请输入手机！'),
			Regexp('1[3458]\d{9}', message='手机格式不正确！') 	# 用于验证手机格式
		],
		description='手机',
		render_kw={
			'class': 'form-control input-lg',
			'placeholder': '请输入手机！',
		},
	)
	pwd = PasswordField(
		label='密码',
		validators=[
			DataRequired('请输入密码！'),
		],
		description='密码',
		render_kw={
			'class': 'form-control input-lg',
			'placeholder': '请输入密码！',
		},
	)
	repwd = PasswordField(
		label='确认密码',
		validators=[
			DataRequired('请输入确认密码！'),
			EqualTo('pwd', message='两次密码不一致！')
		],
		description='确认密码',
		render_kw={
			'class': 'form-control input-lg',
			'placeholder': '请输入确认密码！',
		},
	)
	submit = SubmitField(
		'注册',
		render_kw={
			'class': 'btn btn-lg btn-success btn-block',
		},
	)

	# 注意name、email、phone要保持唯一性，需要验证唯一性
	def validate_name(self, field):
		name = field.data
		user = User.query.filter_by(name=name).count()
		if user == 1:
			raise ValidationError('昵称已经存在！')
	def validate_email(self, field):
		email = field.data
		user = User.query.filter_by(email=email).count()
		if user == 1:
			raise ValidationError('邮箱已经存在！')
	def validate_phone(self, field):
		phone = field.data
		user = User.query.filter_by(phone=phone).count()
		if user == 1:
			raise ValidationError('手机号码已经存在！')
2）在home/views.py中。
@home.route('/regist/', methods=['GET', 'POST'])
def regist():
	form = RegistForm()
	if form.validate_on_submit():
		data = form.data
	return render_template('home/regist.html', form=form)
3）在home/regist.html中。
method="post"
	对相关表单进行替换
	给表单加上错误显示信息
	加上消息闪现
4）运行测试。
5）实现逻辑：
a、在models.py中的User数据模型，实现密码验证。
class User(db.Model):
	...
	def check_pwd(self, pwd):
		form werkzeug.security import check_password_hash
		return check_password_hash(self.pwd, pwd)
b、在home/views.py中。
@home.route('/regist/', methods=['GET', 'POST'])
def regist():
	form = RegistForm()
	if form.validate_on_submit():
		data = form.data
		user = User(
			name=data['name'],
			email=data['email'],
			phone=data['phone'],
			pwd=generate_password_hash(data['pwd']),
			uuid=uuid.uuid4().hex
		)
		db.session.add(user)
		db.session.commit()
		flash('注册成功', 'ok')
	return render_template('home/regist.html', form=form)
6）运行测试。



8-2 	会员登录
1）在forms.py中。
class LoginForm(FlaskForm):
	name = StringField(
		label='账号',
		validators=[
			DataRequired('请输入账号！'),
		],
		description='账号',
		render_kw={
			'class': 'form-control input-lg',
			'placeholder': '请输入账号！',
		},
	)
	pwd = PasswordField(
		label='密码',
		validators=[
			DataRequired('请输入密码！')
		],
		description='密码',
		render_kw={
			'class': 'form-control input-lg',
			'placeholder': '请输入密码！',
		}
	)
	submit = SubmitField(
		'登录',
		render_kw={
			'class': 'btn btn-lg btn-primary btn-block',
		},
	)
2）在views.py中。
@home.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		data = form.data
	return render_template('home/login.html', form=form)
3）在login.html中。
method="post"
	对相关表单进行替换
	给表单加上错误显示信息
	加上消息闪现
4）运行测试。
5）完成登录操作。
@home.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		data = form.data
		user = User.query.filter_by(name=data['name']).first()
		if not user.check_pwd(data['pwd']):
			flash('密码错误！', 'err')
			return redirect(url_for('home.login'))
		session['user'] = user.name
		session['user_id'] = user.id
		userlog = Userlog(
			user_id=user.id,
			ip=request.remote_addr
		)
		db.session.add(userlog)
		db.session.commit()
		return redirect(url_for('home.user'))
	return render_template('home/login.html', form=form)
6）运行测试。
7）注销。
@home.route('/logout/')
def logout():
	session.pop('user', None)
	session.pop('user_id', None)
	return redirect(url_for('home.login'))
8）定义登录装饰器。
from functools import wraps

def user_login_req(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'user' not in session:
			return redirect(url_for('home.login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function
9）给会员中心的所有路由函数都加上装饰器。
user、pwd、comments、loginlog、moviecol
10）运行测试。




8-3 	修改会员资料
1）在forms.py中。
from wtforms.field import FileField

class UserdetailForm(FlaskForm):
	name = StringField(
		label='名称',
		validators=[
			DataRequired('请输入名称！'),
		],
		description='名称',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入名称！',
		},
	)
	email = StringField(
		label='邮箱',
		validators=[
			DataRequired('请输入邮箱！'),
			Email('邮箱格式不正确'),  	# 用于验证邮箱
		],
		description='邮箱',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入邮箱！',
		},
	)
	phone = StringField(
		label='手机',
		validators=[
			DataRequired('请输入手机！'),
			Regexp('1[3458]\d{9}', message='手机格式不正确！') 	# 用于验证手机格式
		],
		description='手机',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入手机！',
		},
	)
	face = FileField(
		label='头像',
		validators=[
			DataRequired('请上传头像！'),
		],
		description='头像',
	)
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
	)
	submit = SubmitField(
		'保存修改',
		render_kw={
			'class': 'btn btn-success'
		}
	)
2）在views.py中。
@home.route('/user/', methods=['GET', 'POST'])
@user_login_req
def user():
	form = UserdetailForm()
	if form.validate_on_submit():
		data = form.data
	return render_template('home/user.html', form=form)
3）在user.html中。
method="post" 	enctype="multipart/form-data"
	添加消息闪现，错误提示。
	替换表单对应的标签。
将上传头像的a标签和input标签删除。
	{{ form.face }}
	<img ..../>
	....
4）运行测试。
5）在views.py中。
@home.route('/user/', methods=['GET', 'POST'])
@user_login_req
def user():
	form = UserdetailForm()

	# 设置页面的初始值。
	user = User.query.get(int(session['user_id']))
	form.face.validators = []
	if request.method == 'GET':
		form.name.data = user.name
		form.email.data = user.email
		form.phone.data = user.phone
		form.info.data = user.info

	if form.validate_on_submit():
		data = form.data
	return render_template('home/user.html', form=form, user=user)
6）显示头像。
...
{{ form.face }}
{% if user.face %}
	<img  src="{{ url_for('static', filename='uploads/users/' + user.face) }}"  style="width: 100px"/>
{% else %}
	<img data-src="..."  />
{% endif %}
7）运行测试。
8）定义上传头像。
from werkzeug.utils import secure_filename

	if form.validate_on_submit():
		data = form.data
		file_face = secure_filename(form.face.data.filename)
		if not os.path.exists(app.config['FC_DIR']):
			os.makedirs(app.config['FC_DIR'])
			os.chmod(app.config['FC_DIR'], 'rw')
		user.face = change_filename(file_face)
		form.face.data.save(app.config['FC_DIR'] +  user.face)

		name_count = User.query.filter_by(name=data['name']).count()
		if data['name'] != user.name and name_count == 1:
			flash('昵称已经存在！', 'err')
			return redirect(url_for('home.user'))

		email_count = User.query.filter_by(email=data['email']).count()
		if data['email'] != user.email and email_count == 1:
			flash('邮箱已经存在！', 'err')
			return redirect(url_for('home.user'))

		phone_count = User.query.filter_by(phone=data['phone']).count()
		if data['phone'] != user.phone and phone_count == 1:
			flash('手机号码已经存在！', 'err')
			return redirect(url_for('home.user'))

		user.name = data['name']
		user.email = data['email']
		user.phone = data['phone']
		user.info = data['info']
		db.session.add(user)
		db.session.commit()
		flash('修改成功！', 'ok')
		return redirect(url_for('home.user'))
9）在__init__.py中。
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/users/')
10）运行测试。


8-4 	修改密码
1）在forms.py中。
class PwdForm(FlaskForm):
	old_pwd = PasswordField(
		label='旧密码',
		validators=[
			DataRequired('请输入旧密码！')
		],
		description='旧密码',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入旧密码！',
		}
	),
	new_pwd = PasswordField(
		label='新密码',
		validators=[
			DataRequired('请输入新密码！')
		],
		description='新密码',
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入新密码！',
		}
	),
	submit = SubmitField(
		'修改密码',
		render_kw={
			'class': 'btn btn-success',
		}
	)
2）在views.py中。
@home.route('/pwd/', methods=['GET', 'POST'])
@user_login_req
def pwd():
	form = PwdForm()
	if form.validate_on_submit():
		data = form.data
		user = User.query.filter_by(name=session['user']).first()
		if not user.check_pwd(data['old_pwd']):
			flash('旧密码错误！', 'err')
			return redirect(url_for('home.pwd'))
		user.pwd = generate_password_hash(data['new_pwd'])
		db.session.add(user)
		db.session.commit()
		flash('修改密码成功，请重新登录！', 'ok')
		return redirect(url_for('home.logout'))
	return render_template('home/pwd.html', form=form)
3）在pwd.html中。
method="post"
	将对应的表单进行替换。
	添加消息闪现，错误提示。
4）运行测试。



8-5 	会员登录日志
1）在views.py中。
@home.route('/loginlog/<int:page>/', methods=['GET'])
@user_login_req
def loginlog(page=None):
	if page is None:
		page = 1
	page_data = Userlog.query.filter_by(
		user_id=int(session['user_id'])
	).order_by(
		Userlog.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('home/loginlog.html', page_data=page_data)
2）在loginlog.html中。
{% for v in page_data.items %}
<tr>
	<td>{{ v.id }}</td>
	<td>{{ v.addtime }}</td>
	<td>{{ v.ip }}</td>
</tr>
{% endfor %]}
3）在menu.html中。
...url_for('home.loginlog', page=1)...
4）运行测试。
5）实现分页。创建ui/home_page.html。
将admin_page.html的代码拷贝进来。
	用userloginlog.html中的nav标签，包裹ul标签。
	将ul的class改为pagination
6）loginlog.html中引用。
{% import "ui/home_page.html" as pg %}
...
{{ pg.page(page_data, 'home.loginlog_list') }}
7）运行测试。



9-1 	上映预告-标签筛选-电影分页
	【上映预告】：就是首页的轮播图
1）在views.py中。
@home.route('/animation/')
def animation():
	data = Preview.query.all()
	return render_template('home/animation.html', data=data)
2）在animation.html中。
<ul>
	{% for v in data %}
	<li id="imgCard{{ v.id-1 }}">
		<a href=""/>......
		<img src="{{ url_for('static', filename="uploads/"+v.logo) }}" />
		<p style="...">{{ v.title }}</p>
	</li>
	{% endfor %}
</ul>
3）运行测试。


	【标签筛选】
1）在views.py中。
@home.route('/')
def index():
	tags = Tag.query.all()
	# 用request.args获取参数
	tid = request.args.get('tid', 0)
	star = request.args.get('star', 0)
	time = request.args.get('time', 0)
	pm = request.args.get('pm', 0)
	cm = request.args.get('cm', 0)
	return render_template('home/index.html', tags=tags)
2）在index.html中。
...
	<td ...>电影标签</td>
	...
	{% for v in tags %}
		<a ...>{{ v.name }}</a>
	{% endfor %}


	...
	<td>电影星级</td>
	<td>
		{% for v in range(6) %}
			<a .... {{ v }}星/>
		{% endfor %}
	</td>
3）如何通过电影标签进行筛选呢？
在views.py中。
@home.route('/')
def index():
	...
	cm = request.args.get('cm', 0)
	p = dict(
		tid=tid,
		star=star,
		time=time,
		pm=pm,
		cm=cm,
	)
	return render_template('home/index.html', tags=tags, p=p)
4）在index.html中。
	<td ...>电影标签</td>
	...
	{% for v in tags %}
		<a .href="{{ url_for('home.index') }}?tid={{ v.id }}&star={{ p['star'] }}&time={{ p['time'] }}&pm={{ p['pm'] }}&cm={{ p['cm'] }}"..>{{ v.name }}</a>
	{% endfor %}

	...

	电影星级
	<a .href="{{ url_for('home.index') }}?tid={{ p['tid'] }}&star={{ v }}&time={{ p['time'] }}&pm={{ p['pm'] }}&cm={{ p['cm'] }}".

	上映时间
	<a .href="{{ url_for('home.index') }}?tid={{ p['tid'] }}&star={{ p['star'] }}&time=1&pm={{ p['pm'] }}&cm={{ p['cm'] }}"..
	<a .href="{{ url_for('home.index') }}?tid={{ p['tid'] }}&star={{ p['star'] }}&time=2&pm={{ p['pm'] }}&cm={{ p['cm'] }}"..

	播放数量
	<a .href="{{ url_for('home.index') }}?tid={{ p['tid'] }}&star={{ p['star'] }}&time={{ p['time'] }}&pm=1&cm={{ p['cm'] }}"..
	<a .href="{{ url_for('home.index') }}?tid={{ p['tid'] }}&star={{ p['star'] }}&time={{ p['time'] }}&pm=2&cm={{ p['cm'] }}"..

	评论数量
	<a .href="{{ url_for('home.index') }}?tid={{ p['tid'] }}&star={{ p['star'] }}&time={{ p['time'] }}&pm={{ p['pm'] }}&cm=1"..
	<a .href="{{ url_for('home.index') }}?tid={{ p['tid'] }}&star={{ p['star'] }}&time={{ p['time'] }}&pm={{ p['pm'] }}&cm=2"..
5）运行测试。查看url的变化，主要就是用这个来进行判断。



	【分页操作】
1）在views.py中。
@home.route('/<int:page>', methods=['GET'])
def index(page=None):
	if page is None:
		page = 1

	tags = Tag.query.all()
	# 用request.args获取参数
	page_data = Movie.query

	# 标签
	tid = request.args.get('tid', 0)
	if int(t.tid) != 0:
		page_data = page_data.filter_by(tag_id=int(tid))

	# 星级
	star = request.args.get('star', 0)
	if int(star) != 0:
		page_data = page_data.filter_by(star=int(star))

	# 时间
	time = request.args.get('time', 0)
	if int(time) != 0:
		if int(time) == 1:
			page_data = page_data.order_by(
				Movie.addtime.desc()
			)
		else:
			page_data = page_data.order_by(
				Movie.addtime.asc()
			)

	# 播放量
	pm = request.args.get('pm', 0)
	if int(pm) != 0:	
		if int(pm) == 1:
			page_data = page_data.order_by(
				Movie.playnum.desc()
			)
		else:
			page_data = page_data.order_by(
				Movie.playnum.asc()
			)

	# 评论量
	cm = request.args.get('cm', 0)
	if int(cm) != 0:
		if int(cm) == 1:
			page_data = page_data.order_by(
				Movie.commentnum.desc()
			)
		else:
			page_data = page_data.order_by(
				Movie.commentnum.asc()
			)

	# 进行分页操作
	page = request.args.get('page', 1)
	page_data = page_data.paginate(page=page, per_page=10)

	p = dict(
		tid=tid,
		star=star,
		time=time,
		pm=pm,
		cm=cm,
	)
	return render_template('home/index.html', tags=tags, p=p, page_data=page_data)
2）在index.html、layout.html、home.html中。
	给所有跳转到home.index的链接都加上：page=1
3）在index.html中，进行分页的展示。
{% import "ui/home_page.html" as pg %}
...
{% for v in page_data.items %}
	<img src="{{ url_for('static', filename='uploads/'+v.logo) }}" ...../>
	{{ v.title }}
	{% for val in range(1, v.star+1) %}
	<span class"glyphicon glyphicon-star" ...>
	{% endfor %}
	{% for val in range(1, 5-v.star+1) %}
	<span class"glyphicon glyphicon-star-empty" ...>
	{% endfor %}
	# 其他的span标签删除掉
{% endfor %}
...
{{ pg.page(page_data, 'home.index') }}






9-2 	电影搜索-电影详情
	【电影搜索、搜索分页】
1）在home.html和layout.html中。
# 添加id。去掉href属性。
<input type="text" class="form-control" placeholder="请输入电影名！" id="key_movie">
<span class="input-group-btn">
	<a id="do_search" class="btn btn-default"><span class="glyphicon glyphicon-search">
</span>&nbsp;搜索</a>
...
$(document).ready(function(){
	...
	$('#do_search').click(function(){
		var key = $('#key_movie').val()
		location.href = "{{ url_for('home.search', page=1) }}?key=" + key
	});
});
2）在views.py中。
@home.route('/search/<int:page>/')
def search(page=None):
	if page is None:
		page = 1
	return render_template('home/search.html')
3）运行测试。点击【搜索】按钮。并添加搜索字段，会发现url会加上key=值。
4）在views.py中。
@home.route('/search/<int:page>/')
def search(page=None):
	if page is None:
		page = 1
	key = request.args.get('key', '')
	movie_count = Movie.query.filter(
		Movie.title.ilike('%' + key + '%')
	).count()
	page_data = Movie.query.filter(
		Movie.title.ilike('%' + key + '%') 	# 模糊匹配
	).order_by(
		Movie.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('home/search.html', key=key, page_data=page_data, movie_count=movie_count)
5）在search.html中。
{% import "ui/home_page.html" as pg %}
....
	与"{{ key }}"有关的电影，共{{ movie_count }}部。
	...
	{% for v in page_data.items %}
		..<img ... style="width:131px;height:83px;"  src="{{ url_for('static', filename='uploads/'+v.logo) }}" alt="{{ v.title }}" />
		{{ v.title }}
		{{ v.info }}
	{% endfor %}
	...
	{{ pg.page(page_data, 'home.search') }}
6）运行测试。



	【电影详情】
1）在views.py中。
@home.route('/play/<int:id>/')
def play(id=None):
	# 关联查询，因为电影是有一个标签的
	movie = Movie.query.join(Tag).filter(
		Tag.id == Movie.tag_id,
		Movie.id == int(id),
	).first_or_404()
	return render_template('home/play.html', movie=movie)
2）在index.html、search.html中。
给播放按钮添加：href="{{ url_for('home.play', id=v.id) }}"
3）在play.html中。
	{{ movie.title }}
	{{ movie.tag.name }}
	{{ movie.length }}
	{{ movie.area }}
	# 将index.html里面的星级呈现代码拷贝过来
	{{ movie.release_time }}
	{{ movie.playnum }}
	{{ movie.commentnum }}
	{{ movie.info }}
...
	file: "{{ url_for('static', filename='uploads/'+movie.url) }}"
	title: '{{ v.title }}'
4）运行测试。



10-1 	电影评论-统计
1）在play.html中。判断登录提示、评论框是否应该出现。
...
{% if "user" not in session %}
<div class="alert alert-danger alert-dismissible" role="alert">
                    <button type="button" class="close" data-dismiss="alert">
                        <span aria-hidden="true">×</span>
                        <span class="sr-only">Close</span>
                    </button>
                    <strong>请先<a href="{{ url_for('home.login') }}" target="_blank" class="text-info">登录</a>，才可参与评论！</strong>
                </div>
{% endif %}
...
{% if "user" in session %}
<form role="form" style="margin-bottom:6px;">
                    <div class="form-group">
                        <div>
                            <label for="input_content">内容</label>
                            <textarea id="input_content"></textarea>
                        </div>
                        <div class="col-xs-12" id="error_content"></div>
                    </div>
                    <a class="btn btn-success" id="btn-sub"><span class="glyphicon glyphicon-edit"></span>&nbsp;提交评论</a>
                    &nbsp;
                    <a class="btn btn-danger" id="btn-col"><span class="glyphicon glyphicon-heart"></span>&nbsp;收藏电影</a>
                </form>
{% endif %}
2）运行测试。
3）在forms.py中定义表单。
class CommentForm(FlaskForm):
	content = TextAreaField(
		label='内容',
		validators=[
			DataRequired('请输入内容！'),
		],
		description='内容',
		render_kw={
			'id': 'input_content',
		}
	)
	submit = SubmitField(
		'提交评论',
		render_kw={
			'class': 'btn btn-success',
			'id': 'btn-sub',
		}
	)
4）在views.py中。
@home.route('/play/<int:id>/', methods=['GET', 'POST'])
def play(id=None):
	# 关联查询，因为电影是有一个标签的
	movie = Movie.query.join(Tag).filter(
		Tag.id == Movie.tag_id,
		Movie.id == int(id),
	).first_or_404()

	form = CommentForm()
	if 'user'in session and from.validate_on_submit():
		data = form.data

	return render_template('home/play.html', movie=movie, form=form)
5）在play.html中。
	# 将消息闪现的代码拷贝进来

	全部评论{{ movie.commentnum }}

	{{ form.content.label }}
	{{ form.content }}
	# 将错误提示代码拷贝进来

	{{ form.csrf_token }}
	{{ form.submit }}
6）运行测试。
7）保存内容。
@home.route('/play/<int:id>/', methods=['GET', 'POST'])
def play(id=None):
	# 关联查询，因为电影是有一个标签的
	movie = Movie.query.join(Tag).filter(
		Tag.id == Movie.tag_id,
		Movie.id == int(id),
	).first_or_404()

	# 页面打开一次，就算播放一次
	movie.playnum = movie.playnum + 1

	form = CommentForm()
	if 'user'in session and from.validate_on_submit():
		data = form.data

		comment = Comment(
			content=data['content'],
			movie_id=movie.id,
			user_id=session['user_id'],
		)
		db.session.add(comment)
		db.session.commit()

		# 注意电影的播放次数和评论数也要相应的改变
		movie.commentnum = movie.commentnum + 1
		flash('添加评论成功！', 'ok')
		return redirect(url_for('home.play', id=movie.id))
	db.session.add(movie)
	db.session.commit()

	return render_template('home/play.html', movie=movie, form=form)
8）运行测试。
	刷新几次网页，看播放数量是否有改变。
9）将评论记录显示出来。
@home.route('/play/<int:id>/<int:page>/', methods=['GET', 'POST'])
def play(id=None, page=None):
	movie = Movie.query.join(Tag).filter(
		Tag.id == Movie.tag_id,
		Movie.id == int(id),
	).first_or_404()

	if page is None:
		page = 1
	page_data = Comment.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == movie.id,
		User.id == Comment.user_id,
	).order_by(
		Comment.addtime.desc()
	).paginate(page=page, per_page=10)



	movie.playnum = movie.playnum + 1
	form = CommentForm()
	if 'user'in session and from.validate_on_submit():
		data = form.data
		comment = Comment(
			content=data['content'],
			movie_id=movie.id,
			user_id=session['user_id'],
		)
		db.session.add(comment)
		db.session.commit()
		movie.commentnum = movie.commentnum + 1
		db.session.add(movie)
		db.session.commit()
		flash('添加评论成功！', 'ok')
		return redirect(url_for('home.play', id=movie.id, page=1))
	db.session.add(movie)
	db.session.commit()
	return render_template('home/play.html', movie=movie, form=form, page_data=page_data)
10）在index.html、search.html中。加上page=1。
	{{ url_for('home.play', id=v.id, page=1) }}
11）在play.html中。
...
{% for v in page_data.items %}
<li class="item cl">
                        <a>
                            <i class="avatar size-L radius">
                                <img alt="50x50" src="{{ url_for('static', filename='uploads/users'+v.user.face) }}" class="img-circle"
                                     style="border:1px solid #abcdef;width: 50px;">
                            </i>
                        </a>

                        <div class="comment-main">
                            <header class="comment-header">
                                <div class="comment-meta">
                                    <a class="comment-author" href="user.html">{{ v.user.name }}</a>
                                    评论于
                                    <time title="{{ v.addtime }}" datetime="{{ v.addtime }}">{{ v.addtime }}
                                    </time>
                                </div>
                            </header>
                            <div class="comment-body">
                                <p>{{ v.content | safe }}</p>  # 让html内容显示出来
                            </div>
                        </div>
                    </li>
{% endfor %}
12）运行测试。
13）实现分页。创建ui/comment_page.html。
将home_page.html的代码拷贝进来。
	{% macro page(data, url, id) -%}
	...
	{{ url_for(url, page=1, id=id) }}首页
	...下面也是一样加上id=id
14）
在play.html中。
{% import "ui/comment_page.html" as pg %}
...
{{ pg.page(page_data, 'home.play', movid.id) }}


	【会员中心的评论记录：查看自己的评论记录】
1）在views.py中。
@home.route('/comments/<int:page>/')
@user_login_req
def comments(page=None):
	if page is None:
		page = 1
	page_data = Comment.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == Comment.movie_id,
		User.id == session['user_id'],
	).order_by(
		Comment.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('home/comments.html', page_data=page_data)
2）在comments.html中。
{% import "ui/home_page.html" as pg %}
...
{% for v in page_data.items %}
<li class="item cl">
                        <a>
                            <i class="avatar size-L radius">
                                <img alt="50x50" src="{{ url_for('static', filename='uploads/users'+v.user.face) }}" class="img-circle"
                                     style="border:1px solid #abcdef;width: 50px;">
                            </i>
                        </a>

                        <div class="comment-main">
                            <header class="comment-header">
                                <div class="comment-meta">
                                    <a class="comment-author" href="user.html">{{ v.user.name }}</a>
                                    评论于
                                    <time title="{{ v.addtime }}" datetime="{{ v.addtime }}">{{ v.addtime }}
                                    </time>
                                </div>
                            </header>
                            <div class="comment-body">
                                <p>{{ v.content | safe }}</p>  # 让html内容显示出来
                            </div>
                        </div>
                    </li>
{% endfor %}
...
{{ pg.page(page_data, 'home.comments') }}
3）在menu.html中。
page=1  →  评论日志
4）运行测试。


10-2 	收藏电影
1）在views.py中。
# 通过异步Ajax的方法来添加电影收藏，return的是json信息
# 添加电影收藏
@home.route('moviecol/add/', methods=['GET'])
@user_login_req
def moviecol_add():
	# import json
	# return json.dumps(dict(ok=1))
2）在play.html中。
<script>
	$(document).ready(function(){
		$('#btn-col').click(function(){
			var mid = {{ movie.id }};
			var uid = {{ session['user_id'] }};
			$.ajax({
				url: "{{ url_for('home.moviecol_add') }}",
				type: "GET",
				data: "mid=" + mid + "&uid=" + uid,
				dataType: "json",
				success: function(res){

				} 
			});
		});
	});
</script>
3）运行测试。刷新play.html，点击【收藏电影】按钮，看有没有返回ok=1。
4）在views.py中。
@home.route('moviecol/add/', methods=['GET'])
@user_login_req
def moviecol_add():
	uid = request.args.get('uid', '')
	mid = request.args.get('mid', '')
	moviecol = Moviecol.query.filter_by(
		user_id=int(uid),
		movie_id=int(mid),
	).count()
	if moviecol == 1: 	# 说明已经收藏
		data = dict(ok=0)
	if moviecol == 0:
		moviecol = Moviecol(
			user_id=int(uid),
			movie_id=int(mid),
		)
		db.session.add(moviecol)
		db.session.commit()
		data = dict(ok=1)
	import json
	return json.dumps(data)
5）运行测试。
6）在play.html中。
在form标签结束之后，添加代码：
	<div class="col-md-12">
		<font style="color:green" id="show_col_msg"></font>
	</div>
	<div class="clearfix"></div>
....
success:function(res){
	if(res.ok == 1){
		$("#show_col_msg").empty();
		$("#show_col_msg").append("收藏成功！");
	}else{
		$("#show_col_msg").empty();
		$("#show_col_msg").append("已经收藏！");
	}
}
7）运行测试。点击【收藏电影】按钮。


	【会员页面里面的收藏结果】
1）在views.py中。
@home.route('/moviecol/<int:page>/')
@user_login_req
def moviecol(page=None):
	if page is None:
		page = 1
	page_dat = Moviecol.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == Moviecol.movie_id,
		User.id == session['user_id'],
	).order_by(
		Moviecol.addtime.desc()
	).paginate(page=page, per_page=10)
	return render_template('home/moviecol.html', page_data=page_data)
2）在moviecol.html中。
{% import "ui/home_page.html" as pg %}
...
{% for v in page_data.items %}
<div class="media">
                    <div class="media-left">
                        <a href="{{ url_for('home.play', id=v.movie_id, page=1) }}">
                            <img class="media-object" style="width:131px;height:83px;" src="{{ url_for('static', filename='uploads/'+v.movie.logo) }}" alt="{{ v.movie.title }}">
                        </a>
                    </div>
                    <div class="media-body">
                        <h4 class="media-heading">{{ v.movie.title }}<a href="{{ url_for('home.play', id=v.movie_id, page=1) }}" class="label label-primary pull-right"><span
                                class="glyphicon glyphicon-play"></span>播放影片</a></h4>
                        {{ v.movie.info }}
                    </div>
                </div>
{% endfor %}
...
{{ pg.page(page_data, 'home.moviecol') }}
3）在menu.html中。
page=1  →  收藏电影
4）运行测试。



10-3 	Flask结合Redis消息队列实现电影弹幕
			【没做完笔记】
1、模型：Movie
2、表单：无
3、请求方法：GET、POST
4、访问控制：无
5、消息队列：Redis
6、Flask第三方扩展：Flask-Redis
7、弹幕播放器插件：dplayer.js（开源）

1）pip install flask-redis
	教程：www.imooc.com/article/19536
2）在Linux机器下下载。
	下载redis-4.0.1.tar.gz
	yum -y install gcc gcc-c++
	tar zxf redis-4.0.1.tar.gz
	cd redis-4.0.1/
	make && make install
	./utils/install_server.sh
		↓
	vim /etc/redis/6379.conf
		bind 192.168.4.1（为当前服务器的地址）
		↓
	redis-cli -h 192.168.4.1
	> ping（看是否正常连接）
3）在views.py中。
将play路由函数的代码复制一遍。进行修改。
@home.route('/video/<int:id>/<int:page>/', methods=['GET', 'POST'])
def video(id=None, page=None):
	movie = Movie.query.join(Tag).filter(
		Tag.id == Movie.tag_id,
		Movie.id == int(id),
	).first_or_404()

	if page is None:
		page = 1
	page_data = Comment.query.join(
		Movie
	).join(
		User
	).filter(
		Movie.id == movie.id,
		User.id == Comment.user_id,
	).order_by(
		Comment.addtime.desc()
	).paginate(page=page, per_page=10)
	movie.playnum = movie.playnum + 1
	form = CommentForm()
	if 'user'in session and from.validate_on_submit():
		data = form.data
		comment = Comment(
			content=data['content'],
			movie_id=movie.id,
			user_id=session['user_id'],
		)
		db.session.add(comment)
		db.session.commit()
		movie.commentnum = movie.commentnum + 1
		flash('添加评论成功！', 'ok')
		return redirect(url_for('home.video', id=movie.id, page=1))
	db.session.add(movie)
	db.session.commit()
	return render_template('home/video.html', movie=movie, form=form, page_data=page_data)
4）将play.html的代码复制一份，为video.html。再进行修改。
	将jwplayer插件对应的js代码去掉。即下面的代码：
<script src="{{ url_for('static', filename='jwplayer/jwplayer.js') }}"></script>
<script type="text/javascript">
	jwplayer.key = "P9VTqT/X6TSP4gi/hy1wy23BivBhjdzVjMeOaQ==";

</script>
<script type="text/javascript">
	jwplayer("moviecontainer").setup({
		flashplayer: "{{ url_for('static', filename='jwplayer/jwplayer.flash.swf') }}",
		playlist: [{
			file: "{{ url_for('static', filename='video/htpy.mp4') }}",
			title: "环太平洋"
		}],
		modes: [{
			type: "html5"
		}, {
			type: "flash",
			src: "{{ url_for('static', filename='jwplayer/jwplayer.flash.swf') }}"
		}, {
			type: "download"
		}],
		skin: {
			name: "vapor"
		},
		"playlist.position": "left",
		"playlist.size": 400,
		height: 500,
		width: 774,
	});

</script>

		home.play  →  home.video
		将jwplayer对应的css引入也删除。

没写完.......................



	【代码优化及Bug处理】
1、头像判断
1）在play.html中，判断用户是否有头像。
{% if v.user.face %}
	<img ...  />
{% else %}
	<img ... data-src="holder.js/50x50" />
{% endif %}
2）在comments.html，也是跟上面一样。
{% if v.user.face %}
...
{% else %}
...
{% endif %}
3）在admin/user_list.html中。也是一样。
{% if v.user.face %}
...
{% else %}
...
{% endif %}
4）user_view.html中。也是一样。
{% if v.user.face %}
...
{% else %}
...这里是holder.js/100x100
{% endif %}


2、关键字搜索分页
当你输入关键字，如“空”跳到搜索页，但如果你点击了【首页】按钮，url上的key信息就不见了，这是不被允许的。
1）创建ui/s_page.html。
	将home_page.html的代码复制过来。
所有需要跳转的地方都加上?key={{ data.key }}，如：
"{{ url_for(url, page=1) }}?key={{ data.key }}">首页
2）在search.html中。
将{% import "ui/home_page.html" as pg %}
	改为
{% import "ui/s_page.html" as pg %}
3）在views.py中。将key传递给页面。
...
def search(page=None):
	...
	page_data.key = key
	return render_template...


3、电影右侧播放页面滚动条
添加滚动条：
<div class="panel-body" style="height:459px;overflow:scroll;">

1）在play.html中。
将
	<div class="panel-body" style...>
改为
<div class="panel-body" style="height:459px;overflow:scroll;">
2）在video.html中。也是跟上面一样的操作。
