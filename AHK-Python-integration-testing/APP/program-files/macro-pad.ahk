F1::
{
	MouseGetPos, MouseX, MouseY
	PixelGetColor, color, %MouseX%, %MouseY%, RGB
	StringLower, color, color
	clipboard := SubStr(color, 3)
	Return
}

F2::Run, www.youtube.com

F3::Send Hello there, This is a preset message that will type out for you automatically if you run this macro

F4::Volume_Mute

F5::Volume_Down

F6::Volume_Up

F9::WheelUp

F10::WheelDown

