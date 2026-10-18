# Recording Your Agent Session with DevRelay (Antigravity & Claude Code)

Because **DevRelay** (`~/.devrelay/bin/dev_mlh_mcp_server`) is a local MCP server that reads and uploads agent transcripts directly from your local machine's coding agent (**Antigravity** or **Claude Code**), follow these 3 quick steps to record and attach your official session to your Hacktoberfest Week 2 DEV submission:

---

## Step 1: Verify DevRelay MCP Is Connected in Antigravity or Claude Code

Open your terminal in the unzipped `dakshin_vani_gemma_menu_translator` folder and confirm DevRelay is registered:

```bash
# Check that the DevRelay binary is present
ls -la ~/.devrelay/bin/dev_mlh_mcp_server
```

If you haven't run the installer recently, re-sync it across both **Antigravity** and **Claude Code**:
```bash
curl -fsSL https://devrelay.com/install.sh | sh
```

---

## Step 2: Run the 3-Turn Build & Verification Session in Antigravity or Claude Code

Open this project directory inside **Antigravity** or run `claude` (**Claude Code**) in your terminal, and paste the following 3 prompts in order so your local agent creates a rich, judge-friendly DevRelay session trace:

### Prompt 1 — Inspect & Run the Gemma 3-Stage South Indian Menu Agent
```text
We are building DakshinVani — an open-source South Indian Restaurant Menu Translator Agent powered by Google Gemma (gemma3:4b via Ollama) for the Hacktoberfest Week 2 Side Hustle challenge.
1. Inspect `data/south_indian_culinary_kb.json` and `agent/gemma_menu_agent.py`.
2. Run `python3 agent/gemma_menu_agent.py --dish "Ghee Roast Podi Masala Dosa" --langs hi,mr,fr,ja,de` and `python3 agent/gemma_menu_agent.py --dish "Mysuru Bisi Bele Bath with Kara Boondi" --langs hi,mr,fr,ja,de` in the terminal to verify how the 3-stage agent (DishDeconstructor -> CulturalBridgeMapper -> GemmaMenuCopywriter) avoids literal translation traps like "Powder Crepe" or "Hot Lentil Bath".
```

### Prompt 2 — Add a Custom Local Specialty & Run Benchmark Tests
```text
Now let's test custom dish synthesis and check the web app:
1. Run `python3 agent/gemma_menu_agent.py --dish "Rava Kesari Bath" --notes "Slow-roasted semolina pudding infused with Pampore saffron, ghee-fried cashews, and ripe pineapple" --langs hi,mr,fr,ja,de`.
2. Verify all 5 target languages (Hindi primary, Marathi, French, Japanese, and German) return generic-vs-agent comparisons, allergen tags, and cultural dining tips.
```

### Prompt 3 — Save the Agent Session & Draft the DEV Post via DevRelay MCP
```text
Use DevRelay (`devrelay-gateway`) to:
1. Check the active Hacktoberfest Week 2 challenge (`get_challenges`).
2. Save/share this agent session transcript via DevRelay so we get the embeddable DevRelay session link.
3. Create a private DEV draft (`create_article` with `published: false`) using the write-up in `DEV_SUBMISSION_POST.md`, tagged `#devchallenge`, `#hf26challenge`, `#gemma`, `#ai`, and embed our DevRelay session link!
```

---

## Step 3: Sign In When the Browser Popup Appears
The first time `devrelay-gateway` invokes `create_article` or saves your session transcript, it will open your browser to sign in with your **MLH / DEV** account. Approve the prompt, and your draft + embedded agent session will appear directly in your DEV dashboard (`https://dev.to/dashboard`)!
