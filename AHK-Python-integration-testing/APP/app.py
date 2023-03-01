import customtkinter, os, uuid
from os.path import exists

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class CustomMacroPreset:
    def __init__(self, id: str, name: str, macroType: str, userInput1: str = None, userInput2: str = None):
        self.id = id
        self.name = name
        self.macroType = macroType
        self.userInput1 = userInput1 if userInput1 is not None else None
        self.userInput2 = userInput2 if userInput2 is not None else None

    # For testing/debug purposes, print(CustomMacroPreset)
    def __repr__(self):
        return "\n{\nid: % s\nname: % s\nmacro Type: % s\nuserInput1: % s\nuserInput2: % s\n}\n" % (self.id, self.name, self.macroType, self.userInput1, self.userInput2)

class CreateMacroWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Create New Macro Preset")
        self.geometry("400x300")

        macroType: str = ''

        # self.presetLabel = customtkinter.CTkLabel(self, text="First function key:", anchor="w")
        # self.presetLabel.pack(padx=20, pady=20)
        self.presetOptionMenu = customtkinter.CTkOptionMenu(master=self, values=App.MACRO_LIST, command=self.save_dropdown_option, dynamic_resizing=False, width=300)
        self.presetOptionMenu.pack(padx=20, pady=20)
        self.presetOptionMenu.set('--No macro selected--')
        self.presetNameEntry = customtkinter.CTkEntry(master=self, placeholder_text="Preset Name", width=300)
        self.presetNameEntry.pack(padx=20, pady=20)
        self.savePresetButton = customtkinter.CTkButton(master=self, text="Save", command=self.create_preset)
        self.savePresetButton.pack(padx=20, pady=20)

    def create_preset(self):
        macroType: str = CreateMacroWindow.macroType
        customName: str = self.presetNameEntry.get()

        if (customName == '') or (macroType == ''):
            return
        
        # If macro requires custom input, open Input dialog
        if (macroType in App.MACRO_LIST_THAT_REQUIRE_CUSTOM_INPUT):
            index = App.MACRO_LIST_THAT_REQUIRE_CUSTOM_INPUT.index(macroType)
            message = App.CUSTOM_INPUT_PLACEHOLDER_MESSAGES[index]
            customInputDialog = customtkinter.CTkInputDialog(text=message, title=(macroType + " - " + customName))
            customInput = customInputDialog.get_input()
            if (customInput != ''):
                newPreset = CustomMacroPreset(str(uuid.uuid4()), customName, CreateMacroWindow.macroType, customInput)
                App.PRESET_NAMES.append(customName)
        else:
            newPreset = CustomMacroPreset(str(uuid.uuid4()), customName, CreateMacroWindow.macroType)
            App.PRESET_NAMES.append(customName)
        
        App.PRESETS.append(newPreset)

        # Close popup
        self.destroy()

    def save_dropdown_option(self, selectedMacro: str):
        CreateMacroWindow.macroType = selectedMacro



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
    MACRO_LIST_THAT_REQUIRE_CUSTOM_INPUT: list[str] = [
        "Open Website", "Open Application", "Run command in current folder", "Open Command Prompt at a Favorite Folder",
        "Open File Explorer at a Favorite Folder", "Insert preset message"
    ]
    CUSTOM_INPUT_PLACEHOLDER_MESSAGES: list[str] = [
        "Type in a Website URL:", "Type in a Application Process (chrome.exe, notepad, etc.):", "Type in a Command (git status, cd Desktop, etc.):",
        "Type in a Folder Path Location:", "Type in a Folder Path Location:", "Type in a Template Message:"
    ]
    PRESETS: list[CustomMacroPreset] = []
    PRESET_NAMES: list[str] = ['--No macro selected--']
    KEY1: str = ''
    KEY2: str = ''
    KEY3: str = ''
    KEY4: str = ''
    KEY1_id: str = ''
    KEY2_id: str = ''
    KEY3_id: str = ''
    KEY4_id: str = ''
    debug_mode: str = "Remap to F1-F4"

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

        self.createNewMacroButton = customtkinter.CTkButton(master=self.sidebar, text="Create New Macro", command=self.open_new_macro_window)
        self.createNewMacroButton.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        self.debugModeLabel = customtkinter.CTkLabel(self.sidebar, text="Debug Mode:", anchor="w")
        self.debugModeLabel.grid(row=4, column=0, padx=(20,20), pady=(20,0))
        self.debugModeMenu = customtkinter.CTkOptionMenu(self.sidebar, values=["Remap to F1-F4", "Remap to F13-F16"], command=self.change_debug_mode)
        self.debugModeMenu.grid(row=5, column=0, padx=(20,20), pady=(10, 20))

        self.appearanceModeLabel = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearanceModeLabel.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))
        self.appearanceModeMenu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.appearanceModeMenu.grid(row=7, column=0, padx=(20, 20), pady=(10, 20))

        # -- Setup Home component --
        
        self.searchBar = customtkinter.CTkEntry(master=self.home, placeholder_text="Search Preset", width=300)
        self.searchBar.grid(row=0, column=0, padx=(12,0), pady=(12,12))
        self.searchBar.bind("<Return>", self.search_preset)

        self.searchButton = customtkinter.CTkButton(master=self.home, text="Search/Refresh", width=90, command=self.search_preset)
        self.searchButton.grid(row=0, column=1, padx=(12,0), pady=(12,12))

        self.keyOneLabel = customtkinter.CTkLabel(master=self.home, text="First function key:", anchor="w")
        self.keyTwoLabel = customtkinter.CTkLabel(master=self.home, text="Second function key:", anchor="w")
        self.keyThreeLabel = customtkinter.CTkLabel(master=self.home, text="Third function key:", anchor="w")
        self.keyFourLabel = customtkinter.CTkLabel(master=self.home, text="Fourth function key:", anchor="w")

        self.keyOneLabel.grid(row=1, column=0, sticky="w", padx=(10, 10), pady=(0, 0))
        self.keyTwoLabel.grid(row=2, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyThreeLabel.grid(row=3, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyFourLabel.grid(row=4, column=0, sticky="w", padx=(10, 10), pady=(10, 0))

        self.keyOneOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key1, dynamic_resizing=False, width=200)
        self.keyTwoOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key2, dynamic_resizing=False, width=200)
        self.keyThreeOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key3, dynamic_resizing=False, width=200)
        self.keyFourOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key4, dynamic_resizing=False, width=200)

        self.keyOneOptionMenu.grid(row=1, column=1, padx=(10,10), pady=(10, 0))
        self.keyTwoOptionMenu.grid(row=2, column=1, padx=(10,10), pady=(10, 0))
        self.keyThreeOptionMenu.grid(row=3, column=1, padx=(10,10), pady=(10, 0))
        self.keyFourOptionMenu.grid(row=4, column=1, padx=(10,10), pady=(10, 0))

        # Set default values
        self.createNewMacroWindow = None
        self.debugModeMenu.set(self.debug_mode)
        self.appearanceModeMenu.set("System")
        self.keyOneOptionMenu.set('--No macro selected--')
        self.keyTwoOptionMenu.set('--No macro selected--')
        self.keyThreeOptionMenu.set('--No macro selected--')
        self.keyFourOptionMenu.set('--No macro selected--')

    def search_preset(self, event=None):
        self.keyOneOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyTwoOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyThreeOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyFourOptionMenu.configure(values=App.PRESET_NAMES)
        # print(self.searchBar.get())
        # print(App.PRESETS)
        # print(App.PRESET_NAMES)
    
    def open_new_macro_window(self):
        self.createNewMacroWindow = CreateMacroWindow(self)

    def run_ahk(self):
        self.create_and_run_ahk_script()

    def create_and_run_ahk_script(self):
        f = open("program-files/macro-pad.ahk", "w")            
        ids = [App.KEY1_id, App.KEY2_id, App.KEY3_id, App.KEY4_id]
        if (self.debug_mode == "Remap to F1-F4"):
            counter = 1
        else:
            counter = 13

        # Write to newly created text file with .ahk extension
        for id in ids:
            macro = self.get_macro_by_id(id)
            if (macro is None):
                counter = counter + 1
                continue
            functionKey: str = "F" + str(counter)
            # Add AutoHotKey remapping functions to text file
            match macro.macroType:
                case "Google Search Selected Text":
                    f.write("{\n" + functionKey + "::\n\tSend, ^c\n\tSleep 50\n\tRun, https://www.google.com/search?q=%clipboard%\n\tReturn\n}\n\n")
                case "Open Website":
                    # website: str = "https://www.ucf.edu"
                    website: str = macro.userInput1
                    f.write(functionKey + "::Run, " + website + "\n\n")
                case "Open Application":
                    # appProcess: str = "Notepad"
                    appProcess: str = macro.userInput1
                    f.write(functionKey + "::Run " + appProcess + "\n\n")
                case "Move up a Folder":
                    f.write(functionKey + "::Send !{Up}\n\n")
                case "Copy HEX color code to clipboard":
                    f.write(functionKey + "::\n{\n\tMouseGetPos, MouseX, MouseY\n\tPixelGetColor, color, %MouseX%, %MouseY%, RGB\n\tStringLower, color, color\n\tclipboard := SubStr(color, 3)\n\tReturn\n}\n\n")
                case "Open Command Prompt in current folder":
                    f.write(functionKey + "::\n{\n\tSend, !d\n\tSend,^c\n\tSleep 50\n\tRun cmd, %clipboard%\n\tReturn\n}\n\n")
                case "Run command in current folder":
                    # command: str = "git status"
                    command: str = macro.userInput1
                    f.write(functionKey + "::\n{\n\tSend, !d\n\tSend,^c\n\tSleep 50\n\tRun cmd, %clipboard%\n\tSleep 100\n\tSend, " + command + "\n\tSleep 100\n\tSend, {Enter}\n\tReturn\n}\n\n")
                case "Open Command Prompt at a Favorite Folder":
                    # folderLocation: str = "C:\\Users\\bvan5\\Desktop\\SeniorDesign"
                    folderLocation: str = macro.userInput1
                    f.write(functionKey + "::Run cmd, " + folderLocation + "\n\n")
                case "Run Command at a Favorite Folder":
                    # folderLocation: str = "C:\\Users\\bvan5\\Desktop\\SeniorDesign"
                    # command: str = "git status"
                    folderLocation: str = macro.userInput1
                    command: str = macro.userInput2
                    f.write(functionKey + '::\n{\n\tRun cmd, ' + folderLocation + '\n\tSleep 100\n\tSend, ' + command + '\n\tSleep 100\n\tSend, {Enter}\n\tReturn\n}\n\n')
                case "Open File Explorer at a Favorite Folder":
                    # folderLocation: str = "C:\\Users\\bvan5\\Desktop\\SeniorDesign"
                    folderLocation: str = macro.userInput1
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
                    # message: str = "this will show up whenever the user is typing"
                    message: str = macro.userInput1
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

    def get_macro_by_id(self, id: str):
        for macro in App.PRESETS:
            if (id == macro.id):
                return macro
        
        return None

    def stop_ahk(self):
        os.system("taskkill /im macro-pad.exe")
    
    def update_key1(self, selectedMacro: str):
        App.KEY1 = selectedMacro
        App.KEY1_id = self.search_for_macro(selectedMacro)

    def update_key2(self, selectedMacro: str):
        App.KEY2 = selectedMacro
        App.KEY2_id = self.search_for_macro(selectedMacro)

    def update_key3(self, selectedMacro: str):
        App.KEY3 = selectedMacro
        App.KEY3_id = self.search_for_macro(selectedMacro)

    def update_key4(self, selectedMacro: str):
        App.KEY4 = selectedMacro
        App.KEY4_id = self.search_for_macro(selectedMacro)
    
    def search_for_macro(self, selectedPreset: str):
        for preset in App.PRESETS:
            if (selectedPreset == preset.name):
                return preset.id
        return ''

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_debug_mode(self, new_debug_mode: str):
        self.debug_mode = new_debug_mode

    def save_custom_presets(self, fileName: str):
        f = open(fileName, "w")

        for macro in App.PRESETS:
            f.write("{\n" + str(macro.id) + "\n" + macro.name + "\n" + macro.macroType)
            if macro.userInput1 is not None:
                f.write("\n" + macro.userInput1)
                if macro.userInput2 is not None:
                    f.write("\n" + macro.userInput2)
            
            f.write("\n},\n")
        
        f.close()

    def load_custom_presets(self, fileName: str):
        if (exists(fileName) == False):
            return

        lines: list[str] = []

        with open(fileName, 'r') as f:
            for line in f:
                lines.append(str(line).replace("\n", ""))

        counter = 0
        for line in lines:
            if (line == "{"):
                tempId = lines[counter + 1]
                tempName = lines[counter + 2]
                tempType = lines[counter + 3]

                if (lines[counter + 4] == '},'):
                    tempMacro = CustomMacroPreset(tempId, tempName, tempType)
                    App.PRESET_NAMES.append(tempName)
                    App.PRESETS.append(tempMacro)
                    counter = counter + 1
                    continue
                
                if (lines[counter + 5] == '},'):
                    userInput1 = lines[counter + 4]
                    tempMacro = CustomMacroPreset(tempId, tempName, tempType, userInput1)
                    App.PRESET_NAMES.append(tempName)
                    App.PRESETS.append(tempMacro)
                else:
                    userInput1 = lines[counter + 4]
                    userInput2 = lines[counter + 5]
                    tempMacro = CustomMacroPreset(tempId, tempName, tempType, userInput1, userInput2)
                    App.PRESET_NAMES.append(tempName)
                    App.PRESETS.append(tempMacro)
            counter = counter + 1
        
        self.keyOneOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyTwoOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyThreeOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyFourOptionMenu.configure(values=App.PRESET_NAMES)

    def on_closing(self, event=0):
        self.save_custom_presets("program-files/your-macros.txt")
        self.destroy()

    def start(self):
        self.load_custom_presets("program-files/your-macros.txt")
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()