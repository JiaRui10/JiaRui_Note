【SQLite、MySQL、MongoDB】
	【SQLite】
嵌入式关系数据库，实现自包容、零配置、支持事务的SQL数据库引擎。
单文件数据库引擎，一个文件即是一个数据库，方便存储和转移。
Linux：基本有预装，如没有：sudo  apt-get install sqlite3
Windows：下载sqlite-dll-*.zip和sqlite-tools-win32-*.zip。将两个文件解压到D:\sqlite3，在将该目录添加到环境变量PATH


	【SQL语法】
SQL是一门ANSI的标准计算机语言，用来访问和操作数据库系统，用于取回和更新数据库中的数据，并与数据库程序协同工作。
注意：每个数据库都有一些它们独特的SQL语言。

SQL语言主要分为：数据定义语言（DDL）和数据操作语言（DML）。
数据定义语言（DDL）是我们有能力创建或删除表格，也可以定义索引（键），规定表之间的链接，以及施加表间的约束。
数据操作语言（DML）用于执行查询、更新、插入和删除记录。
SQL语法对大小写不敏感。
1）数据定义语言（DDL）
创建数据库：		CREATE DATABASE first_db
删除数据库：		DROP DATABASE first_db
创建数据库中的表：		
			CREATE TABLE student(id integer, Name varchar(255), Birth date, Address varchar(255), City varchar(255))

在表中添加列：		ALTER TABLE student ADD class varchar(255)
修改表中某一列的数据类型：
			ALTER TABLE table_name ALTER COLUMN column_name datatype
删除表中的某一列：	ALTER TABLE table_name DROP COLUMN column_name
删除表： 		DROP TABLE student


CREATE INDEX语句用于创建索引，有助于加快SELECT查询和WHERE子句。
单一索引：在表的某一列设置索引。
			CREATE INDEX index_name ON table_name(column_name)
唯一索引：不允许任何重复的值插入到表中。
			CREATE UNIQUE INDEX index_name on table_name(column_name)
组合索引：对一个表中的几列进行索引。
			CREATE INDEX index_name on table_name(column1, column2)
隐式索引：在创建对象时，由数据库服务器自动创建的索引。（比如在之前的student表对Name添加名称为name_index的索引）
			CREATE INDEX name_index ON student(Name)

删除索引：		DROP INDEX name_index

2）数据操作语言（DML）
	增删改查
获取Name和City列的内容：
			SELECT Name, City FROM student

获取所有列：
			SELECT * FROM student

去重复：
			SELECT DISTINCT Name,City FROM student

按条件查找：
			SELECT Name,City FROM student WHERE City='beijing'
			SELECT Name,City FROM student WHERE id > 2
			SELECT * FROM student WHERE Name='marry' and City='shanghai'
			SELECT * FROM student WHERE Name='marry' OR id>2
			SELECT * FROM student WHERE (Name='marry' and City='shanghai') OR id>2

多查询结果进行排序：
（ASC  →  升序；DESC  →  降序）
			SELECT Name,City FROM student ORDER BY id
			SELECT Name,City FROM student ORDER BY Name,id
			SELECT Name,City FROM student ORDER BY id DESC
			SELECT Name,City FROM student ORDER BY Name DESC, id ASC（按Name字母降序排列，Name相同再按照id升序排列）

修改表中的数据：
			UPDATE student SET Name='jack', City='Nanjing' WHERE id = 1

删除表中的行：
			DELETE FROM student 	WHERE Name='jack'

插入新的行：
			INSERT INTO student VALUES(5, 'Bill', '1999-8-10', 'beijing')
			INSERT INTO student (id,Name,City) VALUE(6,'Rose','shenzhen')


	【SQLite增删改查】
创建数据库：
			sqlite3 D:\test.db
创建表：
			CREATE TABLE person (id integer primary key,name varchar(20),age integer);
插入数据：
			INSERT INTO person(name,age) VALUES('qiye',20);	
修改数据：
			UPDATE person SET age=17 WHERE name='qiye';
查询表中的记录：
			SELECT * FROM person;
删除：
			DELETE FROM person WHERE name='qiye';

常用SQLite命令
显示表结构：
			sqlite> .schema [table]
获取所有表和视图：
			sqlite> .tables
获取指定表的索引列表：
			sqlite> .indices [table ]
导出数据库到SQL文件：
			sqlite> .output [filename ]
			sqlite> .dump
			sqlite> .output stdout
从SQL文件导入数据库：
			sqlite> .read [filename ]
格式化输出数据到CSV格式：
			sqlite>.output [filename.csv]
			sqlite>.separator ,
			sqlite>.select * from test;
			sqlite>.output stdout
从CSV文件导入数据到表中：
			sqlite> create table newtable (id integer primary key, name varchar(20), age integer);
			sqlite> .import [filename.csv ] newtable
备份：
			sqlite3 test.db .dump > backup.sql 
恢复：
			sqlite3 test.db < backup.sql


【SQLite事务】
数据库事务指的是作为单个逻辑工作单元执行的一系列操作，要么完全执行，要么完全不执行。比如网上购物，用户付款的过程。
通俗来说，事务是将四个步骤打包成一件事来做，其中任何一个步骤出错，都代表这件事情没完成，数据库就会回滚到之前的状态。

SQLite主要通过以下命令来控制事务：
BEGIN TRANSACTION：启动事务处理
COMMIT：保存更改，或者使用END TRANSACTION命令
ROLLBACK：回滚所做的更改

控制事务的命令只与DML命令中的INSERT、UPDATE和DELETE一起使用，不能在创建表和删除表时使用，因为这两个操作是数据库自动提交的。

示例：
（事务回滚）
	SELECT * FROM person;
	BEGIN;
	INSERT INTO person(name,age) VALUE('qiye', 20);
	ROLLBACK;
	SELECT * FROM person;
