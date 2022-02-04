from class_works import Manager
import keyboard

manager = Manager({}, 1, '')
manager.make_dict()

print('To start the protocol press ctrl + shift + s as the subject begins the first phase. \n'
      'To advance round press ctrl + shift + y. \n'
      'To end a phase press ctrl + shift + t. \n'
      'To start a new phase press ctrl + shift + p \n'
      'To end the protocol press ctrl + shift + e. \n'
      'To stop the program press esc. \n')

keyboard.add_hotkey('ctrl + shift + s', lambda: manager.start())
keyboard.add_hotkey('ctrl + shift + p', lambda: manager.new_phase())
keyboard.add_hotkey('ctrl + shift + y', lambda: manager.new_round())
keyboard.add_hotkey('ctrl + shift + t', lambda: manager.end_phase())
keyboard.add_hotkey('ctrl + shift + e', lambda: manager.end())

keyboard.wait('esc')
