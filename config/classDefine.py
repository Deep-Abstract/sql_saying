
class_info=[
    {
        "class":"user",
        "attrs":["id","username","password","access","info"]
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
"varchar(40)":["name","number"],
"tinyint":["access","level"]
}