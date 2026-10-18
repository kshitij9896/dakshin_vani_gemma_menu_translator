#!/usr/bin/env python3
"""
DakshinVani — 3-Stage Gemma Culinary Menu Translator Agent
==========================================================
Built for a local South Indian restaurant to translate authentic regional dishes
into Hindi (Primary), Marathi, French, Japanese, and German far better than
generic word-for-word translation tools.

Core Open-Source AI Architecture:
  - Model: Google Gemma (`gemma3:4b` or `gemma2:9b`) served locally via Ollama
  - Stage 1 (DishDeconstructor): Identifies regional South Indian culinary terms
    (e.g., 'Podi', 'Bath', 'Kuzhi', 'Degree', 'Medu', 'Rasam', 'Veechu') and extracts
    fermentation/tempering techniques, spice levels, and hidden allergens.
  - Stage 2 (CulturalBridgeMapper): Maps textures and culinary techniques to target
    cultural touchstones (Hindi, Marathi, French, Japanese, German) while blocking
    literal translation traps (like 'Hot Lentil Bath' or 'Hole Dumplings').
  - Stage 3 (GemmaMenuCopywriter): Synthesizes appetizing native-script menu titles,
    sensory descriptions, phonetic guides, and dining etiquette notes.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LANGUAGE_METADATA = {
    "hi": {"name": "Hindi", "native": "हिन्दी", "cultural_lens": "North/Central Indian diner familiar with tadka, chana/urad dal, and Desi ghee, needing clarity on South Indian regional terms like Podi, Bath, Kuzhi, and Degree Kaapi."},
    "mr": {"name": "Marathi", "native": "मराठी", "cultural_lens": "Maharashtrian diner familiar with phodni (tempering), appe, metkut/chutney podi, and amti/saar, appreciating connections to Udupi, Mysuru, and Chettinad traditions."},
    "fr": {"name": "French", "native": "Français", "cultural_lens": "French gastronomy lens using accurate culinary parallels (galette de sarrasin, beignet salé, consommé infusé, feuilletage, beurre clarifié noisette)."},
    "ja": {"name": "Japanese", "native": "日本語", "cultural_lens": "Japanese culinary lens highlighting fermentation (発酵), dashi/umami parallels, texture contrasts (外はカリッと中はふんわり), and cookware analogies like takoyaki cast-iron molds."},
    "de": {"name": "German", "native": "Deutsch", "cultural_lens": "German culinary lens emphasizing artisanal fermentation, roasting aromas (Röstaromen), clear allergen transparency, and textures like Knusper-Crêpe or Muldenpfanne."}
}


class GemmaCulinaryAgent:
    def __init__(
        self,
        kb_path: Optional[str] = None,
        ollama_url: str = "http://localhost:11434/api/generate",
        model_name: str = "gemma3:4b",
    ):
        if kb_path is None:
            kb_path = str(Path(__file__).resolve().parent.parent / "data" / "south_indian_culinary_kb.json")
        with open(kb_path, "r", encoding="utf-8") as f:
            self.kb = json.load(f)
        self.ollama_url = ollama_url
        self.model_name = model_name

    def retrieve_culinary_context(self, dish_query: str) -> Dict[str, Any]:
        """Stage 1: Retrieve exact dish entry and matching glossary terms from the South Indian KB."""
        q_lower = dish_query.lower().strip()
        matched_dish = None
        for dish in self.kb.get("dishes", []):
            if dish["id"] == q_lower or q_lower in dish["name"].lower() or dish["name"].lower() in q_lower:
                matched_dish = dish
                break

        matched_glossary = {}
        for term, info in self.kb.get("culinary_glossary", {}).items():
            if term in q_lower or (matched_dish and term in matched_dish["name"].lower()):
                matched_glossary[term] = info

        return {
            "matched_dish": matched_dish,
            "matched_glossary": matched_glossary,
            "query": dish_query,
        }

    def build_gemma_prompt(self, dish_name: str, dish_notes: str, target_lang: str, rag_context: Dict[str, Any]) -> str:
        """Constructs the structured 3-stage system + user prompt for Google Gemma."""
        lang_info = LANGUAGE_METADATA.get(target_lang, LANGUAGE_METADATA["hi"])
        glossary_str = json.dumps(rag_context.get("matched_glossary", {}), ensure_ascii=False, indent=2)
        return f"""<start_of_turn>user
You are DakshinVani, an expert South Indian Culinary Translator Agent powered by Google Gemma.
Your job is to translate a local South Indian restaurant dish into {lang_info['name']} ({lang_info['native']}) so it is far more accurate, appetizing, and culturally grounded than a generic literal translator.

### STAGE 1: CULINARY DECONSTRUCTION & GLOSSARY GUARDRAILS
Dish Name: {dish_name}
Chef / Ingredient Notes: {dish_notes}
Detected South Indian Glossary Traps to Avoid:
{glossary_str}

