import logging


class Logger:
    def __init__(self, device_id):
        self.device_id = device_id
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self._setup_cloudwatch_logger()
        
    def _setup_cloudwatch_logger(self):
        # Create a CloudWatch log handler (assuming CloudWatch permissions are configured)
        cloudwatch_handler = logging.StreamHandler()  # Replace with actual CloudWatch log handler
        cloudwatch_handler.setLevel(logging.INFO)
        self.logger.addHandler(cloudwatch_handler)
        
        # Console log handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)

    def log(self, message):
        log_message = f"[{self.device_id}] {message}"
        self.logger.info(log_message)
        print(log_message)  # For local console output