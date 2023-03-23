# Programmable Trackpad
Senior Design UCF Spring 2023 - Group 18

# Build 1.1
Features
* Users can now create presets for Encoder Macros only. Users can only select a few macros for the encoders that might make sense for a button but not for a rotary encoder.
* Encoder macros are dynamically written to .AHK file which take up Two Function Keys (Ex: F17 and F18 would be one Volume Control Preset)
* Users current SELECTED presets are now remembered on restart of the app. Details: Added user settings file. User's currently SELECTED presets are now written to and read from this file as well as the app's last appearance mode

Improvements
* Updated "Program Board/Run AHK" and "Stop AHK" buttons to "Start Running Macros" and "Stop Running Macros" respectively
* Styling changes
* Overall code improvement and cleanup

Bug Fixes
* Fixed issue on Create Macro Window popup where the cancel button would still add a preset to the list
* Fixed issue on Create Macro Window popup where a user could create a macro with no settings

# Build 1.0
Application build used for Midterm Demo

Features
* Added ability for custom user input for macros (before it was static and now there are new windows requiring user input)
* On exit of the application your macro list is saved to a file and that file is read on initial load