（事务提交）
	SELECT * FROM person;
	BEGIN;
	INSERT INTO person(name,age) VALUES('qiye', 20);
	ROLLBACK;
	SELECT * FROM person;
	BEGIN;
	INSERT INTO person(name,age) VALUES('qiye', 20);
	COMMIT;
	SELECT * FROM person;


【Python操作SQLite】
import sqlite3
con = sqlite3.connect('D:\test.db')
con = sqlite3.connect(':memory:') 	# 在内存中创建
cur = con.cursor() 	# 创建一个游标对象
	execute()：执行sql语句
	executemany()：执行多条sql语句
	close()：关闭游标
	fetchone()：从结果中取出一条记录，并将游标指向下一条记录
	fetchmany()：从结果中取多条记录
	fetchall()
	scroll()：游标滚动
cur.execute('CREATE TABLE person (id integer primary key,name varchar(20), age integer)')
cur.execute('INSERT INTO person VALUES (?,?,?)', {0, 'qiye', 20})
cur.executemany('INSERT INTO person VALUES (?,?,?)', [(3, 'marry', 20), (4, 'jack', 20)])
con.commit()
con.rollback() 		# 如果出现错误，还可以使用回滚操作

# 查询数据
cur.execute('SELECT * FROM person')

cur.execute('SELECT * FROM person')
res = cur.fetchall()
for line in res:
	print(line)

cur.execute('SELECT * FROM person')
res = cur.fetchone()
print(res)

# 修改和删除数据
cur.execute('UPDATE person SET name=? WHERE id=?', ('role', 1))
cur.execute('DELETE FROM person WHERE id=?', (0,))
con.commit()
con.close()
# 执行完所有操作记得关闭数据库，插入或者修改中文数据时，记得在中文字符串之前加上'u'


	【MySQL】
Ubuntu下安装和配置MySQL：
	sudo apt-get install mysql-server
	sudo apt-get install mysql-client
	sudo apt-get install libmysqlclient-dev
	# 验证是否安装成功
	sudo netstat -tap | grep mysql

	# 登录
	mysql -u -root -p

Windows下安装和配置MySQL：
	略。看书

创建数据库，并设置编码：
			create database test character set gbk;

			use test;

创建表student：
			create table student(
				id int unsigned not null auto_increment primary key,
				name char(8) not null,
				sex char(4) not null,
				age tinyint unsigned not null
			);

导入sql文件：
			（登录前）mysql -D test -u root -p< D:\create_student.sql
			（登录后）source D:\create_student.sql


增删改查操作：
			insert into student values (NULL, "七夜", "男", 24);
			update student set age=18 where name="七夜";
			select name,age from student;
			delete from student where age = 18;
（MySQL中字符串既可以使用单引号包裹，也可以使用双引号包裹。）

添加列：
			alter table student add address varchar(60) after age;
修改列：
			alter table student change address addr char(60);
删除列：
			alter table student drop addr;
重命名表：
			alter table student rename students;


删除数据库和表：
			drop table student;
			drop database test;



MySQL常用命令：
1）连接MySQL：mysql -h 主机地址 -u 用户名 -p 用户密码
连接到本机MySQL：
			mysql -u root -p;
连接到远程主机上的MySQL：
			mysql -h 10.110.18.120 -u -root -p 123;

2）修改密码：mysqladmin -u 用户名 -p 旧密码 -password 新密码
给root加个密码abc12：
			mysqladmin -u root -password abc123;
将root的密码改为root123：
			mysqladmin -u root -p abc123 -password root123;

3）增加新用户：grant 权限1,权限2,...权限n  on  数据库名称.表名称  to  用户名@用户地址  identified  by  '密码'
给来自10.163.215.87的用户qiye分配可对数据库company的employee表进行select、insert、update、delete、create、drop等操作的权限，并设定口令为123：
			grant   select,insert,update,delete,create,drop   on  company.employee  to  qiye@10.163.215.87  identified  by  '123';

4）显示数据库：
			show databases;

5）备份数据库：数据库的备份、表的备份。
a、导出整个数据库
			mysqldump  -u  user_name  -p123456  database_name  >  outfile_name.sql
b、导出一个表
			mysqldump  -u  user_name  -p123456  database_name  table_name  >  outfile_name.sql


【Python操作MySQL】			
	pip install MySQL-python
import MySQLdb
# 打开数据库，获取连接对象
con = MySQLdb.connect(host='localhost', user='root', passwd='', db='test', port=3306, charset='utf-8')
# 获取游标对象
cur = con.cursor()
	execute()
	executemany()
	close()
	fetchone()
	fetchmany()
	fetchall()
	scroll()
# 建表
cur.execute('CREATE TABLE person (id int not null auto_increment primary key, name varchar(20), age int)')
# 插入数据
cur.execute('INSERT INTO person (name,age) VALUES (%s,%s)', ('qiye', 20))
# 执行多条语句，比循环执行效率高很多
cur.executemany('INSERT INTO person (name,age) VALUES (%s,%s)', [('marry', 20), ('jack', 20)])
# 插入数据都不会立即生效，需要进行提交
con.commit()
# 如果出现错误，可以使用回滚操作
con.rollback()

# 查询数据
cur.execute('SELECT * FROM person')

# 提取查询数据
cur.execute('SELECT * FROM person')
res = cur.fetchall()
for line in res:
	print(line)

cur.execute('SELECT * FROM person')
res = cur.fetchone()
print(res)

# 修改和删除数据
cur.execute('UPDATE person SET name=%s WHERE id=%s', ('rose', 1))
cur.execute('DELETE FROM person WHERE id=%s', (0,))
con.commit()
con.close()
