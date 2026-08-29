# ==========================================
# استيراد المكتبات
# ==========================================

from flask import Flask, render_template, request, redirect

from database import (
    add_student,
    get_all_students,
    get_student,
    update_student,
    delete_student,
    search_students,
    create_table,
    get_students_count,
    get_subjects_count
)


# ==========================================
# إنشاء تطبيق Flask
# ==========================================

app = Flask(__name__)


# ==========================================
# إنشاء جدول الطلاب
# إذا لم يكن الجدول موجودًا
# ==========================================

create_table()


# ==========================================
# الصفحة الرئيسية
# ==========================================

# ==========================================
# الصفحة الرئيسية
# ==========================================

@app.route("/")
def home():

    # عدد الطلاب
    students_count = len(get_all_students())

    # عدد المواد
    subjects_count = get_subjects_count()

    # إرسال الأعداد إلى index.html
    return render_template(
        "index.html",
        students_count=students_count,
        subjects_count=subjects_count
    )


# ==========================================
# صفحة عن الموقع
# ==========================================

@app.route("/about")
def about():

    # عرض صفحة about.html
    return render_template("about.html")


# ==========================================
# صفحة إضافة طالب
# ==========================================

@app.route("/form")
def form():

    # عرض نموذج إضافة الطالب
    return render_template("form.html")


# ==========================================
# استقبال بيانات الطالب الجديد
# ==========================================

@app.route("/submit", methods=["POST"])
def submit():

    # استقبال البيانات من form.html
    name = request.form.get("name")
    age = request.form.get("age")
    email = request.form.get("email")
    mada = request.form.get("mada")


    # ------------------------------------------
    # التأكد من إدخال الاسم والعمر
    # ------------------------------------------

    if not name or not age:

        return render_template(
            "form.html",
            error="من فضلك أدخل الاسم والعمر",
            name=name,
            age=age,
            email=email,
            mada=mada
        )


    # ------------------------------------------
    # التأكد أن العمر رقم
    # ------------------------------------------

    if not age.isdigit():

        return render_template(
            "form.html",
            error="العمر يجب أن يكون رقمًا",
            name=name,
            age=age,
            email=email,
            mada=mada
        )


    # ------------------------------------------
    # التأكد من البريد والمادة
    # ------------------------------------------

    if not email or not mada:

        return render_template(
            "form.html",
            error="من فضلك أدخل البريد الإلكتروني واختر المادة",
            name=name,
            age=age,
            email=email,
            mada=mada
        )


    # ------------------------------------------
    # تحويل العمر من نص إلى رقم
    # ------------------------------------------

    age = int(age)


    # ------------------------------------------
    # إضافة الطالب إلى قاعدة البيانات
    # ------------------------------------------

    add_student(
        name,
        age,
        email,
        mada
    )


    # ------------------------------------------
    # بعد نجاح الإضافة
    # الانتقال إلى قائمة الطلاب
    # ------------------------------------------

    return redirect("/students?message=تمت إضافة الطالب بنجاح")


# ==========================================
# قائمة جميع الطلاب
# ==========================================

@app.route("/students")
def students():

    # جلب جميع الطلاب من قاعدة البيانات
    students = get_all_students()

    # إرسال الطلاب إلى students.html
    return render_template(
        "students.html",
        students=students
    )


# ==========================================
# البحث بالاسم أو المادة
# ==========================================

@app.route("/search")
def search():

    # الحصول على كلمة البحث
    search_text = request.args.get("search", "")

    # البحث عن الطلاب باستخدام database.py
    students = search_students(search_text)

    # إرسال نتائج البحث إلى الصفحة
    return render_template(
        "students.html",
        students=students
    )


# ==========================================
# فتح صفحة تعديل طالب
# ==========================================

@app.route("/edit/<int:id>")
def edit(id):

    # جلب الطالب باستخدام رقم ID
    student = get_student(id)


    # إذا لم يتم العثور على الطالب
    if student is None:

        return "الطالب غير موجود"


    # إرسال بيانات الطالب إلى edit.html
    return render_template(
        "edit.html",
        student=student
    )


# ==========================================
# استقبال بيانات التعديل
# ==========================================

@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    # استقبال البيانات الجديدة
    name = request.form.get("name")
    age = request.form.get("age")
    email = request.form.get("email")
    mada = request.form.get("mada")


    # ------------------------------------------
    # التحقق من الاسم والعمر
    # ------------------------------------------

    if not name or not age:

        return render_template(
            "edit.html",
            student=(id, name, age, email, mada),
            error="من فضلك أدخل الاسم والعمر"
        )


    # ------------------------------------------
    # التحقق من أن العمر رقم
    # ------------------------------------------

    if not age.isdigit():

        return render_template(
            "edit.html",
            student=(id, name, age, email, mada),
            error="العمر يجب أن يكون رقمًا"
        )


    # تحويل العمر إلى رقم
    age = int(age)


    # ------------------------------------------
    # تحديث الطالب في قاعدة البيانات
    # ------------------------------------------

    update_student(
        id,
        name,
        age,
        email,
        mada
    )


    # ------------------------------------------
    # العودة إلى قائمة الطلاب
    # ------------------------------------------

    return redirect("/students?message=تمت تعديل الطالب بنجاح")


# ==========================================
# حذف طالب
# ==========================================

@app.route("/delete/<int:id>")
def delete(id):

    # حذف الطالب من قاعدة البيانات
    delete_student(id)

    # العودة إلى قائمة الطلاب
    return redirect("/students?message=تم حذف الطالب بنجاح")


# ==========================================
# تشغيل التطبيق
# ==========================================

if __name__ == "__main__":

    # تشغيل Flask مع وضع Debug
    app.run(debug=True)