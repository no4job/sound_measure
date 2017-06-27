@echo off
setlocal enabledelayedexpansion
if exist dirs.txt  del dirs.txt
for /f "tokens=*" %%G in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\p*"') do (
	for /f "tokens=*" %%F in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\group*"') do (
			for /f "skip=5 tokens=1,2,4 delims= " %%A in ('dir /ad \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\recording*') do  (
				echo %%G\%%F\%%C  %TAB% %%A %TAB% %%B >>dirs.txt 
			)
    )
)

for /f "tokens=*" %%G in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\mgs"') do (
	for /f "tokens=*" %%F in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\group*"') do (
			for /f "skip=5 tokens=1,2,4 delims= " %%A in ('dir /ad \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\recording*') do  (
				echo %%G\%%F\%%C  %TAB% %%A %TAB% %%B >>dirs.txt 
			)
    )
)

endlocal 
@echo on