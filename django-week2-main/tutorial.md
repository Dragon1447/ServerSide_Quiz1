# Writing your first Django app, part 1

## Creating a project

สร้าง project ชื่อ `mysite` ด้วย command
```sh
> django-admin startproject mysite
```

คำสั่งนี้จะสร้าง files ต่างๆ ดังนี้
```python
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py # สำหรับตั้งค่า project
        urls.py # สำหรับกำหนด path url
        asgi.py
        wsgi.py
```

จากนั้นลองทดสอบ run server ขึ้นมาด้วยคำสั่ง

```sh
> python manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
May 23, 2024 - 08:48:22
Django version 4.2.13, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

โดย port default จะเป็น port 8000 แต่ถ้าคุณต้องการเปลี่ยน port สามารถใช้ command

```sh
> python manage.py runserver 8080
```

## Creating the Polls app

เรามาลองสร้าง app Polls กันด้วย command

```sh
> python manage.py startapp polls
```

Command นี้จะทำการสร้าง folder polls ซึ่งมีไฟล์ดังนี้

```sh
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

## Write your first view

เรามาเขียน view แรกกัน เปิดไฟล์ `polls/views.py` และเขียน code ด้านล่าง

```python
# polls/views.py
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

สร้างไฟล์ `polls/urls.py` จากนั้นไปเพิ่ม code ด้านล่างในไฟล์ `polls/urls.py`

```python
# polls/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

แต่จะสามารถเข้าถึง path ใน `polls/urls.py` เราจะต้องไปแก้ไขในไฟล์ `mysite/urls.py` ให้ชื้มาที่ `polls/urls.py`

```python
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

เรามาลองตรวจสอบดูว่า path ที่เรากำหนดใช้งานได้หรือไม่

```sh
> python manage.py runserver
```

เปิด web browser และ เข้าไปที่ url `http://localhost:8000/polls/`

Function `path()` นั้นรับ argument 4 ตัว โดยเป็น required argument 2 ตัวได้แก่ `route` และ `view` และเป็น optional argument 2 ตัว ได้แก่ `kwargs` และ `name`

- Argument: `route` - รับค่า string URL patterns
- Argument: `view` - รับ view ที่จะถูกเรียกเมื่อ Django ทำการ match URL pattern ได้
- Argument: `kwargs` - Arbitrary keyword arguments ซึ่งเราสามารถส่ง argument เพิ่มเติมไปยัง view
- Argument: `name` - เป็น string ชื่อของ path URL โดยการตั้งชื่อจะทำให้เราอ้างอิงถึงได้ง่าย เช่นถ้าต้องการ redirect ไปที่ path นี้ก็สามารถอ้างอิงถึงด้วย name แทนที่จะต้องเขียน full path

## Database setup

ต่อมาเราจะมาทำการตั้งค่าการเชื่อมต่อฐานข้อมูลกัน แต่ก่อนที่จะทำการเชื่อมต่อให้ทำการตรวจสอบก่อนว่าได้มีการ install PostgreSQL ไว้ในเครื่องแล้วหรือยังโดย command

```sh
> postgres --version
postgres (PostgreSQL) 15.0
```

