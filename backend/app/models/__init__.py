"""
数据模型模块初始化
导入所有模型以确保SQLAlchemy能够识别它们
"""
from app.models.user import User
from app.models.user_type import UserType
from app.models.enums import (
    UserStatus, JobStatus, ApplicationStatus, JobFairStatus,
    RegistrationStatus, SessionType, SessionStatus,
    InterviewType, InterviewStatus, MessageType,
    FavoriteType, ScheduleType, OfferStatus,
    RightsType, PurchaseStatus, FeedbackStatus
)
from app.models.school import School, Department, Class
from app.models.profile import StudentProfile, TeacherProfile, EnterpriseProfile
from app.models.job import Resume, Job, JobIntention, JobApplication
from app.models.activity import JobFair, JobFairRegistration, InfoSession, InfoSessionRegistration
from app.models.interview import Interview, Offer
from app.models.chat import ChatSession, Message
from app.models.common import Favorite, Schedule, Feedback
from app.models.todo import Todo
from app.models.mark import Mark
from app.models.rights import Rights, RightsPackage, RightsPackageItem, UserRights, RightsPurchase

__all__ = [
    # 用户相关
    "User",
    "UserType",
    "UserStatus",
    # 学校相关
    "School",
    "Department",
    "Class",
    # 用户档案
    "StudentProfile",
    "TeacherProfile",
    "EnterpriseProfile",
    # 职位相关
    "Resume",
    "Job",
    "JobStatus",
    "JobIntention",
    "JobApplication",
    "ApplicationStatus",
    # 活动相关
    "JobFair",
    "JobFairStatus",
    "JobFairRegistration",
    "InfoSession",
    "SessionType",
    "SessionStatus",
    "InfoSessionRegistration",
    "RegistrationStatus",
    # 面试相关
    "Interview",
    "InterviewType",
    "InterviewStatus",
    "Offer",
    "OfferStatus",
    # 聊天相关
    "ChatSession",
    "Message",
    "MessageType",
    # 通用
    "Favorite",
    "FavoriteType",
    "Schedule",
    "ScheduleType",
    "Feedback",
    "FeedbackStatus",
    # 待办事项
    "Todo",
    # 标记
    "Mark",
    # 权益相关
    "Rights",
    "RightsType",
    "RightsPackage",
    "RightsPackageItem",
    "UserRights",
    "RightsPurchase",
    "PurchaseStatus",
    # 学生点评
    "StudentComment",
]
