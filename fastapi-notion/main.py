from app.config import app
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router

# 라우터 등록
app.include_router(auth_router)
app.include_router(user_router)
