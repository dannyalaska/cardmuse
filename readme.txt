Card Muse 💌 — Personalized Greeting Card Generator
==================================================

Card Muse is a cozy and clever AI-powered greeting card creator that helps you craft beautiful, poetic cards — complete with illustrations, heartfelt messages, and stylish fonts. Inspired by Hallmark magic and Minted-style design, this app brings warmth and whimsy to digital cardmaking.

🎨 Features
----------

✨ Conversational interface — powered by Claude 3.5 Sonnet (via Anthropic API)
✨ Dynamic card style detection and tone matching
✨ AI-generated image prompts (Flux 1 Dev) for visual design
✨ Streamlit UI with editable prompt previews
✨ PIL-rendered inside messages with classic fonts
✨ (Coming soon) JS overlay for adding text on card covers
✨ Metadata tracking and prompt/seed-based image matching
✨ Local-first, private, and offline-ready

🖥 Requirements
--------------

- Python 3.11+
- ComfyUI running locally with a Flux-compatible workflow
- Claude API key (Anthropic)
- Optional: Phi-3 for metadata parsing (local)
- Streamlit
- Requests, PIL, Glob, JSON

📂 Folder Structure
------------------

card-generator/ 
├── app.py # Main Streamlit interface 
├── image_generator.py # Sends prompt to ComfyUI + waits for exact match 
├── metadata_extractor.py # Extracts context + fallback image prompts 
├── model_router.py # Routes LLM calls (Claude + Phi) 
├── config.py # Contains Anthropic API key 
├── inside_generator.py # (In progress) PIL-based text rendering 
├── cardmuse_one.json # Your Flux workflow for generation └── output/ # Where ComfyUI saves image outputs


🚀 Getting Started
------------------

1. Clone the repo  
2. Install dependencies  
3. Add your `config.py` with `ANTHROPIC_API_KEY`  
4. Run ComfyUI with `cardmuse_one.json` loaded  
5. Start the app:
   ```bash
   streamlit run app.py
   