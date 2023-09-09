@echo off
set SourceDir="%USERPROFILE%\\\My Documents\\\projects\\\wadm\\\dist\\\wadm"
set DocumentDir="\\ant\\\dept-na\\\DEN2\\\Support\\\Safety\\\NACF Safety Programs\\\2.5 Regulated Waste\\\Processing Assist\\\wadm"
set LogFile="%USERPROFILE%\\\My Documents\\\wadm\\\Update.log"

echo Updating WADM Processing Assitant
echo From %SourceDir%
echo To %DocumentDir%
robocopy.exe %SourceDir% %DocumentDir% /mt:30 /E /XO /LOG+:%LogFile%
echo copy complete
pause