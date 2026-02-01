import streamlit as st
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="TAKE CONTROL - Paolo Alonge",
    page_icon="assets/logo-premium.png",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom Styling - BRAND COLORS (Blue & Black)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    /* Global Text and Background Enforcement */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Outfit', sans-serif;
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #1a1a1a;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #007BFF 0%, #00BFFF 100%);
        color: #ffffff;
        border: none;
        border-radius: 4px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        padding: 0.6rem 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00BFFF 0%, #007BFF 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Dividers */
    hr {
        border-top: 1px solid #1a1a1a;
        margin: 2rem 0;
    }
    
    /* Expander/Cards */
    .streamlit-expanderHeader {
        background-color: #0a0a0a;
        color: #ffffff;
        border-radius: 4px;
        border: 1px solid #1a1a1a;
    }
    
    /* Custom Classes */
    .highlight {
        color: #007BFF;
        font-weight: bold;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #080808;
        color: #ffffff;
        border: 1px solid #1a1a1a;
        border-radius: 4px;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #007BFF;
        box-shadow: 0 0 0 1px #007BFF;
    }

    /* Hero Section Branding */
    .brand-header {
        padding: 20px 0;
        text-align: left;
    }
    .brand-name {
        font-size: 24px;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 0px;
    }
    .brand-alonge {
        color: #007BFF;
    }
    .brand-subtitle {
        color: #007BFF;
        font-size: 16px;
        margin-top: -5px;
        font-weight: 400;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 600;
        margin: 40px 0;
        line-height: 1.2;
    }
    </style>
""", unsafe_allow_html=True)
# API Setup
# Priority: 1. Streamlit Secrets (Cloud) 2. Environment Variable (Local)
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("assets/logo-premium.png", use_container_width=True)
    except:
        pass
    
    st.markdown("### ⚙️ Impostazioni")
    
    # API Key Handling for User Override or Missing Key
    if not api_key:
        st.warning("⚠️ Chiave API di sistema non trovata.")
        st.caption("Per uso pubblico, configurare i Secrets.")
        user_api_key = st.text_input("Inserisci Gemini API Key", type="password")
        if user_api_key:
            genai.configure(api_key=user_api_key)
            st.success("Chiave caricata!")
    else:
        st.success("✅ App Connessa (Licenza Attiva)")
        genai.configure(api_key=api_key)
    
    # Automatic Model Selection - Defaulting to the best current model (2.0 Flash)
    selected_model_name = "models/gemini-2.0-flash"
    
    try:
        model = genai.GenerativeModel(selected_model_name)
    except Exception as e:
        # Fallback to 1.5 Flash if 2.0 isn't available
        try:
            selected_model_name = "models/gemini-1.5-flash"
            model = genai.GenerativeModel(selected_model_name)
        except Exception as e_inner:
            st.error(f"Errore inizializzazione modello: {e_inner}")

    st.markdown("---")
    st.markdown("**Il Metodo Paolo Alonge**")
    st.info("Ricorda: Non sono le cose a turbarci, ma il nostro giudizio su di esse. - Epitteto")
    st.caption("© 2026 Paolo Alonge Coaching")

# --- MAIN INTERFACE ---

# Brand Header
st.markdown("""
    <div class="brand-header">
        <div class="brand-name">PAOLO <span class="brand-alonge">ALONGE</span></div>
        <div class="brand-subtitle">Coach Gestione Rabbia e Stress</div>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero-title">Sei stanco di conflitti familiari e stress da lavoro?<br>Scopri il Coaching per Genitori e Professionisti</div>', unsafe_allow_html=True)

st.divider()


# 2. Emotional Logger
st.subheader("🧠 Emotional Logger")
st.markdown("Come ti senti in questo momento? Riconoscere l'emozione è il primo passo per controllarla.")

col1, col2 = st.columns(2)
with col1:
    emotional_state = st.selectbox(
        "Seleziona il tuo stato attuale:",
        ["Calmo", "Ansioso", "Arrabbiato", "Triste", "Motivato", "Confuso", "Stressato", "Sopraffatto"]
    )
with col2:
    intensity = st.slider("Intensità (1-10)", 1, 10, 5)

notes = st.text_area("Note (opzionale)", placeholder="Cosa ha scatenato questa reazione? Sii onesto con te stesso.")

if st.button("Registra Emozione"):
    st.success(f"Registrato: {emotional_state} (Livello {intensity})")
    if intensity > 7:
        st.info("⚠️ Intensità elevata. Consiglio di usare l'Agente di Riorientamento qui sotto.")

st.divider()

