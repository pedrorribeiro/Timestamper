from class_works import Manager
import asyncio
import keyboard

manager = Manager({}, 1, '')

keyboard.add_hotkey('ctrl + shift + s', lambda: manager.start())
keyboard.add_hotkey('space', lambda: manager.new_round())
keyboard.add_hotkey('ctrl + shift + e', lambda: manager.end())

keyboard.wait('esc')
