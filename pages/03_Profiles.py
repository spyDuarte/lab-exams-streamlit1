"""
Profiles Page - For managing exam profiles
"""
import streamlit as st
from datetime import datetime

from utils.profile_manager import ExamProfileManager
from data.defaults import REFERENCE_RANGES

# Page config
st.set_page_config(
    page_title="Perfis de Exame | Gerenciador de Exames Laboratoriais",
    page_icon="📋",
    layout="wide"
)

def display_profile_list():
    """Displays the list of all profiles."""
    profiles = st.session_state.profile_manager.get_all_profiles()
    
    if not profiles:
        st.info("Nenhum perfil de exame criado.")
        return
    
    # Sort profiles: favorites first, then by name
    profiles.sort(key=lambda p: (not p['is_favorite'], p['name']))
    
    # Create tabs for Default and Custom profiles
    default_profiles = [p for p in profiles if p['is_default']]
    custom_profiles = [p for p in profiles if not p['is_default']]
    
    tab1, tab2 = st.tabs(["Perfis Padrão", "Perfis Personalizados"])
    
    # Display default profiles
    with tab1:
        if not default_profiles:
            st.info("Nenhum perfil padrão disponível.")
        else:
            for profile in default_profiles:
                with st.expander(f"{profile['name']} {'⭐' if profile['is_favorite'] else ''}", expanded=False):
                    st.write(f"**Descrição:** {profile['description']}")
                    st.write(f"**Exames:** {profile['exam_count']}")
                    st.write(f"**Categorias:** {profile['category_count']}")
                    st.write(f"**Último Uso:** {profile['last_used'].strftime('%d/%m/%Y %H:%M')}")
                    
                    # Create columns for buttons
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        # Use profile button
                        if st.button("Usar Perfil", key=f"use_{profile['name']}"):
                            st.session_state.selected_profile = profile['name']
                            st.switch_page("pages/02_New_Exam.py")
                    
                    with col2:
                        # Toggle favorite button
                        fav_text = "Desfavoritar" if profile['is_favorite'] else "Favoritar"
                        if st.button(fav_text, key=f"fav_{profile['name']}"):
                            st.session_state.profile_manager.toggle_favorite(profile['name'])
                            st.experimental_rerun()
    
    # Display custom profiles
    with tab2:
        if not custom_profiles:
            st.info("Nenhum perfil personalizado criado.")
        else:
            for profile in custom_profiles:
                with st.expander(f"{profile['name']} {'⭐' if profile['is_favorite'] else ''}", expanded=False):
                    st.write(f"**Descrição:** {profile['description']}")
                    st.write(f"**Exames:** {profile['exam_count']}")
                    st.write(f"**Categorias:** {profile['category_count']}")
                    st.write(f"**Último Uso:** {profile['last_used'].strftime('%d/%m/%Y %H:%M')}")
                    
                    # Create columns for buttons
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        # Use profile button
                        if st.button("Usar Perfil", key=f"use_{profile['name']}"):
                            st.session_state.selected_profile = profile['name']
                            st.switch_page("pages/02_New_Exam.py")
                    
                    with col2:
                        # Toggle favorite button
                        fav_text = "Desfavoritar" if profile['is_favorite'] else "Favoritar"
                        if st.button(fav_text, key=f"fav_{profile['name']}"):
                            st.session_state.profile_manager.toggle_favorite(profile['name'])
                            st.experimental_rerun()
                    
                    with col3:
                        # Delete button
                        if st.button("Excluir Perfil", key=f"del_{profile['name']}"):
                            if st.session_state.get('confirm_delete') == profile['name']:
                                try:
                                    st.session_state.profile_manager.delete_profile(profile['name'])
                                    st.success(f"Perfil '{profile['name']}' excluído com sucesso!")
                                    st.session_state.pop('confirm_delete', None)
                                    st.experimental_rerun()
                                except ValueError as e:
                                    st.error(str(e))
                            else:
                                st.session_state.confirm_delete = profile['name']
                                st.warning(f"Clique novamente para confirmar a exclusão de '{profile['name']}'.")
                                st.experimental_rerun()

def create_new_profile():
    """Creates a new profile."""
    st.subheader("Criar Novo Perfil")
    
    with st.form(key="new_profile_form"):
        # Profile name
        profile_name = st.text_input("Nome do Perfil")
        
        # Profile description
        profile_desc = st.text_area("Descrição", height=100)
        
        # Exam categories selection
        st.subheader("Selecione as Categorias e Exames")
        
        # Variable to collect selections
        selected_exams = {}
        
        # Create a section for each category
        for category, exams_dict in REFERENCE_RANGES.items():
            with st.expander(category, expanded=False):
                # Add the category to selected_exams
                selected_exams[category] = []
                
                # Create columns for the checkboxes
                cols = st.columns(3)
                
                # Create checkboxes for each exam
                for i, exam_name in enumerate(exams_dict.keys()):
                    with cols[i % 3]:
                        if st.checkbox(exam_name, key=f"chk_{category}_{exam_name}"):
                            selected_exams[category].append(exam_name)
        
        # Submit button
        submitted = st.form_submit_button("Criar Perfil")
        
        if submitted:
            # Validate form
            if not profile_name:
                st.error("Digite um nome para o perfil.")
                return
            
            # Check if any exam is selected
            has_exams = any(exams for exams in selected_exams.values() if exams)
            
            if not has_exams:
                st.error("Selecione pelo menos um exame.")
                return
            
            # Create the profile
            try:
                st.session_state.profile_manager.create_profile(
                    profile_name,
                    selected_exams,
                    profile_desc
                )
                st.success(f"Perfil '{profile_name}' criado com sucesso!")
                # Switch to list view
                st.session_state.profile_view = "list"
                st.experimental_rerun()
            except ValueError as e:
                st.error(str(e))

def main():
    """Main function for the Profiles page."""
    st.title("Perfis de Exame")
    
    # Initialize view state if not exists
    if 'profile_view' not in st.session_state:
        st.session_state.profile_view = "list"
    
    # Buttons to switch views
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Listar Perfis", use_container_width=True):
            st.session_state.profile_view = "list"
            st.experimental_rerun()
    
    with col2:
        if st.button("Criar Novo Perfil", use_container_width=True):
            st.session_state.profile_view = "create"
            st.experimental_rerun()
    
    # Divider
    st.divider()
    
    # Display the appropriate view
    if st.session_state.profile_view == "list":
        display_profile_list()
    else:
        create_new_profile()

if __name__ == "__main__":
    main()