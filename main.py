from class_works import TimeManagement, Session
import asyncio
import keyboard

sess = Session([], '', '', [], 1, 1)
sess.make_object()

keyboard.add_hotkey('space', lambda: sess.next_round())

keyboard.wait('esc')
