# Build 1.2.0
Features
* Added a search results window triggered by the search bar and/or search button
* Implemented Edit and Delete functionality inside Search Results window
* Added dynamic, scrollable table inside search results window where deleting a macro will update the table without opening and closing the window
* Improved CreateMacroWindow class to have edit functionality. Optional macro can be passed in where if so, it will pre-populate all forms where you can then make edits

Improvements
* Added error popups in CreateMacroWindow if user try to create a blank macro or create a macro with a name that already exists.
* Upgraded tkinter UI library to latest version.
* Overall code improvement and cleanup

The Next Step: Objectives
* Rotary Encoder Macros do not show up in the search results window
* Add more rotary encoder AutoHotKey presets 