โดยถ้ายังไม่ได้ทำการติดตั้ง PostgreSQL ให้่สามารถทการติดตั้งก่อน - [POSTGRES DOWNLOAD](https://www.postgresql.org/download/)

จากนั้นทำการติดตั้ง Postgres Client `psycopg2`

```python
> pip install psycopg2
OR
> pip install psycopg2-binary
OR
> brew install postgresql # for MacOS
```

จากนั้นเปิดไฟล์ `mysite/settings.py` และไปที่

```python
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

```

ให้ทำการแก้ไชเป็นดังนี้

```python
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mypolls",
        "USER": "db_username",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

ก่อนอื่นเราไปทำการสร้าง DATABASE ชื่อ `mypolls` ใน PostgreSQL กันก่อน

เปิด Command Prompt / Terminal ขึ้นมาจากนั้นพิมพ์ command ด้านล่างเพื่อเข้าสู่ SQL Shell

```sh
> psql -U postgres

/ # psql -U postgres
psql (15.0)
Type "help" for help.

postgres=#
```

จากนั้นพิมพ์ SQL `CREATE DATABASE mypolls;` เพื่อทำการสร้าง database (อย่าลืม semicolon ;)


จากนั้นติดตั้ง VS CODE extension ชื่อ `PostgreSQL` by Weijan Chen เพื่อใช้ในการจัดการฐานข้อมูลผ่าน UI

ทำการตั้งค่า connection กรอกข้อมูลดังนี้
```sh
Name: mypolls
Host: 127.0.0.1
Username: your postgres username
Password: your postgres password
Port: 5432 
```

เรามาทำการ migrate เพื่อสร้างตารางในฐานข้อมูลกัน

ใน Django จะมีระบบการจัดการ migrations หรือระบบการจัดการ การสร้าง แก้ไข ลบ ตารางในฐานข้อมูล โดยที่เราไม่จำเป็นจะต้องเขียน SQL query เพื่อจัดการเลย เพียงใช้ command ด้านล่าง

```sh
> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```

ทำการตรวจสอบว่าใน database `mypolls` มีตารางถูกสร้างเพิ่มขึ้นมา

**Congratulation! database setup is completed.**

## Creating models

เรามาสร้าง models กัน โดยใน app polls ของเราซึ่งมี 2 models ได้แก่ `Question` and `Choice` โดยเพิ่ม code ด้านล่างลงในไฟล์ `polls/models.py`

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

แต่ละ model class จะถูกนำไปสร้างเป็น table ใน database และแต่ละ field จะเป็น column ใน table โดยจะเห็นว่าเราได้ทำการกำหนด ประเภทของข้อมูลใน field เช่น CharField คือ field สำหรับบันทึกข้อมูล characters หรือ IntegerField คือ field สำหรับบันทึกข้อมูล integer

## Activating models

ก่อนอื่นเราจะต้องไปแก้ไขค่าตั้งค่าใน `mysite/settings.py` เพื่อให้ Django รู้จักกับ app `polls` ที่เราสร้างขึ้นมาก่อน โดยเพิ่ม "polls" ใน INSTALLED_APPS

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Add your apps here
    "polls",
]
```

ทำการสั่ง `makemigrations` เพื่อสร้างไฟล์ migration ซึ่ง Django จะทำการ generate code สำหรับที่จะใช้นำไปสร้าง แก้ไข ลบ table ใน database โดยยึดจาก class models ที่เรากำหนดในไฟล์ `polls/models.py`

```sh
> python manage.py makemigrations polls
Migrations for 'polls':
  polls/migrations/0001_initial.py
    - Create model Question
    - Create model Choice
```

จะเห็นไฟล์ `polls/migrations/0001_initial.py` จะถูกสร้างขึ้นมาโดย Django

พิมพ์ command ด้านล่างเพื่อเช็คว่า SQL อะไรที่จะถูก generate เมื่อเราสั่ง command `migrate`

```sql
> python manage.py sqlmigrate polls 0001
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "question_text" varchar(200) NOT NULL, "pub_date" timestamp with time zone NOT NULL);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" bigint NOT NULL);
ALTER TABLE "polls_choice" ADD CONSTRAINT "polls_choice_question_id_c5b4b260_fk_polls_question_id" FOREIGN KEY ("question_id") REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;
```

ทำการ migrate เพื่อสร้าง table ใน database `mypolls`

```sh
> python manage.py migrate polls
Operations to perform:
  Apply all migrations: polls
Running migrations:
  Applying polls.0001_initial... OK
```

## Playing with the API

เรามาลองเล่นกับ models ที่เราสร้างด้วย API ของ Django ใน Python shell กัน

```sh
> python manage.py shell

# ทำการ import models Question, Choice
>>> from polls.models import Question, Choice

# ทำการ SELECT ข้อมูลในตาราง question (SELECT * FROM question)
>>> Question.objects.all()
<QuerySet []>

# สร้าง instance ของ Question
>>> from django.utils import timezone
>>> q = Question(question_text="What is new?", pub_date=timezone.now())

# บันทึกข้อมูลลงใน table question
>>> q.save()

# ID ของ question ที่สร้าง = 1
>>> q.id
1

# ตัวแปร q เป็น instance ของ class Question ดังนั้นจะมี attribute question_text, pub_date ซึ่งสามารถเข้าถึงได้โดยใช้ dot notation ของ Python
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2024, 2, 26, 13, 0, 0, 115217, tzinfo=datetime.timezone.utc)

# แก้ไขข้อมูลเปลี่ยน question_text จาก "What's new?" -> "What's up?"
# SQL: UPDATE question SET question.question_text="What's up?" WHERE question.id = 1
>>> q.question_text = "What is up?"
# สั่ง save เพื่อบันทึกข้อมูลลง database
>>> q.save()

# Question.objects.all() แสดงข้อมูลทั้งหมดในตาราง question 
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```

เพิ่ม method __str__() ใน class Question และ Choice เพื่อกำหนดการ convert instance ของ object เป็น string

```python
from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

ลองกลับไปเล่นใน shell เพื่อ print question ID=1 ออกมา

```sh
>>> q = Question.objects.first()
>>> print(q)
What's new?
```

### Exercises
1. ลองสร้าง question ใหม่โดยให้ question_text = "Hello world?" และ pub_date เป็นวันที่ 2024-01-01 11:00:00
2. ลองสร้าง choice สำหรับ question 1 ให้มี 3 choices โดยให้ choice_text = "Yes", "No" และ "OK" และ votes = 0 ทั้ง 3 choices
3. ลองสร้าง choice สำหรับ question 2 ให้มี 2 choices โดยให้ choice_text = "Bye" และ "Hello" และ votes = 0 ทั้ง 2 choices

```sh
# Hint: การสร้าง choice สามารถทำได้ 2 แบบ
# แบบที่ 1
>>> q = Question.objects.get(pk=1) 
>>> q.choice_set.create(choice_text="Yes", votes=0)

# หรือ แบบที่ 2
>>> c = Choice(question=q, choice_text="Yes", votes=0)
>>> c.save()

# ถ้าอยากรู้ว่ามี choice จำนวนเท่าไหร่ของ question ID=1
>>> q.choice_set.count()
1
```

เรามาลองใช้ API ของ Django ในการ query ข้อมูล (SELECT query)

```sh
>>> Question.objects.all()
<QuerySet [<Question: What is up?>, <Question: Hello world?>]>

>>> Question.objects.filter(question_text__icontains="llo")
<QuerySet [<Question: Hello world?>]>

>>> Question.objects.filter(question_text__startswith="What")
<QuerySet [<Question: What is up?>]>

>>> Choice.objects.filter(question_id=1)
<QuerySet [<Choice: Yes>, <Choice: No>, <Choice: OK>]>

>>> Choice.objects.filter(question_id=1, choice_text="Yes")
<QuerySet [<Choice: Yes>]>

>>> Question.objects.first()
<Question: What is up?>

>>> Question.objects.last()
<Question: Hello world?>
```

เราจะมาสร้าง view กันต่อ ตามขั้นตอนในไฟล์ `tutorial-view.md`
