F1::Run chrome.exe

F2::Run, https://www.youtube.com

F3::
{
	MouseGetPos, MouseX, MouseY
	PixelGetColor, color, %MouseX%, %MouseY%, RGB
	StringLower, color, color
	clipboard := SubStr(color, 3)
	Return
}

F4::Run C:\\Users\\bvan5\\Desktop\\SeniorDesign

