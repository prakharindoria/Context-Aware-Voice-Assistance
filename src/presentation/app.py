import streamlit as st
import requests
import os
import edge_tts
import asyncio
import io

# Configuration
BACKEND_URL = os.getenv("WHISPER_SHIELD_BACKEND_URL", "http://localhost:8000")

async def _generate_edge_tts(text: str) -> bytes:
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    audio_fp = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_fp.write(chunk["data"])
    return audio_fp.getvalue()
API_TOKEN = os.getenv("WHISPER_SHIELD_API_TOKEN", "whisper-shield-dev-token-2026")

st.set_page_config(page_title="WhisperShield AI", page_icon="🛡️", layout="wide")

st.title("🛡️ WhisperShield AI")
st.markdown("""
### Context-Aware Voice Privacy Assistant
Securely transcribe and analyze your voice notes for privacy risks before they leave your device.
""")

st.sidebar.header("Settings")
backend_url = st.sidebar.text_input("Backend URL", value=BACKEND_URL)
api_token = st.sidebar.text_input("API Token", value=API_TOKEN, type="password")

# Audio input component
audio_file = st.audio_input("Record your voice")

if audio_file:
    st.audio(audio_file, format="audio/wav")
    
    if st.button("Analyze Privacy Risk"):
        with st.spinner("Transcribing and analyzing..."):
            try:
                # Prepare request
                files = {"file": ("audio.wav", audio_file.getvalue(), "audio/wav")}
                headers = {"X-API-Token": api_token}
                
                response = requests.post(
                    f"{backend_url}/analyze-privacy",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Transcript")
                        st.info(result["transcript"])
                        
                        st.subheader("Detected Privacy Entities")
                        if result["detected_entities"]:
                            for entity in result["detected_entities"]:
                                st.warning(f"- **{entity['text']}** ({entity['entity_type']}): Risk {entity['risk_score']}")
                        else:
                            st.success("No specific PII keywords detected.")

                    with col2:
                        st.subheader("Privacy Assessment")
                        risk_level = result["risk_level"]
                        
                        if risk_level == "CRITICAL":
                            st.error(f"Risk Level: {risk_level}")
                        elif risk_level == "HIGH":
                            st.warning(f"Risk Level: {risk_level}")
                        else:
                            st.success(f"Risk Level: {risk_level}")
                            
                        st.metric("Privacy Risk Score", f"{result['score']:.2f}")
                        st.subheader("Recommendation")
                        st.markdown(f"> {result['recommendation']}")

                    # Generate Audio output
                    summary_text = f"Transcript: {result['transcript']}. "
                    if result["detected_entities"]:
                        summary_text += "Detected Privacy Entities: "
                        for entity in result["detected_entities"]:
                            summary_text += f"{entity['text']} is a {entity['entity_type']} with risk {entity['risk_score']}. "
                    else:
                        summary_text += "No specific PII keywords detected. "
                    summary_text += f"Privacy Assessment: Risk Level is {result['risk_level']}. "
                    summary_text += f"Privacy Risk Score: {result['score']:.2f}. "
                    summary_text += f"Recommendation: {result['recommendation']}"

                    audio_bytes = asyncio.run(_generate_edge_tts(summary_text))

                    import base64
                    b64 = base64.b64encode(audio_bytes).decode()
                    md = f"""
                        <audio controls autoplay="true">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                        """
                    st.markdown(md, unsafe_allow_html=True)
                
                else:
                    st.error(f"Backend error ({response.status_code}): {response.text}")
                    
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

st.divider()
st.caption("WhisperShield AI MVP - Built with Clean Architecture & Azure OpenAI")
