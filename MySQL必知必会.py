###了解SQL
# 数据库基础
数据库：保存有组织的数据的容器（通常是一个文件或一组文件）。
相当于一个文件柜。

数据库软件应称为DBMS（数据库管理系统），它替你访问数据库。

表：某种特定类型数据的结构化清单。

模式可以用来描述数据库中特定的表以及整个数据库（和其中表的关系）。

列（column）：表中的一个字段。所有表都是由一个或多个列组成的。
行（row）：表中的一个记录。

主键：一列（或一组列），其值能够唯一区分表中每个行。
主键用来表示一个特定的行。没有主键，更新或删除表中特定行很困难，因为没有安全的方法保证只涉及相关的行。

任何列都可以作为主键，只要满足条件：
a、任意两行都不具有相同的主键值。
b、每个行都必须具有一个主键值（主键列不允许NULL值）

也可以使用多个列作为主键。


SQL：结构化查询语言。专门用来与数据库通信的语言。





###MySQL简介
#简介
MySQL是一种DBMS，即它是一种数据库软件。

DBMS可分为两类：一类为基于共享文件系统的DBMS，另一类为基于客户机-服务器的DBMS。


#MySQL工具
mysql命令行实用程序：
    mysql -u ben -p -h myserver -P 9999

MySQL Administrator：
    图形交互客户机
MySQL Query Browser
    图形交互客户机





###使用MySQL
#连接
MySQL与所有客户机-服务器DBMS一样，要求在能执行命令之前登录到DBMS。登录名可以与网络登录名不相同。MySQL在内部保存自己的用户列表，并且把每个用户与各种权限关联起来。

# 选择数据库
use crashcourse;

#显示数据库、表、表中的列
show databases;
show tables;
show columns from customers;   （desc customers;）

# 显示广泛的服务器状态信息
show status; 
# 显示创建特定数据库或表的MySQL语句
show create database;
show create table;
# 显示授予用户的安全权限
show grants;
# 显示服务器错误或警告消息
show errors;
show warnings;





###检索数据
用途：从一个或多个表中检索信息。
select prod_name from products;     # 单个列
select prod_id, prod_name, prod_price from products;    # 多个列
select * from products;     # 所有列

# 检索不同的行
select distinct vend_id from products;  # 去重

# 限制结果
# 为了返回第一行或前几行，可使用LIMIT子句。
select prod_name from products limit 5;
select prod_name from products limit 5, 5;  # 返回从行5开始的5行
注意：limit 1,1将检索出第二行而不是第一行。
    ↓
select prod_name from products limit 4 offset 3;    # 从行3开始取4行


# 使用完全限定的表明（同时使用表明和列字）
select products.prod_name from crashcourse.products;





###排序检索数据
检索出的数据并不是以纯粹的随机顺序显示的。如果不排序，数据一般将以它在底层表中出现的顺序显示。这可以是数据最初添加到表中的书序。但是，如果数据后来进行过更新或删除，则此顺序将会受到MySQL重用回收存储空间的影响。因此，如果不明确控制的话，不能（也不应该）依赖该排序顺序。

select prod_name from products order by prod_name;
select prod_id, prod_price, prod_name from products order by prod_price, prod_name;

# 指定排序方法。以降序排序
select prod_id, prod_price, prod_name from products order by prod_price desc;
# 以降序排序产品，然后再对产品名排序
select prod_id, prod_price, prod_name from products order by prod_price desc, prod_name;

# 找出一个列中最高或最低的值。
# 如：找出最贵物品的值。
select prod_price from products order by prod_price desc limit 1;





###过滤数据
select prod_name, prod_price from products where prod_price = 2.50;

注意：在同时使用order by和where子句时，应该让order by位于where之后，否则将会产生错误。

# 不匹配检查
# 如：列出不是由供应商1003制造的所有产品
select vend_id, prod_name from products where vend_id <> 1003;
select vend_id, prod_name from products where vend_id != 1003;

# 范围值检查
# 如：检索价格在5美元和10美元之间的所有产品
select prod_name, prod_price from products where prod_price between 5 and 10;

# 空值检查
在创建表时，表设计人员可以指定其中的列是否可以不包含值。在一个列不包含值时，称其为包含空值NULL。
select prod_name from products where prod_price is null;





###数据过滤
MySQL允许给出多个WHERE子句。这些子句可以两种方式使用：以AND子句的方式或OR子句的方式使用。

select prod_id, prod_price, prod_name from products where vend_id = 1003 and prod_price <= 10;

select prod_name, prod_price from products where vend_id = 1002 or vend_id = 1003;


# and or的计算次序
SQL在处理OR操作符前，优先处理AND操作符。
select prod_name, prod_price from products where vend_id = 1002 or vend_id = 1003 and prod_price >= 10;
# SQL看到上述语句，理解为：由供应商1003制造的任何价格为10美元（含）以上的产品，或者由供应商1003制造的任何产品，而不管其价格如何。
            ↓
# 圆括号具有较AND或OR操作符高的计算次序。
select prod_name, prod_price from products where (vend_id = 1002 or vend_id = 1003) and prod_price >= 10;


# IN操作符
IN操作符用来指定条件范围，范围中的每个条件都可以进行匹配。IN取合法值的由逗号分隔的清单，全都括在圆括号中。
IN操作符完成与OR相同的功能。
select prod_name, prod_price from products where vend_id in (1002, 1003) order by prod_name


