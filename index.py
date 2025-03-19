# Desc: Entry point for our backend system of the Kala app
from conf import load_env

load_env()

print("Loading Kala App...")

from apis import chats
from app import getFlaskApp

app = getFlaskApp()
