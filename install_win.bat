setlocal enabledelayedexpansion
@ECHO OFF
SET _plugindir=%USERPROFILE%\Praat\plugin_pralign
RD /Q /S "%_plugindir%"
MD "%_plugindir%"
COPY %~dp0*.py "%_plugindir%"
COPY %~dp0*.praat "%_plugindir%"
MD "%_plugindir%\par.spanish"
COPY par.spanish\* "%_plugindir%\par.spanish"
MD "%_plugindir%\par.dutch"
COPY par.dutch\* "%_plugindir%\par.dutch"
echo Installing completed, please press enter to close this window...
pause > nul
