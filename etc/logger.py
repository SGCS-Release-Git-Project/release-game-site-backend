"""
logger.py

Descriptions
- Custom Log 셋팅 함수 정의

Globals
- None

Classes:
- None

Functions:
- rInit_Logger

"""


import logging


def rInit_Logger(name:str, level:str) -> logging:

    """Log 출력 함수"""

    # _nameToLevel = {
    #     'CRITICAL': CRITICAL,
    #     'FATAL': FATAL,
    #     'ERROR': ERROR,
    #     'WARN': WARNING,
    #     'WARNING': WARNING,
    #     'INFO': INFO,
    #     'DEBUG': DEBUG,
    #     'NOTSET': NOTSET,
    # }

    logger = logging.getLogger(name=name)
    logger.setLevel(level)

    formatter = logging.Formatter('|%(asctime)s|==|%(name)s||%(levelname)s| %(message)s | %(funcName)s',
                                datefmt='%Y-%m-%d %H:%M:%S'
                                )


    stream_handler = logging.StreamHandler() ## 스트림 핸들러 생성
    stream_handler.setFormatter(formatter) ## 텍스트 포맷 설정
    
    logger.addHandler(stream_handler) ## 핸들러 등록


    return logger