# 3. Reorientation Agent
st.subheader("🛡️ Agente di Riorientamento")
st.markdown("Descrivi la situazione che ti sta turbando o bloccando. L'agente applicherà i principi dell'**Ingegneria delle Emozioni** per darti una prospettiva chiara e azionabile.")

user_input = st.text_area("Descrivi la situazione:", height=150, placeholder="Esempio: Mi sento frustrato perché il mio team non rispetta le scadenze...")

if st.button("Analizza con TAKE CONTROL"):
    if not user_input:
        st.error("Per favore, inserisci una descrizione della situazione.")
    elif 'model' not in locals():
        st.error("Configura prima l'API Key nel menu laterale.")
    else:
        with st.spinner("Analisi in corso... Respira."):
            # ENHANCED PROMPT - METODO PAOLO ALONGE
            prompt = f"""
            Agisci come Paolo Alonge, esperto coach del metodo 'TAKE CONTROL' e 'Ingegneria delle Emozioni'.
            Il tuo tono deve essere:
            - **Empatico ma Fermo**: Comprendi il dolore ma non indulgere nel vittimismo.
            - **Pratico e Diretto**: Niente giri di parole filosofici fini a se stessi. Solo strumenti applicabili.
            - **Stoico e Razionale**: Porta l'utente a distinguere ciò che controlla da ciò che non controlla.

            Analizza questo input dell'utente: "{user_input}"

            Formatta la risposta in Markdown con questa struttura esatta:
            
            ### 1. 🛑 Stop e Analisi
            Identifica l'impressione (o il giudizio automatico) che l'utente sta avendo. Separa i fatti oggettivi dalle interpretazioni emotive.
            
            ### 2. ⚖️ Dicotomia del Controllo
            Elenca chiaramente:
            * **Cosa è in tuo potere:** (Le tue azioni, le tue reazioni, le tue parole)
            * **Cosa NON è in tuo potere:** (Le azioni degli altri, il passato, i risultati esterni)
            
            ### 3. 🚀 Azione Immediata (Take Control)
            Dai 1 o 2 consigli estremamente pratici e immediati per agire ORA. Un esercizio mentale o un'azione fisica.
            
            Chiudi con una frase breve e potente per motivare l'azione.
            """
            try:
                # Use the model selected in the sidebar
                # model is already initialized in the sidebar code block content, 
                # but depending on scope we might need to re-init if variable not available globally,
                # however Streamlit reruns the whole script so 'model' from sidebar should be available if initialized there.
                # To be safe/explicit:
                model = genai.GenerativeModel(selected_model_name)
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                 st.error(f"Errore: {e}")
                 st.warning("Suggerimento: Prova a cambiare modello nelle Impostazioni (menu laterale).")

st.divider()

# 4. Daily Exercise
st.subheader("⚔️ Esercizio del Giorno")
st.markdown("Una pratica stoica o CBT per rafforzare la tua resilienza oggi.")

exercises = [
    {
        "title": "Praemeditatio Malorum (Premeditazione dei mali)",
        "desc": "Immagina lo scenario peggiore per la tua sfida di oggi. Visualizzalo nei dettagli. Accettalo mentalmente come se fosse già accaduto. Ora, pianifica razionalmente come lo affronteresti. Questo toglie potere alla paura."
    },
    {
        "title": "Journaling della Gratitudine (Focus)",
        "desc": "Scrivi 3 cose per cui sei grato oggi. Attenzione: non cose generiche. Cerca cose specifiche, anche piccole, o addirittura difficoltà che ti hanno insegnato qualcosa."
    },
    {
        "title": "La Veduta dall'Alto",
        "desc": "Chiudi gli occhi. Immagina di allontanarti dal tuo corpo, salire sopra la tua casa, la tua città, fino allo spazio. Guarda il tuo problema attuale da lassù. Quanto appare piccolo nell'ordine universale delle cose?"
    },
    {
        "title": "Amor Fati (Amore per il destino)",
        "desc": "Non desiderare che le cose accadano come vuoi tu, ma desidera che accadano così come accadono, e la tua vita scorrerà serena. Accogli ogni evento di oggi come se lo avessi scelto tu."
    },
    {
        "title": "Il cerchio del controllo",
        "desc": "Prendi un foglio. Disegna un cerchio. Scrivi dentro tutto ciò che puoi controllare riguardo al tuo problema attuale. Scrivi fuori tutto il resto. Dimentica ciò che è fuori. Agisci ferocemente su ciò che è dentro."
    }
]

if st.button("Genera Nuova Sfida"):
    ex = random.choice(exercises)
    st.info(f"**{ex['title']}**")
    st.write(ex['desc'])

st.markdown("---")
