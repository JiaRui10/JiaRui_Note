网易云课堂——Flask系列教程
### Python虚拟环境介绍与安装：
1. 因为python的框架更新迭代太快了，有时候需要在电脑上存在一个框架的多个版本，这时候虚拟环境就可以解决这个问题。
2. 通过以下命令安装虚拟环境：pip install virtualenv
3. 开辟新的虚拟环境：virtualenv [virtualenv-name]
4. 激活虚拟环境：
    * [类linux]：source [虚拟环境的目录]/bin/activate
    * [windows]：直接进入到虚拟环境的目录，然后执行activate
    * 退出虚拟环境：deactivate

### 第一个flask程序讲解：
1. 第一次创建项目的时候，要添加flask的虚拟环境。添加虚拟环境的时候，一定要选择到python这个执行文件。
比如你的flask的虚拟环境的目录在/User/Virtualenv/flask-env/bin/python。
2. flask程序代码的详细解释：
    ```
    # 从flask这个框架中导入Flask这个类
    from flask import Flask
 
    # 初始化一个Flask对象
    # Flaks()
    # 需要传递一个参数__name__
    # 1. 方便flask框架去寻找资源
    # 2. 方便flask插件比如Flask-Sqlalchemy出现错误的时候，好去寻找问题所在的位置
    app = Flask(__name__)
 
 
    # @app.route是一个装饰器
    # @开头，并且在函数的上面，说明是装饰器
    # 这个装饰器的作用，是做一个url与视图函数的映射
    # 127.0.0.1:5000/   ->  去请求hello_world这个函数，然后将结果返回给浏览器
    @app.route('/')
    def hello_world():
        return '我是第一个flask程序'
 
 
    # 如果当前这个文件是作为入口程序运行，那么就执行app.run()
    if __name__ == '__main__':
        # app.run()
        # 启动一个应用服务器，来接受用户的请求
        # while True:
        #   listen()
        app.run()
    ```

### 设置debug模式：
1. 在app.run()中传入一个关键字参数debug,app.run(debug=True)，就设置当前项目为debug模式。
2. debug模式的两大功能：
    * 当程序出现问题的时候，可以在页面中看到错误信息和出错的位置。
    * 只要修改了项目中的`python`文件，程序会自动加载，不需要手动重新启动服务器。



### 使用配置文件：
1. 新建一个`config.py`文件。 
	写入代码： DEBUG = True
2. 在主app文件中导入这个文件，并且配置到`app`中，示例代码如下：
    ```
    import config
    app.config.from_object(config)
    ```
3. 还有许多的其他参数，都是放在这个配置文件中，比如`SECRET_KEY`和`SQLALCHEMY`这些配置，都是在这个文件中。


### url传参数：
1. 参数的作用：可以在相同的URL，但是指定不同的参数，来加载不同的数据。
2. 在flask中如何使用参数：
    ```
    @app.route('/article/<id>')
    def article(id):
        return u'您请求的参数是：%s' % id
    ``` 
    * 参数需要放在两个尖括号中。
    * 视图函数中需要放和url中的参数同名的参数。


### 反转URL：
1. 什么叫做反转URL：从视图函数到url的转换叫做反转url
2. 反转url的用处：
    * 在页面重定向的时候，会使用url反转。
    * 在模板中，也会使用url反转。
    url_for()

### 页面跳转和重定向：
1. 用处：在用户访问一些需要登录的页面的时候，如果用户没有登录，那么可以让她重定向到登录页面。
2. 代码实现：
    ```
    from flask import redirect,url
    return redirect(url_for('login'))
    ```

### Flask渲染Jinja2模板和传参：
1. 如何渲染模板：
    * 模板放在`templates`文件夹下
    * 从`flask`中导入`render_template`函数。
    * 在视图函数中，使用`render_template`函数，渲染模板。注意：只需要填写模板的名字，不需要填写`templates`这个文件夹的路径。
