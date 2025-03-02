"""
Settings Page - For application settings
"""
import streamlit as st
import os
import json
import tempfile
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Configurações | Gerenciador de Exames Laboratoriais",
    page_icon="⚙️",
    layout="wide"
)

def export_data():
    """Exports all application data to a JSON file."""
    # Get data from session state
    data = {
        'profiles': st.session_state.profiles,
        'favorite_profiles': list(st.session_state.favorite_profiles),
        'exported_at': datetime.now().isoformat()
    }
    
    # Convert data to JSON
    json_str = json.dumps(data, default=str, indent=2)
    
    # Create a download button
    st.download_button(
        label="Baixar Dados",
        data=json_str,
        file_name="lab_exam_data.json",
        mime="application/json"
    )

def import_data():
    """Imports application data from a JSON file."""
    uploaded_file = st.file_uploader("Escolha um arquivo de backup", type="json")
    
    if uploaded_file is not None:
        try:
            # Read the JSON file
            data = json.loads(uploaded_file.read().decode('utf-8'))
            
            # Validate the data
            if 'profiles' not in data or 'favorite_profiles' not in data:
                st.error("Arquivo de backup inválido. Formato não reconhecido.")
                return
            
            # Import confirmation
            if st.button("Confirmar Importação"):
                # Update session state
                st.session_state.profiles = data['profiles']
                st.session_state.favorite_profiles = set(data['favorite_profiles'])
                
                st.success("Dados importados com sucesso!")
                st.info("Recarregue a página para ver as alterações.")
        
        except Exception as e:
            st.error(f"Erro ao importar dados: {str(e)}")

def theme_settings():
    """Theme settings section."""
    st.subheader("Tema da Aplicação")
    
    # Theme selection
    theme = st.radio(
        "Escolha o tema:",
        ["light", "dark"],
        horizontal=True,
        index=0 if st.session_state.theme == "light" else 1
    )
    
    # Apply theme
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.success(f"Tema alterado para: {theme}")
        st.info("Algumas alterações de tema podem exigir recarregar a página.")

def clear_data():
    """Reset application data section."""
    st.subheader("Reiniciar Dados da Aplicação")
    
    st.warning("""
    Isso irá reiniciar todos os dados do aplicativo, incluindo perfis personalizados.
    Esta ação não pode ser desfeita!
    """)
    
    # Confirm reset
    if st.button("Reiniciar Todos os Dados"):
        if st.session_state.get('confirm_reset'):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key not in ['_is_running', '_component_instances']:
                    del st.session_state[key]
            
            st.success("Dados reiniciados com sucesso!")
            st.info("Recarregue a página para aplicar as alterações.")
        else:
            st.session_state.confirm_reset = True
            st.error("Clique novamente para confirmar a reinicialização dos dados.")
            st.experimental_rerun()

def main():
    """Main function for the Settings page."""
    st.title("Configurações")
    
    # Create tabs for different settings
    tab1, tab2, tab3, tab4 = st.tabs([
        "Tema", "Exportar Dados", "Importar Dados", "Reiniciar Dados"
    ])
    
    with tab1:
        theme_settings()
    
    with tab2:
        st.subheader("Exportar Dados")
        st.write("""
        Exporte todos os dados da aplicação para backup ou transferência.
        Isso inclui todos os perfis de exame e configurações.
        """)
        export_data()
    
    with tab3:
        st.subheader("Importar Dados")
        st.write("""
        Importe dados de um arquivo de backup.
        Isso irá substituir todos os dados atuais da aplicação.
        """)
        import_data()
    
    with tab4:
        clear_data()
    
    # About section
    st.divider()
    st.subheader("Sobre o Aplicativo")
    st.write("""
    **Gerenciador de Exames Laboratoriais** - Versão 1.0
    
    Desenvolvido com Streamlit. Este aplicativo permite gerenciar resultados 
    de exames laboratoriais, comparando-os com valores de referência e
    gerando relatórios formatados.
    """)

if __name__ == "__main__":
    main()