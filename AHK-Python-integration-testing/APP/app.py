import customtkinter, os

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Programmable MacroPad"
    WIDTH = 800
    HEIGHT = 500
    MACRO_LIST: list[str] = [
        "Google Search Selected Text", "Open Website", "Open Application", "Move up a Folder",
        "Copy HEX color code to clipboard", "Open Command Prompt in current folder", "Run command in current folder",
        "Open Command Prompt at a Favorite Folder", "Run Command at a Favorite Folder", 
        "Open File Explorer at a Favorite Folder", "Volume Up", "Volume Down", "Volume Mute", "Play/Pause Media","Empty Recycle Bin", 
        "Insert preset message",
        ]
    KEY1: str = ''
    KEY2: str = ''
    KEY3: str = ''
    KEY4: str = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- Setup main frame --
        self.title(App.APP_NAME)
        self.geometry("800x500")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-w>", self.on_closing)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = customtkinter.CTkFrame(master=self, width=150, corner_radius=0)
        self.sidebar.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.home = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.home.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # -- Setup Sidebar component --
        self.sidebar.grid_rowconfigure(2, weight=1)

        self.runAhkButton = customtkinter.CTkButton(master=self.sidebar, text="Program Board / Run AHK", command=self.run_ahk)
        self.runAhkButton.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.stopAhkButton = customtkinter.CTkButton(master=self.sidebar,text="Stop AHK", command=self.stop_ahk)
        self.stopAhkButton.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.appearanceModeLabel = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearanceModeLabel.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearanceModeMenu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.appearanceModeMenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # -- Setup Home component --
        
        self.searchBar = customtkinter.CTkEntry(master=self.home, placeholder_text="Search Preset", width=300)
        self.searchBar.grid(row=0, column=0, padx=(12,0), pady=(12,12))
        self.searchBar.bind("<Return>", self.search_preset)

        self.searchButton = customtkinter.CTkButton(master=self.home, text="Search", width=90, command=self.search_preset)
        self.searchButton.grid(row=0, column=1, padx=(12,0), pady=(12,12))

        self.keyOneLabel = customtkinter.CTkLabel(master=self.home, text="First function key:", anchor="w")
        self.keyTwoLabel = customtkinter.CTkLabel(master=self.home, text="Second function key:", anchor="w")
        self.keyThreeLabel = customtkinter.CTkLabel(master=self.home, text="Third function key:", anchor="w")
        self.keyFourLabel = customtkinter.CTkLabel(master=self.home, text="Fourth function key:", anchor="w")

        self.keyOneLabel.grid(row=1, column=0, sticky="w", padx=(10, 10), pady=(0, 0))
        self.keyTwoLabel.grid(row=2, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyThreeLabel.grid(row=3, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyFourLabel.grid(row=4, column=0, sticky="w", padx=(10, 10), pady=(10, 0))

        self.keyOneOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.MACRO_LIST, command=self.update_key1, dynamic_resizing=False, width=200)
        self.keyTwoOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.MACRO_LIST, command=self.update_key2, dynamic_resizing=False, width=200)
        self.keyThreeOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.MACRO_LIST, command=self.update_key3, dynamic_resizing=False, width=200)
        self.keyFourOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.MACRO_LIST, command=self.update_key4, dynamic_resizing=False, width=200)

        self.keyOneOptionMenu.grid(row=1, column=1, padx=(10,10), pady=(10, 0))
        self.keyTwoOptionMenu.grid(row=2, column=1, padx=(10,10), pady=(10, 0))
        self.keyThreeOptionMenu.grid(row=3, column=1, padx=(10,10), pady=(10, 0))
        self.keyFourOptionMenu.grid(row=4, column=1, padx=(10,10), pady=(10, 0))

        # Set default values
        self.appearanceModeMenu.set("System")
        self.keyOneOptionMenu.set('--No macro selected--')
        self.keyTwoOptionMenu.set('--No macro selected--')
        self.keyThreeOptionMenu.set('--No macro selected--')
        self.keyFourOptionMenu.set('--No macro selected--')


    def search_preset(self, event=None):
        print(self.searchBar.get())

    def run_ahk(self):
        self.create_and_run_ahk_script(App.KEY1, App.KEY2, App.KEY3, App.KEY4)

    def create_and_run_ahk_script(self, key1: str, key2: str, key3: str, key4: str):
        f = open("program-files/macro-pad.ahk", "w")            
        keys = [key1, key2, key3, key4]
        counter = 1

        # Write to newly created text file with .ahk extension
        for key in keys:
            functionKey: str = "F" + str(counter)
            # Add AutoHotKey remapping functions to text file
            match key:
                case "Google Search Selected Text":
                    f.write("{\n" + functionKey + "::\n\tSend, ^c\n\tSleep 50\n\tRun, https://www.google.com/search?q=%clipboard%\n\tReturn\n}\n\n")
                case "Open Website":
                    website: str = "https://www.ucf.edu"
                    f.write(functionKey + "::Run, " + website + "\n\n")
                case "Open Application":
                    appProcess: str = "Notepad"
                    f.write(functionKey + "::Run " + appProcess + "\n\n")
                case "Move up a Folder":
                    f.write(functionKey + "::Send !{Up}\n\n")
                case "Copy HEX color code to clipboard":
                    f.write(functionKey + "::\n{\n\tMouseGetPos, MouseX, MouseY\n\tPixelGetColor, color, %MouseX%, %MouseY%, RGB\n\tStringLower, color, color\n\tclipboard := SubStr(color, 3)\n\tReturn\n}\n\n")
                case "Open Command Prompt in current folder":
                    f.write(functionKey + "::\n{\n\tSend, !d\n\tSend,^c\n\tSleep 50\n\tRun cmd, %clipboard%\n\tReturn\n}\n\n")
                case "Run command in current folder":
                    command: str = "git status"
                    f.write(functionKey + "::\n{\n\tSend, !d\n\tSend,^c\n\tSleep 50\n\tRun cmd, %clipboard%\n\tSleep 100\n\tSend, " + command + "\n\tSleep 100\n\tSend, {Enter}\n\tReturn\n}\n\n")
                case "Open Command Prompt at a Favorite Folder":
                    folderLocation: str = "C:\\Users\\bvan5\\Desktop\\SeniorDesign"
                    f.write(functionKey + "::Run cmd, " + folderLocation + "\n\n")
                case "Run Command at a Favorite Folder":
                    folderLocation: str = "C:\\Users\\bvan5\\Desktop\\SeniorDesign"
                    command: str = "git status"
                    f.write(functionKey + '::\n{\n\tRun cmd, ' + folderLocation + '\n\tSleep 100\n\tSend, ' + command + '\n\tSleep 100\n\tSend, {Enter}\n\tReturn\n}\n\n')
                case "Open File Explorer at a Favorite Folder":
                    folderLocation: str = "C:\\Users\\bvan5\\Desktop\\SeniorDesign"
                    f.write(functionKey + "::Run " + folderLocation + "\n\n")
                case "Volume Up":
                    f.write(functionKey + "::Volume_Up\n\n")
                case "Volume Down":
                    f.write(functionKey + "::Volume_Down\n\n")
                case "Volume Mute":
                    f.write(functionKey + "::Volume_Mute\n\n")
                case "Play/Pause Media":
                    f.write(functionKey + "::Media_Play_Pause\n\n")
                case "Empty Recycle Bin":
                    f.write(functionKey + "::FileRecycleEmpty\n\n")
                case "Insert preset message":
                    message: str = "this will show up whenever the user is typing"
                    f.write(functionKey + "::Send " + message + "\n\n")

            counter = counter + 1
        
        # Save newly created .ahk file
        f.close()

        path: str = "program-files/"
        os.chdir(path)
        # Compile .ahk file into .exe using AHK's compiler
        os.popen('Ahk2Exe.exe /in "macro-pad.ahk"').read()

        # Run .exe that will remap function keys and go back to root directory
        os.popen('macro-pad.exe')
        os.chdir('..')


    def stop_ahk(self):
        os.system("taskkill /im macro-pad.exe")
    
    def update_key1(self, selectedMacro: str):
        App.KEY1 = selectedMacro

    def update_key2(self, selectedMacro: str):
        App.KEY2 = selectedMacro

    def update_key3(self, selectedMacro: str):
        App.KEY3 = selectedMacro

    def update_key4(self, selectedMacro: str):
        App.KEY4 = selectedMacro

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()