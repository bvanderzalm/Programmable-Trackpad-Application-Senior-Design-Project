import customtkinter, os, sys

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Programmable MacroPad"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry("800x500")
        # self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-w>", self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Program Board / Run AHK",
                                                command=self.run_ahk)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Stop AHK",
                                                command=self.stop_ahk)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Select Macros:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["F1 - Google search selected text", "F2 - Open UCF site", "F3 - Open Notepad", "F4 - Move up a folder"],
                                                                       command=self.edit_macro)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)



        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="Search Preset")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_preset)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_preset)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.appearance_mode_optionemenu.set("System")

    def search_preset(self, event=None):
        print(self.entry.get())

    def run_ahk(self):
        key1 = "Google search selected text"
        key2 = "Open UCF site"
        key4 = "Open Notepad"
        key3 = "Move up a folder"

        self.create_and_run_ahk_script(key1, key2, key3, key4)

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