from enum import StrEnum


QUARTERLY_INCOME_STATEMENT_COLLECTION = "quarterly_income_statements"
FIRESTORE_DATABASE = "financial-data"

class LlmModels(StrEnum):
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_0_FLASH = "gemini-2.0-flash-exp"
    GEMINI_3_FLASH = "gemini-3-pro-preview"
    
LOG_TYPE = "log_type"

class FiscalQuarterEnum(StrEnum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"

class ExchangesEnum(StrEnum):
    NASDAQ = "NASDAQ"
    NYSE = "NYSE"
    AMEX = "AMEX"
    OTC = "OTC"
    FINRA = "FINRA"
    LSE = "LSE"
    SSE = "SSE"
    TSE = "TSE"
    ASX = "ASX"
    HKEX = "HKEX"
    BSE = "BSE"
    

class LogType:
    class General(StrEnum):
        GENERAL_LOG = "general_log"
        HEARTBEAT = "heartbeat"
        INIT = "init"
        LOAD_KEYS = "load_keys"
        SKIP_ACCOUNT = "skip_account"

    class Errors(StrEnum):
        ERROR = "error"
        FILE_NOT_FOUND = "FileNotFoundError"
        YAML_ERROR = "YAMLError"
        VALUE_ERROR = "ValueError"
        KEY_ERROR = "KeyError"
        
    class Response(StrEnum):
        RESPONSE = "response"
        ACK = "ack"
        NACK = "nack"
        FAILED_RESPONSE = "failed_response"