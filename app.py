# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import tempfile

# ---------------------------
# Language mapping
# ---------------------------
LANGUAGES = {
    "Auto Detect": None,
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Dutch": "nl",
    "Bengali": "bn",
    "Urdu": "ur",
    "Arabic": "ar",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Odia": "or",
    "Nepali": "ne",
    "Sinhala": "si",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Malay": "ms",
    "Swahili": "sw",
    "Polish": "pl",
    "Czech": "cs",
    "Romanian": "ro",
    "Hungarian": "hu",
    "Greek": "el",
    "Turkish": "tr",
    "Korean": "ko",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
}

# ---------------------------
# Load API key
# ---------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env — add GEMINI_API_KEY=your_key and restart.")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="Simple GenAI App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# DARK MODE CSS - Always dark
# ---------------------------
st.markdown("""
<style>
/* Make sidebar always visible and nice */
[data-testid="stSidebar"] {
    background-color: #1e293b;
    padding: 20px;
    min-width: 250px !important;
}

/* Main app dark theme */
.stApp {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Cards for better UI */
.card {
    background: #1e293b;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    border: 1px solid #334155;
    color: #e2e8f0;
}

/* Buttons */
.stButton > button {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
    transition: all 0.3s;
}

.stButton > button:hover {
    background-color: #2563eb;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

/* Text areas */
.stTextArea textarea {
    border-radius: 10px;
    border: 2px solid #475569;
    font-size: 16px;
    padding: 15px;
    background-color: #1e293b;
    color: #e2e8f0;
}

.stTextArea textarea:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Radio buttons in sidebar */
[data-testid="stSidebar"] .stRadio > div {
    flex-direction: column;
    gap: 10px;
}

[data-testid="stSidebar"] .stRadio label {
    padding: 12px 15px;
    border-radius: 8px;
    border: 2px solid #475569;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.3s;
    width: 100% !important;
    display: block !important;
    background-color: #334155;
    color: #e2e8f0;
}

[data-testid="stSidebar"] .stRadio label:hover {
    border-color: #3b82f6;
    background-color: #475569;
}

[data-testid="stSidebar"] .stRadio input:checked + label {
    background-color: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

/* Hide default Streamlit elements we don't need */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Make all text white in sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] div {
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR - Always Dark Mode
# ---------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #3b82f6; margin-bottom: 5px;">🧠</h1>
        <h2 style="color: #e2e8f0; margin: 0;">GenAI App</h2>
        <p style="color: #94a3b8; font-size: 14px;">Three Powerful Tools in One</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature selection - This will show BOTH icons and text
    st.markdown("### Choose Feature")
    
    # This will display both icons and full text
    option = st.radio(
        "Select a feature:",
        ["📊 Sentiment Analysis", "✨ Text Generation", "🌍 Translator"],
        key="feature_selector"
    )
    
    st.markdown("---")
    
    # Quick tips - Simplified
    st.markdown("**Quick Info:**")
    st.markdown("""
    - Sentiment Analysis: Analyze emotions
    - Text Generation: Create content
    - Translator: Translate text/voice
    """)
    
    st.markdown("---")
    
    # API status
    if API_KEY:
        st.success("✓ API Connected")
    else:
        st.error("✗ API Error")

# ---------------------------
# MAIN CONTENT AREA
# ---------------------------
st.markdown(f"""
<div class="card">
    <h1 style="color: #e2e8f0; margin-top: 0;">
        {option.split(' ')[1] if ' ' in option else option}
    </h1>
    <p style="color: #94a3b8;">
        Welcome to your AI-powered workspace
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# SENTIMENT ANALYSIS
# ---------------------------
if "Sentiment Analysis" in option:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔍 Analyze Sentiment</h3>
            <p>Paste any text below to analyze its emotional tone.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Example sentiments
        with st.expander("📋 Try these examples", expanded=True):
            examples = {
                "Positive": "I absolutely love this product! It has changed my life for the better.",
                "Negative": "This is the worst service I've ever experienced. Never coming back.",
                "Neutral": "The package arrived on Tuesday as scheduled."
            }
            
            example_choice = st.selectbox("Load example:", ["Select..."] + list(examples.keys()))
            if example_choice != "Select...":
                user_text = examples[example_choice]
            else:
                user_text = ""
        
        user_input = st.text_area(
            "Enter text to analyze:",
            value=user_text,
            height=150,
            placeholder="Type or paste your text here...",
            key="sentiment_input"
        )
        
        analyze_col1, analyze_col2 = st.columns([1, 3])
        with analyze_col1:
            analyze_btn = st.button("🚀 Analyze", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📈 How It Works</h3>
            <p>Our AI analyzes:</p>
            <ul>
                <li>Positive sentiment 😊</li>
                <li>Negative sentiment 😠</li>
                <li>Neutral sentiment 😐</li>
            </ul>
            <p><small>Powered by Gemini AI</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    if analyze_btn:
        if not user_input.strip():
            st.warning("⚠️ Please enter some text to analyze.")
        else:
            with st.spinner("🤔 Analyzing sentiment..."):
                prompt = f"""
                Analyze the sentiment of this text and classify it as:
                - POSITIVE if it expresses happiness, satisfaction, or approval
                - NEGATIVE if it expresses anger, disappointment, or disapproval  
                - NEUTRAL if it's factual without strong emotion
                
                Text: "{user_input}"
                
                Respond with exactly one word: POSITIVE, NEGATIVE, or NEUTRAL
                """
                try:
                    resp = client.models.generate_content(
                        model="models/gemini-2.5-flash", 
                        contents=prompt
                    )
                    sentiment = resp.text.strip().upper()
                    
                    # Display result with nice UI
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("📊 Analysis Result")
                    
                    # Color-coded result
                    if "POSITIVE" in sentiment:
                        st.success(f"## 😊 {sentiment}")
                        st.progress(0.9)
                        st.markdown("This text expresses positive emotions!")
                    elif "NEGATIVE" in sentiment:
                        st.error(f"## 😠 {sentiment}")
                        st.progress(0.2)
                        st.markdown("This text expresses negative emotions.")
                    else:
                        st.info(f"## 😐 {sentiment}")
                        st.progress(0.5)
                        st.markdown("This text is neutral or factual.")
                    
                    st.markdown(f"**Text analyzed:** _{user_input[:100]}..._")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ---------------------------
# TEXT GENERATION
# ---------------------------
elif "Text Generation" in option:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>✨ Generate Text</h3>
            <p>Ask AI to write anything - stories, emails, code, or creative content.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prompt templates
        with st.expander("💡 Prompt Templates", expanded=True):
            templates = {
                "Creative Story": "Write a short story about a robot who discovers art",
                "Professional Email": "Write a professional email requesting a meeting",
                "Code Explanation": "Explain how a neural network works in simple terms",
                "Product Description": "Write a compelling description for a smart watch"
            }
            
            template_choice = st.selectbox("Use template:", ["Custom Prompt"] + list(templates.keys()))
            if template_choice != "Custom Prompt":
                user_prompt = templates[template_choice]
            else:
                user_prompt = ""
        
        prompt_input = st.text_area(
            "Enter your prompt:",
            value=user_prompt,
            height=120,
            placeholder="What would you like to create?",
            key="gen_prompt"
        )
        
        # Generation parameters
        col_a, col_b = st.columns(2)
        with col_a:
            tone = st.selectbox("Tone:", ["Professional", "Creative", "Casual", "Formal", "Friendly"])
        with col_b:
            length = st.selectbox("Length:", ["Short", "Medium", "Long"])
        
        generate_btn = st.button("✨ Generate", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🎯 Best Practices</h3>
            <ul>
                <li>Be specific in your prompt</li>
                <li>Mention desired length</li>
                <li>Specify tone/style</li>
                <li>Provide context when needed</li>
            </ul>
            <p><small>Tip: The clearer your prompt, the better the result!</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    if generate_btn:
        if not prompt_input.strip():
            st.warning("⚠️ Please enter a prompt.")
        else:
            with st.spinner("✨ Creating magic..."):
                enhanced_prompt = f"""
                You are a helpful AI assistant. Generate text with the following requirements:
                - Tone: {tone}
                - Length: {length}
                - Prompt: {prompt_input}
                
                Provide a well-structured, engaging response.
                """
                try:
                    resp = client.models.generate_content(
                        model="models/gemini-2.5-flash", 
                        contents=enhanced_prompt
                    )
                    
                    # Display result
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("📝 Generated Text")
                    st.markdown(resp.text)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Text",
                        data=resp.text,
                        file_name="generated_text.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ---------------------------
# TRANSLATOR
# ---------------------------
else:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🌍 AI Translator</h3>
            <p>Translate text or audio between 30+ languages instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Translation mode
        mode = st.radio(
            "Translation Mode:",
            ["📝 Text Translation", "🎤 Voice Translation"],
            horizontal=True
        )
        
        # Language selection
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            source_lang = st.selectbox(
                "From:",
                list(LANGUAGES.keys()),
                index=0,
                key="source_lang"
            )
        
        with lang_col2:
            target_lang = st.selectbox(
                "To:",
                list(LANGUAGES.keys()),
                index=list(LANGUAGES.keys()).index("Telugu") if "Telugu" in LANGUAGES else 1,
                key="target_lang"
            )
        
        # Text translation
        if "Text" in mode:
            st.markdown("### 📝 Enter Text")
            
            with st.expander("🌐 Example Texts", expanded=False):
                examples = {
                    "Hello, how are you?": "English",
                    "नमस्ते, आप कैसे हैं?": "Hindi",
                    "Hola, ¿cómo estás?": "Spanish"
                }
                for text, lang in examples.items():
                    if st.button(f"Use: '{text[:20]}...' ({lang})", key=text):
                        st.session_state.translate_text = text
            
            text_to_translate = st.text_area(
                "Text to translate:",
                value=st.session_state.get("translate_text", ""),
                height=120,
                placeholder="Type or paste text here...",
                key="translate_input"
            )
            
            translate_btn = st.button("🌐 Translate", type="primary", use_container_width=True)
            
            if translate_btn:
                if not text_to_translate.strip():
                    st.warning("⚠️ Please enter text to translate.")
                else:
                    with st.spinner("🔍 Translating..."):
                        prompt = f"""
                        Translate the following text from {source_lang} to {target_lang}:
                        
                        Text: "{text_to_translate}"
                        
                        Provide only the translation, no additional text.
                        """
                        try:
                            resp = client.models.generate_content(
                                model="models/gemini-2.5-flash", 
                                contents=prompt
                            )
                            translation = resp.text.strip()
                            
                            # Display results
                            st.markdown("<div class='card'>", unsafe_allow_html=True)
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.markdown(f"**Original ({source_lang}):**")
                                st.info(text_to_translate)
                            
                            with col_b:
                                st.markdown(f"**Translation ({target_lang}):**")
                                st.success(translation)
                            
                            # Audio output
                            st.markdown("### 🔊 Listen to Translation")
                            tts_lang = LANGUAGES.get(target_lang, "en")
                            try:
                                tts = gTTS(text=translation, lang=tts_lang)
                                audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                                tts.save(audio_file.name)
                                
                                st.audio(audio_file.name, format="audio/mp3")
                                
                                with open(audio_file.name, "rb") as f:
                                    st.download_button(
                                        "📥 Download Audio",
                                        f,
                                        file_name=f"translation_{target_lang}.mp3",
                                        mime="audio/mp3",
                                        use_container_width=True
                                    )
                            except Exception as e:
                                st.warning(f"Audio generation not available for {target_lang}")
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"❌ Translation error: {str(e)}")
        
        # Voice translation
        else:
            st.markdown("### 🎤 Upload Audio")
            st.info("Supported formats: MP3, WAV, M4A, OGG")
            
            audio_file = st.file_uploader(
                "Choose an audio file",
                type=["mp3", "wav", "m4a", "ogg", "flac"],
                key="audio_upload"
            )
            
            if audio_file is not None:
                # Show audio player
                st.audio(audio_file, format=f"audio/{audio_file.name.split('.')[-1]}")
                
                if st.button("🎤 Transcribe & Translate", type="primary", use_container_width=True):
                    with st.spinner("Processing audio..."):
                        # Save uploaded file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp:
                            tmp.write(audio_file.read())
                            audio_path = tmp.name
                        
                        try:
                            # Convert to WAV if needed
                            if not audio_path.endswith('.wav'):
                                sound = AudioSegment.from_file(audio_path)
                                wav_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
                                sound.export(wav_path, format="wav")
                            else:
                                wav_path = audio_path
                            
                            # Transcribe
                            recognizer = sr.Recognizer()
                            with sr.AudioFile(wav_path) as source:
                                audio_data = recognizer.record(source)
                            
                            src_lang_code = LANGUAGES.get(source_lang)
                            if src_lang_code:
                                transcript = recognizer.recognize_google(audio_data, language=src_lang_code)
                            else:
                                transcript = recognizer.recognize_google(audio_data)
                            
                            st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.subheader("📝 Transcription")
                            st.info(transcript)
                            
                            # Translate transcription
                            with st.spinner("Translating..."):
                                prompt = f"Translate from {source_lang} to {target_lang}: {transcript}"
                                resp = client.models.generate_content(
                                    model="models/gemini-2.5-flash", 
                                    contents=prompt
                                )
                                translation = resp.text.strip()
                                
                                st.subheader(f"🌐 Translation ({target_lang})")
                                st.success(translation)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"❌ Audio processing error: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🗣️ Supported Languages</h3>
            <p>30+ languages including:</p>
            <ul>
                <li>English 🇬🇧</li>
                <li>Hindi 🇮🇳</li>
                <li>Telugu 🇮🇳</li>
                <li>Spanish 🇪🇸</li>
                <li>French 🇫🇷</li>
                <li>Japanese 🇯🇵</li>
                <li>Chinese 🇨🇳</li>
                <li>Arabic 🇸🇦</li>
            </ul>
            <p><small>More languages added regularly</small></p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col1:
    st.markdown("🧠 **Simple GenAI App**")
with footer_col2:
    st.markdown("<div style='text-align: center; color: #94a3b8;'>Made with Streamlit & Gemini API</div>", unsafe_allow_html=True)
with footer_col3:
    st.markdown("<div style='text-align: right; color: #94a3b8;'>v1.0</div>", unsafe_allow_html=True)