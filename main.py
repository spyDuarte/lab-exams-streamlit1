"""
Laboratory Exam Manager - Main Streamlit Application
"""
import logging
import os
import streamlit as st
from datetime import datetime
from PIL import Image
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Import local modules
from utils.profile_manager import ExamProfileManager
from data.defaults import REFERENCE_RANGES, CHECKUP_CATEGORIES

# Configure Streamlit page
st.set_page_config(
    page_title="Gerenciador de Exames Laboratoriais",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'profile_manager' not in st.session_state:
    st.session_state.profile_manager = ExamProfileManager()

if 'current_exam_results' not in st.session_state:
    st.session_state.current_exam_results = {}

if 'last_exam_date' not in st.session_state:
    st.session_state.last_exam_date = datetime.now().strftime("%d/%m/%Y")

if 'theme' not in st.session_state:
    st.session_state.theme = "light"

# Main dashboard view
def main():
    """Main dashboard for the application."""
    
    # Application title and header
    st.title("Gerenciador de Exames Laboratoriais")
    
    # Display welcome message
    st.markdown("""
    ### Bem-vindo ao Gerenciador de Exames Laboratoriais!
    
    Este aplicativo permite gerenciar resultados de exames laboratoriais, comparando-os com 
    valores de referência e gerando relatórios formatados.
    
    Use a navegação lateral para acessar as diferentes funcionalidades do sistema.
    """)
    
    # Quick actions section
    st.header("Ações Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧪 Novo Exame", use_container_width=True):
            st.switch_page("pages/02_New_Exam.py")
    
    with col2:
        if st.button("📋 Gerenciar Perfis", use_container_width=True):
            st.switch_page("pages/03_Profiles.py")
    
    with col3:
        if st.button("⚙️ Configurações", use_container_width=True):
            st.switch_page("pages/04_Settings.py")
    
    # Recently used profiles
    st.header("Perfis Recentes")
    profiles = st.session_state.profile_manager.get_all_profiles()
    
    # Sort profiles by last used date (most recent first)
    profiles.sort(key=lambda p: p['last_used'], reverse=True)
    
    # Show top 3 most recently used profiles
    recent_profiles = profiles[:3]
    
    if recent_profiles:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, profile in enumerate(recent_profiles):
            if i < 3:  # Limit to 3 profiles
                with cols[i]:
                    st.subheader(profile['name'])
                    st.write(f"**Descrição:** {profile['description']}")
                    st.write(f"**Exames:** {profile['exam_count']}")
                    st.write(f"**Categorias:** {profile['category_count']}")
                    
                    if st.button(f"Usar {profile['name']}", key=f"use_profile_{i}", use_container_width=True):
                        st.session_state.selected_profile = profile['name']
                        st.switch_page("pages/02_New_Exam.py")
    else:
        st.info("Nenhum perfil de exame utilizado recentemente.")
    
    # About section
    st.header("Sobre o Sistema")
    st.markdown("""
    O **Gerenciador de Exames Laboratoriais** é uma aplicação web que permite o registro,
    análise e acompanhamento de resultados de exames laboratoriais.
    
    ### Principais Recursos:
    
    - Criação de perfis personalizados de exames
    - Registro de resultados com validação automática
    - Comparação com valores de referência
    - Exportação de resultados em PDF
    - Visualização formatada dos resultados
    """)

# Run the main function
if __name__ == "__main__":
    main()