# NOT操作符
NOT WHERE：否定它之后所跟的任何条件。
在与IN操作符联合使用时，NOT使找出与条件列表不匹配的行非常简单。
# 如：列出除1002和1003之外的所有供应商制造的产品
select prod_name, prod_price from products where vend_id NOT IN (1002, 1003) order by prod_name;





###用通配符进行过滤
通配符：用来匹配值的一部分的特殊字符。
搜索模式：由字面值、通配符或两者组合构成的搜索条件。
为在搜索子句中使用通配符，必须使用LIKE操作符。LIKE指示MySQL，后跟的搜索模式利用通配符匹配而不是直接相等匹配进行比较。

操作符何时不是操作符？在它作为谓词的时候。

# 百分号（%）通配符
%表示任何字符出现任意次数。
# 如：找出所有以词jet起头的产品
select prod_id, prod_name from products where prod_name LIKE 'jet%';

# 匹配任何位置包含文本anvil的值，而不论它之前或之后出现什么字符
select prod_id, prod_name from products where prod_name LIKE '%anvil%';

# 找出以s起头以e结尾的所有产品
select prod_name from products where prod_name LIKE 's%e';

注意：除了一个或多个字符外，%还能匹配0个字符。%代表搜索模式中给定位置的0个、1个或多个字符。


# 下划线（_）通配符
用途与%一样，但下划线只匹配单个字符而不是多个字符。
_总是匹配一个字符，不能多也不能少。

select prod_id, prod_name from products where prod_name LIKE '_ ton anvil';

通配符搜索的处理一般要比前面技巧的其他搜索所花时间更长。
    不要过度使用通配符
    尽量不要把它们放在搜索模式的开始处
    仔细注意通配符的位置





###用正则表达式进行搜索
# 如：检索列prod_name包含文本1000的所有行
select prod_name from products where prod_name REGEXP '1000' order by prod_name;

select prod_name from products where prod_name REGEXP '.000' order by prod_name;
# .是正则表达式中一个特殊的字符

LIKE和REGEXP之间一个重要的差别：
select prod_name from products where prod_name LIKE '1000' order by prod_name;
select prod_name from products where prod_name REGEXP '1000' order by prod_name;
如果执行上述两条语句，会发现第一条语句不返回数据，而第二条语句返回一行，为什么？
LIKE匹配整个列，如果被匹配的文本在列值中出现，LIKE将不会找到它，响应的行也不被返回（除非使用通配符）。而REGEXP在列值内进行匹配，如果被匹配的文本在列值中出现，REGEXP将会找到它，相应的行将被返回。这是一个非常重要的差别。
（LIKE匹配整个串而REGEXP匹配子串）

# 搜索两个串之一，使用|
select prod_name from products where prod_name REGEXP '1000|2000' order by prod_name;


# 匹配几个字符之一
select prod_name from products where prod_name REGEXP '[123] Ton' order by prod_name;

# 匹配范围
select prod_name from products where prod_name REGEXP '[1-5] Ton' order by prod_name;

# 匹配特殊字符
select vend_name from vendors where vend_name REGEXP '.' order by vend_name;    # .匹配任意字符，因此每个行都被检索出来
select vend_name from vendors where vend_name REGEXP '\\.' order by vend_name;


# 匹配字符类


# 匹配多个实例
select prod_name from products where prod_name REGEXP '\\([0-9] sticks?\\)'
# 如：匹配连在一起的4个数字
select prod_name from products where prod_name REGEXP '[[:digit:]]{4}' order by prod_name;


# 定位符
# 如：找出以一个数（包括以小数点开始的数）开始的所有产品
select prod_name from products where prod_name REGEXP '^[0-9\\.]' order by prod_name;





###创建计算字段
存储在表中的数据都不是应用程序所需要的，我们需要直接从数据库中检索出转换、计算或格式化过的数据；而不是检索出数据，然后再在客户机应用程序或报告程序中重新格式化。
这就是计算字段发挥作用的所在了。
计算字段是运行在SELECT语句内创建的。

注意：只有数据库知道SELECT语句中哪些列是实际的表列，哪些列是计算字段。

# 拼接字段
拼接：将值联结到一起构成单个值。使用Concat()函数来拼接两个列。
vendors表包含供应商名和位置信息。假如要生成一个供应商报表，需要再供应商的名字中按照name(location)这样的格式列出供应商的位置。
此报表需要单个值，而表中数据存储在两个列vend_name和vend_country中。此外，需要用括号将vend_country括起来，这些东西都没有明确存储在数据库表中。我们来看看怎样编写返回供应商名和位置的SELECT语句。
select Concat(vend_name, '(', vend_country, ')') from vendors order by vend_name;

# 删除数据右侧多余的空格来整理数据。可以使用RTrim()函数来完成
select Concat(RTrim(vend_name), ' (', RTrim(vend_country), ')') from vendors order by vend_name;

# 别名：是一个字段或值得替换名。用AS关键字赋予。
# AS vend_title指示SQL创建一个包含指定计算的名为vend_title的计算字段
select Concat(RTrim(vend_name), ' (', RTrim(vend_country), ')') AS vend_title from vendors order by vend_name;


# 执行算术计算
计算字段的另一常见用途是对检索出的数据进行算术计算。
# 如：汇总物品的价格（单价乘以订购数量）
select prod_id,
            quantity,
            item_price,
            quantity*item_price AS expanded_price
from orderitems
where order_num = 20005;


11.1