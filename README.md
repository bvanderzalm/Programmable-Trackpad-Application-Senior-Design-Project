# Programmable Trackpad
Senior Design UCF Spring 2023 - Group 18 - Taylor Barnes (CpE), Jonah Halili (CpE), Brian Modica (CpE), Bradley Vanderzalm (CpE)

https://programmabletrackpad-group18.web.app/

<em>The programmable trackpad is a device that assists the productivity of PC users by implementing shortcut macro keys and rotary encoders in a trackpad device which serves as a replacement for a programmable mouse. This device gives users a method for performing common actions and opening frequently-used applications with a single button press. Users can program these shortcuts themselves with a simple computer application that requires no specialized knowledge. Now, PC users who prefer a trackpad can take advantage of the same convenience one would receive from a programmable mouse.</em>

## Build 1.2.1 (Improvements and Bug Fix)
Improvements
* "Start Running Macros" button now doesn't give a warning message when attempting to run it with an existing .ahk script running. (Fix: call Stop AHK before Run AHK)
* Removed run command at favorite folder macro due to it needing two custom inputs from the user which they could not supply with the given GUI
* Cleaned up GUI grid and layout
* Removed Debug dropdown and debug console window on final app.exe file
* Added error popup messages on existing return checks in Create Encoder Macro Window
* Adjusted instructions label for Create Website macro URL form input

Bug Fix
* Fixed issue with Media Previous macro not showing up on .ahk file

# Build 1.2.0
Features
* Added a search results window triggered by the search bar and/or search button
* Implemented Edit and Delete functionality inside Search Results window
* Added dynamic, scrollable table inside search results window where deleting a macro will update the table without opening and closing the window
* Improved CreateMacroWindow class to have edit functionality. Optional macro can be passed in where if so, it will pre-populate all forms where you can then make edits

Improvements
* Anytime the user creates, edits, or deletes a macro the dropdowns will be updated automatically
* Added error popups in CreateMacroWindow if user try to create a blank macro or create a macro with a name that already exists
* Upgraded tkinter UI library to latest version
* Overall code improvement and cleanup

## Build 1.1.2 (Improvement)
Improvement
* User no longer has to click the refresh button to see their newly created macros in the home screen dropdowns. Now whenever they finish creating a macro and the popup window closes, the dropdowns are automatically refreshed

## Build 1.1.1 (HotFix)
Bug Fixes
* Increased the amount of hotkeys that can occur within an interval (about 2 seconds) to 400 instead of 71. An warning popup would occur when using the rotary encoder macros very quickly

# Build 1.1.0
Features
* Users can now create presets for Encoder Macros only. Users can only select a few macros for the encoders that might make sense for a button but not for a rotary encoder
* Encoder macros are dynamically written to .AHK file which take up Two Function Keys (Ex: F17 and F18 would be one Volume Control Preset)
* Users current SELECTED presets are now remembered on restart of the app. Details: Added user settings file. User's currently SELECTED presets are now written to and read from this file as well as the app's last appearance mode

Improvements
* Updated "Program Board/Run AHK" and "Stop AHK" buttons to "Start Running Macros" and "Stop Running Macros" respectively
* Styling changes
* Overall code improvement and cleanup

Bug Fixes
* Fixed issue on Create Macro Window popup where the cancel button would still add a preset to the list
* Fixed issue on Create Macro Window popup where a user could create a macro with no settings

# Build 1.0.0
--Build used for Midterm Demo--

Features
* Added ability for custom user input for macros (before it was static and now there are new windows requiring user input)
* On exit of the application your macro list is saved to a file and that file is read on initial load
