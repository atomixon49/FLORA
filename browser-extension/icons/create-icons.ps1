# FLORA Icon Creator - PowerShell Script
# Crea iconos simples para la extensión

Add-Type -AssemblyName System.Drawing

# Función para crear un icono
function Create-Icon {
    param(
        [int]$Size,
        [string]$FileName
    )
    
    # Crear bitmap
    $bitmap = New-Object System.Drawing.Bitmap($Size, $Size)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    
    # Configurar calidad
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAlias
    
    # Fondo con gradiente (simulado con color sólido)
    $backgroundBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(102, 126, 234))
    $graphics.FillRectangle($backgroundBrush, 0, 0, $Size, $Size)
    
    # Flor central
    $flowerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    $centerX = $Size / 2
    $centerY = $Size / 2
    $flowerSize = $Size * 0.6
    
    # Pétalos (5 pétalos)
    for ($i = 0; $i -lt 5; $i++) {
        $angle = ($i * 2 * [Math]::PI) / 5
        $petalX = $centerX + [Math]::Cos($angle) * $flowerSize * 0.3
        $petalY = $centerY + [Math]::Sin($angle) * $flowerSize * 0.3
        
        $petalRect = New-Object System.Drawing.RectangleF(
            $petalX - $flowerSize * 0.15, 
            $petalY - $flowerSize * 0.25, 
            $flowerSize * 0.3, 
            $flowerSize * 0.5
        )
        $graphics.FillEllipse($flowerBrush, $petalRect)
    }
    
    # Centro de la flor
    $centerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 215, 0))
    $centerRect = New-Object System.Drawing.RectangleF(
        $centerX - $flowerSize * 0.15, 
        $centerY - $flowerSize * 0.15, 
        $flowerSize * 0.3, 
        $flowerSize * 0.3
    )
    $graphics.FillEllipse($centerBrush, $centerRect)
    
    # Texto "F" si es lo suficientemente grande
    if ($Size -ge 32) {
        $font = New-Object System.Drawing.Font("Arial", $Size * 0.3, [System.Drawing.FontStyle]::Bold)
        $textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
        $format = New-Object System.Drawing.StringFormat
        $format.Alignment = [System.Drawing.StringAlignment]::Center
        $format.LineAlignment = [System.Drawing.StringAlignment]::Center
        
        $graphics.DrawString("F", $font, $textBrush, $centerX, $centerY + $Size * 0.1, $format)
    }
    
    # Guardar como PNG
    $bitmap.Save($FileName, [System.Drawing.Imaging.ImageFormat]::Png)
    
    # Limpiar recursos
    $graphics.Dispose()
    $bitmap.Dispose()
    $backgroundBrush.Dispose()
    $flowerBrush.Dispose()
    $centerBrush.Dispose()
    if ($Size -ge 32) {
        $font.Dispose()
        $textBrush.Dispose()
        $format.Dispose()
    }
}

Write-Host "🌸 Creando iconos para FLORA..." -ForegroundColor Magenta

# Crear iconos en diferentes tamaños
Create-Icon -Size 16 -FileName "icon16.png"
Write-Host "✅ icon16.png creado" -ForegroundColor Green

Create-Icon -Size 32 -FileName "icon32.png"
Write-Host "✅ icon32.png creado" -ForegroundColor Green

Create-Icon -Size 48 -FileName "icon48.png"
Write-Host "✅ icon48.png creado" -ForegroundColor Green

Create-Icon -Size 128 -FileName "icon128.png"
Write-Host "✅ icon128.png creado" -ForegroundColor Green

Write-Host "🎉 Todos los iconos creados exitosamente!" -ForegroundColor Magenta
Write-Host "Ahora puedes cargar la extensión en Chrome" -ForegroundColor Yellow
