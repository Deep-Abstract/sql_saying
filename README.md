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

```

```

- `insert`
    ```

    ```








