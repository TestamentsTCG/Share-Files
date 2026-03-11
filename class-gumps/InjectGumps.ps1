# InjectGumps.ps1 - Perilous Legends Gump Injector v1
# Run as Administrator. Place in same folder as PNGs and all_classes_gumps.txt
# Usage: Right-click -> Run with PowerShell (as Admin)

$UO_DIR = "C:\Program Files (x86)\Electronic Arts\Ultima Online Classic"
$GUMPART = Join-Path $UO_DIR "Gumpart.mul"
$GUMPIDX = Join-Path $UO_DIR "Gumpidx.mul"
$IDX_ENTRY = 12
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$BATCH = Join-Path $SCRIPT_DIR "all_classes_gumps.txt"
$LOG = Join-Path $SCRIPT_DIR "inject_log.txt"

function Log($msg) {
    Write-Host $msg
    Add-Content $LOG $msg
}

Clear-Content $LOG -ErrorAction SilentlyContinue
Log "InjectGumps.ps1 v1 - $(Get-Date)"
Log "Working dir: $SCRIPT_DIR"
Log "UO dir: $UO_DIR"

# Verify files exist
if (!(Test-Path $GUMPART)) { Log "ERROR: Gumpart.mul not found at $GUMPART"; Read-Host "Press Enter"; exit }
if (!(Test-Path $GUMPIDX)) { Log "ERROR: Gumpidx.mul not found at $GUMPIDX"; Read-Host "Press Enter"; exit }
if (!(Test-Path $BATCH))   { Log "ERROR: Batch file not found at $BATCH"; Read-Host "Press Enter"; exit }

Log "Gumpart.mul size: $((Get-Item $GUMPART).Length) bytes"
Log "Gumpidx.mul size: $((Get-Item $GUMPIDX).Length) bytes"

function RgbToColor16($r, $g, $b) {
    $r5 = $r -shr 3
    $g5 = $g -shr 3
    $b5 = $b -shr 3
    return [uint16](($r5 -shl 10) -bor ($g5 -shl 5) -bor $b5)
}

function EncodeGump($pngPath) {
    Add-Type -AssemblyName System.Drawing
    $bmp = [System.Drawing.Bitmap]::FromFile($pngPath)
    $width = $bmp.Width
    $height = $bmp.Height

    $ms = New-Object System.IO.MemoryStream
    $bw = New-Object System.IO.BinaryWriter($ms)

    # Write placeholder lookup table
    for ($i = 0; $i -lt $height; $i++) { $bw.Write([int32]0) }

    $rowOffsets = New-Object int[] $height

    for ($y = 0; $y -lt $height; $y++) {
        $rowOffsets[$y] = [int]($ms.Position / 4)
        $x = 0
        while ($x -lt $width) {
            $px = $bmp.GetPixel($x, $y)
            $color = RgbToColor16 $px.R $px.G $px.B
            $runStart = $x
            $x++
            while ($x -lt $width) {
                $px2 = $bmp.GetPixel($x, $y)
                $c2 = RgbToColor16 $px2.R $px2.G $px2.B
                if ($c2 -ne $color) { break }
                $x++
            }
            $run = $x - $runStart
            while ($run -gt 0) {
                $chunk = [Math]::Min($run, 32767)
                $bw.Write([int16]$color)
                $bw.Write([int16]$chunk)
                $run -= $chunk
            }
        }
    }

    # Write lookup table
    $endPos = $ms.Position
    $ms.Seek(0, [System.IO.SeekOrigin]::Begin) | Out-Null
    foreach ($offset in $rowOffsets) { $bw.Write([int32]$offset) }
    $ms.Seek($endPos, [System.IO.SeekOrigin]::Begin) | Out-Null

    $bmp.Dispose()
    return @{ Data = $ms.ToArray(); Width = $width; Height = $height }
}

function ExpandIdx($gumpId) {
    $needed = ($gumpId + 1) * $IDX_ENTRY
    $current = (Get-Item $GUMPIDX).Length
    if ($needed -gt $current) {
        Log "  Expanding Gumpidx.mul from $current to $needed bytes..."
        $toAdd = $needed - $current
        $fill = New-Object byte[] $toAdd
        for ($i = 0; $i -lt $fill.Length; $i++) { $fill[$i] = 0xFF }
        $fs = [System.IO.File]::Open($GUMPIDX, [System.IO.FileMode]::Append)
        $fs.Write($fill, 0, $fill.Length)
        $fs.Close()
        Log "  Expanded OK."
    }
}

function InjectGump($gumpId, $pngPath) {
    if (!(Test-Path $pngPath)) {
        Log "  ERROR [$gumpId]: File not found: $pngPath"
        return $false
    }
    Log "  Injecting [$gumpId]: $(Split-Path -Leaf $pngPath)"
    try {
        ExpandIdx $gumpId
        $encoded = EncodeGump $pngPath
        $data = $encoded.Data
        $width = $encoded.Width
        $height = $encoded.Height

        # Append to Gumpart.mul
        $offset = (Get-Item $GUMPART).Length
        $fs = [System.IO.File]::Open($GUMPART, [System.IO.FileMode]::Append)
        $fs.Write($data, 0, $data.Length)
        $fs.Close()

        # Update Gumpidx.mul entry
        $extra = ($width -shl 16) -bor $height
        $fs = [System.IO.File]::Open($GUMPIDX, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Write)
        $fs.Seek($gumpId * $IDX_ENTRY, [System.IO.SeekOrigin]::Begin) | Out-Null
        $bw = New-Object System.IO.BinaryWriter($fs)
        $bw.Write([int32]$offset)
        $bw.Write([int32]$data.Length)
        $bw.Write([int32]$extra)
        $bw.Close()
        $fs.Close()

        Log "  OK [$gumpId]: ${width}x${height} -> offset $offset, $($data.Length) bytes"
        return $true
    } catch {
        Log "  ERROR [$gumpId]: $_"
        return $false
    }
}

# Run batch
$ok = 0; $fail = 0
$lines = Get-Content $BATCH
foreach ($line in $lines) {
    $line = $line.Trim()
    if ($line -eq "" -or $line.StartsWith("#")) { continue }
    $parts = $line -split "\s+", 2
    if ($parts.Length -ne 2) { Log "SKIP: $line"; continue }
    $id = [int]$parts[0]
    $png = $parts[1]
    if (![System.IO.Path]::IsPathRooted($png)) { $png = Join-Path $SCRIPT_DIR $png }
    if (InjectGump $id $png) { $ok++ } else { $fail++ }
}

Log ""
Log "Done: $ok injected, $fail failed."
Read-Host "Press Enter to close"
