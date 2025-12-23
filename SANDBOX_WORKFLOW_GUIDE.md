# 🏖️ SANDBOX WORKFLOW GUIDE - Windows Sandbox Sessions

## Problem
Windows Sandbox är fantastiskt för säkerhet, men allt försvinner när du stänger ner. Detta system löser det genom att göra din workspace "portable" - spara innan stängning, återställ i ny session.

## 🚀 Quick Start

### Första gången (Setup):
```bash
# Du är redan här - workspace är redo!
# Testa systemet:
python TEST_MEMORY.py
python ACTIVATE_MEMORY.py
```

### Innan du stänger sandbox:
```bash
# VIKTIGT: Exportera workspace innan du stänger!
python SANDBOX_EXPORT.py

# Filen sparas på Desktop:
# Datacenter_Export_YYYYMMDD_HHMMSS.zip

# Kopiera denna fil till host-datorn (t.ex. D:\Sandbox_Backups\)
```

### Nästa sandbox-session:
```bash
# 1. Kopiera export-filen till Documents i nya sandboxen
# 2. Kör import:
python SANDBOX_IMPORT.py

# Eller specificera path:
python SANDBOX_IMPORT.py D:\Backups\Datacenter_Export_20241223_120000.zip

# 3. Fortsätt arbeta där du slutade!
python ACTIVATE_MEMORY.py
```

## 🔄 Automatisk Backup (Rekommenderat)

### Kör i separat terminal:
```bash
# Auto-export var 30:e minut
python AUTO_SANDBOX_EXPORT.py --watch

# Eller var 15:e minut
python AUTO_SANDBOX_EXPORT.py --watch -i 15
```

Detta exporterar automatiskt din workspace med jämna mellanrum. Senaste filen finns alltid på Desktop.

## 📁 Vad som sparas

### ✅ Inkluderat:
- Alla source-filer (.py, .md, .json, etc.)
- Databaser (MEMORY_CORE/central_memory.db)
- Konfigurationsfiler (.env, .gitignore)
- Checkpoints och handoffs
- Projektstruktur
- Skills och dokumentation

### ❌ Exkluderat (för att spara plats):
- Python cache (__pycache__, *.pyc)
- IDE-filer (.idea, .vscode)
- Virtuella miljöer (venv/)
- Stora mediafiler (video, audio)
- Temporära filer
- Node_modules (om några)

Se `.sandboxignore` för fullständig lista.

## 🎯 Workflow-exempel

### Normal arbetsdag i sandbox:

```bash
# 1. MORGON - Starta ny sandbox
# Kopiera senaste export till Documents
cd Documents
python SANDBOX_IMPORT.py Desktop\Datacenter_Export_Latest.zip

# 2. Aktivera minne
cd Datacenter
python ACTIVATE_MEMORY.py

# 3. Starta auto-backup (separat terminal)
python AUTO_SANDBOX_EXPORT.py --watch -i 30

# 4. ARBETA NORMALT
# Systemet sparar automatiskt var 30:e minut

# 5. LUNCH/PAUS - Manuell export (för säkerhets skull)
python SANDBOX_EXPORT.py

# 6. KVÄLL - Innan du stänger
python SANDBOX_EXPORT.py
# Kopiera filen från Desktop till host
# Done! Kan stänga sandbox.
```

## 💾 Backup-strategi

### På host-datorn:
```
D:\Sandbox_Backups\
├── Datacenter_Export_20241223_090000.zip  # Morgon
├── Datacenter_Export_20241223_120000.zip  # Lunch
├── Datacenter_Export_20241223_150000.zip  # Eftermiddag
└── Datacenter_Export_20241223_180000.zip  # Kväll (senaste)
```

### Rekommendation:
- Behåll senaste 3-5 exports
- Ta backup före större ändringar
- Synka till cloud (OneDrive, Dropbox) för extra säkerhet

## 🔐 Verifiering

### Kontrollera export-integritet:
```bash
# Exporterar och visar checksum
python SANDBOX_EXPORT.py
# Output: SHA-256: abc123def456...

# Vid import verifieras automatiskt
python SANDBOX_IMPORT.py
```

## 🛠️ Troubleshooting

