from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from sqlalchemy import select, insert, delete

from app.schemas import Student, StudentCreate
from app.database import engine, students_table



# إنشاء موجه المسارات الخاص بالطلاب
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)



# ---------------------------------------------------------
# 1. جلب جميع الطلاب (مع فلترة اختيارية باسم الطالب)
# ---------------------------------------------------------
@router.get("/", response_model=List[Student])
def get_students(name: Optional[str] = None):
    """جلب قائمة الطلاب مع إمكانية البحث الجزئي باسم الطالب."""
    with engine.connect() as conn:
        stmt = select(students_table)
        
        if name:
            # البحث عن مطابقة جزئية في خانة الاسم
            stmt = stmt.where(students_table.c.name.ilike(f"%{name}%"))
            
        result = conn.execute(stmt)
        return [dict(row._mapping) for row in result]



# ---------------------------------------------------------
# 2. إدخال طالب جديد
# ---------------------------------------------------------
@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    """إضافة طالب جديد في قاعدة البيانات وإرجاع بياناته المسجلة."""
    with engine.connect() as conn:
        stmt = insert(students_table).values(**student.model_dump()).returning(students_table)
        result = conn.execute(stmt)
        conn.commit()
        
        new_student = result.fetchone()
        return dict(new_student._mapping)



# ---------------------------------------------------------
# 3. جلب بيانات طالب محدد بـ ID
# ---------------------------------------------------------
@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int):
    """الاستعلام عن طالب محدد بالـ ID أو إرجاع خطأ 404 إذا لم يُعثر عليه."""
    with engine.connect() as conn:
        stmt = select(students_table).where(students_table.c.id == student_id)
        result = conn.execute(stmt).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
            
        return dict(result._mapping)



# ---------------------------------------------------------
# 4. حذف طالب محدد بـ ID
# ---------------------------------------------------------
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    """حذف سجل الطالب بعد التأكد من وجوده في قاعدة البيانات."""
    with engine.connect() as conn:
        stmt = select(students_table).where(students_table.c.id == student_id)
        existing = conn.execute(stmt).fetchone()
        
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
            
        del_stmt = delete(students_table).where(students_table.c.id == student_id)
        conn.execute(del_stmt)
        conn.commit()
        return