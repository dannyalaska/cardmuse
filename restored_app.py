
import streamlit as st
import requests
from image_generator import generate_card_image
from model_router import call_llm
from metadata_extractor import extract_metadata_from_llm

st.set_page_config(page_title="Card Muse", layout="centered")
st.title("Card Muse")
st.markdown("Your poetic paper muse 💌")

# --- Init ---
if "chat" not in st.session_state:
    st.session_state.chat = []
if "metadata" not in st.session_state:
    st.session_state.metadata = {}
if "image_prompt_ready" not in st.session_state:
    st.session_state.image_prompt_ready = False
if "image_prompt" not in st.session_state:
    st.session_state.image_prompt = ""
if "image_generated" not in st.session_state:
    st.session_state.image_generated = False
if "image_path" not in st.session_state:
    st.session_state.image_path = ""
if "image_prompt_suggestion" not in st.session_state:
    st.session_state.image_prompt_suggestion = ""
if "wants_inside" not in st.session_state:
    st.session_state.wants_inside = None

# --- Chat UI ---
for msg in st.session_state.chat:
    st.chat_message(msg["role"]).markdown(msg["content"])

user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    st.session_state.metadata.update(extract_metadata_from_llm(st.session_state.chat))
    reply = call_llm(st.session_state.chat)
    st.session_state.chat.append({"role": "assistant", "content": reply})

    # Try to find a valid image prompt suggestion
    for line in reply.split("\n"):
        if "design" in line.lower() and ("background" in line or "illustration" in line):
            if len(line) > 50:
                st.session_state.image_prompt_suggestion = "greeting card with " + line.strip().rstrip(".")
                break

    if st.session_state.image_prompt_suggestion:
        st.session_state.image_prompt = st.session_state.image_prompt_suggestion
        st.session_state.image_prompt_ready = True
    st.rerun()

# --- Generate Image Step ---
if st.session_state.image_prompt_ready and not st.session_state.image_generated:
    st.markdown("### I have a design idea based on what we discussed.")
    st.markdown("Edit or approve this image prompt:")
    st.session_state.image_prompt = st.text_area("Image Prompt", st.session_state.image_prompt, height=100)

    if st.button("🎨 Yes, generate this image"):
        st.markdown("### One moment while I paint something lovely...")
        with st.spinner("Rendering your card... This usually takes 1–2 minutes."):
            image_path, error = generate_card_image(st.session_state.image_prompt)
            if image_path:
                st.image(image_path, caption="Card Cover", use_container_width=True)
                st.session_state.image_generated = True
                st.session_state.image_path = image_path
            else:
                st.warning(error or "No image generated.")
        st.rerun()

# --- Inside Message Decision ---
if st.session_state.image_generated and st.session_state.wants_inside is None:
    st.markdown("Would you like to add a personal message inside the card?")
    if st.button("Yes, help me write one"):
        st.session_state.wants_inside = True
        st.rerun()
    elif st.button("Skip the inside"):
        st.session_state.wants_inside = False
        st.rerun()
