"""
Management of exam profiles: creation, retrieval, deletion, and favorites.
"""
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
import streamlit as st

from models.exam import ExamProfile
from data.defaults import CHECKUP_CATEGORIES, REFERENCE_RANGES, DEFAULT_DESCRIPTIONS

class ExamProfileManager:
    """Manages exam profiles: creation, retrieval, deletion, and marking as favorite."""
    
    def __init__(self) -> None:
        """Initialize the profile manager and load default profiles."""
        if 'profiles' not in st.session_state:
            st.session_state.profiles = {}
            
        if 'favorite_profiles' not in st.session_state:
            st.session_state.favorite_profiles = set()
            
        # Load default profiles if none exist
        if not st.session_state.profiles:
            self.load_default_profiles()
    
    def load_default_profiles(self) -> None:
        """Loads the default exam profiles."""
        for pf_name, cats in CHECKUP_CATEGORIES.items():
            cat_map: Dict[str, List[str]] = {}
            for cat in cats:
                if cat in REFERENCE_RANGES:
                    cat_map[cat] = list(REFERENCE_RANGES[cat].keys())
            
            pf = ExamProfile(
                name=pf_name,
                categories=cat_map,
                description=DEFAULT_DESCRIPTIONS.get(pf_name, ""),
                is_default=True
            )
            
            st.session_state.profiles[pf_name] = pf.dict()
            logging.debug(f"Default profile loaded: {pf_name}")
    
    def create_profile(self, name: str, categories: Dict[str, List[str]], desc: str = "") -> ExamProfile:
        """
        Creates a new exam profile.
        
        Args:
            name: Profile name.
            categories: Dictionary with categories and list of exams.
            desc: Profile description.
            
        Returns:
            Created ExamProfile instance.
            
        Raises:
            ValueError: If a profile with the same name already exists.
        """
        if name in st.session_state.profiles:
            logging.error(f"Profile '{name}' already exists.")
            raise ValueError("Profile with this name already exists.")
            
        pf = ExamProfile(
            name=name,
            categories=categories,
            description=desc,
            is_default=False
        )
        
        st.session_state.profiles[name] = pf.dict()
        logging.info(f"Profile created: {name}")
        return pf
    
    def get_profile(self, name: str) -> Optional[ExamProfile]:
        """
        Returns a profile by name.
        
        Args:
            name: Profile name.
            
        Returns:
            ExamProfile instance if found, otherwise None.
        """
        if name not in st.session_state.profiles:
            return None
            
        p_dict = st.session_state.profiles[name]
        p = ExamProfile(**p_dict)
        p.update_last_used()
        
        # Update the session state with the new last_used timestamp
        st.session_state.profiles[name] = p.dict()
        
        return p
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """
        Returns a list with all profiles and their metadata.
        """
        output = []
        for n, p_dict in st.session_state.profiles.items():
            p = ExamProfile(**p_dict)
            output.append({
                'name': p.name,
                'description': p.description,
                'exam_count': p.get_exam_count(),
                'category_count': p.get_category_count(),
                'is_default': p.is_default,
                'is_favorite': (n in st.session_state.favorite_profiles),
                'last_used': p.last_used
            })
        return output
    
    def delete_profile(self, name: str) -> None:
        """
        Deletes a profile by name.
        
        Args:
            name: Profile name.
            
        Raises:
            ValueError: If the profile is not found or is a default profile.
        """
        pf = self.get_profile(name)
        if not pf:
            logging.error("Profile not found.")
            raise ValueError("Profile not found.")
            
        if pf.is_default:
            logging.error("Cannot delete default profiles.")
            raise ValueError("Cannot delete default profiles.")
            
        del st.session_state.profiles[name]
        
        if name in st.session_state.favorite_profiles:
            st.session_state.favorite_profiles.remove(name)
            
        logging.info(f"Profile deleted: {name}")
    
    def toggle_favorite(self, name: str) -> None:
        """
        Toggles the favorite status of a profile.
        
        Args:
            name: Profile name.
            
        Raises:
            ValueError: If the profile doesn't exist.
        """
        if name not in st.session_state.profiles:
            logging.error("Profile does not exist.")
            raise ValueError("Profile does not exist.")
            
        if name in st.session_state.favorite_profiles:
            st.session_state.favorite_profiles.remove(name)
            logging.debug(f"Profile removed from favorites: {name}")
        else:
            st.session_state.favorite_profiles.add(name)
            logging.debug(f"Profile marked as favorite: {name}")