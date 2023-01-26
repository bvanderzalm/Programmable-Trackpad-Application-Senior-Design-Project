{
F1::
    Send, ^c
    Sleep 50
    Run, https://www.google.com/search?q=%clipboard%
    Return
}

F2::Run, Chrome.exe "https://www.ucf.edu"

F3::Run Notepad

; Move up a folder in file explorer
F4::Send !{Up}
