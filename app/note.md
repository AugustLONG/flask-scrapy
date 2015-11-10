
* 要记录自己之后需要在博客上所写的东西

* os.path 的问题

* 添加 shell 的记录

* 关于 blueprint 的加入

* 如何解决中文字符的输入，采用的是 声明编码+用u来转换,而对于 message，比较复杂，采用的是 {{message.decode('utf-8')}}

* 关于一系列的 bug,最后还是页面写的有问题，没有设计好。比如 没有添加 {block page_content %} ，再比如没有
  在 视图里引入还没有 定义的 main.user，这个 Bug 自己应该发现的更早的

* staticmethond 这里说的是不使用实例来进行

* flask.ext.login : login_manager 的文档，关于 anonmousUser

* 如何处理用户角色，在 Role用户里增加一个 role类，然后用  insert_roles 来添加
同时用 位处理 的方式来进行。然后 增加函数 self.can 和 self.is_administor

* 还有 匿名用户，anonymousUser

* @staticmethod，在不用类的实例的情况下进行初始化；super(User,self).__int__(**kewargs)
则是读取参数

* 关于上下文处理器，app_context_processor ，增加全局变量

* 关于单元测试，还是数据库的生成有问题

* 关于数据库更新，嗯哼

* 看关于 sqlalchemy 的资料，defautl=的意思是默认？？

* 对于时间的处理还是问题，比如 moment().format('L') moment.formNow() 都是非常好的

* 提示说 main.views 缺少 Permission.不知道 上下文可以使用是针对 模板来说的，在 view里还是
要有定义才行 。Get

* 在 {% block head %} 部分通过 <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename="style.css") }}">
来添加自己定义的 css 元素。 恩，还是 前端的基础知识要有

* user.posts 可以直接使用

* _post.html 多个页面使用一个模板，非常好的方法

* 随机生成数据这点，有可能的话还是要做 Interfitty 容错处理。关于 randint() 等等，还是要看其他

* 分页这里，自己实现的非常不好；-） 晚上要重看，宏是做什么的……

* Flask-pagedown 的文档,如何使得显示结果也是 ,有些麻烦

---

* 我们说数据库里的 一对多、多对一关系都比较好实现，但是 多对多怎么做？

我们说学生选课，也是一个学生可以选择多个老师，一个老师可以选择多个学生

registrations = db.Table('registrations',
                 db.Column('student_id',db.Integer,db.ForeignKey('students.id')),
                 db.Column('class_id',db.Integer,db.ForeignKey('classes.id')))
class Student(db.Model):
    classes = db.relationship('Class',secondary=registrations,
                              backref= db.backref('students',lazy='dynamic')
                              lazy='dynamic')

    之后用 s.classes.append(c) db.session.add(s) 就完成了多余的选课工作

* git checkout 12a 还可以看到对应的单元测试，ing~

* 关于构造器，不应该是用 follower_id，为什么可以直接用 follower  self.remove 和 self.delete 区别

* 关于为什么 remove 需要两个参数之类的…………，delete 可以直接删除

* 好吧，在路由里面定义，还必须是同名函数，还有_ 和 -

* 数据库的显示还是存在些许问题，用户名显示的格式出错

* 接下来要看测试方面的事情。然后 写感受，翻译文档。之后还要增加翻页，属性管理等等。

* 今天晚上看一部分的 Scrapy