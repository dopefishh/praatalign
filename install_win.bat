@ECHO OFF
ECHO Setting directory
SET _plugindir=%USERPROFILE%\Praat\plugin_pralign
ECHO Clearing out directory
RD /Q /S "%_plugindir%"
echo Creating directory
MD "%_plugindir%"
echo Copy plugin files
ROBOCOPY "%CD%" "%_plugindir%" /S /Z /XD .* /XF .* /XF install* /XF temp* /XD tutorial*
echo Installing completed, please press enter to close this window...
pause > nul
