setlocal enabledelayedexpansion
set br=""
for /f "skip=5 tokens=3  delims= " %%J in ('dir  /-C \\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R\P01\group1\recording10017\cam120-1455614872-581.mp4') do if !br!=="" (
echo !br!
echo %%J
set br=yes
)

endlocal 