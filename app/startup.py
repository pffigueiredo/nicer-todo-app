from nicegui import Client, ui
from app import todo

def startup() -> None:
    todo.create()