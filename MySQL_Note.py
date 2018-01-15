增删改查，简称CRUD。

【数据库简介】
数据库系统解决的问题：持久化存储，优化读写，保证数据的有效性
主要分为两类：文档型、服务型

#E-R模型
当前物理的数据库都是按照E-R模型进行设计的
E表示entry，实体
R表示relationship，关系
一个实体转换为数据库中的一个表
关系描述两个实体之间的对应规则，包括
            一对一
            一对多
            多对多
关系转换为数据库表中的一个列 *在关系型数据库中一行就是一个对象

#三范式
经过研究和对使用中问题的总结，对于设计数据库提出了一些规范，这些规范被称为范式
第一范式（1NF)：列不可拆分
第二范式（2NF)：唯一标识
第三范式（3NF)：引用主键
说明：后一个范式，都是在前一个范式的基础上建立的



【数据库完整性】
一个数据库就是一个完整的业务单元，可以包含多张表，数据被存储在表中
在表中为了更加准确的存储数据，保证数据的正确有效，可以在创建表的时候，为表添加一些强制性的验证，包括数据字段的类型、约束

#字段类型
在mysql中包含的数据类型很多，这里主要列出来常用的几种
数字：int,decimal
字符串：char,varchar,text
日期：datetime
布尔：bit

#约束
主键primary key：不能重复，唯一标识。根据主键查询速度非常快
非空not null
惟一unique
默认default
外键foreign key



【图形窗口操作】
Navicat
    预留栏位，可以防止以后需要给数据库增加字段。

#逻辑删除
对于重要数据，并不希望物理删除，一旦删除，数据无法找回
一般对于重要数据，会设置一个isDelete的列，类型为bit，表示逻辑删除
大于大量增长的非重要数据，可以进行物理删除
数据的重要性，要根据实际开发决定



【命令脚本操作】
mysql -uroot -p
mysql --help

查看版本：select version();
显示当前时间：select now();

远程连接：mysql -hip地址 -uroot -p

当前所有的数据库：show databases;
当前所有的表：show tables;

创建数据库：create database 数据库名 charset=utf8;

删除数据库：drop database 数据库名;

切换数据库：use 数据库名;

查看当前选择的数据库：select database();

创建表：
create table 表名(列及类型);
如：
create table students(
id int auto_increment primary key not null,
name varchar(10) not null,
birthday datetime，
gender bit default 1,
isDelete bit default 0
);

查看表结构：desc students;

修改表：
alter table 表名 add|change|drop 列名 类型;
如：
alter table students add birthday datetime;

删除表：drop table 表名;

更改表名：rename table 原表名 to 新表名;

查看表的创建语句：
show create table 表名;

查询：
select * from 表名

增加：
全列插入：insert into 表名 values(...)             # id列用0占位
缺省插入：insert into 表名(列1,...) values(值1,...)
同时插入多条数据：insert into 表名 values(...),(...)...;
或insert into 表名(列1,...) values(值1,...),(值1,...)...;

修改：
update 表名 set 列1=值1,... where 条件

删除：
delete from 表名 where 条件

逻辑删除，本质就是修改操作update：
alter table students add isdelete bit default 0;
如果需要删除则：
update students isdelete=1 where ...;

数据备份：
a、进入超级管理员
sudo -s
b、进入mysql库目录
cd /var/lib/mysql
c、运行mysqldump命令
mysqldump –uroot –p 数据库名 > ~/Desktop/备份文件.sql;

数据恢复：
a、连接mysql，创建数据库
b、退出连接，执行如下命令
mysql -uroot –p 数据库名 < ~/Desktop/备份文件.sql



【查询】
概念：原始集、结果集。

#条件
消除重复行：
select distinct gender from students;
select distinct id,gender from students;

（比较运算符）
select * from students where id>3;
select * from subjects where id<=4;
select * from students where name!='黄蓉';
查询没被删除的学生：
select * from students where isdelete=0;

（逻辑运算符）
select * from students where id>3 and gender=0;
select * from students where id<4 or isdelete=0;

