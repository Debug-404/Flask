import sqlite3


class StudentList:
    def __init__(self):
        self.name = "studentList.db"

    def __enter__(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_avl, exc_tb):
        self.cursor.close()
        self.conn.close()

    def register(self, user: str, paw: str) -> bool:
        """
        注册信息(学号,密码) 成功返回Ture
        """
        sql = f"insert into web_db(No,pad) values('{user}','{paw}');"
        try:
            self.cursor.execute(sql)
        except sqlite3.IntegrityError:
            return False
        self.conn.commit()
        return True

    def login(self, user: str) -> bool:
        """
        判断某个学号是否存在(web表)
        """
        sql = f"select count(*) from web_db where No='{user}' limit 1"
        if self.cursor.execute(sql).fetchall()[0][0] == 1:
            return True
        else:
            return False

    def selectPassword(self, user: str, paw: str) -> bool:
        """
        查询输入的密码与数据库的密码是否一致。相同返回Ture
        """
        sql = f"SELECT pad FROM web_db WHERE No='{user}'"
        if self.cursor.execute(sql).fetchall()[0][0] == paw:
            return True
        else:
            return False

    def getAllStudentInfo(self) -> list:
        """
        获取全部学生信息的基础信息
        """
        sql = "SELECT id,name,sex,age,address FROM student_info ORDER BY id asc"
        date = self.cursor.execute(sql).fetchall()
        return date

    def getOneStudentInfo(self, user: str) -> list:
        """
        获取某个学生的基础信息
        """
        sql = f"SELECT * FROM student_info WHERE id='{user}'"
        return self.cursor.execute(sql).fetchall()

    def changePassword(self, user: str, pad: str) -> bool:
        """
        修改登录密码
        """
        sql = f"update web_db set pad = '{pad}' where No= '{user}'"
        try:
            self.cursor.execute(sql)
        except sqlite3.DataError:  # 因处理数据问题引起的错误引发异常
            return False
        self.conn.commit()
        return True

    def intoStudentInfo(
            self, user: str, name: str, sex: str, age: str, address: str
    ) -> bool:
        """
        写入学生信息
        """
        sql = f"INSERT INTO student_info (id,name,sex,age,address) /" \
              f"fVALUES('{user}','{name}','{sex}','{age}','{address}')"
        try:
            self.cursor.execute(sql)
        except sqlite3.IntegrityError:  # 当数据库的关系完整性受到影响时引发异常
            return False
        self.conn.commit()
        return True

    def selectIn(self, user: str) -> bool:
        """
        判断某个学号是否存在于数据库中(student_info表) 存在return Ture
        """
        sql = f"select count(*) from student_info where id='{user}' limit 1"
        if self.cursor.execute(sql).fetchall()[0][0] == 1:
            return True
        else:
            return False

    def delStudent(self, user: str) -> bool:
        """
        删除单个学生信息
        """
        if self.selectIn(user):
            sql = f"DELETE FROM student_info WHERE id='{user}'"
            try:
                self.cursor.execute(sql)
            except sqlite3.OperationalError:  # 无法处理事务
                return False
            self.conn.commit()
            return True
        else:
            return False

    def upDataStudentInfo(
            self, user: str, name: str, sex: str, age: str, address: str
    ) -> None:
        """
        更新单个学生信息
        """
        sql = f"UPDATE student_info set name='{name}',sex='{sex}',age='{age}',address='{address}' WHERE id='{user}'"
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        else:
            self.conn.commit()

    def getAllCourse(self) -> list:
        """
        获取每个课程的人数
        """
        sql = "SELECT cur.curriculum_name,cur.curriculum_id,count(gr.id)  FROM grade AS gr JOIN curriculum AS cur ON " \
              "gr.curriculum_id = cur.curriculum_id GROUP BY cur.curriculum_id "
        return self.cursor.execute(sql).fetchall()

    def getAllStudentScore(self) -> list:
        """
        获取单个课程全部学生的成绩 未完成
        """
        sql = ""
        return self.cursor.execute(sql).fetchall()

    def getOneStudentScore(self, user: str) -> dict:
        """
        获取单个学生的课程成绩和基础信息
        """
        sql = f"SELECT cur.curriculum_name,gr.curriculum_id,gr.gradeNumber,cur.credit  FROM grade AS gr LEFT " \
              f"JOIN curriculum AS cur ON gr.curriculum_id = cur.curriculum_id WHERE id='{user}' "
        info = f"SELECT id,name FROM student_info WHERE id='{user}'"
        return {"info": self.cursor.execute(info).fetchall(), "grade": self.cursor.execute(sql).fetchall()}
