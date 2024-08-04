# WEEK 3 Exercises - Django Model (3 คะแนน)

## Creating Models

1. สร้าง project ใหม่ชื่อ "myshop" (สร้าง vitual environment ใหม่ด้วย)
2. สร้าง app ชื่อ shop และทำการตั้งค่าใน `settings.py`
3. แก้ไขไฟล์ `models.py` สร้าง models ตาม ERD นี้

![ERD-E-COMMERCE](/images/WEEK3-ERD(e-commerce).png)

4. ทำการ makemigrations
5. ทำการ migrate เพื่อสร้างตาราง

### การให้คะแนน

- สร้าง models ที่มีความสัมพันธ์แบบ one-to-many ได้ครบถ้วนถูกต้อง (0.5 คะแนน)
- สร้าง models ที่มีความสัมพันธ์แบบ one-to-one ได้ครบถ้วนถูกต้อง (0.5 คะแนน)
- สร้าง models ที่มีความสัมพันธ์แบบ many-to-many ได้ครบถ้วนถูกต้อง (1 คะแนน)
- กำหนด ENUM method ใน model PaymentMethod ได้ถูกต้อง (0.5 คะแนน)

## Datetime & Timezone

1. แปลง `datetime.now()` เป็น time zone "Asia/Bangkok" (0.2 คะแนน)
2. จงหาว่านับจากวันนี้ไปอีก 500 วันเป็นวันที่เท่าไหร่ และ เป็นวันอะไรในสัปดาห์ (0.3 คะแนน)
**Hint:** [weekday](https://docs.python.org/3/library/datetime.html#datetime.date.weekday)
