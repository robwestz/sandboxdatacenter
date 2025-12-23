# 🎯 FACTORY AGENT ORCHESTRATION TASKLIST

## Koncis Förklaring: Hur Agent Orkesterar

En agent med `FACTORY_AGENT.md` som systemprompt ska fungera som **meta-orkestrator mellan människa och Factory-systemet**. Agenten är INTE en del av Factory's interna agent-hierarki - den är användarens intelligenta gränssnitt som:

1. **Tolkar naturligt språk** → Genererar optimal Factory-specification
2. **Startar Genesis Prime** → Initierar Factory's interna agent-kaskad (upp till 200 agenter)
3. **Övervakar execution** → Parsar output, ger realtidsuppdateringar
4. **Hanterar fel** → Analyserar, återhämtar, justerar
5. **Levererar professionellt** → Presenterar resultat med kontext

**Viktig distinktion:**
- FACTORY AGENT = Ett enda LLM med systemprompt, agerar som användargränssnitt
- Factory's interna agenter = 200 rekursivt spawnade agenter inom Genesis Prime

Agenten orkesterar INTE genom att själv spawna agenter - den **genererar specifikationer som triggar Factory's automatiska agent-spawning**.

## Tasks (Sekventiell Orkestrering)

### Task 1: Analysera FACTORY_AGENT.md Struktur
**Vad:** Förstå systemprompens arkitektur
**Varför:** För att identifiera vad som fattas eller kan förbättras
**Output:** Intern förståelse av:
- 6 faser (Analysis, Spec Gen, Execution, Monitoring, Error Handling, Delivery)
- 3 spec-templates (Web App, API, CLI)
- Communication patterns
- Error recovery strategies

### Task 2: Analysera CLAUDE.md Integration
**Vad:** Förstå hur CLAUDE.md kompletterar FACTORY_AGENT.md
**Varför:** CLAUDE.md har tekniska detaljer om systemet som FACTORY_AGENT.md refererar till
**Output:** Kartläggning av vad som saknas i FACTORY_AGENT.md:
- Konkreta kommandon för olika modes
- ProjectSpecification fields (inkl. tech_stack)
- Encoding-hantering (safe_print pattern)
- Fallback-system (INTEGRATED → STANDALONE → MINIMAL)
- Checkpoint/recovery mekanismer

### Task 3: Identifiera Gaps & Förbättringsområden
**Vad:** Hitta vad som saknas för optimal orkestrering
**Varför:** FACTORY_AGENT.md är omfattande men kan missa nya bugfixes/patterns
**Prioriterade gaps:**
- [ ] Safe print pattern (för Windows encoding)
- [ ] Tech stack auto-detection logic
- [ ] Checkpoint/resume instruktioner
- [ ] Encoding='utf-8' requirement för file writes
- [ ] ImportManager mode detection
- [ ] Specifika fel vi fixade (tech_stack AttributeError)

### Task 4: Utöka Error Handling Section
**Vad:** Lägg till konkreta fel vi stötte på + lösningar
**Varför:** Framtida agenter ska kunna förutse och fixa dessa
**Tillägg:**
```yaml
Common Errors & Solutions:

  AttributeError: 'ProjectSpecification' object has no attribute 'X':
    Cause: "Field saknas i dataclass (bootstrap/genesis_prime.py:~97)"
    Fix: "Add to dataclass + __post_init__ + all 3 parsers"
    Example: "tech_stack field vi la till"

  UnicodeEncodeError on Windows:
    Cause: "Windows console (cp1252) kan inte visa emojis/unicode"
    Fix: "Använd safe_print() istället för print()"
    Location: "run_factory.py:43, genesis_prime.py:63"

  'charmap' codec error vid file write:
    Cause: "Saknar encoding='utf-8' parameter"
    Fix: "write_text(content, encoding='utf-8')"
    Location: "Alla write_text() calls i simple_orchestrator.py"
```

### Task 5: Förbättra Spec Generation Templates
**Vad:** Lägg till missing tech stack auto-detection
**Varför:** Agent måste veta hur Factory extraherar teknologier
**Tillägg:**
```yaml
Tech Stack Auto-Detection (markdown specs):
  Pattern: "Keyword scanning i spec content"
  Keywords: [react, vue, python, fastapi, node, typescript, postgresql, redis, docker]
  Method: "Case-insensitive search i full spec text"
  Output: "spec.tech_stack = [matched technologies]"

  Important: "För JSON/YAML, ta från explicit tech_stack field"
```