（模糊查询）
%表示任意多个任意字符
_表示一个任意字符
查询姓黄的学生：
select * from students where name like '黄%';
查询姓黄并且名字是一个字的学生：
select * from students where name like '黄_';
查询姓黄或叫靖的学生：
select * from students where name like '黄%' or name like '%靖%';

（范围查询）
in表示在一个非连续的范围内
查询编号是1或3或8的学生：
select * from students where id in(1,3,8);
between ... and ...表示在一个连续的范围内
查询学生是3至8的学生：
select * from students where id between 3 and 8;
查询学生是3至8的男生：
select * from students where id between 3 and 8 and gender=1;

（空判断）
注意：null与''是不同的
判空is null
查询没有填写地址的学生：
select * from students where hometown is null;
判非空is not null
查询填写了地址的学生：
select * from students where hometown is not null;
查询填写了地址的女生：
select * from students where hometown is not null and gender=0;

（优先级）
小括号，not，比较运算符，逻辑运算符
and比or先运算，如果同时出现并希望先算or，需要结合()使用



#聚合
将现有的多行数据进行统计，统计的结果是你看不到任何一条具体的数据了。
为了快速得到统计数据，提供了5个聚合函数

count(*)表示计算总行数，括号中写星与列名，结果是相同的
查询学生总数：
select count(*) from students;

max(列)表示求此列的最大值
查询女生的编号最大值：
select max(id) from students where gender=0;

min(列)表示求此列的最小值
查询未删除的学生最小编号：
select min(id) from students where isdelete=0;

sum(列)表示求此列的和
查询男生的编号之后：
select sum(id) from students where gender=1;

avg(列)表示求此列的平均值
查询未删除女生的编号平均值：
select avg(id) from students where isdelete=0 and gender=0;


#分组
目的：为了更好的统计数据。非聚合的字段，是不会出现在结果集当中的。
按照字段分组，表示此字段相同的数据会被放到一个组中
分组后，只能查询出相同的数据列，对于有差异的数据列无法出现在结果集中
可以对分组后的数据进行统计，做聚合运算

语法：
select 列1,列2,聚合... from 表名 group by 列1,列2,列3...
（将列相同的数据合成到一组）

查询男女生总数：
select gender as 性别,count(*)
from students
group by gender;

查询各城市人数：
select hometown as 家乡,count(*)
from students
group by hometown;


分组后的数据筛选
语法：
select 列1,列2,聚合... from 表名
group by 列1,列2,列3...
having 列1,...聚合...

having后面的条件运算符与where的相同
查询男生总人数：
方案一
select count(*)
from students
where gender=1;
-----------------------------------
方案二：
select gender as 性别,count(*)
from students
group by gender
having gender=1;

对比where与having：
where是对from后面指定的表进行数据筛选，属于对原始数据的筛选
having是对group by的结果进行筛选


#排序
语法：
select * from 表名
order by 列1 asc|desc,列2 asc|desc,...

将行数据按照列1进行排序，如果某些行列1的值相同时，则按照列2排序，以此类推
默认按照列值从小到大排列
asc从小到大排列，即升序
desc从大到小排序，即降序
查询未删除男生学生信息，按学号降序：
select * from students
where gender=1 and isdelete=0
order by id desc;

查询未删除科目信息，按名称升序：
select * from subject
where isdelete=0
order by stitle;


#分页
当数据量过大时，在一页中查看数据是一件非常麻烦的事情
语法：
select * from 表名
limit start,count

从start开始，获取count条数据
start索引从0开始

已知：每页显示m条数据，当前显示第n页
求总页数：此段逻辑后面会在python中实现
查询总条数p1
使用p1除以m得到p2
如果整除则p2为总数页
如果不整除则p2+1为总页数
求第n页的数据
select * from students
where isdelete=0
limit (n-1)*m,m


