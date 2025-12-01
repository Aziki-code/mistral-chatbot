# GitHub Copilot Integration Guide

## Sådan får du din GitHub Token

### Trin 1: Gå til GitHub Settings
1. Log ind på [GitHub](https://github.com)
2. Klik på dit profilbillede øverst til højre
3. Vælg **Settings**
4. Scroll ned i venstre sidebar og klik på **Developer settings**
5. Klik på **Personal access tokens** → **Tokens (classic)**

### Trin 2: Opret nyt token
1. Klik på **Generate new token** → **Generate new token (classic)**
2. Giv dit token et beskrivende navn, f.eks. "AzikiAI Chatbot"
3. Vælg en udløbsdato (anbefalet: 90 dage eller No expiration for test)
4. Vælg følgende scopes:
   - ✅ `read:user` - Læs brugerdata
   - ✅ `copilot` - Adgang til GitHub Copilot (hvis tilgængelig)
   
5. Klik på **Generate token** nederst

### Trin 3: Kopier token
1. **VIGTIGT:** Kopier token'et NU - du kan ikke se det igen!
2. Token'et ser sådan ud: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Trin 4: Tilføj til .env filen
1. Åbn/opret `.env` filen i projektets rodmappe
2. Tilføj linjen:
   ```
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   (erstatt med dit faktiske token)

### Alternative: GitHub Models API
Hvis du ikke har adgang til Copilot API, kan du også bruge GitHub Models:
- Samme token fungerer
- Chatbotten vil automatisk vælge den rigtige endpoint
- Gratis adgang til GPT-4o og andre modeller

### Fejlfinding
**Problem:** "GITHUB_TOKEN not found"
- Løsning: Sørg for at `.env` filen er i samme mappe som `chatbot_sql.py`

**Problem:** "Error communicating with GitHub API"
- Løsning 1: Tjek at dit token har de rette scopes
- Løsning 2: Tjek at dit token ikke er udløbet
- Løsning 3: Brug Mistral AI som fallback (tilføj MISTRAL_API_KEY til .env)

## Fordele ved GitHub Copilot
- ✅ Bruger dine eksisterende GitHub credentials
- ✅ Kraftfuld GPT-4 baseret AI
- ✅ Optimeret til kodning og programmering
- ✅ Sikker og enterprise-ready
- ✅ Automatisk fallback til Mistral AI hvis GitHub ikke er tilgængelig

## Sikkerhed
- 🔒 Gem ALDRIG dit token i git repositories
- 🔒 `.env` filen er allerede i `.gitignore`
- 🔒 Rotér tokens regelmæssigt (hver 90 dag)
- 🔒 Brug kun minimal scopes der er nødvendige
