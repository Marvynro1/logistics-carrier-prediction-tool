$Host.UI.RawUI.WindowTitle = "Logistics Predictor Backend"

$asciiArt = @"
'##::::'##::::'###::::'##:::::::'##::::'##:                                                   
 ##:::: ##:::'## ##::: ##::::::: ##:::: ##:                                                   
 ##:::: ##::'##:. ##:: ##::::::: ##:::: ##:                                                   
 ##:::: ##:'##:::. ##: ##::::::: ##:::: ##:                                                   
. ##:: ##:: #########: ##:::::::. ##:: ##::                                                   
:. ## ##::: ##.... ##: ##::::::::. ## ##:::                                                   
::. ###:::: ##:::: ##: ########:::. ###::::                                                   
:::...:::::..:::::..::........:::::...:::::                                                   
'####:'##::: ##:'########::'##::::'##::'######::'########:'########::'####:'########::'######::
. ##:: ###:: ##: ##.... ##: ##:::: ##:'##... ##:... ##..:: ##.... ##:. ##:: ##.....::'##... ##:
: ##:: ####: ##: ##:::: ##: ##:::: ##: ##:::..::::: ##:::: ##:::: ##:: ##:: ##::::::: ##:::..::
: ##:: ## ## ##: ##:::: ##: ##:::: ##:. ######::::: ##:::: ########::: ##:: ######:::. ######::
: ##:: ##. ####: ##:::: ##: ##:::: ##::..... ##:::: ##:::: ##.. ##:::: ##:: ##...:::::..... ##:
: ##:: ##:. ###: ##:::: ##: ##:::: ##:'##::: ##:::: ##:::: ##::. ##::: ##:: ##:::::::'##::: ##:
'####: ##::. ##: ########::. #######::. ######::::: ##:::: ##:::. ##:'####: ########:. ######::
....::..::::..::........::::.......::::......::::::..:::::..:::::..::....::........:::......:::
"@

# Print the ASCII art in green
Write-Host $asciiArt -ForegroundColor Green

Write-Host ""
Write-Host "================================================================="
Write-Host "Welcome to the Logistics Carrier Prediction Tool Setup"
Write-Host "================================================================="
Write-Host ""
Write-Host "Please ensure Docker Desktop is running before you continue."
Write-Host ""

# Prompt the user for the Anvil Uplink Key
$anvilKey = Read-Host -Prompt "To start the script, please enter the Anvil Uplink Key"

# Create the .env file
Set-Content -Path ".env" -Value "ANVIL_UPLINK_KEY=$anvilKey"

# Ensure that the container is stopped when the user presses Ctrl+C
try {
    Write-Host ""
    Write-Host "Starting Docker container... (Press Ctrl+C in this window to stop)" -ForegroundColor Yellow
    Write-Host "Monitoring logs for server readiness..." -ForegroundColor Yellow
    Write-Host ""

    $browserOpened = $false

    # Run docker-compose and process its output
    docker-compose up --build 2>&1 | ForEach-Object {
        Write-Host $_
        if ($_ -match "as SERVER" -and $browserOpened -eq $false) {
            $browserOpened = $true
            Write-Host ""
            Write-Host "Backend server is ready! Opening Anvil App and JupyterLab..." -ForegroundColor Green
            
            # Open the URLs
            Start-Process "https://ddhrgvebw25wfi2b.anvil.app/I6RUPSWSD4AFO3BBKAXT63P7"
            Start-Process "http://localhost:8888"

            # --- Print the URLs to the console ---
            Write-Host ""
            Write-Host "You can access the apps at the following URLs:" -ForegroundColor Yellow
            Write-Host "  - Anvil Web App: https://ddhrgvebw25wfi2b.anvil.app/I6RUPSWSD4AFO3BBKAXT63P7" -ForegroundColor Cyan
            Write-Host "  - JupyterLab:    http://localhost:8888" -ForegroundColor Cyan
        }
    }
}
finally {
    # This block will always run to ensure a clean shutdown
    Write-Host ""
    Write-Host "Shutting down Docker container..." -ForegroundColor Red
    docker-compose down
    Write-Host "Container stopped." -ForegroundColor Green
}