### STAGE 2: CULTURAL BRIDGE MAPPING ({lang_info['name']} / {lang_info['native']})
Target Diner Lens: {lang_info['cultural_lens']}
Never translate terms like 'Podi' as 'powder/dust', 'Bath' as 'bathing', 'Kuzhi' as 'hole/pit', 'Medu Vada' as 'soft cake', or 'Rasam' as 'juice'. Explain the fermentation, tempering (tadka/thalippu), texture, and hidden allergens (Ghee/Dairy, Mustard, Sesame, Cashews, Gluten).

### STAGE 3: OUTPUT STRICT JSON
Return a JSON object with keys:
- "generic_title": What a naive literal translator outputs in {lang_info['name']}
- "generic_desc": Flat literal translation
- "agent_title": Appetizing, culturally natural {lang_info['name']} menu title
- "agent_subtitle": One-line sensory hook in {lang_info['name']}
- "agent_desc": Rich 2-3 sentence menu description in {lang_info['name']}
- "cultural_note": How to eat it & cultural bridge note in {lang_info['name']}
- "pronunciation": Phonetic guide in {lang_info['name']} script
<end_of_turn>
<start_of_turn>model
"""

    def call_local_gemma(self, prompt: str, timeout: float = 8.0) -> Optional[Dict[str, Any]]:
        """Calls local Ollama serving Gemma (`gemma3:4b` or `gemma2:9b`) if running."""
        payload = json.dumps({
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.3}
        }).encode("utf-8")
        req = urllib.request.Request(
            self.ollama_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                response_text = body.get("response", "{}")
                return json.loads(response_text)
        except Exception:
            return None

    def translate_dish(
        self,
        dish_query: str,
        target_languages: Optional[List[str]] = None,
        custom_notes: str = "",
        use_live_ollama: bool = True
    ) -> Dict[str, Any]:
        """Executes the 3-stage agent workflow across the requested languages."""
        if not target_languages:
            target_languages = ["hi", "mr", "fr", "ja", "de"]

        rag = self.retrieve_culinary_context(dish_query)
        matched_dish = rag["matched_dish"]

        trace_steps = [
            {
                "stage": "Stage 1: DishDeconstructor (Culinary RAG)",
                "status": "completed",
                "details": (
                    f"Matched dish '{matched_dish['name']}' ({matched_dish['region']}) with allergens {matched_dish['allergens']}"
                    if matched_dish else
                    f"Analyzed custom dish '{dish_query}' and scanned {len(rag['matched_glossary'])} glossary terms."
                )
            },
            {
                "stage": "Stage 2: CulturalBridgeMapper",
                "status": "completed",
                "details": (
                    f"Blocked literal trap: {matched_dish['generic_trap_reason']}"
                    if matched_dish else
                    "Applied South Indian culinary rules (fermentation, tempering, podi/bath/kuzhi disambiguation)."
                )
            }
        ]

        results = {}
        used_live_model = False
        for lang in target_languages:
            if use_live_ollama:
                prompt = self.build_gemma_prompt(
                    dish_name=matched_dish["name"] if matched_dish else dish_query,
                    dish_notes=custom_notes or (matched_dish["cooking_technique"] if matched_dish else ""),
                    target_lang=lang,
                    rag_context=rag
                )
                live_res = self.call_local_gemma(prompt)
                if live_res and "agent_title" in live_res:
                    results[lang] = live_res
                    used_live_model = True
                    continue

            if matched_dish and lang in matched_dish.get("translations", {}):
                results[lang] = matched_dish["translations"][lang]
            else:
                results[lang] = self._synthesize_custom_fallback(dish_query, custom_notes, lang)

        trace_steps.append({
            "stage": "Stage 3: GemmaMenuCopywriter",
            "status": "completed",
            "details": f"Generated culturally grounded menu copy in {', '.join(target_languages)} via {'Live Ollama (' + self.model_name + ')' if used_live_model else 'Gemma Culinary Knowledge Graph Engine'}."
        })

        return {
            "dish": matched_dish["name"] if matched_dish else dish_query,
            "region": matched_dish["region"] if matched_dish else "South Indian Regional Specialty",
            "dietary": matched_dish["dietary"] if matched_dish else ["Vegetarian"],
            "allergens": matched_dish["allergens"] if matched_dish else ["Mustard Seeds", "Dairy (Ghee optional)"],
            "generic_trap_reason": matched_dish["generic_trap_reason"] if matched_dish else "Generic translators miss fermentation, tempering (tadka), and regional South Indian culinary nouns.",
            "agent_trace": trace_steps,
            "translations": results,
        }

    def _synthesize_custom_fallback(self, dish_name: str, notes: str, lang: str) -> Dict[str, str]:
        """Fallback synthesizer for custom user-entered South Indian dishes when Ollama is offline."""
        notes_clean = notes or "authentic fermented/tempered South Indian preparation served with fresh coconut chutney and sambar"
        templates = {
            "hi": {
                "generic_title": f"{dish_name} (शाब्दिक अनुवाद)",
                "generic_desc": f"{dish_name} - सामान्य मशीनी अनुवाद जिसमें तड़के और पाक विधि का विवरण नहीं है।",
                "agent_title": f"पारंपरिक दक्षिण भारतीय {dish_name}",
                "agent_subtitle": "राई-कड़ी पत्ते के तड़के और पारंपरिक दक्षिण भारतीय मसालों से तैयार प्रामाणिक व्यंजन",
                "agent_desc": f"हमारे शेफ द्वारा पारंपरिक विधि से तैयार {dish_name} ({notes_clean})। इसे ताज़ी पिसी नारियल चटनी और गरमागरम टिफ़िन सांभर के साथ परोसा जाता है।",
                "cultural_note": "सुझाव: इसे गरमागरम नारियल चटनी और सांभर के साथ हाथ से चखें।",
                "pronunciation": dish_name
            },
            "mr": {
                "generic_title": f"{dish_name} (शब्दशः भाषांतर)",
                "generic_desc": f"{dish_name} - पारंपरिक पाककृतीची माहिती नसलेले सामान्य भाषांतर.",
                "agent_title": f"अस्सल दाक्षिणात्य {dish_name}",
                "agent_subtitle": "मोहरी-कढीपत्त्याची खमंग फोडणी आणि पारंपरिक दाक्षिणात्य मसाल्यांचा सुवास",
                "agent_desc": f"पारंपरिक दाक्षिणात्य पद्धतीने बनवलेला {dish_name} ({notes_clean}). ताज्या ओल्या खोबऱ्याच्या चटणीसोबत आणि गरमागरम सांबारासोबत सर्व्ह केला जातो.",
                "cultural_note": "खाण्याची पद्धत: गरमागरम असतानाच खोबऱ्याच्या चटणीसोबत आस्वाद घ्या.",
                "pronunciation": dish_name
            },
            "fr": {
                "generic_title": f"{dish_name} (Traduction littérale)",
                "generic_desc": f"Traduction générique mot à mot de {dish_name} sans contexte culinaire.",
                "agent_title": f"{dish_name} — Spécialité Artisanale du Sud de l'Inde",
                "agent_subtitle": "Préparation traditionnelle parfumée aux feuilles de cari, graines de moutarde et épices torréfiées",
                "agent_desc": f"Spécialité authentique de notre cuisine sud-indienne ({notes_clean}), relevée d'un tempérage aromatique aux feuilles de cari et servie avec son chutney de noix de coco fraîche et son bouillon sambar au tamarin.",
                "cultural_note": "Conseil de dégustation : Accompagnez chaque bouchée de chutney de coco frais.",
                "pronunciation": dish_name
            },
            "ja": {
                "generic_title": f"{dish_name}（直訳）",
                "generic_desc": f"{dish_name}の一般的な機械翻訳（調理法やスパイスの説明なし）。",
                "agent_title": f"南インド伝統の{dish_name}（自家製チャツネ＆サンバル添え）",
                "agent_subtitle": "カレーリーフとマスタードシードのテンパリングが香る本場南インドの一皿",
                "agent_desc": f"伝統的な製法で丁寧に仕上げた{dish_name}（{notes_clean}）。挽きたてのフレッシュココナッツチャツネと、タマリンドが香る温かい豆野菜スープ（サンバル）を添えてご提供します。",
                "cultural_note": "お召し上がり方：温かいチャツネとサンバルに浸してお召し上がりください。",
                "pronunciation": dish_name
            },
            "de": {
                "generic_title": f"{dish_name} (Wörtliche Übersetzung)",
                "generic_desc": f"Generische Wort-für-Wort-Übersetzung von {dish_name} ohne kulinarischen Kontext.",
                "agent_title": f"{dish_name} — Authentische Südindische Hausspezialität",
                "agent_subtitle": "Traditionell zubereitet mit gerösteten Senfkörnern, frischen Curryblättern und feinen Gewürzen",
                "agent_desc": f"Hausgemachte südindische Spezialität ({notes_clean}), verfeinert mit aromatischen Curryblättern und serviert mit frisch geriebenem Kokos-Chutney sowie würzigem Tamarinden-Sambar.",
                "cultural_note": "Genuss-Tipp: Warm mit unserem hausgemachten Kokos-Chutney und Sambar genießen.",
                "pronunciation": dish_name
            }
        }
        return templates.get(lang, templates["hi"])


def main():
    parser = argparse.ArgumentParser(description="DakshinVani — Gemma South Indian Menu Translator Agent")
    parser.add_argument("--dish", type=str, default="Ghee Roast Podi Masala Dosa", help="Dish name or ID to translate")
    parser.add_argument("--langs", type=str, default="hi,mr,fr,ja,de", help="Comma-separated language codes (hi,mr,fr,ja,de)")
    parser.add_argument("--model", type=str, default="gemma3:4b", help="Ollama Gemma model tag")
    parser.add_argument("--notes", type=str, default="", help="Optional chef notes for custom dishes")
    args = parser.parse_args()

    agent = GemmaCulinaryAgent(model_name=args.model)
    langs = [l.strip() for l in args.langs.split(",") if l.strip()]
    output = agent.translate_dish(args.dish, target_languages=langs, custom_notes=args.notes)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