2. 模板传参：
    * 如果只有一个或者少量参数，直接在`render_template`函数中添加关键字参数就可以了。
    * 如果有多个参数的时候，那么可以先把所有的参数放在字典中，然后在`render_template`中，
    使用两个星号，把字典转换成关键参数传递进去，这样的代码更方便管理和使用。
@app.route('/')
def index():
	context = {
		'username': '姓名',
		'gender': '男',
		'age': 18,
	}
	return render_template('index.html', **context)  	# 关键字参数传递
3. 在模板中，如果要使用一个变量，语法是：`{{params}}`
4. 访问模型中的属性或者是字典，可以通过`{{params.property}}`的形式，或者是使用`{{params['age']}}`.


### if判断： 
1. 语法：       ```     {% if xxx %}     {% else %}     {% endif %}     ``` 
2. if的使用，可以和python中相差无几。

### for循环遍历列表和字典：
1. 字典的遍历，语法和`python`一样，可以使用`items()`、`keys()`、`values()`、`iteritems()`、`iterkeys()`、`itervalues()`
    ```
    {% for k,v in user.items() %}
        <p>{{ k }}：{{ v }}</p>
    {% endfor %}
    ```
2. 列表的遍历：语法和`python`一样。
    ```
    {% for website in websites %}
        <p>{{ website }}</p>
    {% endfor %}
    ```


### 过滤器：
1. 介绍和语法：
    * 介绍：过滤器可以处理变量，把原始的变量经过处理后再展示出来。作用的对象是变量。
    * 语法：
        ```
        # 如果有头像，显示头像。如果没有，显示默认头像。
        {{ avatar|default('xxx') }}
        ```
2. default过滤器：如果当前变量不存在，这时候可以指定默认值。
3. length过滤器：求列表或者字符串或者字典或者元组的长度。
4. 常用的过滤器：
    abs(value)：返回一个数值的绝对值。示例：-1|abs
    default(value,default_value,boolean=false)：如果当前变量没有值，则会使用参数中的值来代替。示例：name|default('xiaotuo')——如果name不存在，则会使用xiaotuo来替代。boolean=False默认是在只有这个变量为undefined的时候才会使用default中的值，如果想使用python的形式判断是否为false，则可以传递boolean=true。也可以使用or来替换。
    escape(value)或e：转义字符，会将<、>等符号转义成HTML中的符号。示例：content|escape或content|e。
    first(value)：返回一个序列的第一个元素。示例：names|first
    format(value,*arags,**kwargs)：格式化字符串。比如：
 
      {{ "%s" - "%s"|format('Hello?',"Foo!") }}
      将输出：Helloo? - Foo!
    last(value)：返回一个序列的最后一个元素。示例：names|last。
 
    length(value)：返回一个序列或者字典的长度。示例：names|length。
    join(value,d=u'')：将一个序列用d这个参数的值拼接成字符串。
    safe(value)：如果开启了全局转义，那么safe过滤器会将变量关掉转义。示例：content_html|safe。
    int(value)：将值转换为int类型。
    float(value)：将值转换为float类型。
    lower(value)：将字符串转换为小写。
    upper(value)：将字符串转换为小写。
    replace(value,old,new)： 替换将old替换为new的字符串。
    truncate(value,length=255,killwords=False)：截取length长度的字符串。
    striptags(value)：删除字符串中所有的HTML标签，如果出现多个空格，将替换成一个空格。
    trim：截取字符串前面和后面的空白字符。
    string(value)：将变量转换成字符串。
    wordcount(s)：计算一个长字符串中单词的个数。


### 继承和block：
1. 继承作用和语法：
    * 作用：可以把一些公共的代码放在父模板中，避免每个模板写同样的代码。
    * 语法：
        ```
        {% extends 'base.html' %}
        ```
