from enum import Enum

class BranchEnum(str, Enum):
    IT = "IT"
    CSE = "CSE"
    AIML = "AIML"
    ECE = "ECE"
    CYS = "CYS"
    DS = "DS"
    CSBS = "CSBS"

class ReportTypeEnum(str, Enum):
    LOST = "LOST"
    FOUND = "FOUND"

class ReportStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    MATCHED = "MATCHED"
    CLAIMED = "CLAIMED"
    CLOSED = "CLOSED"

class VisibilityEnum(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

class ImportanceEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"