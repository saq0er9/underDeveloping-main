from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from sqlalchemy import select, insert, delete

from app.schemas import Course, CourseCreate
from app.database import engine, courses_table



# إنشاء موجه المسارات الخاص بالدورات
router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)



# ---------------------------------------------------------
# 1. جلب جميع الدورات (مع فلترة اختيارية باسم المحاضر)
# ---------------------------------------------------------
@router.get("/", response_model=List[Course])
def get_courses(instructor: Optional[str] = None):
    """جلب كافة الدورات مع إمكانية البحث الجزئي غير الحساس للحالة في اسم المحاضر."""
    with engine.connect() as conn:
        stmt = select(courses_table)
        
        if instructor:
            # الفلترة باستعمال ilike للبحث المرن غير الحساس لحالة الأحرف
            stmt = stmt.where(courses_table.c.instructor.ilike(f"%{instructor}%"))
            
        result = conn.execute(stmt)
        # تحويل صفوف النتيجة إلى القواميس المطلوبة لـ Pydantic
        return [dict(row._mapping) for row in result]



# ---------------------------------------------------------
# 2. إنشاء دورة جديدة
# ---------------------------------------------------------
@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    """إضافة دورة جديدة في قاعدة البيانات وإرجاع السجل المضاف شاملاً الـ ID."""
    with engine.connect() as conn:
        # إدراج البيانات مع إرجاع الصف المُنشأ مباشرة باستخدام returning
        stmt = insert(courses_table).values(**course.model_dump()).returning(courses_table)
        result = conn.execute(stmt)
        conn.commit()
        
        new_course = result.fetchone()
        return dict(new_course._mapping)



# ---------------------------------------------------------
# 3. جلب دورة محددة بـ ID
# ---------------------------------------------------------
@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    """البحث عن دورة باستخدام المفتاح الرئيسي، ورفع استثناء 404 في حال عدم وجودها."""
    with engine.connect() as conn:
        stmt = select(courses_table).where(courses_table.c.id == course_id)
        result = conn.execute(stmt).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
            
        return dict(result._mapping)



# ---------------------------------------------------------
# 4. حذف دورة محددة بـ ID
# ---------------------------------------------------------
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    """التحقق من وجود الدورة أولاً، ثم حذفها وإرجاع استجابة فارغة برمز 204."""
    with engine.connect() as conn:
        # التأكد من وجود السجل قبل الحذف
        stmt = select(courses_table).where(courses_table.c.id == course_id)
        existing = conn.execute(stmt).fetchone()
        
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
            
        # تنفيذ أمر الحذف واعتماده
        del_stmt = delete(courses_table).where(courses_table.c.id == course_id)
        conn.execute(del_stmt)
        conn.commit()
        return