2. block实现：
    * 作用：可以让子模板实现一些自己的需求。父模板需要提前定义好。
    * 注意点：字模板中的代码，必须放在block块中。
    {% block content %}{% endblock %}
 
### url链接：使用`url_for(视图函数名称)`可以反转成url。
 
### 加载静态文件：
1. 语法：`url_for('static',filename='路径')`
2. 静态文件，flask会从`static`文件夹中开始寻找，所以不需要再写`static`这个路径了。
3. 可以加载`css`文件，可以加载`js`文件，还有`image`文件。
    ```
    第一个：加载css文件
    <link rel="stylesheet" href="{{ url_for('static',filename='css/index.css') }}">
    第二个：加载js文件
    <script src="{{ url_for('static',filename='js/index.js') }}"></script>
    第三个：加载图片文件
    <img src="{{ url_for('static',filename='images/zhiliao.png') }}" alt="">
    ```





### 安装MySQL-python
数据库引擎，或者叫MySQL中间件。

1. 如果是在类unix系统上，直接进入虚拟环境，输入`sudo pip install mysql-python`。
2. 如果是在windows系统上，那么在这里下载`http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python`下载`MySQL_python‑1.2.5‑cp27‑none‑win_amd64.whl`，然后在命令行中，进入到`MySQL_python‑1.2.5‑cp27‑none‑win_amd64.whl`所在的目录，输入以下命令进行安装：
    ```
pip install MySQL_python‑1.2.5‑cp27‑none‑win_amd64.whl
	↓
没有安装成功：https://www.cnblogs.com/chenjingyi/p/5740415.html


### Flask-SQLAlchemy的介绍与安装：
1. ORM：Object Relationship Mapping（模型关系映射）。
2. flask-sqlalchemy是一套ORM框架。
3. ORM的好处：可以让我们操作数据库跟操作对象是一样的，非常方便。因为一个表就抽象成一个类，一条数据就抽象成该类的一个对象。
4. 安装`flask-sqlalchemy`：`sudo pip install flask-sqlalchemy`。



### Flask-SQLAlchemy的使用：
1. 初始化和设置数据库配置信息：
    * 使用flask_sqlalchemy中的SQLAlchemy进行初始化：
        ```
        from flask_sqlalchemy import SQLAlchemy
        app = Flask(__name__)
        db = SQLAlchemy(app)
        ```
2. 设置配置信息：在`config.py`文件中添加以下配置信息：
    ```
    # dialect+driver://username:password@host:port/database
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'db_demo1'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST
                                                 ,PORT,DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```

3. 在主`app`文件中，添加配置文件：
    ```
    app = Flask(__name__)
    app.config.from_object(config)
    db = SQLAlchemy(app)
    ```
4. 做测试，看有没有问题：
    ```
    db.create_all()
    ```
    如果没有报错，说明配置没有问题，如果有错误，可以根据错误进行修改。

### 使用Flask-SQLAlchemy创建模型与表的映射：
1. 模型需要继承自`db.Model`，然后需要映射到表中的属性，必须写成`db.Column`的数据类型。
2. 数据类型：
    * `db.Integer`代表的是整形.
    * `db.String`代表的是`varchar`，需要指定最长的长度。
    * `db.Text`代表的是`text`。
3. 其他参数：
    * `primary_key`：代表的是将这个字段设置为主键。
    * `autoincrement`：代表的是这个主键为自增长的。
    * `nullable`：代表的是这个字段是否可以为空，默认可以为空，可以将这个值设置为`False`，在数据库中，这个值就不能为空了。
4. 最后需要调用`db.create_all`来将模型真正的创建到数据库中。


### Flask-SQLAlchemy数据的增、删、改、查：
1. 增：
    ```
    # 增加：
    article1 = Article(title='aaa',content='bbb')
    db.session.add(article1)
    # 事务
    db.session.commit()
    ```
2. 查：
    ```
    # 查
    # select * from article where article.title='aaa';
    article1 = Article.query.filter(Article.title == 'aaa').first()
    print 'title:%s' % article1.title
    print 'content:%s' % article1.content
    ```
3. 改：
    ```
    # 改：
    # 1. 先把你要更改的数据查找出来
    article1 = Article.query.filter(Article.title == 'aaa').first()
    # 2. 把这条数据，你需要修改的地方进行修改
    article1.title = 'new title'
    # 3. 做事务的提交
    db.session.commit()
    ```
4. 删：
    ```
    # 删
    # 1. 把需要删除的数据查找出来
    article1 = Article.query.filter(Article.content == 'bbb').first()
    # 2. 把这条数据删除掉
    db.session.delete(article1)
    # 3. 做事务提交
    db.session.commit()
    ```





### Flask-SQLAlchemy外键及其关系：
1. 外键：
    ```
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer,primary_key=True,autoincrement=True)
        username = db.Column(db.String(100),nullable=False)

    class Article(db.Model):
        __tablename__ = 'article'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        title = db.Column(db.String(100),nullable=False)
        content = db.Column(db.Text,nullable=False)
        author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

        author = db.relationship('User',backref=db.backref('articles')) 	
    ```
2. `author = db.relationship('User',backref=db.backref('articles'))`解释：
    * 给`Article`这个模型添加一个`author`属性，可以访问这篇文章的作者的数据，像访问普通模型一样。
    * `backref`是定义反向引用，可以通过`User.articles`访问这个模型所写的所有文章。

 查找文章对应的作者：
 	article = Article.query.filter(Article.title == 'aaa').first()
 	print('username: {}'.format(article.author.username))
 找出作者写过的所有文章：
 	user = User.query.filter(User.username == 'zhiliao').first()
 	result = user.articles    	# 后面的.articles为backref=db.backref('articles') 这里决定
 	for article in result:
 		print article.title

3. 多对多：
    * 多对多的关系，要通过一个中间表进行关联。
    * 中间表，不能通过`class`的方式实现，只能通过`db.Table`的方式实现。
    * 设置关联：`tags = db.relationship('Tag',secondary=article_tag,backref=db.backref('articles'))`需要使用一个关键字参数`secondary=中间表`来进行关联。
    * 访问和数据添加可以通过以下方式进行操作：
        - 添加数据：
            ```
            article1 = Article(title='aaa')
            article2 = Article(title='bbb')

            tag1 = Tag(name='111')
            tag2 = Tag(name='222')

            article1.tags.append(tag1)
            article1.tags.append(tag2)

            article2.tags.append(tag1)
            article2.tags.append(tag2)

            db.session.add(article1)
            db.session.add(article2)

            db.session.add(tag1)
            db.session.add(tag2)

            db.session.commit()
            ``` 
        - 访问数据：
            ```
            article1 = Article.query.filter(Article.title == 'aaa').first()
            tags = article1.tags
            for tag in tags:
                print tag.name
            ```


### Flask-Script的介绍与安装：
1. Flask-Script：Flask-Script的作用是可以通过命令行的形式来操作Flask。例如通过命令跑一个开发版本的服务器、设置数据库，定时任务等。
2. 安装：首先进入到虚拟环境中，然后`pip install flask-script`来进行安装。
3. 如果直接在主`manage.py`中写命令，那么在终端就只需要`python manage.py command_name`就可以了。
4. 如果把一些命令集中在一个文件中，那么在终端就需要输入一个父命令，比如`python manage.py db init`。
5. 例子：
    manage.py
    ```
    from flask_script import Manager
    from flask_script_demo import app
    from db_scripts import DBManager

    manager = Manager(app)


    # 和数据库相关的操作，我都放在一起

    @manager.command
    def runserver():
        print '服务器跑起来了!!!!!'
    manager.add_command('db',DBManager)

    if __name__ == '__main__':
        manager.run()
    ```
6. 有子命令的例子：
    db_scripts.py
    ```
    #encoding: utf-8

    from flask_script import Manager

    DBManager = Manager()

    @DBManager.command
    def init():
        print '数据库初始化完成'

    @DBManager.command
    def migrate():
        print '数据表迁移成功'
    ```




### 分开`models`以及解决循环引用：
1. 分开models的目的：为了让代码更加方便的管理。
2. 如何解决循环引用：把`db`放在一个单独的文件中，切断循环引用的线条就可以了。



### Flask-Migrate的介绍与安装：
1. 介绍：因为采用`db.create_all`在后期修改字段的时候，不会自动的映射到数据库中，必须删除表，然后重新运行`db.craete_all`才会重新映射，这样不符合我们的需求。因此flask-migrate就是为了解决这个问题，她可以在每次修改模型后，可以将修改的东西映射到数据库中。
2. 首先进入到你的虚拟环境中，然后使用`pip install flask-migrate`进行安装就可以了。
3. 使用`flask_migrate`必须借助`flask_scripts`，这个包的`MigrateCommand`中包含了所有和数据库相关的命令。
4. `flask_migrate`相关的命令：
    * `python manage.py db init`：初始化一个迁移脚本的环境，只需要执行一次。
    * `python manage.py db migrate`：将模型生成迁移文件，只要模型更改了，就需要执行一遍这个命令。
    * `python manage.py db upgrade`：将迁移文件真正的映射到数据库中。每次运行了`migrate`命令后，就记得要运行这个命令。
5. 注意点：需要将你想要映射到数据库中的模型，都要导入到`manage.py`文件中，如果没有导入进去，就不会映射到数据库中。
6. `manage.py`的相关代码：
    ```
    from flask_script import Manager
    from migrate_demo import app
    from flask_migrate import Migrate,MigrateCommand
    from exts import db
    from models import Article

    # init
    # migrate
    # upgrade
    # 模型  ->  迁移文件  ->  表

    manager = Manager(app)

    # 1. 要使用flask_migrate，必须绑定app和db
    migrate = Migrate(app,db)

    # 2. 把MigrateCommand命令添加到manager中
    manager.add_command('db',MigrateCommand)

    if __name__ == '__main__':
        manager.run()
    ```


### cookie：
1. `cookie`出现的原因：在网站中，http请求是无状态的。也就是说即使第一次和服务器连接后并且登录成功后，第二次请求服务器依然不能知道当前请求是哪个用户。cookie的出现就是为了解决这个问题，第一次登录后服务器返回一些数据（cookie）给浏览器，然后浏览器保存在本地，当该用户发送第二次请求的时候，就会自动的把上次请求存储的cookie数据自动的携带给服务器，服务器通过浏览器携带的数据就能判断当前用户是哪个了。
2. 如果服务器返回了`cookie`给浏览器，那么浏览器下次再请求相同的服务器的时候，就会自动的把`cookie`发送给浏览器，这个过程，用户根本不需要管。
3. `cookie`是保存在浏览器中的，相对的是浏览器。

### session：
1. `session`介绍：session和cookie的作用有点类似，都是为了存储用户相关的信息。不同的是，cookie是存储在本地浏览器，而session存储在服务器。存储在服务器的数据会更加的安全，不容易被窃取。但存储在服务器也有一定的弊端，就是会占用服务器的资源，但现在服务器已经发展至今，一些session信息还是绰绰有余的。
2. 使用`session`的好处：
    * 敏感数据不是直接发送回给浏览器，而是发送回一个`session_id`，服务器将`session_id`和敏感数据做一个映射存储在`session`(在服务器上面)中，更加安全。
    * `session`可以设置过期时间，也从另外一方面，保证了用户的账号安全。

### flask中的session工作机制：
1. flask中的session机制是：把敏感数据经过加密后放入`session`中，然后再把`session`存放到`cookie`中，下次请求的时候，再从浏览器发送过来的`cookie`中读取`session`，然后再从`session`中读取敏感数据，并进行解密，获取最终的用户数据。
2. flask的这种`session`机制，可以节省服务器的开销，因为把所有的信息都存储到了客户端（浏览器）。
3. 安全是相对的，把`session`放到`cookie`中，经过加密，也是比较安全的，这点大家放心使用就可以了。

### 操作session：
1. session的操作方式：
    * 使用`session`需要从`flask`中导入`session`，以后所有和`sessoin`相关的操作都是通过这个变量来的。
    * 使用`session`需要设置`SECRET_KEY`，用来作为加密用的。并且这个`SECRET_KEY`如果每次服务器启动后都变化的话，那么之前的`session`就不能再通过当前这个`SECRET_KEY`进行解密了。
    * 操作`session`的时候，跟操作字典是一样的。
    * 添加`session`：`session['username']`。
    * 删除：`session.pop('username')`或者`del session['username']`。
    * 清除所有`session`：`session.clear()`
    * 获取`session`：`session.get('username')`
2. 设置session的过期时间：
    * 如果没有指定session的过期时间，那么默认是浏览器关闭后就自动结束
    * 如果设置了session的permanent属性为True，那么过期时间是31天。
    * 可以通过给`app.config`设置`PERMANENT_SESSION_LIFETIME`来更改过期时间，这个值的数据类型是`datetime.timedelay`类型。

import os
app.config['SECRET_KEY'] = os.urandom(24)


### get请求和post请求：
1. get请求：
    * 使用场景：如果只对服务器获取数据，并没有对服务器产生任何影响，那么这时候使用get请求。
    * 传参：get请求传参是放在url中，并且是通过`?`的形式来指定key和value的。
2. post请求：
    * 使用场景：如果要对服务器产生影响，那么使用post请求。
    * 传参：post请求传参不是放在url中，是通过`form data`的形式发送给服务器的。

### get和post请求获取参数：
1. get请求是通过`flask.request.args`来获取。
2. post请求是通过`flask.request.form`来获取。
3. post请求在模板中要注意几点：
    * input标签中，要写name来标识这个value的key，方便后台获取。
    * 在写form表单的时候，要指定`method='post'`，并且要指定`action='/login/'`。
4. 示例代码：
    ```
        <form action="{{ url_for('login') }}" method="post">
            <table>
                <tbody>
                    <tr>
                        <td>用户名：</td>
                        <td><input type="text" placeholder="请输入用户名" name="username"></td>
                    </tr>
                    <tr>
                        <td>密码：</td>
                        <td><input type="text" placeholder="请输入密码" name="password"></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td><input type="submit" value="登录"></td>
                    </tr>
                </tbody>
            </table>
        </form>
    ```

### 保存全局变量的g属性：
g：global
1. g对象是专门用来保存用户的数据的。
2. g对象在一次请求中的所有的代码的地方，都是可以使用的。

### 钩子函数（hook）：
1. before_request：
    * 在请求之前执行的
    * 是在视图函数执行之前执行的
    * 这个函数只是一个装饰器，他可以把需要设置为钩子函数的代码放到视图函数执行之前来执行
2. context_processor：
    * 上下文处理器应该返回一个字典。字典中的`key`会被模板中当成变量来渲染。
    * 上下文处理器中返回的字典，在所有页面中都是可用的。
    * 被这个装饰器修饰的钩子函数，必须要返回一个字典，即使为空也要返回。


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    g.user = user
    if session.get('username'):
        g.username = session.get('username')
# 可以减少后期其他视图函数对数据库进行操作。




    【项目实战】
1-1     项目结构搭建
1）创建flask项目，会出现static、templates文件夹，还有根目录下面的zlktqa.py。
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
    app.run()
2）在根目录下创建config.py。
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

# 数据库相关配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlktqa_demo'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST
                                                 ,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
3）进入mysql，将zlktqa_demo数据库创建出来。
create database zlktqa_demo charset utf8;
4）在zlktqa.py中，导入配置。
import config
...
app.config.from_object(config)
5）在根目录下创建exts.py，专门用来存放db。
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
6）在根目录下创建models.py文件，用于存放模型。
from exts import db
7）在根目录下创建manage.py文件，用于存放命令。
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand  # 模型到表的迁移
from zlktqa import app
from exts import db
# 等后面模型创建好了，模型也要导入进来

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()



1-2     完成导航栏
编写index.html。
使用bootstrap cdn、jquery cnd。
使用bootstrap就是复制粘贴、复制粘贴。



1-3     父模板抽离
编写base.html。



1-4     登录页面完成
login.html。

在zlktqa.py中。
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        pass



1-5     注册页面完成
regist.html。
在zlktqa.py中。
@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        pass



1-6     User模型创建
1）在models.py中。
class User(db.Model):    
    __tablename__ = "users"
        id = db.Column(db.Integer,primary_key=True,autoincrement=True)
        username = db.Column(db.String(50),nullable=False)
        telephone = db.Column(db.String(11),nullable=False)
        _password = db.Column(db.String(100),nullable=False)
2）将用户模型映射到数据库的表中。
在manage.py中。
from models import User
...
3）打开终端：
python manage.py db init        # 初始化迁移环境
python manage.py db migrate 
python manage.py db upgrade
4）在数据库中查看，是否有表生成。



1-7     注册功能完成
1）在zlktqa.py中。
from exts import db

db.init_app(app)

@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机已被注册，请更换手机号码！'
        else:
            if password1 != password2:
                return '两次密码不相等，请核对后再填写'
            else:
                user = User(
                    telephone=telephone,
                    username=username,
                    password=password1
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))



1-8     登录功能完成
1）在zlktqa.py中。
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(
            User.telephone==telephone,
            User.password==password,
        ).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号码或者密码错误，请确认后登录'

...
def logout():
    session.clear()
    return redirect(url_for('login'))



1-9         发布问答界面完成
1）在zlktqa.py中。
@app.route('/question/', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        pass
2）question.html。



1-10    登录限制
1）一般把装饰器相关的代码放在一个文件中。创建decorators.py。
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # pass
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper
2）在zlktqa.py中。
from decorators import login_required
给需要限制登录的视图函数，加上装饰器。



1-11    发布问答功能完成
1）在models.py中。
from datetime import datetime

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('questions'))

2）将用户模型映射到数据库的表中。
在manage.py中导入Question模型。
打开终端：
python manage.py db migrate
python manager.py db upgrade
3）在zlktqa.py中。
@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))



1-12    首页布局完成
index.html。



1-13    首页功能完成
1）
@app.route('/')
def index():
    context = {
        # 排序
        'questions': Question.query.order_by('-create_time').all()
    }
    returm render_template('index.html', **context)
2）在index.html中就不能将数据写死了。



1-14    问答详情完成
1）编写detail.html。
2）
@app.route('/detail/<int:question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)
3）修改detail.html。



1-15    评论布局完成
1）编写detail.html。
2）
@app.route('/add_answer/', methods=['POST'])
def add_answer():
    content = request.form.get('answer_content')



1-16    评论模型和功能实现
1）在models.py中。
class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('user.id'))

    question = db.relationship('Question',backref=db.backref('answers',order_by=create_time.desc()))
    author = db.relationship('UserModel',backref=db.backref('answers'))
2）将用户模型映射到数据库的表中。
在manage.py中导入Answer。
打开终端：
python manage.py db migrate
python manage.py db upgrade
3）打开mysql。查看是否正常生成。
4）
@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))
5）
在detail.html中。
{% for answer in question.answers %}
    ...
{% endfor %}



1-17    评论列表展示
detail.html中。