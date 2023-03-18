F13::
{
	MouseGetPos, MouseX, MouseY
	PixelGetColor, color, %MouseX%, %MouseY%, RGB
	StringLower, color, color
	clipboard := SubStr(color, 3)
	Return
}

F14::Send Hello there, This is a preset message that will type out for you automatically if you run this macro

F15::Run, www.youtube.com

F16::Volume_Mute

F17::Volume_Down

F18::Volume_Up

F21::WheelUp

F22::WheelDown

