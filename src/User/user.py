from .auth import MoodleAgent

import sys, traceback

class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username.lower().strip()
        self.password = password.strip()
        self.moodle_instance = None
        
        try:
            self.moodle_instance: MoodleAgent = MoodleAgent(self.username, self.password)
            
        except Exception as e:            
            raise ValueError("Authentication failed. Check your username and password.")
            
        else:
            self.full_name: str = self.moodle_instance.get_full_name()
            print(f"\nBem-vindo(a), {self.full_name}!")