$PATH_FIRMWARE       = ".\iot-reference-stm32u5"
$PATH_QUICK_CONNECT  = ".\STM32U5_AWS_QuickConnect"
$PATH_TOOLS          = ".\tools"
$PATH_LOG            = ".\log"
$PATH_DOWNLOAD       = (Get-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders").PSObject.Properties["{374DE290-123F-4565-9164-39C4925E467B}"].Value

$ZIP_STM32_CUBE_PROG           = "en.stm32cubeprg-win64-v2-12-0.zip"
$ZIP_STM32_CUBE_IDE            = "en.st-stm32cubeide_1.11.0_13638_20221122_1308_x86_64.exe.zip"
$ZIP_X_CUBE_AWS                = "en.x-cube-aws_v3-0-0.zip"

function Remove-File($path)
{
    Write-Host "Removing $path"
    Remove-Item $path -Recurse -Force >$null 2>&1
}

function Remove-Program($program)
{
    if($program -eq "python")
    {
        pip uninstall -r .\requirements.txt

    }

    Write-Host "Uninstalling $program"
    Get-Package *$program* | Uninstall-Package -Force
}

Remove-File $PATH_FIRMWARE
Remove-File $PATH_QUICK_CONNECT
Remove-File $PATH_TOOLS
Remove-File $PATH_LOG
Remove-File $PATH_DOWNLOAD\$ZIP_STM32_CUBE_PROG
Remove-File $PATH_DOWNLOAD\$ZIP_STM32_CUBE_IDE
Remove-File $PATH_DOWNLOAD\$ZIP_X_CUBE_AWS

Remove-Program "aws"
Remove-Program "perl"
Remove-Program "cmake"
Remove-Program "python"

#Set-ExecutionPolicy Restricted -Scope CurrentUser