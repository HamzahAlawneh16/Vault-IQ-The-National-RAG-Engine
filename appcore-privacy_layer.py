import re

class PrivacyLayer:
    """
    Leadership Principle: Earn Trust.
    Ensures that sensitive information (Emails, Phone numbers) is masked 
    before indexing or sending to external LLMs.
    """
    def __init__(self):
        # Regex patterns for common sensitive data in Jordan/Region
        self.email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        self.phone_pattern = r'\+?\d{10,12}'

    def mask_data(self, text: str) -> str:
        """
        Complexity: O(N) where N is the length of the text.
        Simple yet effective first layer of defense.
        """
        text = re.sub(self.email_pattern, "[EMAIL_MASKED]", text)
        text = re.sub(self.phone_pattern, "[PHONE_MASKED]", text)
        return text