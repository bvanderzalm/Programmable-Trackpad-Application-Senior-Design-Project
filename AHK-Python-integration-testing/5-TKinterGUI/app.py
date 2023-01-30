import customtkinter, os

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Programmable MacroPad"
    WIDTH = 800
    HEIGHT = 500
    MACRO_LIST: list[str] = ["Google search selected text", "Open UCF site", "Open Notepad", "Move up a folder"]
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

        self.macro_label = customtkinter.CTkLabel(self.sidebar, text="Select Macros:", anchor="w")
        self.macro_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.macro_option_menu = customtkinter.CTkOptionMenu(self.sidebar, values=["F1 - Google search selected text", "F2 - Open UCF site", "F3 - Open Notepad", "F4 - Move up a folder"],
                                                                       command=self.edit_macro)
        self.macro_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearanceModeLabel = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearanceModeLabel.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearanceModeMenu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.appearanceModeMenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # -- Setup Home component --

        self.searchBar = customtkinter.CTkEntry(master=self.home, placeholder_text="Search Preset", width=300)
        self.searchBar.grid(row=0, column=0, sticky="we", padx=(12,0), pady=(12,12))
        self.searchBar.bind("<Return>", self.search_preset)

        self.searchButton = customtkinter.CTkButton(master=self.home, text="Search", width=90, command=self.search_preset)
        self.searchButton.grid(row=0, column=1, sticky="w", padx=(12,0), pady=(12,12))

        self.keyOneLabel = customtkinter.CTkLabel(self.home, text="First function key:", anchor="w")
        self.keyTwoLabel = customtkinter.CTkLabel(self.home, text="Second function key:", anchor="w")
        self.keyThreeLabel = customtkinter.CTkLabel(self.home, text="Third function key:", anchor="w")
        self.keyFourLabel = customtkinter.CTkLabel(self.home, text="Fourth function key:", anchor="w")

        self.keyOneLabel.grid(row=1, column=0, sticky="w", padx=(10, 10), pady=(0, 0))
        self.keyTwoLabel.grid(row=2, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyThreeLabel.grid(row=3, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyFourLabel.grid(row=4, column=0, sticky="w", padx=(10, 10), pady=(10, 0))

        self.keyOneOptionMenu = customtkinter.CTkOptionMenu(self.home, values=App.MACRO_LIST, command=self.update_key1)
        self.keyTwoOptionMenu = customtkinter.CTkOptionMenu(self.home, values=App.MACRO_LIST, command=self.update_key2)
        self.keyThreeOptionMenu = customtkinter.CTkOptionMenu(self.home, values=App.MACRO_LIST, command=self.update_key3)
        self.keyFourOptionMenu = customtkinter.CTkOptionMenu(self.home, values=App.MACRO_LIST, command=self.update_key4)

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
                case "Google search selected text":
                    f.write("{\n" + functionKey + "::\n\tSend, ^c\n\tSleep 50\n\tRun, https://www.google.com/search?q=%clipboard%\n\tReturn\n}\n\n")
                case "Open UCF site":
                    f.write(functionKey + '::Run, Chrome.exe "https://www.ucf.edu"\n\n')
                case "Open Notepad":
                    f.write(functionKey + "::Run Notepad\n\n")
                case "Move up a folder":
                    f.write(functionKey + "::Send !{Up}\n\n")
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

    def edit_macro(self, macro: str):
        if macro == "F1 - Google search selected text":
            print('Edit F1 Macro')
        elif macro == "F2 - Open UCF site":
            print('Edit F2 Macro')
        elif macro == "F3 - Open Notepad":
            print('Edit F3 Macro')
        elif macro == "F4 - Move up a folder":
            print('Edit F4 Macro')

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()