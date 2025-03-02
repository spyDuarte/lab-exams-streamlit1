"""
New Exam Page - For entering exam results
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import io
import base64

from utils.formatter import ExamResultFormatter, get_status_from_values
from utils.pdf_exporter import PDFExporter
from models.validation import ExamDataValidator, ValidationError
from data.defaults import REFERENCE_RANGES

# Page config
st.set_page_config(
    page_title="Novo Exame | Gerenciador de Exames Laboratoriais",
    page_icon="🧪",
    layout="wide"
)

# Initialize validator
validator = ExamDataValidator()

def create_download_link(pdf_bytes, filename):
    """Creates a download link for a PDF file."""
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Baixar PDF</a>'
    return href

def display_results(results, exam_type, date_str):
    """Displays the exam results."""
    st.header("Resultados do Exame")
    
    # Display date and type
    st.write(f"**Tipo de Exame:** {exam_type}")
    st.write(f"**Data:** {date_str}")
    
    # Display results by category
    for category, exams in results.items():
        if exams:
            with st.expander(category, expanded=True):
                # Create a dataframe for each category
                data = []
                for exam_name, vals in exams.items():
                    status = get_status_from_values(vals['value'], vals['reference'])
                    data.append({
                        "Exame": exam_name,
                        "Resultado": f"{vals['value']} {vals['unit']}",
                        "Referência": f"{vals['reference']} {vals['unit']}",
                        "Status": status
                    })
                
                if data:
                    df = pd.DataFrame(data)
                    
                    # Style the dataframe
                    def highlight_status(val):
                        if val == 'ALTO' or val == 'BAIXO':
                            return 'background-color: #ffcccc'
                        elif val == 'NORMAL':
                            return 'background-color: #ccffcc'
                        return ''
                    
                    # Apply styling
                    styled_df = df.style.applymap(highlight_status, subset=['Status'])
                    
                    # Display the dataframe
                    st.dataframe(styled_df, use_container_width=True)
    
    # Export options
    st.subheader("Opções de Exportação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        orientation = st.radio(
            "Orientação do PDF:",
            ["portrait", "landscape"],
            horizontal=True,
            index=0
        )
    
    # Create PDF exporter
    exporter = PDFExporter(exam_type, date_str, results)
    exporter.set_orientation(orientation)
    
    # Generate PDF
    pdf_bytes = exporter.export()
    
    # Create download button
    filename = f"Exame_{exam_type}_{date_str.replace('/', '_')}.pdf"
    
    with col2:
        st.download_button(
            label="Baixar PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf"
        )
    
    # Formatter for copying
    formatter = ExamResultFormatter(exam_type, date_str, results)
    
    # Text representation
    with st.expander("Visualizar em Formato de Texto"):
        st.code(formatter.format_text())
    
    # Tabular representation
    with st.expander("Visualizar em Formato Tabular"):
        st.code(formatter.format_tabular())

def create_exam_form(profile_name):
    """Creates the form for entering exam results."""
    profile = st.session_state.profile_manager.get_profile(profile_name)
    
    if not profile:
        st.error(f"Perfil não encontrado: {profile_name}")
        return
    
    # Create a form
    with st.form(key="exam_form"):
        st.subheader(f"Exame: {profile.name}")
        st.write(f"**Descrição:** {profile.description}")
        
        # Date picker
        col1, col2 = st.columns([1, 3])
        with col1:
            date = st.date_input("Data do Exame", datetime.now())
        
        # Variable to collect results
        all_results = {}
        
        # Create sections for each category
        for category, exams in profile.categories.items():
            if exams and category in REFERENCE_RANGES:
                st.subheader(category)
                
                # Create a new dict for this category
                all_results[category] = {}
                
                # Create columns for the exam entries
                cols = st.columns(3)
                
                # Create input fields for each exam
                for i, exam_name in enumerate(exams):
                    if exam_name in REFERENCE_RANGES[category]:
                        # Get reference range
                        ref_range = REFERENCE_RANGES[category][exam_name]
                        
                        # Create input field in the appropriate column
                        with cols[i % 3]:
                            ref_text = f"{ref_range['min']}-{ref_range['max']} {ref_range['unit']}"
                            st.text(f"Ref: {ref_text}")
                            
                            value = st.text_input(
                                exam_name,
                                key=f"{category}_{exam_name}"
                            )
                            
                            # Store the value if not empty
                            if value.strip():
                                try:
                                    valid_v = validator.validate_numeric_value(value, exam_name)
                                    
                                    if valid_v is not None:
                                        all_results[category][exam_name] = {
                                            'value': str(valid_v),
                                            'unit': ref_range['unit'],
                                            'reference': f"{ref_range['min']}-{ref_range['max']}"
                                        }
                                except ValidationError as e:
                                    st.error(str(e))
        
        # Submit button
        submitted = st.form_submit_button("Salvar Resultados")
        
        if submitted:
            try:
                # Validate date
                validator.validate_date(date)
                
                # Check if at least one result was entered
                has_results = any(category for category in all_results.values() if category)
                
                if not has_results:
                    st.error("Preencha pelo menos um resultado.")
                    return
                
                # Store the results in session state
                st.session_state.current_exam_results = all_results
                st.session_state.last_exam_date = date.strftime("%d/%m/%Y")
                st.session_state.last_exam_type = profile.name
                
                st.success("Resultados salvos com sucesso!")
                
                # Rerun to display results
                st.experimental_rerun()
                
            except ValidationError as e:
                st.error(str(e))

def main():
    """Main function for the New Exam page."""
    st.title("Novo Exame")
    
    # Check if we have results to display
    if 'current_exam_results' in st.session_state and st.session_state.current_exam_results:
        # Display the results
        display_results(
            st.session_state.current_exam_results,
            st.session_state.last_exam_type,
            st.session_state.last_exam_date
        )
        
        # Add button to start a new exam
        if st.button("Iniciar Novo Exame"):
            st.session_state.current_exam_results = {}
            st.experimental_rerun()
            
    else:
        # Get all profiles
        profiles = st.session_state.profile_manager.get_all_profiles()
        profile_names = [p['name'] for p in profiles]
        
        # Profile selection
        if 'selected_profile' in st.session_state:
            default_index = profile_names.index(st.session_state.selected_profile) if st.session_state.selected_profile in profile_names else 0
            st.session_state.selected_profile = None  # Reset after use
        else:
            default_index = 0
        
        selected_profile = st.selectbox(
            "Selecionar Perfil de Exame:",
            profile_names,
            index=default_index
        )
        
        if selected_profile:
            create_exam_form(selected_profile)

if __name__ == "__main__":
    main()