@SETLOCAL
@IF EXIST "%~dp0\/bin/sh.exe" (
  "%~dp0\/bin/sh.exe"  "%~dp0\..\node_modules\@pnpm\exe\pn" %*
) ELSE (
  @SET PATHEXT=%PATHEXT:;.JS;=;%
  /bin/sh  "%~dp0\..\node_modules\@pnpm\exe\pn" %*
)
