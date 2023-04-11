import customtkinter, os, uuid, sys, tkinter
from os.path import exists
from tkinter import messagebox

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
    
class SearchResultsWindow(customtkinter.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Search Results")
        self.geometry("1050x400")

        self.generate_table()

    def generate_table(self):
        self.resultsGrid = customtkinter.CTkScrollableFrame(master=self, width=1000, height=400)
        self.resultsGrid.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        numResults: int = App.searchResults.__len__()
        msg: str = "Showing " + str(numResults) + " of " + str(App.PRESETS.__len__()) + " Custom Presets with Search Query: "

        self.resultMessage = customtkinter.CTkLabel(master=self.resultsGrid, text=msg, anchor="w")
        self.resultMessage.grid(row=0, column=0, padx=(12,0), pady=(12,12))

        self.searchQueryLabel = customtkinter.CTkLabel(master=self.resultsGrid, text=App.searchQuery, anchor="w", 
                                                       font = customtkinter.CTkFont(size=12, weight="bold"))
        self.searchQueryLabel.grid(row=0, column=1, padx=(12,0), pady=(12,12))

        rowCounter = 1
        for index, macro in enumerate(App.searchResults):
            customNameLabel = customtkinter.CTkLabel(master=self.resultsGrid, 
                                                     text=macro.name, width=60, height=25,
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
            customNameLabel.grid(row=rowCounter, column=0, padx=30)

            macroTypeLabel = customtkinter.CTkLabel(master=self.resultsGrid, text=macro.macroType)
            macroTypeLabel.grid(row=rowCounter, column=1, padx=30)

            editButton = customtkinter.CTkButton(master=self.resultsGrid, text="Edit", 
                                                 command=lambda k=index: self.edit_macro(k))
            editButton.grid(row=rowCounter, column=2, padx=30)

            deleteButton = customtkinter.CTkButton(master=self.resultsGrid, text="Delete", 
                                                   command=lambda k=index: self.delete_macro(k), 
                                                   fg_color="red", hover_color="#800000")
            deleteButton.grid(row=rowCounter, column=3, padx=30)

            linebreak = customtkinter.CTkLabel(master=self.resultsGrid, text='____________________________________', 
                                               font = customtkinter.CTkFont(size=20, weight="bold"))
            linebreak.grid(row=(rowCounter + 1), column=0)
            rowCounter = rowCounter + 2
    
    def edit_macro(self, index: int):
        macro: CustomMacroPreset = App.searchResults[index]
        if (App.main.createNewMacroWindow is not None):
            App.main.createNewMacroWindow.destroy()
        App.main.createNewMacroWindow = CreateMacroWindow(macro)
        self.destroy()
    
    def delete_macro(self, index: int):
        self.resultsGrid.grid_forget()
        macro: CustomMacroPreset = App.searchResults[index]
        App.searchResults.pop(index)

        for index, preset in enumerate(App.PRESETS):
            if (preset.id == macro.id):
                App.PRESETS.pop(index)
        
        App.PRESET_NAMES = []
        for preset in App.PRESETS:
            App.PRESET_NAMES.append(preset.name)

        if (App.KEY1_id == macro.id):
            App.main.keyOneOptionMenu.set('--No Macro Selected--')
            App.main.update_key1('')
        
        if (App.KEY2_id == macro.id):
            App.main.keyTwoOptionMenu.set('--No Macro Selected--')
            App.main.update_key2('')

        if (App.KEY3_id == macro.id):
            App.main.keyThreeOptionMenu.set('--No Macro Selected--')
            App.main.update_key3('')
        
        if (App.KEY4_id == macro.id):
            App.main.keyFourOptionMenu.set('--No Macro Selected--')
            App.main.update_key4('')
                
        App.main.refresh_dropdowns()
        self.generate_table()

class CreateMacroWindow(customtkinter.CTkToplevel):
    macroType: str = ''

    def __init__(self, macroToEdit: CustomMacroPreset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        CreateMacroWindow.macroType = ''
        self.macroToEdit = macroToEdit

        self.presetOptionMenu = customtkinter.CTkOptionMenu(master=self, values=App.MACRO_LIST, command=self.save_dropdown_option, dynamic_resizing=False, width=300)
        self.presetOptionMenu.pack(padx=20, pady=20)
        self.presetOptionMenu.set('--No Macro Selected--')
        self.presetNameEntry = customtkinter.CTkEntry(master=self, width=300)
        self.presetNameEntry.pack(padx=20, pady=20)
        self.presetNameEntry.bind("<Return>", self.keybind_create_preset)
        self.savePresetButton = customtkinter.CTkButton(master=self, text="Save", command=self.create_preset)
        self.savePresetButton.pack(padx=20, pady=20)

        if (self.macroToEdit is None):
            self.title("Create New Macro Preset")
            self.presetOptionMenu.set('--No Macro Selected--')
            self.presetNameEntry.configure(placeholder_text="Preset Name")
        
        else:
            self.title("Edit " + self.macroToEdit.name)
            self.save_dropdown_option(self.macroToEdit.macroType)
            self.presetOptionMenu.set(self.macroToEdit.macroType)
            entryText = tkinter.StringVar()
            entryText.set(self.macroToEdit.name)
            self.presetNameEntry.configure(textvariable=entryText)
            
    def keybind_create_preset(self, text):
        self.create_preset()

    def create_preset(self):
        macroType: str = CreateMacroWindow.macroType
        customName: str = self.presetNameEntry.get()

        if (customName == '') or (macroType == ''):
            messagebox.showerror("Error", "Please fill out the entire form")
            return

        duplicateName: bool = customName in App.PRESET_NAMES
        if ((duplicateName and self.macroToEdit is None) or (duplicateName and self.macroToEdit.macroType != macroType)):
            msg: str = 'The name "' + customName + '" is already in use, please type another name'
            messagebox.showerror("Error", msg)
            return
        
        # If macro requires custom input, open Input dialog
        if (macroType in App.MACRO_LIST_THAT_REQUIRE_CUSTOM_INPUT):
            index = App.MACRO_LIST_THAT_REQUIRE_CUSTOM_INPUT.index(macroType)
            message = App.CUSTOM_INPUT_PLACEHOLDER_MESSAGES[index]
            prePopulatedInput = ""
            if (self.macroToEdit is not None and macroType == self.macroToEdit.macroType):
                prePopulatedInput = self.macroToEdit.userInput1

            customInputDialog = customtkinter.CTkInputDialog(text=message, title=(macroType + " - " + customName), 
                                                             pre_populated_value=prePopulatedInput)
            customInput = customInputDialog.get_input()
            if (customInput != None and customInput != ''):
                if (self.macroToEdit is None):
                    self.add_new_macro(customName, macroType, customInput)
                else:
                    self.edit_existing_macro(self.macroToEdit, customName, macroType, customInput)
        # No custom input, only name and macroType
        else:
            if (self.macroToEdit is None):
                self.add_new_macro(customName, macroType)
            else:
                self.edit_existing_macro(self.macroToEdit, customName, macroType)

        # Close popup
        self.destroy()

    def save_dropdown_option(self, selectedMacro: str):
        CreateMacroWindow.macroType = selectedMacro

    def add_new_macro(self, customName: str, macroType: str, customInput: str = None):
        newPreset = CustomMacroPreset(str(uuid.uuid4()), customName, macroType, customInput)
        App.PRESET_NAMES.append(customName)
        App.PRESETS.append(newPreset)
        App.main.refresh_dropdowns()

    def edit_existing_macro(self, macro: CustomMacroPreset, customName: str, macroType: str, customInput: str = None):
        index = self.find_macro_index(macro)
        if (index != -1):
            App.PRESETS[index].name = customName
            App.PRESETS[index].macroType = macroType
            if (customInput is not None):
                App.PRESETS[index].userInput1 = customInput
            self.update_preset_name_list(macro)
            App.main.refresh_dropdowns()
    
    def find_macro_index(self, macro: CustomMacroPreset):
        for index, preset in enumerate(App.PRESETS):
            if (preset.id == macro.id):
                return index
        
        return -1

    def update_preset_name_list(self, macro: CustomMacroPreset):
        App.PRESET_NAMES = []
        for preset in App.PRESETS:
            App.PRESET_NAMES.append(preset.name)

        if (App.KEY1_id == macro.id):
            App.main.keyOneOptionMenu.set(macro.name)
            App.KEY1_id = macro.id
        
        if (App.KEY2_id == macro.id):
            App.main.keyTwoOptionMenu.set(macro.name)
            App.KEY2_id = macro.id

        if (App.KEY3_id == macro.id):
            App.main.keyThreeOptionMenu.set(macro.name)
            App.KEY3_id = macro.id
        
        if (App.KEY4_id == macro.id):
            App.main.keyFourOptionMenu.set(macro.name)
            App.KEY4_id = macro.id
        

class CreateRotaryEncoderMacroWindow(customtkinter.CTkToplevel):
    macroType: str = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Create New Rotary Encoder Macro Preset")
        self.geometry("275x300")
        CreateRotaryEncoderMacroWindow.macroType = ''

        self.presetLabel = customtkinter.CTkLabel(self, text="Create New Rotary Encoder Macro Preset:", anchor="w")
        self.presetLabel.pack(padx=20, pady=20)
        self.presetOptionMenu = customtkinter.CTkOptionMenu(master=self, values=App.ROTARY_ENCODER_MACRO_LIST, command=self.save_dropdown_option, dynamic_resizing=False, width=300)
        self.presetOptionMenu.pack(padx=20, pady=20)
        self.presetOptionMenu.set('--No Encoder Macro Selected--')
        self.presetNameEntry = customtkinter.CTkEntry(master=self, placeholder_text="Encoder Preset Name", width=300)
        self.presetNameEntry.bind("<Return>", self.keybind_create_preset)
        self.presetNameEntry.pack(padx=20, pady=20)
        self.savePresetButton = customtkinter.CTkButton(master=self, text="Save", command=self.create_preset)
        self.savePresetButton.pack(padx=20, pady=20)

    def keybind_create_preset(self, text):
        self.create_preset()

    def create_preset(self):
        macroType: str = CreateRotaryEncoderMacroWindow.macroType
        customName: str = self.presetNameEntry.get()

        if (customName == '') or (macroType == ''):
            messagebox.showerror("Error", "Please fill out the entire form")
            return

        if (customName in App.ENCODER_PRESETS_NAMES):
            msg: str = 'The name "' + customName + '" is already in use, please type another name'
            messagebox.showerror("Error", msg)
            return
                
        newPreset = CustomMacroPreset(str(uuid.uuid4()), customName, macroType)
        App.ENCODER_PRESETS_NAMES.append(customName)
        App.ENCODER_PRESETS.append(newPreset)
        App.main.refresh_dropdowns()

        # Close popup
        self.destroy()

    def save_dropdown_option(self, selectedMacro: str):
        CreateRotaryEncoderMacroWindow.macroType = selectedMacro

class App(customtkinter.CTk):

    APP_NAME = "Programmable Trackpad"
    WIDTH = 800
    HEIGHT = 500
    main = customtkinter.CTk()
    searchQuery: str = ''
    searchResults: list[CustomMacroPreset] = []
    ROTARY_ENCODER_MACRO_LIST: list[str] = [
        "Volume Control", "Mouse Scroll", 
    ]
    MACRO_LIST: list[str] = [
        "Google Search Selected Text", "Copy HEX color code to clipboard", "Open Website", "Open Application", "Volume Up", "Volume Down", "Volume Mute", "Play/Pause Media",
        "Media Next", "Media Previous", "Browser Back", "Browser Forward", "Browser Refresh", "Insert preset message", "Empty Recycle Bin", "Open File Explorer at a Favorite Folder",
        "Open Command Prompt in current folder", "Run command in current folder",
        "Open Command Prompt at a Favorite Folder", 
    ]
    MACRO_LIST_THAT_REQUIRE_CUSTOM_INPUT: list[str] = [
        "Open Website", "Open Application", "Run command in current folder", "Open Command Prompt at a Favorite Folder",
        "Open File Explorer at a Favorite Folder", "Insert preset message"
    ]
    CUSTOM_INPUT_PLACEHOLDER_MESSAGES: list[str] = [
        "Type in a Website URL in https format:", "Type in a Application Process (chrome.exe, notepad, etc.):", "Type in a Command (git status, cd Desktop, etc.):",
        "Type in a Folder Path Location:", "Type in a Folder Path Location:", "Type in a Template Message:"
    ]
    PRESETS: list[CustomMacroPreset] = []
    PRESET_NAMES: list[str] = ['--No Macro Selected--']
    ENCODER_PRESETS: list[CustomMacroPreset] = []
    ENCODER_PRESETS_NAMES: list[str] = ['--No Encoder Macro Selected--']
    KEY1_id: str = ''
    KEY2_id: str = ''
    KEY3_id: str = ''
    KEY4_id: str = ''
    ENCODER1_id: str = ''
    ENCODER2_id: str = ''
    ENCODER3_id: str = ''
    debug_mode: str = "Remap to F1-F4"
    appearance_mode: str = "System"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- Setup main frame --
        self.title(App.APP_NAME)
        self.geometry("800x550")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = customtkinter.CTkFrame(master=self, width=150, corner_radius=0)
        self.sidebar.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.home = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.home.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # -- Setup Sidebar component --
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.runAhkButton = customtkinter.CTkButton(master=self.sidebar, text="Start Running Macros", command=self.run_ahk)
        self.runAhkButton.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.stopAhkButton = customtkinter.CTkButton(master=self.sidebar,text="Stop Running Macros", command=self.stop_ahk)
        self.stopAhkButton.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.createNewMacroButton = customtkinter.CTkButton(master=self.sidebar, text="Create New Macro", command=self.open_new_macro_window)
        self.createNewMacroButton.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        self.createNewRotaryEncoderMacroButton = customtkinter.CTkButton(master=self.sidebar, text="Create New Rotary Encoder Macro", command=self.open_new_rotary_encoder_macro_window)
        self.createNewRotaryEncoderMacroButton.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)

        # self.debugModeLabel = customtkinter.CTkLabel(self.sidebar, text="Debug Mode:", anchor="w")
        # self.debugModeLabel.grid(row=4, column=0, padx=(20,20), pady=(20,0))
        # self.debugModeMenu = customtkinter.CTkOptionMenu(self.sidebar, values=["Remap to F1-F4", "Remap to F13-F16"], command=self.change_debug_mode)
        # self.debugModeMenu.grid(row=5, column=0, padx=(20,20), pady=(10, 20))

        self.appearanceModeLabel = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearanceModeLabel.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearanceModeMenu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.appearanceModeMenu.grid(row=7, column=0, padx=(20, 20), pady=(10, 20))

        # -- Setup Home component --
        
        self.searchBar = customtkinter.CTkEntry(master=self.home, placeholder_text="Search Preset", width=300)
        self.searchBar.grid(row=0, column=0, padx=(12,0), pady=(12,12))
        self.searchBar.bind("<Return>", self.search_preset)

        self.searchButton = customtkinter.CTkButton(master=self.home, text="Search", width=90, command=self.search_preset)
        self.searchButton.grid(row=0, column=1, padx=(12,0), pady=(12,12))

        # Button Keys
        self.buttonLabel = customtkinter.CTkLabel(master=self.home, text="-- BUTTONS --", anchor="w")
        self.buttonLabel.grid(row=1, column=0, sticky="w", padx=(200, 10), pady=(30,20))

        self.keyOneLabel = customtkinter.CTkLabel(master=self.home, text="First Function key:", anchor="w")
        self.keyTwoLabel = customtkinter.CTkLabel(master=self.home, text="Second Function key:", anchor="w")
        self.keyThreeLabel = customtkinter.CTkLabel(master=self.home, text="Third Function key:", anchor="w")
        self.keyFourLabel = customtkinter.CTkLabel(master=self.home, text="Fourth Function key:", anchor="w")

        self.keyOneLabel.grid(row=2, column=0, sticky="w", padx=(10, 10), pady=(0, 0))
        self.keyTwoLabel.grid(row=3, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyThreeLabel.grid(row=4, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.keyFourLabel.grid(row=5, column=0, sticky="w", padx=(10, 10), pady=(10, 0))

        self.keyOneOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key1, dynamic_resizing=False, width=200)
        self.keyTwoOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key2, dynamic_resizing=False, width=200)
        self.keyThreeOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key3, dynamic_resizing=False, width=200)
        self.keyFourOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.PRESET_NAMES, command=self.update_key4, dynamic_resizing=False, width=200)

        self.keyOneOptionMenu.grid(row=2, column=1, padx=(10,10), pady=(10, 0))
        self.keyTwoOptionMenu.grid(row=3, column=1, padx=(10,10), pady=(10, 0))
        self.keyThreeOptionMenu.grid(row=4, column=1, padx=(10,10), pady=(10, 0))
        self.keyFourOptionMenu.grid(row=5, column=1, padx=(10,10), pady=(10, 0))

        # Rotary Encoders
        self.encoderLabel = customtkinter.CTkLabel(master=self.home, text="-- ENCODERS --", anchor="w")
        self.encoderLabel.grid(row=6, column=0, sticky="w", padx=(200, 10), pady=(30,20))

        self.encoderOneLabel = customtkinter.CTkLabel(master=self.home, text="First Encoder:", anchor="w")
        self.encoderTwoLabel = customtkinter.CTkLabel(master=self.home, text="Second Encoder:", anchor="w")
        self.encoderThreeLabel = customtkinter.CTkLabel(master=self.home, text="Third Encoder:", anchor="w")

        self.encoderOneLabel.grid(row=7, column=0, sticky="w", padx=(10, 10), pady=(0, 0))
        self.encoderTwoLabel.grid(row=8, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.encoderThreeLabel.grid(row=9, column=0, sticky="w", padx=(10, 10), pady=(10, 0))

        self.encoderOneOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.ENCODER_PRESETS_NAMES, command=self.update_enc_key1, dynamic_resizing=False, width=210)
        self.encoderTwoOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.ENCODER_PRESETS_NAMES, command=self.update_enc_key2, dynamic_resizing=False, width=210)
        self.encoderThreeOptionMenu = customtkinter.CTkOptionMenu(master=self.home, values=App.ENCODER_PRESETS_NAMES, command=self.update_enc_key3, dynamic_resizing=False, width=210)

        self.encoderOneOptionMenu.grid(row=7, column=1, padx=(10,10), pady=(10, 0))
        self.encoderTwoOptionMenu.grid(row=8, column=1, padx=(10,10), pady=(10, 0))
        self.encoderThreeOptionMenu.grid(row=9, column=1, padx=(10,10), pady=(10, 0))

        # Set default values
        self.createNewMacroWindow = None
        self.createNewEncoderMacroWindow = None
        self.searchWindow = None
        # self.debugModeMenu.set(self.debug_mode)
        self.appearanceModeMenu.set(self.appearance_mode)
        self.keyOneOptionMenu.set('--No Macro Selected--')
        self.keyTwoOptionMenu.set('--No Macro Selected--')
        self.keyThreeOptionMenu.set('--No Macro Selected--')
        self.keyFourOptionMenu.set('--No Macro Selected--')
        self.encoderOneOptionMenu.set('--No Encoder Macro Selected--')
        self.encoderTwoOptionMenu.set('--No Encoder Macro Selected--')
        self.encoderThreeOptionMenu.set('--No Encoder Macro Selected--')

    def search_preset(self, event=None):
        if self.searchWindow is not None:
            self.searchWindow.destroy()
        App.searchQuery = self.searchBar.get().lower()
        App.searchResults = self.get_macros_by_name(App.searchQuery)
        App.main = self
        self.searchWindow = SearchResultsWindow(self)

    def get_macros_by_name(self, searchQuery: str):
        searchResults: list[CustomMacroPreset] = []

        for macro in App.PRESETS:
            if (macro.name.lower().find(searchQuery) != -1 or macro.macroType.lower().find(searchQuery) != -1):
                searchResults.append(macro)

        return searchResults

    def refresh_dropdowns(self):
        self.keyOneOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyTwoOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyThreeOptionMenu.configure(values=App.PRESET_NAMES)
        self.keyFourOptionMenu.configure(values=App.PRESET_NAMES)

        self.encoderOneOptionMenu.configure(values=App.ENCODER_PRESETS_NAMES)
        self.encoderTwoOptionMenu.configure(values=App.ENCODER_PRESETS_NAMES)
        self.encoderThreeOptionMenu.configure(values=App.ENCODER_PRESETS_NAMES)
    
    def open_new_macro_window(self):
        if (self.createNewMacroWindow is not None):
            self.createNewMacroWindow.destroy()

        App.main = self
        self.createNewMacroWindow = CreateMacroWindow(None)
    
    def open_new_rotary_encoder_macro_window(self):
        if (self.createNewEncoderMacroWindow is not None):
            self.createNewEncoderMacroWindow.destroy()

        App.main = self
        self.createNewEncoderMacroWindow = CreateRotaryEncoderMacroWindow(self)

    def run_ahk(self):
        self.stop_ahk()
        self.create_ahk_script()
        self.compile_ahk()

    def create_ahk_script(self):
        f = open("program-files/macro-pad.ahk", "w")
        f.write("#MaxHotkeysPerInterval 400\n\n")

        ids = [App.KEY1_id, App.KEY2_id, App.KEY3_id, App.KEY4_id]
        # if (self.debug_mode == "Remap to F1-F4"):
        #     counter = 1
        #     encCounter = 5
        # else:
        counter = 13
        encCounter = 17

        # Write to newly created text file with .ahk extension
        for id in ids:
            macro = self.get_macro_by_id(id, False)
            if (macro is None):
                counter = counter + 1
                continue
            functionKey: str = "F" + str(counter)
            # Add AutoHotKey remapping functions to text file
            match macro.macroType:
                case "Google Search Selected Text":
                    f.write("{\n" + functionKey + "::\n\tSend, ^c\n\tSleep 50\n\tRun, https://www.google.com/search?q=%clipboard%\n\tReturn\n}\n\n")
                case "Open Website":
                    website: str = macro.userInput1
                    f.write(functionKey + "::Run, " + website + "\n\n")
                case "Open Application":
                    appProcess: str = macro.userInput1
                    f.write(functionKey + "::Run " + appProcess + "\n\n")
                case "Move up a Folder":
                    f.write(functionKey + "::Send !{Up}\n\n")
                case "Copy HEX color code to clipboard":
                    f.write(functionKey + "::\n{\n\tMouseGetPos, MouseX, MouseY\n\tPixelGetColor, color, %MouseX%, %MouseY%, RGB\n\tStringLower, color, color\n\tclipboard := SubStr(color, 3)\n\tReturn\n}\n\n")
                case "Open Command Prompt in current folder":
                    f.write(functionKey + "::\n{\n\tSend, !d\n\tSend,^c\n\tSleep 50\n\tRun cmd, %clipboard%\n\tReturn\n}\n\n")
                case "Run command in current folder":
                    command: str = macro.userInput1
                    f.write(functionKey + "::\n{\n\tSend, !d\n\tSend,^c\n\tSleep 50\n\tRun cmd, %clipboard%\n\tSleep 100\n\tSend, " + command + "\n\tSleep 100\n\tSend, {Enter}\n\tReturn\n}\n\n")
                case "Open Command Prompt at a Favorite Folder":
                    folderLocation: str = macro.userInput1
                    f.write(functionKey + "::Run cmd, " + folderLocation + "\n\n")
                # case "Run Command at a Favorite Folder":
                #     folderLocation: str = macro.userInput1
                #     command: str = macro.userInput2
                #     f.write(functionKey + '::\n{\n\tRun cmd, ' + folderLocation + '\n\tSleep 100\n\tSend, ' + command + '\n\tSleep 100\n\tSend, {Enter}\n\tReturn\n}\n\n')
                case "Open File Explorer at a Favorite Folder":
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
                    message: str = macro.userInput1
                    f.write(functionKey + "::Send " + message + "\n\n")
                case "Media Next":
                    f.write(functionKey + "::Media_Next\n\n")
                case "Media Previous":
                    f.write(functionKey + "::Media_Prev\n\n")
                case "Browser Back":
                    f.write(functionKey + "::Browser_Back\n\n")
                case "Browser Forward":
                    f.write(functionKey + "::Browser_Forward\n\n")
                case "Browser Refresh":
                    f.write(functionKey + "::Browser_Refresh\n\n")

            counter = counter + 1

        encoderIds = [App.ENCODER1_id, App.ENCODER2_id, App.ENCODER3_id]

        # Write and remap function keys to same .ahk file
        for id in encoderIds:
            macro = self.get_macro_by_id(id, True)
            if (macro is None):
                encCounter = encCounter + 2
                continue
            functionKey: str = "F" + str(encCounter)
            nextKey: str = "F" + str(encCounter + 1)

            match macro.macroType:
                case "Volume Control":
                    f.write(functionKey + "::Volume_Down\n\n")
                    f.write(nextKey + "::Volume_Up\n\n")
                case "Mouse Scroll":
                    f.write(functionKey + "::WheelUp\n\n")
                    f.write(nextKey + "::WheelDown\n\n")
            
            encCounter = encCounter + 2
        
        # Save newly created .ahk file
        f.close()
    
    def compile_ahk(self):
        path: str = "program-files/"
        os.chdir(path)
        # Compile .ahk file into .exe using AHK's compiler
        os.popen('Ahk2Exe.exe /in "macro-pad.ahk"').read()

        # Run .exe that will remap function keys and go back to root directory
        os.popen('macro-pad.exe')
        os.chdir('..')


    def get_macro_by_id(self, id: str, encoder: bool):
        if (encoder == False):
            for macro in App.PRESETS:
                if (id == macro.id):
                    return macro
                
        elif (encoder == True):
            for macro in App.ENCODER_PRESETS:
                if (id == macro.id):
                    return macro
        
        return None

    def stop_ahk(self):
        os.system("taskkill /im macro-pad.exe")
    
    def update_key1(self, selectedMacro: str):
        App.KEY1_id = self.search_for_macro(selectedMacro)

    def update_key2(self, selectedMacro: str):
        App.KEY2_id = self.search_for_macro(selectedMacro)

    def update_key3(self, selectedMacro: str):
        App.KEY3_id = self.search_for_macro(selectedMacro)

    def update_key4(self, selectedMacro: str):
        App.KEY4_id = self.search_for_macro(selectedMacro)

    def search_for_macro(self, selectedPreset: str):
        for preset in App.PRESETS:
            if (selectedPreset == preset.name):
                return preset.id
        return ''

    def update_enc_key1(self, selectedMacro: str):
        App.ENCODER1_id = self.search_for_encoder_macro(selectedMacro)

    def update_enc_key2(self, selectedMacro: str):
        App.ENCODER2_id = self.search_for_encoder_macro(selectedMacro)

    def update_enc_key3(self, selectedMacro: str):
        App.ENCODER3_id = self.search_for_encoder_macro(selectedMacro)

    def search_for_encoder_macro(self, selectedPreset: str):
        for preset in App.ENCODER_PRESETS:
            if (selectedPreset == preset.name):
                return preset.id
        return ''

    def change_appearance_mode(self, new_appearance_mode: str):
        self.appearance_mode = new_appearance_mode
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_debug_mode(self, new_debug_mode: str):
        self.debug_mode = new_debug_mode

    def save_user_settings(self, fileName: str):
        f = open(fileName, "w")

        ids = [App.KEY1_id, App.KEY2_id, App.KEY3_id, App.KEY4_id, App.ENCODER1_id, App.ENCODER2_id, App.ENCODER3_id]

        counter = 0
        encoder = False
        for id in ids:
            if (counter >= 4):
                encoder = True

            macro = self.get_macro_by_id(id, encoder)
            if (macro is None):
                f.write("None\n")
            else:
                f.write(macro.id + "\n")
            
            counter = counter + 1
        
        f.write(self.appearance_mode + "\n")
        
        f.close()

    def save_custom_presets(self, fileName: str, encoder: bool):
        f = open(fileName, "w")

        if (encoder == False):
            for macro in App.PRESETS:
                f.write("{\n" + str(macro.id) + "\n" + macro.name + "\n" + macro.macroType)
                if macro.userInput1 is not None:
                    f.write("\n" + macro.userInput1)
                    if macro.userInput2 is not None:
                        f.write("\n" + macro.userInput2)
                
                f.write("\n},\n")

        elif (encoder == True):    
            for macro in App.ENCODER_PRESETS:
                f.write("{\n" + str(macro.id) + "\n" + macro.name + "\n" + macro.macroType + "\n},\n")
        
        f.close()
    
    def load_user_settings(self, fileName: str):
        # Avoid reading a file that doesn't exist
        if (exists(fileName) == False):
            return
        
        # Read text file
        lines: list[str] = []
        with open(fileName, 'r') as f:
            for line in f:
                lines.append(str(line).replace("\n", ""))

        # Set Ids and appearance mode
        if (lines[0] != 'None'):
            App.KEY1_id = lines[0]
        if (lines[1] != 'None'):
            App.KEY2_id = lines[1]
        if (lines[2] != 'None'):
            App.KEY3_id = lines[2]
        if (lines[3] != 'None'):
            App.KEY4_id = lines[3]

        if (lines[4] != 'None'):
            App.ENCODER1_id = lines[4]
        if (lines[5] != 'None'):
            App.ENCODER2_id = lines[5]
        if (lines[6] != 'None'):
            App.ENCODER3_id = lines[6]

        self.change_appearance_mode(lines[7])
        self.appearanceModeMenu.set(self.appearance_mode)

        # Prepopulate macro dropdowns
        macro = self.get_macro_by_id(App.KEY1_id, False)
        if (macro is not None):
            self.keyOneOptionMenu.set(macro.name)
        
        macro = self.get_macro_by_id(App.KEY2_id, False)
        if (macro is not None):
            self.keyTwoOptionMenu.set(macro.name)

        macro = self.get_macro_by_id(App.KEY3_id, False)
        if (macro is not None):
            self.keyThreeOptionMenu.set(macro.name)

        macro = self.get_macro_by_id(App.KEY4_id, False)
        if (macro is not None):
            self.keyFourOptionMenu.set(macro.name)

        macro = self.get_macro_by_id(App.ENCODER1_id, True)
        if (macro is not None):
            self.encoderOneOptionMenu.set(macro.name)

        macro = self.get_macro_by_id(App.ENCODER2_id, True)
        if (macro is not None):
            self.encoderTwoOptionMenu.set(macro.name)

        macro = self.get_macro_by_id(App.ENCODER3_id, True)
        if (macro is not None):
            self.encoderThreeOptionMenu.set(macro.name)                        

    def load_custom_presets(self, fileName: str, encoder: bool):
        # Avoid reading a file that doesn't exist
        if (exists(fileName) == False):
            return
        
        # Read text file
        lines: list[str] = []
        with open(fileName, 'r') as f:
            for line in f:
                lines.append(str(line).replace("\n", ""))
        
        # Interpret text file and store macros into Object array 
        if (encoder == False):
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
        
        elif (encoder == True):
            counter = 0
            for line in lines:
                if (line == "{"):
                    id = lines[counter + 1]
                    name = lines[counter + 2]
                    macroType = lines[counter + 3]
                    macro = CustomMacroPreset(id, name, macroType)
                    App.ENCODER_PRESETS_NAMES.append(name)
                    App.ENCODER_PRESETS.append(macro)
                counter = counter + 1
            
            self.encoderOneOptionMenu.configure(values=App.ENCODER_PRESETS_NAMES)
            self.encoderTwoOptionMenu.configure(values=App.ENCODER_PRESETS_NAMES)
            self.encoderThreeOptionMenu.configure(values=App.ENCODER_PRESETS_NAMES)
    
    def on_closing(self, event=0):
        self.save_custom_presets("program-files/your-macros.txt", False)
        self.save_custom_presets("program-files/encoder-macros.txt", True)
        self.save_user_settings("program-files/user-settings.txt")
        # self.destroy()
        sys.exit()

    def start(self):
        self.load_custom_presets("program-files/your-macros.txt", False)
        self.load_custom_presets("program-files/encoder-macros.txt", True)
        self.load_user_settings("program-files/user-settings.txt")
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()