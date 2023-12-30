from enum import Enum


class FileTypeEnum(Enum):
    TXT = 1
    PDF = 2
    PNG = 3
    JPG = 4
    JPEG = 5
    GIF = 6
    PPT = 7
    PPTX = 8
    DOC = 9
    DOCX = 10
    XLS = 11
    XLSX = 12
    CSV = 13
    MP3 = 14
    MP4 = 15


class IsIoEnum(Enum):
    不可上传 = 0
    可上传 = 1


class IsDeleteEnum(Enum):
    未删除 = 0
    删除 = 1


class IsTopEnum(Enum):
    未置顶 = 0
    置顶 = 1


class NoteStateEnum(Enum):
    草稿 = 0
    审核中 = 1
    审核通过 = 2
    审核未通过 = 3
