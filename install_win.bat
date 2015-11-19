setlocal enabledelayedexpansion
@ECHO OFF
SET _plugindir=%USERPROFILE%\Praat\plugin_pralign
RD /Q /S "%_plugindir%"
MD "%_plugindir%"
COPY %~dp0*.py "%_plugindir%"
COPY %~dp0*.praat "%_plugindir%"
FOR /D %%i IN (%~dp0par.*) DO (
	SET test=%%i
	SET test=!test:~-7%!
	MD "%_plugindir%\!test!\"
	COPY "%%i\*" "%_plugindir%\!test!\"
)
echo Installing completed, please press enter to close this window...
pause > nul
