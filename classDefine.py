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
    "varchar(50)": ["username", "password"],
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
