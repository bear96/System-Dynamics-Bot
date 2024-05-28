@echo off
setlocal enabledelayedexpansion

if defined OPENAI_API_KEY (
    echo OPENAI_API_KEY is already set to: !OPENAI_API_KEY!
    goto end
)

if exist .openai_key (
    set /p choice=Do you want to use the saved API key? [Y/N]: 
    if /i "!choice!"=="Y" (
        set /p OPENAI_API_KEY=< .openai_key
        echo Using saved API key: !OPENAI_API_KEY!
        goto end
    )
)


set /p OPENAI_API_KEY=Enter your OpenAI API key: 


set /p save=Do you want to save this API key for future use? [Y/N]: 
if /i "!save!"=="Y" (
    echo !OPENAI_API_KEY!>.openai_key
    echo API key saved.
)

:end
