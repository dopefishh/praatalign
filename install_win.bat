@ECHO OFF
ECHO Setting directory
SET _plugindir=%USERPROFILE%\Praat\plugin_pralign
ECHO Clearing out directory
RD /Q /S "%_plugindir%"
echo Creating directory
MD "%_plugindir%" "bin"
echo Copy binaries
ROBOCOPY /PURGE bin_win bin /Z
echo Copy plugin files
ROBOCOPY "%CD%" "%_plugindir%" /S /Z /XD .* /XF .* /XF install* /XF temp* /XD bin_*
echo Installing completed, please press enter to close this window...
pause > nul
