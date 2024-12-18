import os
import hmac

import dotenv

dotenv.load_dotenv()


def credentials(username: str, password: str):
    """Checks whether a password entered by the user is correct."""
    
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    
    if username == USERNAME and hmac.compare_digest(password, PASSWORD):
        return True
    return False
