"""
数据模型枚举类型
"""
from enum import Enum


class UserStatus(str, Enum):
    """用户状态"""
    ACTIVE = "ACTIVE"  # 活跃
    INACTIVE = "INACTIVE"  # 未激活
    BANNED = "BANNED"  # 已禁用
    PENDING = "PENDING"  # 待审批（教师注册）
    REJECTED = "REJECTED"  # 已拒绝（教师注册）


class JobStatus(str, Enum):
    """职位状态"""
    DRAFT = "DRAFT"  # 草稿
    PENDING = "PENDING"  # 待审核
    PUBLISHED = "PUBLISHED"  # 已发布
    CLOSED = "CLOSED"  # 已关闭


class ApplicationStatus(str, Enum):
    """申请状态"""
    PENDING = "PENDING"  # 待处理
    VIEWED = "VIEWED"  # 已查看
    INTERVIEWED = "INTERVIEWED"  # 已面试
    ACCEPTED = "ACCEPTED"  # 已接受
    REJECTED = "REJECTED"  # 已拒绝


class JobFairStatus(str, Enum):
    """双选会状态"""
    DRAFT = "DRAFT"  # 草稿
    PENDING = "PENDING"  # 待审核
    PUBLISHED = "PUBLISHED"  # 已发布
    ENDED = "ENDED"  # 已结束


class RegistrationStatus(str, Enum):
    """报名状态"""
    PENDING = "PENDING"  # 待审核
    APPROVED = "APPROVED"  # 已通过
    REJECTED = "REJECTED"  # 已拒绝
    CHECKED_IN = "CHECKED_IN"  # 已签到


class SessionType(str, Enum):
    """宣讲会类型"""
    OFFLINE = "OFFLINE"  # 线下
    ONLINE = "ONLINE"  # 线上
    LIVE = "LIVE"  # 直播


class SessionStatus(str, Enum):
    """宣讲会状态"""
    DRAFT = "DRAFT"  # 草稿
    PENDING = "PENDING"  # 待审核
    PUBLISHED = "PUBLISHED"  # 已发布
    ENDED = "ENDED"  # 已结束


class InterviewType(str, Enum):
    """面试类型"""
    VIDEO = "VIDEO"  # 视频面试
    VOICE = "VOICE"  # 语音面试
    OFFLINE = "OFFLINE"  # 线下面试


class InterviewStatus(str, Enum):
    """面试状态"""
    SCHEDULED = "SCHEDULED"  # 已安排
    IN_PROGRESS = "IN_PROGRESS"  # 进行中
    COMPLETED = "COMPLETED"  # 已完成
    CANCELLED = "CANCELLED"  # 已取消


class MessageType(str, Enum):
    """消息类型"""
    TEXT = "TEXT"  # 文本
    IMAGE = "IMAGE"  # 图片
    FILE = "FILE"  # 文件
    LOCATION = "LOCATION"  # 位置
    SYSTEM = "SYSTEM"  # 系统消息


class FavoriteType(str, Enum):
    """收藏类型"""
    JOB = "JOB"  # 职位
    RESUME = "RESUME"  # 简历
    SCHOOL = "SCHOOL"  # 学校
    STUDENT = "STUDENT"  # 学生
    ENTERPRISE = "ENTERPRISE"  # 企业


class ScheduleType(str, Enum):
    """日程类型"""
    JOB_FAIR = "JOB_FAIR"  # 双选会
    INFO_SESSION = "INFO_SESSION"  # 宣讲会
    INTERVIEW = "INTERVIEW"  # 面试
    MANUAL = "MANUAL"  # 手动添加


class OfferStatus(str, Enum):
    """Offer状态"""
    PENDING = "PENDING"  # 待处理
    ACCEPTED = "ACCEPTED"  # 已接受
    REJECTED = "REJECTED"  # 已拒绝
    EXPIRED = "EXPIRED"  # 已过期


class RightsType(str, Enum):
    """权益类型"""
    FEATURE = "FEATURE"  # 功能
    QUOTA = "QUOTA"  # 配额
    DURATION = "DURATION"  # 时长


class PurchaseStatus(str, Enum):
    """购买状态"""
    PENDING = "PENDING"  # 待支付
    PAID = "PAID"  # 已支付
    FAILED = "FAILED"  # 支付失败
    REFUNDED = "REFUNDED"  # 已退款


class FeedbackStatus(str, Enum):
    """反馈状态"""
    PENDING = "PENDING"  # 待处理
    PROCESSING = "PROCESSING"  # 处理中
    RESOLVED = "RESOLVED"  # 已解决
    REJECTED = "REJECTED"  # 已拒绝


class VerificationStatus(str, Enum):
    """认证状态"""
    PENDING = "PENDING"  # 待审核
    APPROVED = "APPROVED"  # 已通过
    REJECTED = "REJECTED"  # 已拒绝