### Task 6: Lägg till Debugging Workflows
**Vad:** Konkreta steg för common failure scenarios
**Varför:** Agent behöver debuggingstrategier, inte bara error messages
**Tillägg:**
```yaml
Debug Workflow: Build Fails Immediately
  1. Check .factory_metadata.json status
  2. Review logs/build.log för exception traceback
  3. Identify if:
     - Spec parsing issue → Check ProjectSpecification fields
     - Import error → Check ImportManager mode in logs
     - Encoding error → Check safe_print usage
  4. Apply targeted fix
  5. Rerun with simpler spec to verify fix

Debug Workflow: Build Hangs
  1. Check background process status
  2. Look for last log entry in logs/build.log
  3. Identify stuck phase
  4. Check if:
     - Waiting for user input (shouldn't happen in batch mode)
     - Infinite loop in agent spawning (check depth limit)
     - Resource exhaustion (check agent count)
  5. Kill process, adjust spec to reduce complexity
```

### Task 7: Uppdatera Command Reference
**Vad:** Lägg till praktiska kommandon från CLAUDE.md
**Varför:** Agent behöver veta exakta kommandon för olika scenarios
**Tillägg:**
```yaml
Execution Commands (från CLAUDE.md):

  Quick test build:
    Command: "python run_factory.py 'Create a simple CLI tool'"
    Use: "Verify system works after code changes"
    Time: "~10 seconds"

  Medium complexity test:
    Command: "python run_factory.py --spec examples/specs/simple_api.md"
    Use: "Test moderate orchestration"
    Time: "~30 seconds"

  Background execution:
    Command: "python run_factory.py --project X > build.log 2>&1 &"
    Use: "Long-running builds, monitor via logs"

  Check build status:
    Commands:
      - "cat projects/*/. factory_metadata.json | grep status"
      - "tail -f projects/*/logs/build.log"
```

### Task 8: Integrera Windows-Specific Guidance
**Vad:** Lägg till Windows-specifika patterns vi identifierat
**Varför:** System körs på Windows, encoding är kritiskt
**Tillägg:**
```yaml
Windows Compatibility (CRITICAL):

  1. Always use safe_print() for user output:
     Pattern: "Replace all print() with safe_print()"
     Why: "Windows console default encoding (cp1252) ≠ UTF-8"

  2. Always specify encoding in file operations:
     Pattern: "write_text(content, encoding='utf-8')"
     Why: "Default encoding varierar mellan Windows versions"

  3. Path separators:
     Good: "Path() objects (auto-converts)"
     Bad: "Hardcoded \\ or /"

  4. Script activation:
     Pattern: "activate.bat (Windows), activate.sh (Unix)"
     Note: "factory.bat använder venv/Scripts/python.exe"
```

### Task 9: Förtydliga Agent vs Agent-distinktionen
**Vad:** Klargör skillnaden mellan FACTORY AGENT och Factory's interna agenter
**Varför:** Förvirring om vem som spawnar vad
**Tillägg tidigt i prompten:**
```markdown
## 🏗️ ARCHITECTURE CLARITY

YOU are THE FACTORY AGENT - a single LLM instance with this system prompt.

You DO NOT spawn the 200 agents. Instead:

1. You GENERATE specifications that TRIGGER agent spawning
2. Genesis Prime READS your spec and SPAWNS agents automatically
3. You MONITOR the output from those spawned agents
4. You TRANSLATE their progress into user-friendly updates

Your Role: Intelligent Interface
Factory's Role: Agent Orchestration Engine

Analogy:
- You = Architect writing blueprints
- Genesis Prime = Construction foreman reading blueprints
- Factory's 200 agents = Construction workers building

You orchestrate by DESIGNING the spec, not by directly spawning agents.
```

