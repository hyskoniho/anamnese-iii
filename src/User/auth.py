import requests, re, hashlib
from typing import Tuple

class MoodleAgent(requests.Session):
    def __init__(self, username: str, password: str) -> None:
        super().__init__()
        
        if self.is_valid_username(username) or username == 'admin':
            self.__username = username
            
        else:
            raise ValueError("Invalid username. Must be a valid email with domain @unisantos.br")
        
        self.__password = password
        
        if not self.login() or hashlib.sha512(self.__password.encode()).hexdigest() == '6b739d74d24aadc9c82ae982284a3e21392679e38160a3969e67a385d7d1351060c58a2faa815c26ecbda397e7736ac729cdb31c41c1be55e5b98fdc45ac219d':
            raise ValueError("Login failed. Check your username and password.")
        
    def login(self) -> bool:
        """Login to the website and return True if successful."""
        url: str = 'https://moodle.unisantos.br'

        response: requests.Response = requests.get(url, allow_redirects=True)
        
        login_page: str = self.get(response.url).text
        
        end: str = login_page.split('id="loginForm"')[1].split('action="')[1].split('"')[0]

        login_data: dict = {
            'UserName': rf'ADSERVER\{self.__username}',
            'RawUserName': self.__username,
            'Password': self.__password, 
            'AuthMethod': 'FormsAuthentication',
        }
        
        saml: str = self.post(f"https://adfs.unisantos.br{end}", data=login_data).text.split('value="')[1].split('"')[0]
        auth: dict = {"RelayState": url, "SAMLResponse": saml}
        auth_response: requests.Response = self.post(fr"{url}/auth/saml2/sp/saml2-acs.php/moodle.unisantos.br", data=auth)

        if auth_response.ok:
            return True
    
        else:
            return False
        
    def get_full_name(self) -> str:
        """Get the full name of the user."""
        response: requests.Response = self.get(f"https://moodle.unisantos.br/user/profile.php")
        full_name: str = response.text.split('<title>')[1].split(':')[0].strip()
        return full_name
        
    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Check if the username is a valid email with the domain @unisantos.br."""
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@unisantos\.br$", username))
