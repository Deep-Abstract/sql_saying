# sql saying : A Convenient SQL Wrapper

`sql saying` is a lightweight MySQL wrapper using [pymysql](https://github.com/PyMySQL/PyMySQL).  
It's for the people who're trying to develop projects with database operations in a fast and graceful way.

## Connect Database So Easy

Just write a file [daoDetails.py](./daoDetails.py).
```python
dbargs = {'user': 'your_username',
          'password': 'your_passwd',
          'db': 'your_db_name',
          'host': 'localhost'}
```


## Define Tables So Easy

Just write a file [classDefine.py](./classDefine.py).

```python
class_info = [
    {
        "class": "user",
        "attrs": ["id", "username", "password", "access", "info", "school", "email", 'img']
    },
    {
        "class": "course",
        "attrs": ["id", "name", "time", "finalexamdate"]
    }
]

class_type_map = {
    "int": ["id"],
    "datetime": ["date"],
    "double": ["money"],
    "float": ["gpa"],
    "text": ["text"],
    "integer": ["time", "total"],
    "varchar(10)": ["school"],
    "varchar(40)": ["name", "number"],
    "varchar(70)": ["src", "img"],
    "tinyint": ["access", "level"]
}
```

- **class_info** 
    defines your tables in the database,while
- **class_type_map** 
    defines the data type of a field with its name   
    (to search substring of a field is a sign for specific type or not).

And then when you `import entity`, `entity.Entities` can be used to initial your tables:

```python
import dao
from entity import Entities 

for template_entity in Entities.items():
    dao.deploy(template_entity).create_table()
    # dao.deploy(template_entity['class']).drop_table() # if you want to delete the table.
```

## Graceful Pythonic SQL Operations

Assume you've initialized a table `user`.

**`user`**

| id | username | password  | email       |
|--- | -------  | -------   | -------     |
| 0  | archer   | ubw       | xxx@yyy.com |
| 1  | misaka   | bilibili  | zzz@aaa.com |
|... | ...      | ...       |     ...     | 


- `select`

    ```python
    import dao
    userDao = baseDao('user')
    userDao.select(id=1, username='unknown')
    # `select * where id=1 and username='unknown'`
    #=> ()
    userDao.select(password = 'ubw')
    # `select * where password='ubw'`
    # => {'id':1, 
    #    'username':'misaka',
    #    'password':'bilibili',
    #    'email':'zzz@aaa.com'}
    configs = dict()
    configs['username'] = 'misaka'
    configs['id'] = 1
    userDao.select(**configs)
    #=> {'id':1, 
    #    'username':'misaka',
    #    'password':'bilibili',
    #    'email':'zzz@aaa.com'}

    userDao.selectAll()
    # which equals to 
    # `select * from user;`
    ```

- `insert`

    ```python
    import dao
    userDao = baseDao('user')

    # insert single tuple.
    userDao.add(username='saber', password='ex')
    # `insert into user (username, password) values ('saber', 'ex');`
    # the field `email` is not assigned and it's a default value `null`.

    # insert multiple tuples.
    userDao.add_multiple(['username', 'password'], # fields

                         [['saber','ex'],          # values
                          ['ruiko','lv0'],
                          ...
                         ])
    ```

- `delete`

    Very similar to `baseDao.add`.

    ```python
    import dao
    userDao = baseDao('user')
    userDao.delete(username = 'saber', password = 'ex')
    # `delete from user where username='saber' and password='ex';`

    ```

- `update`

    ```python
    """
        change the information of selected records.
        
        match the records by passing key-value pairs.
        and change the value of specific field by passing _key-value pairs, \
        like this way:
        
        userDao.change(username='caster',_username="rider")
        #you change usernames of all the records whose username are 'caster' to 'rider'.
    """
    userDao.change(username='caster',_username="rider", _password='1')
    # `update user set username='rider', password='1' where username='caster';`
    ```

- `check`

    To check if any record matching some conditions exists in your datas.

    ```python
    userDao.check(username='nightnight', email='twshere@outlook.com')
    #=> 0
    userDao.check(username='archer')
    #=> 1
    ```

## Powerful Entity Template

```python

from entity import Entity
User = Entity(['username', 'password', 'email', 'id'], name = 'user')
User.to_map()
# =>{'username':None,
#    'password':None,
#    'email':None,
#    'id':None}

a_user = User() # `User` looks like a entity class.
a_user.username = '123'
a_user['email'] = 'xxx@b.com'
a_user.to_map()
# =>{'username':'123',
#    'password':None,
#    'email':'xxx@b.com',
#    'id':None}

# user an template to create a database.
from dao import deploy
deploy(User).create_table()
# now the table `user` has been created!

```