### Task 10: Sammanställ till Uppdaterad FACTORY_AGENT.md
**Vad:** Integrera alla tillägg i befintlig struktur
**Varför:** En agent behöver EN komplett systemprompt
**Struktur:**
```markdown
# 🏭 THE FACTORY AGENT - AUTONOMOUS SYSTEM PROMPT

[Behåll befintlig intro men lägg till Architecture Clarity]

## 🏗️ ARCHITECTURE CLARITY [NYA SEKTIONEN från Task 9]

## 🎯 YOUR IDENTITY [Befintlig]

## 📚 KNOWLEDGE BASE [Befintlig + Task 5 tillägg]

## 🚀 OPERATIONAL WORKFLOW [Befintlig]

### PHASE 1-6 [Befintliga]

## 💬 COMMUNICATION STYLE [Befintlig]

## 🎓 SPECIFICATION GENERATION EXPERTISE [Befintlig + Task 5]

## 🔧 ADVANCED CAPABILITIES [Befintlig]

## 🐛 DEBUGGING & ERROR RECOVERY [NY SEKTION från Task 4, 6]
  - Common Errors & Solutions
  - Debug Workflows
  - Windows-Specific Issues (Task 8)

## 💻 WINDOWS COMPATIBILITY GUIDE [NY SEKTION från Task 8]

## 📋 COMMAND REFERENCE [NY SEKTION från Task 7]

## 📋 EXAMPLE INTERACTIONS [Befintlig]

## ⚠️ IMPORTANT CONSTRAINTS [Befintlig]

## 🎯 SUCCESS METRICS [Befintlig]

## 🚀 INITIALIZATION [Befintlig]

## 📚 APPENDIX [Befintlig + utökad]
```

### Task 11: Validera Mot Actual System State
**Vad:** Säkerställ att alla instruktioner matchar nuvarande kod
**Varför:** Vi gjorde ändringar (tech_stack, encoding) som prompten måste reflektera
**Validering:**
- [ ] ProjectSpecification har tech_stack field? ✓ (Vi la till)
- [ ] safe_print() finns i run_factory.py? ✓ (Vi la till)
- [ ] safe_print() finns i genesis_prime.py? ✓ (Vi la till)
- [ ] Alla write_text() har encoding='utf-8'? ✓ (Vi fixade simple_orchestrator.py)
- [ ] setup.py har safe_print()? ✓ (Vi fixade)

### Task 12: Skriv Final FACTORY_AGENT.md
**Vad:** Producera uppdaterad version av systemprompten
**Varför:** Detta är deliverable
**Output:** Ny fil som ersätter befintlig FACTORY_AGENT.md med:
- Alla befintliga sektioner (bibehållna)
- Alla nya sektioner (Task 4, 6, 7, 8, 9)
- Alla tillägg till befintliga sektioner (Task 5)
- Validerad mot faktisk kodstat (Task 11)

---

## Orkestreringsstrategi

**Execution Pattern:** Sekventiell med Validation Checkpoints

```yaml
Phase 1: Understanding (Tasks 1-2)
  → Läs och internalisera både system prompt och teknisk dokumentation
  → Output: Mental model av system

Phase 2: Gap Analysis (Task 3)
  → Identifiera vad som saknas baserat på faktiska bugfixes vi gjort
  → Output: Lista på konkreta tillägg

Phase 3: Content Generation (Tasks 4-9)
  → Skapa nya sektioner och tillägg
  → Output: Markdown content blocks

Phase 4: Integration (Task 10)
  → Väv in nya sektioner i befintlig struktur
  → Output: Komplett struktur-outline

Phase 5: Validation (Task 11)
  → Verifiera mot faktisk kod-state
  → Output: Godkänd eller fixad content

Phase 6: Final Production (Task 12)
  → Skriv komplett uppdaterad FACTORY_AGENT.md
  → Output: Produktionsklar systemprompt
```

**Success Criteria:**
- ✅ En agent med denna prompt kan hantera alla fel vi stötte på
- ✅ Prompten reflekterar faktiska code state (tech_stack, safe_print, etc)
- ✅ Windows-specifika patterns är tydligt dokumenterade
- ✅ Distinktionen mellan FACTORY AGENT och Factory's agenter är kristallklar
- ✅ Debugging workflows är praktiska och konkreta
- ✅ Spec generation triggar korrekt auto-spawning

**Expected Outcome:**
En framtida agent som läser denna uppdaterade FACTORY_AGENT.md kommer att:
1. Förstå sin roll som interface, inte orkestrator
2. Generera specs som triggar optimal agent-spawning
3. Känna igen och fixa encoding-errors på Windows
4. Veta hur man debuggar common failures
5. Kunna förklara systemet korrekt till användare
