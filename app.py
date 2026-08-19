import os
import re
import random
import gradio as gr
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from weasyprint import HTML, CSS
from datetime import datetime


API_KEY = os.getenv("GEMINI_API_KEY")

def create_llm():
    return LLM(
        model="gemini/gemini-3-flash",
        api_key=API_KEY
    )


os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

search_tool = SerperDevTool()

# ==========================================
# 1. PDF GENERATION
# ==========================================
def create_pdf(text, lang_code):
    file_path = f"Note_{lang_code}_{datetime.now().strftime('%H%M%S')}.pdf"
    
    direction = "rtl" if lang_code == "AR" else "ltr"
    align = "right" if lang_code == "AR" else "left"

    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @font-face {{
                font-family: 'DejaVu';
                src: url('DejaVuSans.ttf');
            }}

            body {{
                font-family: 'DejaVu';
                direction: {direction};
                text-align: {align};
                font-size: 11pt;
                line-height: 1.6;
            }}

            h2, h3 {{
                text-align: center;
                color: #1a5f7a;
            }}

            p {{
                margin-bottom: 14pt;
                text-align: justify;
            }}
        </style>
    </head>
    <body>
        <h2>ROYAUME DU MAROC</h2>
        <h3>Cabinet Stratégique Atlas-Omnis</h3>
        <hr>
        <p>{text.replace('\n', '<br>')}</p>
    </body>
    </html>
    """

    HTML(string=html_content).write_pdf(file_path)

    return file_path

# ==========================================
# 2. AGENT SYSTEM
# ==========================================
def create_cabinet():
    chercheur = Agent(
        role="Directeur OSINT & Intelligence Économique",
        goal="Collecter des données massives, exhaustives et ultra-détaillées.",
        backstory="Spécialiste en renseignement territorial marocain. Vous fournissez des pages de contexte. INTERDICTION DE RÉSUMER.",
        tools=[search_tool],
        llm=create_llm(), 
        verbose=True
    )

    juriste = Agent(
        role="Conseiller Juridique d'État",
        goal="Disséquer le cadre légal marocain avec une précision chirurgicale.",
        backstory="Expert en droit public et Dahirs. Vous utilisez votre capacité de raisonnement pour trouver les lois spécifiques. INTERDICTION DE RÉSUMER.",
        llm=create_llm(), 
        verbose=True
    )

    statisticien = Agent(
        role="Analyste Quantitatif & Data Scientist",
        goal="Produire une modélisation mathématique et statistique détaillée.",
        backstory="Mathématicien. Vous construisez des scénarios complexes avec une logique parfaite. INTERDICTION DE RÉSUMER.",
        llm=create_llm(), 
        verbose=True
    )

    financier = Agent(
        role="Inspecteur des Finances Publiques",
        goal="Réaliser un audit financier et macroéconomique exhaustif.",
        backstory="Expert budgétaire. Vous décomposez les coûts et l'impact économique. INTERDICTION DE RÉSUMER.",
        llm=create_llm(), 
        verbose=True
    )

    redacteur = Agent(
        role="Rédacteur Officiel de Haut Niveau",
        goal="Rédiger une note ministérielle KILOMÉTRIQUE, intégrant chaque détail et info des experts précédents en un seul texte complet.",
        backstory="Haut fonctionnaire. Votre plume est riche et analytique. OBLIGATION de développer chaque idée sur plusieurs pages.",
        llm=create_llm(), 
        verbose=True
    )

    traducteur = Agent(
        role="Traducteur Institutionnel Assermenté",
        goal="Traduire l'intégralité du long rapport en arabe classique (Fusha).",
        backstory="Maître linguiste. Vous ne coupez aucun paragraphe et gardez le phrasé noble.",
        llm=create_llm(), 
        verbose=True
    )

    auditeur = Agent(
        role="Contrôleur Qualité & Audit Final",
        goal="Consolider les textes massifs et appliquer un formatage intraitable.",
        backstory="Garant de la structure. Vous assurez la présence absolue des balises [FRANCAIS] et [ARABE].",
        llm=create_llm(), 
        verbose=True
    )

    return chercheur, juriste, statisticien, financier, redacteur, traducteur, auditeur

# ==========================================
# 3. EXECUTION PIPELINE
# ==========================================
def run_mission(query, progress=gr.Progress()):
    if not query:
        return "Veuillez entrer une instruction.", None, None

    experts = create_cabinet()

    tasks = [
        Task(
            description=f"Recherche EXHAUSTIVE sur: {query}. Interdiction de faire court. Listez un maximum d'exemples et de faits.", 
            agent=experts[0], 
            expected_output="Un dossier de recherche massif, plein de données."
        ),
        Task(
            description="Analyse juridique complète. Expliquez en détail les Dahirs et lois marocaines touchant à ce sujet.", 
            agent=experts[1], 
            expected_output="Un mémorandum juridique profond et sourcé."
        ),
        Task(
            description="Développement des KPIs. Expliquez le raisonnement mathématique derrière chaque statistique.", 
            agent=experts[2], 
            expected_output="Une modélisation quantitative détaillée."
        ),
        Task(
            description="Évaluation financière approfondie. Détaillez les micro et macro-impacts économiques.", 
            agent=experts[3], 
            expected_output="Un rapport financier exhaustif."
        ),
        Task(
            description="RÉDACTION STRATÉGIQUE. Rédigez un document d'État avec plusieurs grands chapitres très détaillés. INTERDICTION de résumer. Un seule rapport avec tous les informations donnée par les autres agents", 
            agent=experts[4], 
            expected_output="Un texte ministérielle extrêmement longue (minimum 1500 mots)."
        ),
        Task(
            description="Traduction intégrale en arabe classique. Ne coupez aucun paragraphe.", 
            agent=experts[5], 
            expected_output="La traduction exacte et intégrale."
        ),
        Task(
            description="Audit final et intégration stricte des textes. AUCUNE modification du contenu.",
            agent=experts[6],
            expected_output="Format exact : [FRANCAIS] texte en français [/FRANCAIS] \n\n [ARABE] texte en arabe [/ARABE]"
        ),
    ]

    crew = Crew(
        agents=experts,
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    try:
        progress(0.2, desc="Activation du Cabinet...")
        result = str(crew.kickoff())

        fr_match = re.search(r"\[FRANCAIS\](.*?)\[/FRANCAIS\]", result, re.DOTALL)
        ar_match = re.search(r"\[ARABE\](.*?)\[/ARABE\]", result, re.DOTALL)

        txt_fr = fr_match.group(1).strip() if fr_match else "Erreur FR - Balises manquantes."
        txt_ar = ar_match.group(1).strip() if ar_match else "Erreur AR - Balises manquantes."

        pdf_fr = create_pdf(txt_fr, "FR")
        pdf_ar = create_pdf(txt_ar, "AR")

        # Preview truncates the markdown in the UI so Gradio doesn't lag with massive text,
        # but the full text is saved to the PDFs.
        preview = f"### 🇫🇷\n{txt_fr[:1000]}...\n\n---\n### 🇲🇦\n<div dir='rtl'>{txt_ar[:1000]}...</div>"

        return preview, pdf_fr, pdf_ar

    except Exception as e:
        return f"Erreur: {str(e)}", None, None

# ==========================================
# 4. UI
# ==========================================
with gr.Blocks() as app:
    gr.Markdown("# 🇲🇦 Cabinet Atlas-Omnis 4.0")
    gr.Markdown("Système stratégique multi-agents")

    with gr.Row():
        inp = gr.Textbox(label="Instruction Stratégique", lines=5)
        btn = gr.Button("Lancer la recherche Profonde")

    preview = gr.Markdown()
    with gr.Row():
        out_fr = gr.File(label="PDF FR")
        out_ar = gr.File(label="PDF AR")

    btn.click(fn=run_mission, inputs=inp, outputs=[preview, out_fr, out_ar])

app.launch()
