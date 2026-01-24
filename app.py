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
    page_icon="assets/logo-official.png",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom Styling - BRAND COLORS
# Primary Dark: #0e1117 (Streamlit default dark is close, but we enforce) or #001f3f
# Gold/Orange Accent: #D4Af37 (Gold) / #ff6600 (Orange hint) based on typical branding
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    /* Global Text */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0e1117; /* Deep Dark Background */
        color: #E0E0E0;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #C5A059 0%, #E0C070 100%);
        color: #000000;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.3s ease;
        padding: 0.6rem 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #E0C070 0%, #C5A059 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(197, 160, 89, 0.3);
        color: #000000;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Dividers */
    hr {
        border-top: 1px solid rgba(197, 160, 89, 0.5);
        margin: 2rem 0;
    }
    
    /* Expander/Cards */
    .streamlit-expanderHeader {
        background-color: #1A1D29;
        color: #E0E0E0;
        border-radius: 8px;
    }
    
    /* Custom Classes */
    .highlight {
        color: #C5A059;
        font-weight: bold;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #1A1D29;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 8px;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #C5A059;
        box-shadow: 0 0 0 1px #C5A059;
    }
    </style>
""", unsafe_allow_html=True)

# API Setup
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
        st.image("assets/logo-official.png", use_container_width=True)
    except:
        st.title("TAKE CONTROL")
    
    st.markdown("### ⚙️ Impostazioni")
    
    # Model Selector - Dynamic Fetch with graceful fallback
    available_models = ["models/gemini-1.5-flash", "models/gemini-2.0-flash", "models/gemini-1.5-pro"]
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model_list = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_list.append(m.name)
            if model_list:
                available_models = sorted(model_list, reverse=True)
        except Exception:
            pass

    # Default index logic - Prefer Flash for speed/cost, or Pro if user prefers
    default_index = 0
    for i, m in enumerate(available_models):
        if "1.5-flash" in m:
            default_index = i
            break

    selected_model_name = st.selectbox("Seleziona Modello AI", available_models, index=default_index)

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
    
    # Initialize model with selected option
    try:
        model = genai.GenerativeModel(selected_model_name)
    except Exception as e:
        st.error(f"Errore inizializzazione modello: {e}")

    st.markdown("---")
    st.markdown("**Il Metodo Paolo Alonge**")
    st.info("Ricorda: Non sono le cose a turbarci, ma il nostro giudizio su di esse. - Epitteto")
    st.caption("© 2026 Paolo Alonge Coaching")

# --- MAIN INTERFACE ---

# 1. Welcome Interface

col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        st.image("assets/logo-official.png", width=150)
    except:
        pass
with col_title:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    st.title("TAKE CONTROL")

st.markdown("<p style='text-align: center; font-size: 1.6em; color: #E0E0E0; font-weight: 300; letter-spacing: 1px;'>Domina la tua mente, domina la tua vita.</p>", unsafe_allow_html=True)

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
