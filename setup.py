from cx_Freeze import setup, Executable

files = {"include_files": ["./class_works.py",
                           "./settings.json", "./clicker.json"],
         "packages": ["pyautogui", "keyboard"]}
setup(
        name="TimeStamper (GAIN Project Custom Edition)",
        version="3.01",
        description="Timestamp manager for neuro-behavioral study protocol.",
        options={'build.exe': files},
        executables=[Executable("main.py"), Executable("click_record.py"), Executable("maker.py")])
