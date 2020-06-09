$path = "./Output.txt"

Write-output $args[1] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue
Write-output $args[2] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue
Write-output $args[3] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue
Write-output $args[4] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue
Write-output $args[5] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue
Write-output $args[6] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue
Write-output $args[7] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue
Write-output $args[8] | Out-file -FilePath $path -Append -Force -ErrorAction SilentlyContinue  