.. image:: https://img.shields.io/badge/license-Apache-blue.svg
    :target: https://github.com/DeepAbstract/PyMVC/blob/master/LICENSE

PyMVC
======



.. contents:: Table of Contents
   :local:

ReadMe File: dao.
中文文档：

Requirements
-------------

* PyMySQL
	- pip install pymysql


Config
------

使用本dao你需要预先做几件事。我不崇尚让大家先把web后端开发中的entity包先一个个写好，而我这里使用的方法是这样的：

在 mvc 文件目录下有一个config文件夹，进去需要填写两个文件

- classDefine.py 

- daoDetails.py

这两个文件的作用，在java web里应该需要用至少1000倍于此的代码才能完成

- classDefine.py中配置两个变量：

	* classInfo : 一个list，其中每个元素是一个dict，

	- dict有两个键：class 和 attrs，
		
	 class 表示 一个entity类的类名，是一个字符串
		
 	 attrs 表示 一个entity类的属性，是一个字符串列表
 
 * class_type_map:一个dict,用来将entity的属性按照一定的关系转成MySQL数据类型。

	- 键名是表示MySQL数据类型；键值是一个字符串list，如果一个entity的属性字符串包含这个list中的一个值，那么这个属性就会对应到键名指定的MySQL类型。

- demo:

.. code:: python


	class_info=[
    	{
        "class":"user",
        "attrs":["id","username","password","access","info","school","email",'img']
    	},
    	{
        "class":"course",
        "attrs":["id","name","time","finalexamdate"]
    	}
		]


	class_type_map={
	"int":["id"],
	"datetime":["date"],
	"double":["money"],
	"float":["gpa"],
	"text":["text"],
	"integer":["time","total"],
	"varchar(10)":["school"],
	"varchar(40)":["name","number"],
	"varchar(70)":["src","img"],
	"tinyint":["access","level"]
	}


- daoDetails.py
- 可以看成是配置MySQL连接的一个json。
- demo:

.. code:: python
		dbargs={
    		"host":"x.x.x.x",
    		"db":"xxx",
    		"user":"xxx",
    		"passwd":"xxx",
    		"port":3306
			}




Document
--------

然后你就可以开心的from mvc import dao了。

dao里有两个东西要用

* following

		- baseDao

		- deploy

		- deploy类是用来建立和删除数据库对应表的。

			- 构造一个deploy类，你需要一个entity对象。如果你写好了config里的文件，你就可以这样获得一个名为user（如果classDefine中有的话）的entity对象：
			
.. code:: python
			from mvc.entity import entities
			User=entities.user
				#这个User是一个属性值全空的对象，你可以把它当做类使用。
			newuser=User()
				#__call__方法是深拷贝。
			from mvc.dao import deploy
			dep=deploy(newuser)
			dep.createTable(); #创建数据表
			dep.dropTable(); #删除数据表

		- baseDao类是用来创建一个dao对象的，它不需要传入entity对象来构造。

.. code:: python

			userdao=baseDao('user')
				#这就相当于创建了java web后台里的一个UserDao类的实例。
			userdao.add(user=newuser)
				#user表增加一条记录，其字段值是newuser的各属性值。
			#类似的还有
			userdao.add(username="saber",password="123",email="fafafa@bili.com")
				#user表增加一条记录，其字段值与传入参数分别对应

			"""
			add 方法和delete，select方法一致，都可以传入对象做参数，或者按照字典形式传参，
				其中select和delete方法中，传入的各个参数之间是 逻辑交 的关系，也就是MySQL里面 where ... and ... and ...的形式。
			change方法稍微有一点不同，它接受 属性/字段名=value的传参，这些  属性/字段名 表示需要改变的  属性/字段名 的值，
					在  属性/字段名前面加上"_"，表示需要将这些选中的记录的对应  属性/字段名 修改成对应值。
			"""

All above is what should be known about PyMVC!

Enjoy yourself with easily operating MySQL databases!



