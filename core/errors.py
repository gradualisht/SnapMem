class SnapMemError(Exception):
    
    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}

class ParseError(SnapMemError):
    pass

class InvalidMemoryError(SnapMemError):
    pass

class MemoryFileNotFoundError(SnapMemError):
    pass

class InvalidExportError(SnapMemError):
    pass

class DuplicateMemoryError(SnapMemError):
    pass

class FileOperationError(SnapMemError):
    pass
