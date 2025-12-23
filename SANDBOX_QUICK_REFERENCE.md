# 🏖️ SANDBOX QUICK REFERENCE

## ⚡ One-Liner Commands

### Before Shutdown (MUST DO!):
```bash
python SANDBOX_EXPORT.py
```
**Filen sparas på Desktop → Kopiera till host!**

### New Session (Quick Start):
```bash
python SANDBOX_IMPORT.py
```
**Auto-hittar och återställer senaste export**

### Background Auto-Backup:
```bash
python AUTO_SANDBOX_EXPORT.py --watch -i 30
```
**Kör i separat terminal - exporterar var 30:e minut**

---

## 📋 Complete Workflow

### 🌅 MORGON (Ny Sandbox):
```bash
# 1. Kopiera senaste export till Documents
# 2. Restore workspace:
cd Documents\Datacenter
python SANDBOX_IMPORT.py

# 3. Starta auto-backup (separat terminal):
python AUTO_SANDBOX_EXPORT.py --watch -i 30

# 4. Fortsätt arbeta!
```

### 🌙 KVÄLL (Innan Stängning):
```bash
# 1. Final export:
python SANDBOX_EXPORT.py

# 2. Kopiera från Desktop till host
# 3. Stäng sandbox - allt är sparat!
```

---

## 🎯 Windows Batch Scripts

### Dubbelklicka för export:
`QUICK_EXPORT.bat` - Exporterar och pausar

### Dubbelklicka för import:
`QUICK_IMPORT.bat` - Importerar och aktiverar minne

---

## 💾 Vad Exporteras?

✅ **Inkluderat:**
- Källkod (.py, .md, .json)
- Databaser (MEMORY_CORE/)
- Config (.env, .gitignore)
- Checkpoints & handoffs
- Skills & docs

❌ **Exkluderat:**
- Python cache (__pycache__)
- IDE-filer (.idea, .vscode)
- Virtual environments (venv/)
- Temp/log-filer

---

## 🔧 Troubleshooting

**Export hittar inte filer:**
```bash
cd C:\Users\WDAGUtilityAccount\Documents\Datacenter
python SANDBOX_EXPORT.py
```

**Import hittar inte arkiv:**
```bash
python SANDBOX_IMPORT.py C:\Path\To\Export.zip
```

**Dependencies saknas:**
```bash
pip install -r requirements.txt
```

---

## 📊 File Locations

**Export skapas här:**
- `C:\Users\WDAGUtilityAccount\Desktop\Datacenter_Export_*.zip`

**Import letar här:**
1. Current directory
2. Documents folder
3. Desktop

**Host backup rekommendation:**
- `D:\Sandbox_Backups\` (eller liknande)

---

## ⚠️ VIKTIGT!

1. **EXPORTERA ALLTID** innan du stänger sandbox
2. **Kopiera till host** - allt försvinner annars
3. **Behåll flera versioner** - senaste 3-5 exports
4. **Auto-backup i bakgrunden** rekommenderas starkt

---

## 🎊 Du är nu sandbox-säker!

Med detta system kan du använda Windows Sandbox som din huvudarbetsmiljö utan risk att förlora arbete!

**En export på Desktop = Ingen förlorad data!** 🏖️

---

📖 **Full dokumentation:** [SANDBOX_WORKFLOW_GUIDE.md](SANDBOX_WORKFLOW_GUIDE.md)
