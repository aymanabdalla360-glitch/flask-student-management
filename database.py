# ==========================================
# استيراد مكتبة SQLite
# ==========================================

import sqlite3

# ==========================================
# الاتصال بقاعدة البيانات
# ==========================================

def get_db_connection():

    # فتح الاتصال بقاعدة البيانات
    conn = sqlite3.connect("students.db")

    # إعادة الاتصال للدالة التي طلبته
    return conn

# ==========================================
# إنشاء جدول الطلاب
# ==========================================

def create_table():

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # إنشاء جدول students إذا لم يكن موجودًا
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            age INTEGER NOT NULL,

            email TEXT NOT NULL,

            mada TEXT NOT NULL
        )
    """)

    # حفظ إنشاء الجدول
    conn.commit()

    # إغلاق الاتصال
    conn.close()

# ==========================================
# إضافة طالب جديد
# ==========================================

def add_student(name, age, email, mada):

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # إضافة الطالب إلى جدول students
    conn.execute(
        """
        INSERT INTO students (name, age, email, mada)
        VALUES (?, ?, ?, ?)
        """,

        # إرسال القيم مكان علامات ?
        (name, age, email, mada)
    )

    # حفظ عملية الإضافة
    conn.commit()

    # إغلاق الاتصال
    conn.close()

# ==========================================
# جلب جميع الطلاب
# ==========================================

def get_all_students():

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # جلب جميع الطلاب من الجدول
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    # إغلاق الاتصال
    conn.close()

    # إعادة جميع الطلاب إلى app.py
    return students

# ==========================================
# جلب طالب واحد باستخدام id
# ==========================================

def get_student(id):

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # البحث عن الطالب صاحب هذا الرقم
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",

        # وضع id مكان علامة ?
        (id,)
    ).fetchone()

    # إغلاق الاتصال
    conn.close()

    # إعادة بيانات الطالب إلى app.py
    return student

# ==========================================
# تعديل بيانات طالب
# ==========================================

def update_student(id, name, age, email, mada):

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # تعديل بيانات الطالب
    conn.execute(
        """
        UPDATE students

        SET name = ?,
            age = ?,
            email = ?,
            mada = ?

        WHERE id = ?
        """,

        # إرسال القيم بالترتيب
        (name, age, email, mada, id)
    )

    # حفظ التعديل
    conn.commit()

    # إغلاق الاتصال
    conn.close()

# ==========================================
# حذف طالب
# ==========================================

def delete_student(id):

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # حذف الطالب صاحب هذا id
    conn.execute(
        "DELETE FROM students WHERE id = ?",

        # وضع id مكان علامة ?
        (id,)
    )

    # حفظ عملية الحذف
    conn.commit()

    # إغلاق الاتصال
    conn.close()
    
# ==========================================
# البحث بالاسم أو المادة
# ==========================================

def search_students(search):

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # البحث في الاسم أو المادة
    students = conn.execute(
        """
        SELECT * FROM students
        WHERE name LIKE ?
        OR mada LIKE ?
        """,

        # إرسال كلمة البحث إلى العمودين
        (f"%{search}%", f"%{search}%")
    ).fetchall()

    # إغلاق الاتصال
    conn.close()

    # إعادة نتائج البحث إلى app.py
    return students

# ==========================================
# حساب عدد الطلاب
# ==========================================

def get_students_count():

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # حساب عدد الطلاب الموجودين في جدول students
    count = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    # إغلاق الاتصال
    conn.close()

    # إعادة عدد الطلاب إلى app.py
    return count

# ==========================================
# حساب عدد المواد
# ==========================================

def get_subjects_count():

    # الاتصال بقاعدة البيانات
    conn = get_db_connection()

    # حساب عدد المواد المختلفة
    count = conn.execute(
        "SELECT COUNT(DISTINCT mada) FROM students"
    ).fetchone()[0]

    # إغلاق الاتصال
    conn.close()

    # إعادة العدد
    return count