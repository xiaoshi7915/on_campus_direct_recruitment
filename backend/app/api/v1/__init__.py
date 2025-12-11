"""
API v1版本路由
"""
from fastapi import APIRouter
from app.api.v1 import (
    auth, users, jobs, resumes, applications, profile,
    job_fairs, info_sessions, interviews, schedules, favorites, upload, chat, statistics, sms, students, rights, departments, schools, student_comments, talent_recommendations, approvals, teacher_management
)

# 创建API路由器
api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["职位"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["简历"])
api_router.include_router(applications.router, prefix="/applications", tags=["职位申请"])
api_router.include_router(profile.router, prefix="/profile", tags=["用户档案"])
api_router.include_router(job_fairs.router, prefix="/job-fairs", tags=["双选会"])
api_router.include_router(info_sessions.router, prefix="/info-sessions", tags=["宣讲会"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["面试"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["日程"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["收藏"])
api_router.include_router(upload.router, prefix="/upload", tags=["文件上传"])
api_router.include_router(chat.router, prefix="/chat", tags=["聊天"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["数据统计"])
api_router.include_router(sms.router, prefix="/sms", tags=["短信验证码"])
api_router.include_router(students.router, prefix="/students", tags=["学生管理"])
api_router.include_router(rights.router, prefix="/rights", tags=["权益管理"])
api_router.include_router(departments.router, prefix="/departments", tags=["院系管理"])
api_router.include_router(schools.router, prefix="/schools", tags=["学校管理"])
api_router.include_router(student_comments.router, prefix="/student-comments", tags=["学生点评"])
api_router.include_router(talent_recommendations.router, prefix="/talent-recommendations", tags=["人才推荐"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["审批流程"])
api_router.include_router(teacher_management.router, prefix="/teacher-management", tags=["教师管理"])
