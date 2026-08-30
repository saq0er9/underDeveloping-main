from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import students, courses

app = FastAPI(title="Course & Student Management API")



# 1. تحديد النطاقات المسموح لها بالاتصال بالـ API
origins = [
    "http://localhost:5173",    # المنفذ الافتراضي لتطبيق React عند إنشائه بـ Vite
    "http://127.0.0.1:5173",
    "http://localhost:3000",    # المنفذ الافتراضي لـ Create React App
]



# 2. إضافة CORSMiddleware للتطبيق
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # السماح للنطاقات المحددة أعلاه فقط
    allow_credentials=True,      # السماح بتمرير ملفات تعريف الارتباط (Cookies) والتأكيد
    allow_methods=["*"],         # السماح بجميع العمليات (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],         # السماح بجميع أنواع الـ Headers
)



# 3. تسجيل موجهات المسارات (Routers)
app.include_router(students.router)
app.include_router(courses.router)



@app.get("/")
def root():
    return {"message": "API is running successfully"}