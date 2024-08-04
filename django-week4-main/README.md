# Django WEEK 4 - Making Queries

[Django Doc](https://docs.djangoproject.com/en/5.0/topics/db/queries/)

เมื่อเราทำการประกาศ class models.Model ใน models.py แล้ว เราจะสามารถใช้งาน database-abstraction API ที่จะช่วยให้่เรา create, retrieve, update และ delete ข้อมูลในฐานข้อมูลได้่อย่างง่ายและรวดเร็วมากๆ โดยไม่จำเป็นจะต้องเป็น SQL แม้แต่นิดเดียว

เรามา setup project กันสำหรับ tutorial นี้

1. สร้าง project ใหม่ชื่อ `week4_tutorial` (สร้าง vitual environment ใหม่ด้วย)
2. สร้าง app ชื่อ `blogs` และทำการตั้งค่าใน `settings.py`
3. แก้ไขไฟล์ `/blogs/models.py` และเพิ่ม code ด้่านล่างลงไป โดย models เหล่านี้เราจะใช้ในการทำ tutorial วันนี้กัน

```Python
from datetime import date

from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline
```

4. ทำการ `makemigrations` และ `migration`

## Creating objects

ใน Django จะใช้หลักการดังนี้ `model class` จะเปรียบเสมืิอน `database table` และ `instance` ของ class นั้นๆ จะเปรียบเสมือนข้อมูล 1 `record` ใน table

การสร้าง instance ของ class model ก็สามารถทำได้ง่ายๆ ดังนี้

**NOTE: ให้เปิด Django shell ขึ้นมา (`python manage.py shell`) และพิมพ์คำสั่งดังนี้**

```python
>>> from blogs.models import Blog
>>> b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
>>> b.save()
```

ซึ่ง Django จะเป็นการ generate SQL command `INSERT` เมื่อเราสั่ง `save()`

## Saving changes to objects

ในการบันทึกการแก้ไข record ที่มีอยู่ใน database แล้วก็ใช้ `save()` เช่นเดียวกัน

```python
>>> b.name = "New name"
>>> b.save()
```

ซึ่ง Django จะเป็นการ generate SQL command `UPDATE` เมื่อเราสั่ง `save()`

## Saving ForeignKey and ManyToManyField fields

การ update foreign key ก็สามารถทำได้เหมือนกับการ update field ปกติ โดยใช้ `save()`

```python
>>> from blogs.models import Blog, Entry
>>> entry = Entry.objects.get(pk=1)
>>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
>>> entry.blog = cheese_blog # Update FK blog ของ entry (ID = 1) ไปที่ cheese_blog (name = "Cheddar Talk")
>>> entry.save()
```

แต่การ update ManyToManyField จะทำงานแตกต่างไปนิดหน่อย เราจะต้องใช้ `add()` ดังตัวอย่าง

สมมติเราต้องการ add instance `joe` เป็นหนึ่งใน `authors` ของ instance `entry` (ID = 1)

```python
>>> from blogs.models import Author
>>> joe = Author.objects.create(name="Joe")
>>> entry.authors.add(joe)
```

เราสามารถ `add()` ที่ละหลายๆ instances เข้าไปก็ได้

```python
>>> john = Author.objects.create(name="John")
>>> paul = Author.objects.create(name="Paul")
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)
```

## Retrieving objects

การ `SELECT` ข้อมูลออกมาจาก database นั้นทาง Django มี API ให้เราใช้งานได้ง่ายและสามารถทำ query ที่ซับซ้อนได้ด้วย โดยเราจะได้ instance ของ class `Queryset` มาใช้งาน

> A **QuerySet** represents a collection of objects from your database. It can have zero, one or many filters. **Filters** narrow down the query results based on the given parameters. In SQL terms, a QuerySet equates to a SELECT statement, and a filter is a limiting clause such as WHERE or LIMIT.

เราจะใช้งาน API ของ Django โดยการเรียกใช้ Manager ของ class `models.Model` การเข้าใช้งาน Manager จะเข้าถึงด้วย `.objects` ยกตัวอย่างถ้าเราต้องการ SELECT ข้อมูลทั้งหมดในตาราง `Entry`

```Python
>>> Entry.objects.all() # SELECT * FROM entry;
```

### Retrieving specific objects with filters

ทีนี้เรามาลองเพิ่ม filter conditions กันบ้าง (ซึ่งก็คือการ `SELECT` โดยใส่เงื่อนไขใน `WHERE`)

ยกตัวอย่างเช่นสมมติเราต้องการ QuerySet ของ blog entries ในปี 2010

```python
>>> Entry.objects.filter(pub_date__year=2010)
```

### Chaining filters

เราสามารถ chain method `filter()` และ `exclude()` ได้

**NOTE:** `exclude()` คือการใส่เงื่อนไขที่จะกรองข้อมูลออก ดังในตัวอย่างด้านล่างคือการกรองข้อมูล blog entries หลังจากวันปัจจุบันออก

```python
>>> Entry.objects.filter(headline__startswith="What").exclude(
...     pub_date__gte=datetime.date.today()
... ).filter(pub_date__gte=datetime.date(2005, 1, 30))
```

```sql
SELECT * FROM entry WHERE entry.headline LIKE "What%" AND entry.pub_date < CURRENT_TIME AND entry.pub_date >= "2005-01-30"
```

### Retrieving a single object with get()

การใช้ method `filter()` จะ return `QuerySet` ออกมาเสมอ แม้ว่า record ของข้อมูลที่ได้จากการ filter จะมีเพียง 1 record ก็จะได้ `QuerySet` ที่มีข้อมูล 1 แถวออกจาก ดังนั้นถ้าเราต้องการที่จะได้ instance ของ class นั้นมาใช้งานเลย (ไม่ใช่ `QuerySet`) เราจะต้องใช้ `get()`

```python
>>> one_entry = Entry.objects.get(pk=1)
>>> one_entry = Entry.objects.filter(pk=1).first()
>>> one_entry = Entry.objects.filter(pk=1)[0]
>>> # ทั้ง 3 บรรทัดนี้ให้ผลเหมือนกัน
```

### Limiting QuerySets

ในกรณีที่เราต้อง SELECT และต้องการ LIMIT ผลลัพธ์เราสามารถทำได้คล้ายๆ กับการ slice list ของ Python

```python
>>> Entry.objects.all()[:5] # LIMIT 5

>>> Entry.objects.all()[5:10] # OFFSET 5 LIMIT 5
```

**NOTE:** การใช้ negative index (`Entry.objects.all()[-1]`) นั้นไม่ support

## Comparing objects

การเปรียบเทียบ instance ของ model 2 ตัวว่าเป็นตัวเดียวกันไหม สามารถทำได้โดยใช้ `==`

```python
>>> some_entry == other_entry
>>> some_entry.id == other_entry.id
```

## Deleting objects

การลบข้อมูลออกจาก database สามารถทำได้โดยใช้ method `delete()`

ลบทีละตัว

```python
>>> e.delete()
(1, {'blog.Entry': 1})
```

ลบทีละหลายตัว

```python
>>> Entry.objects.filter(pub_date__year=2005).delete()
(5, {'blog.Entry': 5})
```

## Copying model instances
Django ไม่มี method สำหรับ copy model instances แต่เราสามารถทำการ copy และสร้าง instance ใหม่ที่มีทุก field เหมือนต้นฉบับได้โดยการ set ให้ instance.pk = None และ instnace._state.adding = True

ดังในตัวอย่าง

```python
blog = Blog(name="My blog", tagline="Blogging is easy")
blog.save()  # blog.pk == 1

blog.pk = None
blog._state.adding = True
blog.save()  # blog.pk == 2
```

## Performing raw SQL query

ในกรณีที่เราต้องการที่จะเขียน SQL query เอง (ORM ของ Django อาจจะไม่รองรับ ... ซึ่งผมแทบไม่เคยเจอเลยเพราะ ORM ของ Django นั้น advanced มากๆ)

เราสามารถทำได้โดยใช้ `raw()` method

> Manager.raw(raw_query, params=(), translations=None)

```python
# สมมติเรามี model Person
class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)
```

```sh
# สามารถเขียน SELECT query ได้ดังนี้
>>> for p in Person.objects.raw("SELECT * FROM myapp_person"):
...     print(p)
...
John Smith
Jane Jones
```

```sh
# สมมติชื่อ field ไม่ตรงกับที่ประกาศใน model
>>> name_map = {"first": "first_name", "last": "last_name", "bd": "birth_date", "pk": "id"}
>>> Person.objects.raw("SELECT * FROM some_other_table", translations=name_map)
```

ผลลัพธ์ที่ได้จาก `raw()` เป็น instance ของ class `django.db.models.query.RawQuerySet` ซึ่งใช้งานคล้ายกับ `QuerySet` ที่เราคุ้นเคย
