# 1. Build FileLogger context manager with timestamps, automatic closing, exception handling and with statement.
from datetime import datetime

class FileLogger:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, "a")
        self.log("Logger Started")
        return self

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file.write(f"[{timestamp}] {message}\n")

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.log(f"ERROR: {exc_value}")

        self.log("Logger Closed")
        self.file.close()

        
        return False

try:
    with FileLogger("app.log") as logger:
        logger.log("Application Started")
        logger.log("User Logged In")

      

        logger.log("Application Finished")

except Exception as e:
    print("Exception:", e)