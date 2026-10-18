---
title: "DakshinVani: A Local Gemma Agent That Saves South Indian Menus from 'Hot Lentil Bath' & 'Pit Dumplings'"
published: false
tags: devchallenge, hf26challenge, gemma, ai
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).*

## What I Built

**DakshinVani (दक्षिण वाणी)** translates South Indian restaurant menus into Hindi, Marathi, French, Japanese, and German — without falling into the literal-translation traps that make generic tools turn beloved dishes into nonsense or culinary horror.

Walk into an authentic South Indian tiffin room and run their menu through a generic translation tool. Suddenly, iconic dishes turn into comedy—or worse, culinary horror:

| Authentic Dish | Generic Translator Output (Literal Trap) | Why Diners Walk Away |
| :--- | :--- | :--- |
| **Mysuru Bisi Bele Bath** | *"गर्म दाल स्नान"* / *"Hot Lentil Bath"* / *"温かいレンズ豆のお風呂"* | Translates Kannada *Bath* (spiced rice dish) as a literal bath! |
| **Ghee Roast Podi Masala Dosa** | *"घी रोस्ट पाउडर डोसा"* / *"Clarified Butter Powder Crepe"* | Translates *Milagai Podi* (stone-ground roasted lentil & chili condiment) as industrial "powder/dust". |
| **Medu Vada with Tiffin Sambar** | *"सॉफ्ट दाल केक"* / *"Gâteau mou aux lentilles"* / *"柔らかい豆のケーキ"* | Translates *Medu* (soft interior) as a sweet/soggy "soft bean cake" instead of a crisp savory black-gram fritter. |
| **Chettinad Kuzhi Paniyaram** | *"गड्ढे के पकौड़े"* / *"Boulettes de fosse"* / *"穴の団子"* | Translates *Kuzhi* (cast-iron dimpled mold) as "pit/hole dumplings". |
| **Kumbakonam Degree Filter Kaapi** | *"तापमान फ़िल्टर कॉफ़ी"* / *"Temperature Filtered Coffee"* | Misses that *Degree* refers to lactometer-certified pure full-cream cow's milk pulled between a brass *Davara* and *Tumbler*. |

**DakshinVani** is an open-source, locally hosted **3-Stage Culinary Menu Translator Agent** powered by **Google Gemma (`gemma3:4b`)** that translates South Indian restaurant menus into **Hindi (हिन्दी — Primary)**, **Marathi (मराठी)**, **French (Français)**, **Japanese (日本語)**, and **German (Deutsch)**.

Who'd pay for this: small family-run tiffin rooms and South Indian restaurants abroad, who need accurate, appetizing multilingual menus for tourists and diaspora diners but can't afford a recurring SaaS translation subscription or risk their recipes being sent to third-party training pipelines.

## Demo

<!-- TODO: add deployed link once hosted. Locally, run `python -m uvicorn server:app --reload --port 8000` and open http://localhost:8000 -->

## Code

<!-- TODO: embed GitHub repo link once pushed -->

## How I Built It

### How the 3-Stage Gemma Agent Works
1. **Stage 1 — `DishDeconstructor` (Culinary RAG & Allergen Extraction)**: Scans dish names and chef notes against a curated South Indian Culinary Knowledge Base (`south_indian_culinary_kb.json`), flagging regional nouns (*Podi*, *Bath*, *Kuzhi*, *Degree*, *Medu*, *Rasam*, *Pesarattu*, *Veechu*), cooking vessels, fermentation times, and hidden allergens (A2 cow ghee, sesame oil, mustard seeds, cashews, urad dal).
2. **Stage 2 — `CulturalBridgeMapper`**: Maps textures and techniques to each target language's culinary intuition:
   - **Hindi (हिन्दी)**: Bridges South Indian tempering (*thalippu*) and *Podi/Bath* concepts for North/Central Indian diners.
   - **Marathi (मराठी)**: Connects *Kuzhi Paniyaram* to *Appe*, *Milagu Rasam* to digestive *Saar*, and *Bisi Bele Bath* to *Masale Bhat* with *Marathi Moggu* (kapok buds).
   - **French (Français)**: Uses precise gastronomic parallels (*galette dentelle fermentée*, *beignet salé crousti-moelleux*, *consommé au tamarin*, *feuilletage à la volée*).
   - **Japanese (日本語)**: Draws intuitive parallels to cast-iron *Takoyaki* molds for *Kuzhi Paniyaram*, *Ganmodoki* textures for *Medu Vada*, and *Ochazuke* dining style for *Rasam*.
   - **German (Deutsch)**: Highlights sourdough-style natural fermentation, *Gusseisen-Muldenpfanne* baking, and strict allergen clarity.
3. **Stage 3 — `GemmaMenuCopywriter`**: Generates print-ready multilingual menu cards with native script titles, sensory descriptions, phonetic pronunciation guides, and a *"How to Eat"* note.

## Why Does Open Innovation Matter?

Small family-run tiffin rooms operate on razor-thin margins. They won't pay $50/month for a recurring SaaS subscription just to translate seasonal specials, and they don't want their secret family spice ratios (*Bisi Bele Bath 18-spice masala* or *Milagai Podi* proportions) sent to third-party training pipelines.

By running **Google Gemma (`gemma3:4b`)** locally via **Ollama**:
- **Zero Marginal API Cost**: Once set up on a restaurant manager's laptop, translating new daily specials into 5 languages costs ₹0 / $0.
- **Domain Control Over Generic APIs**: Closed translation APIs don't let you inject a deterministic South Indian culinary ontology before decoding. With open-weight Gemma + our local JSON RAG graph, the restaurant owns both the glossary and the tone.
- **Offline Reliability**: Works entirely offline inside the restaurant kitchen or print shop.

## Prize Categories
- **Best Use of Gemma**: Uses Google's open-weight **Gemma** model (`gemma3:4b` / `gemma2:9b`) as the reasoning and multilingual copywriting engine in a 3-stage agentic pipeline.

## My Agent Session

{% agent_session 1002 %}

> *Session Link: [View interactive agent session on DEV](https://dev.to/agent_sessions/dakshinvani-building-an-open-source-gemma-south-indian-menu-translator-agent-mfuow8)*
> *Recorded with DevRelay in Google Antigravity (Gemini 3.8 Flash)*
