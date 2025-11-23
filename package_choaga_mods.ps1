# PowerShell script to package all Choaga mod files for distribution
# This includes AutoFishMultiSpotTask, mod files, assets, and installation scripts

$ErrorActionPreference = "Stop"

# Get the working directory (where this script is located)
$workingDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $workingDir

Write-Host "=== Choaga Mods Distribution Package Creator ===" -ForegroundColor Cyan
Write-Host ""

# Package name
$packageName = "Choaga_Mods_Package"
$zipName = "$packageName.zip"

# Remove old zip if exists
if (Test-Path $zipName) {
    Remove-Item $zipName -Force
    Write-Host "Removed old package: $zipName" -ForegroundColor Yellow
}

# Create temp directory
$tempDir = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
Write-Host "Created temp directory: $tempDir" -ForegroundColor Green

$exitCode = 0

try {
    # 1. Copy AutoFishMultiSpotTask.py
    Write-Host "`n[1/6] Copying AutoFishMultiSpotTask.py..." -ForegroundColor Cyan
    $taskSource = "src\tasks\fullauto\AutoFishMultiSpotTask.py"
    if (Test-Path $taskSource) {
        $taskDest = Join-Path $tempDir "src\tasks\fullauto"
        New-Item -ItemType Directory -Path $taskDest -Force | Out-Null
        Copy-Item $taskSource $taskDest -Force
        Write-Host "  ✓ Copied AutoFishMultiSpotTask.py" -ForegroundColor Green
    } else {
        throw "ERROR: $taskSource not found!"
    }

    # 2. Copy mod/fish/ folder with all images
    Write-Host "`n[2/6] Copying mod/fish/ folder..." -ForegroundColor Cyan
    $modFishSource = "mod\fish"
    if (Test-Path $modFishSource) {
        $modFishDest = Join-Path $tempDir "mod\fish"
        # Copy all PNG files from mod/fish
        $imageFiles = Get-ChildItem -Path $modFishSource -Filter "*.png" -Recurse
        if ($imageFiles.Count -gt 0) {
            New-Item -ItemType Directory -Path $modFishDest -Force | Out-Null
            Copy-Item -Path "$modFishSource\*.png" -Destination $modFishDest -Force
            Write-Host "  ✓ Copied $($imageFiles.Count) PNG files from mod/fish/" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ WARNING: No PNG files found in mod/fish/" -ForegroundColor Yellow
        }
    } else {
        throw "ERROR: $modFishSource not found!"
    }

    # 3. Copy assets folder (if it exists and contains result.json)
    Write-Host "`n[3/6] Copying assets folder..." -ForegroundColor Cyan
    $assetsSource = "assets"
    if (Test-Path $assetsSource) {
        $assetsDest = Join-Path $tempDir "assets"
        New-Item -ItemType Directory -Path $assetsDest -Force | Out-Null
        
        # Copy result.json if it exists
        $resultJson = Join-Path $assetsSource "result.json"
        if (Test-Path $resultJson) {
            Copy-Item $resultJson $assetsDest -Force
            Write-Host "  ✓ Copied assets/result.json" -ForegroundColor Green
        }
        
        # Copy images folder if it exists
        $imagesSource = Join-Path $assetsSource "images"
        if (Test-Path $imagesSource) {
            $imagesDest = Join-Path $assetsDest "images"
            Copy-Item -Path $imagesSource -Destination $imagesDest -Recurse -Force
            Write-Host "  ✓ Copied assets/images/ folder" -ForegroundColor Green
        }
    } else {
        Write-Host "  ⚠ WARNING: assets folder not found (optional)" -ForegroundColor Yellow
    }

    # 4. Copy installation scripts
    Write-Host "`n[4/6] Copying installation scripts..." -ForegroundColor Cyan
    $scripts = @("add_autofish_to_config.bat", "add_autofish_to_config.py")
    foreach ($script in $scripts) {
        if (Test-Path $script) {
            Copy-Item $script $tempDir -Force
            Write-Host "  ✓ Copied $script" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ WARNING: $script not found" -ForegroundColor Yellow
        }
    }

    # 5. Copy README/DISTRIBUTE file
    Write-Host "`n[5/6] Copying README..." -ForegroundColor Cyan
    $readmeFiles = @("DISTRIBUTE_AutoFishMultiSpotTask.txt", "README.md")
    $readmeCopied = $false
    foreach ($readme in $readmeFiles) {
        if (Test-Path $readme) {
            Copy-Item $readme $tempDir -Force
            Write-Host "  ✓ Copied $readme" -ForegroundColor Green
            $readmeCopied = $true
            break
        }
    }
    if (-not $readmeCopied) {
        Write-Host "  ⚠ WARNING: No README file found" -ForegroundColor Yellow
    }

    # 6. Create installation instructions
    Write-Host "`n[6/6] Creating installation instructions..." -ForegroundColor Cyan
    $installInstructions = @"
INSTALLATION INSTRUCTIONS
=========================

1. Extract this zip file to a temporary location

2. Copy files to your ok-dna installation:
   
   a) Copy AutoFishMultiSpotTask.py to:
      [your ok-dna folder]\src\tasks\fullauto\AutoFishMultiSpotTask.py
   
   b) Copy the mod\fish\ folder to:
      [your ok-dna folder]\mod\fish\
      (Make sure all PNG files are copied)
   
   c) If assets folder exists, copy it to:
      [your ok-dna folder]\assets\
      (This is optional - only if assets were included)

3. Run add_autofish_to_config.bat to automatically add the task to config.py
   OR manually add this line to config.py's 'onetime_tasks' list:
   ["src.tasks.fullauto.AutoFishMultiSpotTask", "AutoFishMultiSpotTask"],

4. Restart ok-dna and the task will appear in your task list

NOTES:
- The add_autofish_to_config.bat script will automatically find your ok-dna installation
- Make sure your game resolution is set to 1920x1080 for best results
- All image files in mod/fish/ are required for the task to work properly

"@
    
    $installPath = Join-Path $tempDir "INSTALL.txt"
    Set-Content -Path $installPath -Value $installInstructions
    Write-Host "  ✓ Created INSTALL.txt" -ForegroundColor Green

    # Create zip from temp directory
    Write-Host "`nCreating zip package..." -ForegroundColor Cyan
    Compress-Archive -Path "$tempDir\*" -DestinationPath $zipName -Force
    Write-Host "✓ Package created: $zipName" -ForegroundColor Green

    # Show package contents
    Write-Host "`nPackage contents:" -ForegroundColor Cyan
    $zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path $zipName))
    $zip.Entries | Select-Object FullName | Format-Table -AutoSize
    $zip.Dispose()

    Write-Host "`n=== Package creation complete! ===" -ForegroundColor Green
    Write-Host "Package location: $(Resolve-Path $zipName)" -ForegroundColor Yellow
    $exitCode = 0

} catch {
    Write-Host "`n✗ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    $exitCode = 1
} finally {
    # Cleanup
    if (Test-Path $tempDir) {
        Remove-Item $tempDir -Recurse -Force
        Write-Host "`nCleaned up temp directory" -ForegroundColor Gray
    }
}

exit $exitCode