### Export hittar inte filer:
```bash
# Kör från Datacenter-mappen
cd C:\Users\WDAGUtilityAccount\Documents\Datacenter
python SANDBOX_EXPORT.py
```

### Import kan inte hitta arkiv:
```bash
# Specificera full path
python SANDBOX_IMPORT.py C:\Path\To\Export.zip

# Eller kopiera till Documents först
copy D:\Backups\Export.zip C:\Users\WDAGUtilityAccount\Documents\
python SANDBOX_IMPORT.py Export.zip
```

### Dependencies saknas efter import:
```bash
# Import installerar automatiskt, men om det misslyckas:
pip install -r requirements.txt
```

### Minne aktiveras inte:
```bash
# Verifiera först
python TEST_MEMORY.py

# Sedan aktivera
python ACTIVATE_MEMORY.py

# Kontrollera databas
python check_memory_stats.py
```

## 📊 Kommandoreferens

### Export:
```bash
python SANDBOX_EXPORT.py              # Standard export
python SANDBOX_EXPORT.py -o custom.zip # Custom namn
```

### Import:
```bash
python SANDBOX_IMPORT.py                    # Auto-hitta senaste
python SANDBOX_IMPORT.py archive.zip        # Specifik fil
python SANDBOX_IMPORT.py --force            # Skriv över befintligt
```

### Auto-export:
```bash
python AUTO_SANDBOX_EXPORT.py --now         # Export nu
python AUTO_SANDBOX_EXPORT.py --watch       # Watch mode (30 min)
python AUTO_SANDBOX_EXPORT.py --watch -i 15 # Watch mode (15 min)
```

### Minne:
```bash
python TEST_MEMORY.py          # Verifiera innehåll
python ACTIVATE_MEMORY.py      # Aktivera system
python AUTO_CHECKPOINT.py      # Spara checkpoint
python check_memory_stats.py   # Visa statistik
```

## 🎓 Best Practices

### DO:
1. ✅ Exportera INNAN du stänger sandbox
2. ✅ Kör auto-export i bakgrunden
3. ✅ Behåll flera backup-versioner
4. ✅ Verifiera import efter restore
5. ✅ Använd TEST_MEMORY.py för att se status

### DON'T:
1. ❌ Glöm inte exportera innan shutdown
2. ❌ Förlita dig på EN enda backup
3. ❌ Radera backups för tidigt
4. ❌ Skippa verifiering efter import
5. ❌ Arbeta utan auto-export i bakgrunden

## 🎯 Pro Tips

### 1. Scheduled exports under dagen:
Kör `AUTO_SANDBOX_EXPORT.py --watch -i 15` i bakgrunden för export var 15:e minut.

### 2. Quick-backup shortcut:
```bash
# Skapa alias/script för snabb export
python SANDBOX_EXPORT.py && echo "Backup on Desktop!"
```

### 3. Cloud sync:
```powershell
# PowerShell script för auto-sync till OneDrive
$source = "$env:USERPROFILE\Desktop\Datacenter_Export_*.zip"
$dest = "D:\OneDrive\Sandbox_Backups\"
Copy-Item $source $dest -Force
```

### 4. Pre-shutdown reminder:
Sätt en post-it på skärmen: "EXPORT BEFORE CLOSING!"

### 5. Morning routine:
```bash
# Skapa morning_start.bat på Desktop:
cd C:\Users\WDAGUtilityAccount\Documents\Datacenter
python SANDBOX_IMPORT.py
python ACTIVATE_MEMORY.py
start python AUTO_SANDBOX_EXPORT.py --watch -i 30
```

## 📈 Workflow Evolution

### Level 1 (Början):
- Manuell export innan stängning
- Manuell import vid start

### Level 2 (Bekväm):
- Auto-export var 30:e minut
- Quick-import script

### Level 3 (Pro):
- Auto-export var 15:e minut
- Cloud-sync automation
- Multiple backup-locations
- Versionshantering av exports

## 🎊 Du är nu sandbox-säker!

Med detta system kan du arbeta i Windows Sandbox med samma kontinuitet som på vanlig maskin, samtidigt som du behåller alla säkerhetsfördelar!

**Kom ihåg: Ett export på Desktop är värt tusen missade ändringar!** 🏖️
