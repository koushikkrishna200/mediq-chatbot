import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load user config (we'll store credentials here)
def load_auth_config():
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def setup_authenticator(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    return authenticator
