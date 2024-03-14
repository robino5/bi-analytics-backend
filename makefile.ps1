# Define targets
function Clean {
    CleanPyc
    CleanBuild
    CleanTest
    Write-Host "All build, test, coverage, and Python artifacts have been removed."
}

function CleanBuild {
    Remove-Item -Path "build/" -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path "dist/" -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path ".eggs/" -Force -Recurse -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Filter "*.egg-info" -Recurse | ForEach-Object { Remove-Item -Path $_.FullName -Force -Recurse }
    Get-ChildItem -Path . -Filter "*.egg" -Recurse | ForEach-Object { Remove-Item -Path $_.FullName -Force }
}

function CleanPyc {
    Get-ChildItem -Path . -Filter "*.pyc" -Recurse | ForEach-Object { Remove-Item -Path $_.FullName -Force }
    Get-ChildItem -Path . -Filter "*.pyo" -Recurse | ForEach-Object { Remove-Item -Path $_.FullName -Force }
    Get-ChildItem -Path . -Filter "*~" -Recurse | ForEach-Object { Remove-Item -Path $_.FullName -Force }
    Get-ChildItem -Path . -Filter "__pycache__" -Recurse | ForEach-Object { Remove-Item -Path $_.FullName -Force -Recurse }
}

function CleanTest {
    Remove-Item -Path ".tox/" -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path ".coverage" -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "htmlcov/" -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path ".pytest_cache/" -Force -Recurse -ErrorAction SilentlyContinue
}

function Format-PythonCode {
    param (
        [string]$Path = (Get-Location).Path
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Invalid path: $Path"
        return
    }


    # Run ruff
    Write-Host "Running ruff..."
    & ruff $Path --fix
    Write-Host "ruff completed running."

    # Run black
    Write-Host "Running black..."
    & black $Path
    Write-Host "black completed running."

    # Run node prettier
    Write-Host "Running prettier..."
    & npm run format
    Write-Host "prettier completed running."
}

# Call the target based on the provided argument
$target = $args[0]
switch ($target) {
    "clean" { Clean }
    "clean-build" { CleanBuild }
    "clean-pyc" { CleanPyc }
    "clean-test" { CleanTest }
    "lint" {Format-PythonCode}
    default { Write-Host "Invalid target: $target" }
}