完整的查询顺序：
select distinct *
from 表名
where ....
group by ... having ...
order by ...
limit star,count
执行顺序为：
from 表名
where ....
group by ...
select distinct *
having ...
order by ...
limit star,count


【高级】
实体与实体之间有3种对应关系，这些关系也需要存储下来
在开发中需要对存储的数据进行一些处理，用到内置的一些函数
视图用于完成查询语句的封装
事务可以保证复杂的增删改操作有效


【关系】
    行对行。。。
一对一，关系字段存在于哪个表都行。
一对多，关系字段存在于【多】的表中。
多对多，则新建一张表存储关系。

成绩表scores和学生表students、科目subjects的关系：都是n对1

外键是外键，关系是关系。
先有关系，再有外键。
（为了保证数据有效性，在关系字段上，添加外键约束）

a、创建表、并添加外键：
create table scores(
id int auto_increment primary key not null,
score decimal(5,2),
stuid int,
subid int,
foreign key(stuid) references students(id),     # 外键
foreign key(subid) references subjects(id)      # 外键
);
b、插入测试数据
insert into scores values(0,100,1,1);
c、外键约束的级联操作
级联操作的类型包括：
            restrict（限制）：默认值，抛异常
            cascade（级联）：如果主表的记录删掉，则从表中相关联的记录都将被删除
            set null：将外键设置为空
            no action：什么都不做
语法：
alter table scores add constraint stu_sco foreign key(stuid) references students(id) on delete cascade;

一般做法：
如果一个表的主键会被别的表引用，那最好给这个表做逻辑删除，不要做物理删除。



【连接】
连接查询：想要的信息来源于多张表
select * from scores;           # 缺点：不够直观
# 实际想看到的效果：郭靖 python 100
# join后面跟的是表名，on后面跟的是关系
select students.name,subjects.title,scores.score 
from scores
inner join students on scores.stuid=students.id
inner join students on scores.subid=subjects.id;
            ↓
另一种写法，也是一样的效果：
select students.name, subjects.title, scores.score
from students
inner join scores on scores.stuid=students.id
inner join subjects on scores.subid=subjects.id;


连接查询，一共有三种：
            表A inner join 表B：表A与表B匹配的行会出现在结果中
            表A left join 表B：表A与表B匹配的行会出现在结果中，外加表A中独有的数据，未对应的数据使用null填充
            表A right join 表B：表A与表B匹配的行会出现在结果中，外加表B中独有的数据，未对应的数据使用null填充
在查询或条件中推荐使用“表名.列名”的语法
如果多个表中列名不重复可以省略“表名.”部分
如果表的名称太长，可以在表名后面使用' as 简写名'或' 简写名'，为表起个临时的简写名称

查询学生的姓名、平均分：
select students.sname,avg(scores.score)
from scores
inner join students on scores.stuid=students.id
group by students.sname;
查询男生的姓名、总分：
select students.sname,sum(scores.score)
from scores
inner join students on scores.stuid=students.id
where students.gender=1
group by students.sname;
查询科目的名称、平均分：
select subjects.stitle,avg(scores.score)
from scores
inner join subjects on scores.subid=subjects.id
group by subjects.stitle;
查询未删除科目的名称、最高分、平均分：
select subjects.stitle,avg(scores.score),max(scores.score)
from scores
inner join subjects on scores.subid=subjects.id
where subjects.isdelete=0
group by subjects.stitle;



【自关联】
省市区因为所有数据加起来不算很多，所以将其设计为一张表。
注意点：需要统一结构。
create table areas(
    id int primary key auto_increment not null,
    title varchar(20),
    pid int,
    foreign key(pid) references areas(id)       # 自引用自关联
);
source areas.sql        # 导入数据

查询一共有多少个省：
select count(*) from areas where pid is null;

查询省的名称为“山西省”的所有城市：
select city.* from areas as city
inner join areas as province on city.pid=province.aid
where province.atitle='山西省';

查询市的名称为“广州市”的所有区县：
select dis.* from areas as dis
inner join areas as city on city.aid=dis.pid
where city.atitle='广州市';






















