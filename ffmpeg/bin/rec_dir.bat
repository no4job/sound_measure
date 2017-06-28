@echo off
setlocal enabledelayedexpansion
goto mgs
if exist dirs.txt  del dirs.txt
for /f "tokens=*" %%G in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\p*"') do (
	for /f "tokens=*" %%F in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\group*"') do (
			REM for /f "skip=5 tokens=1,2,4 delims= " %%A in ('dir /ad \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\recording*') do  (
			for /f "tokens=*" %%H in ('dir /b /ad \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\recording*') do  (
				for /f "tokens=*" %%I in ('dir /b /a-d \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\%%H\cam*.mp4') do  (
					set br=""
					for /f "skip=5 tokens=3  delims= " %%J in ('dir  /-C \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\%%H\%%I') do if !br!=="" (
						REM echo %%J
						set size=%%J
						set br=yes
					)
					for /f "tokens=1,2,3* delims=-" %%A in ("%%I") do  (
						echo %%G %TAB% %%F %TAB% %%H %TAB% %%A %TAB% %%A-%%B-%%C %TAB% %%B %TAB% !size! >>dirs.txt 
					)
				)	
			)
    )
)
:mgs
for /f "tokens=*" %%G in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\MGS*"') do (
	for /f "tokens=*" %%F in ('dir /b /ad "\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\group*"') do (
			REM for /f "skip=5 tokens=1,2,4 delims= " %%A in ('dir /ad \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\recording*') do  (
			for /f "tokens=*" %%H in ('dir /b /ad \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\recording*') do  (
				for /f "tokens=*" %%I in ('dir /b /a-d \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\%%H\cam*.mp4') do  (
					set br=""
					for /f "skip=5 tokens=3  delims= " %%J in ('dir  /-C \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\%%G\%%F\%%H\%%I') do if !br!=="" (
						REM echo %%J
						set size=%%J
						set br=yes
					)
					for /f "tokens=1,2,3* delims=-" %%A in ("%%I") do  (
						echo %%G %TAB% %%F %TAB% %%H %TAB% %%A %TAB% %%A-%%B-%%C %TAB% %%B %TAB% !size! >>dirs.txt 
					)
				)	
			)
    )
)

endlocal 
@echo on