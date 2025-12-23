# GitHub Setup Guide för Datacenter

## Varför GitHub?

Eftersom copy-paste från Windows Sandbox till host inte är tillgängligt i denna session, använder vi GitHub som:
- **Sekundär backup** (utöver sandbox-export-systemet)
- **Versionskontroll** för kodändringar
- **Enkel syncing** mellan sessioner
- **Säker lagring** av konfigurationer

## Setup-steg

### 1. Skapa GitHub Repository

```bash
# Initiera git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Lägg till remote
git remote add origin https://github.com/YOUR_USERNAME/datacenter.git
```

### 2. Första commit

```bash
# Stage alla filer (respekterar .gitignore)
git add .

# Commit
git commit -m "Initial commit: Datacenter workspace with sandbox system"

# Push till GitHub
git branch -M main
git push -u origin main
```

### 3. I nästa Sandbox-session

```bash
# Clone från GitHub
git clone https://github.com/YOUR_USERNAME/datacenter.git

# Eller om redan klonad, pull senaste
cd datacenter
git pull origin main
```

## .gitignore Strategi

### Vad som IGNORERAS (sparas lokalt):
- ✗ `.env` - API-nycklar
- ✗ `*.db` - Databaser (lokalt minne)
- ✗ `Datacenter_Export_*.zip` - Temp-backups
- ✗ `__pycache__/` - Python cache
- ✗ `.venv/` - Virtual environment
- ✗ IDE-filer (`.idea/`, `.vscode/`)

### Vad som SPARAS (committas till GitHub):
- ✓ All `.py` source code
- ✓ Dokumentation (`.md` filer)
- ✓ Configuration templates (`.env.example`)
- ✓ Scripts (`SANDBOX_*.py`, `AUTO_*.py`)
- ✓ Batch files (`.bat`)
- ✓ Policies och workflows
- ✓ Skills och examples

## Workflow

### Daglig utveckling:

```bash
# Morgon: Clone/Pull
git clone https://github.com/username/datacenter.git
# eller
git pull origin main

# Under dagen: Work normally
# Sandbox-systemet sparar automatiskt (--watch mode)

# Innan stängning:
git add .
git commit -m "Updates: describe what changed"
git push origin main

# OCH exportera workspace
python SANDBOX_EXPORT.py
```

### Säkerhetskopior:

1. **GitHub** - Source code och config
2. **Sandbox-export** - Full workspace snapshot
3. **Host (om möjligt)** - Lokala backups

## Viktiga Filer att ALDRIG committa

Dessa är redan i `.gitignore`:

```
.env                    # API keys
*.db                    # Databases
Datacenter_Export_*.zip # Export archives
__pycache__/           # Python cache
.venv/                 # Virtual environment
```

## Konfiguration för säkerhet

### 1. GitHub Personal Access Token (PAT)

```bash
# Använd PAT istället för lösenord
git config --global user.email "email@example.com"
# Använd PAT när den frågas om lösenord
```

### 2. .env.example (för dokumentation)

Skapa `.env.example` med exempel:

```
# .env.example (COMMIT THIS)
ANTHROPIC_API_KEY=your-key-here
LANGSMITH_API_KEY=your-key-here
DATABASE_URL=postgresql://localhost:5432/datacenter
```

Sedan:

```bash
# .env (DO NOT COMMIT - redan i .gitignore)
ANTHROPIC_API_KEY=sk-ant-xxxxx
LANGSMITH_API_KEY=lsm-xxxx
```

## Snabb-referens

```bash
# Se status
git status

# Se senaste commits
git log --oneline -10

# Se vad som förändrades
git diff

# Undo senaste ändringar (lokalt)
git checkout -- .

# Se vad som kommer committas
git diff --cached

# Undo senaste commit (om inte push:ad)
git reset --soft HEAD~1
```

## GitHub Actions (framtida)

Du kan sätta upp CI/CD för att:
- Köra TEST_MEMORY.py på varje push
- Validera filstruktur
- Kontrollera att .gitignore är korrekt

Se [GitHub Actions documentation](https://docs.github.com/en/actions).

## Sync mellan Sandbox och Host

Med GitHub:

```
Host Computer
     ↓
GitHub (cloud)
     ↓
Windows Sandbox
```

1. Gör ändringar i sandbox
2. `git push` för backup
3. Nästa session: `git clone` eller `git pull`
4. Sandbox-export + GitHub = dubbel säkerhet

## Rekommendationer

1. **Commit ofta** - Små, fokuserade commits
2. **Bra meddelanden** - "Lägg till X-funktion" inte bara "uppdatering"
3. **Push dagligen** - Innan du stänger sandbox
4. **Använd branches** - För större features
5. **Keep .env säker** - Aldrig commita secrets

## Troubleshooting

**Problem: Authentication failed**
```bash
# Använd Personal Access Token istället för lösenord
# Generera på: https://github.com/settings/tokens
```

**Problem: Repository redan existerar**
```bash
# Remove old connection
git remote remove origin

# Lägg till ny
git remote add origin https://github.com/USERNAME/datacenter.git
```

**Problem: Vill INTE committa en fil**
```bash
# Ta bort från tracking (men behåll lokalt)
git rm --cached filename.txt

# Lägg till i .gitignore
echo "filename.txt" >> .gitignore

# Commit ändringarna
git commit -m "Remove tracked file: filename.txt"
```

---

**Säkerhet först:** GitHub är för kod, inte för API-nycklar. `.gitignore` skyddar dina secrets!
