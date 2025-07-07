"""
People Information Manager
Handles loading, saving, and managing people information
"""
import json
import logging
import os
import sys
import time
from typing import Dict, Any, Optional
from pathlib import Path

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import StorageConfig

logger = logging.getLogger(__name__)

class PeopleManager:
    """
    Manages people information database (JSON file)
    """
    
    def __init__(self, config: StorageConfig = None):
        self.config = config or StorageConfig()
        self.people_info = {}
        self.load_people_info()
    
    def load_people_info(self) -> bool:
        """
        Load people information from JSON file
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if self.config.PEOPLE_INFO_FILE.exists():
                with open(self.config.PEOPLE_INFO_FILE, 'r', encoding='utf-8') as f:
                    self.people_info = json.load(f)
                logger.info(f"Loaded information for {len(self.people_info)} people")
                return True
            else:
                logger.warning("People info file not found. Creating default config...")
                self._create_default_config()
                return False
        except json.JSONDecodeError:
            logger.error("Error reading people_info.json. Using empty config.")
            self.people_info = {}
            return False
        except Exception as e:
            logger.error(f"Error loading people info: {e}")
            self.people_info = {}
            return False
    
    def save_people_info(self) -> bool:
        """
        Save people information to JSON file
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Ensure config directory exists
            self.config.PEOPLE_INFO_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config.PEOPLE_INFO_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.people_info, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved information for {len(self.people_info)} people")
            return True
        except Exception as e:
            logger.error(f"Error saving people info: {e}")
            return False
    
    def get_person_info(self, name: str) -> Dict[str, Any]:
        """
        Get detailed information for a person
        
        Args:
            name: Person's name
            
        Returns:
            Person information dictionary
        """
        return self.people_info.get(name, self._get_default_person_info(name))
    
    def _get_default_person_info(self, name: str) -> Dict[str, Any]:
        """Get default person information template"""
        return {
            "full_name": name,
            "position": "Unknown",
            "department": "Unknown",
            "email": "N/A",
            "phone": "N/A",
            "bio": "No information available",
            "avatar": "",
            "join_date": "",
            "employee_id": "",
            "skills": [],
            "projects": []
        }
    
    def add_person(self, name: str, info: Dict[str, Any]) -> bool:
        """
        Add new person information
        
        Args:
            name: Person's name (key)
            info: Person information dictionary
            
        Returns:
            True if added successfully
        """
        try:
            # Validate required fields
            required_fields = ["full_name"]
            for field in required_fields:
                if field not in info:
                    info[field] = name
            
            self.people_info[name] = info
            self.save_people_info()
            logger.info(f"Added new person: {name}")
            return True
        except Exception as e:
            logger.error(f"Error adding person {name}: {e}")
            return False
    
    def update_person(self, name: str, info: Dict[str, Any]) -> bool:
        """
        Update existing person information
        
        Args:
            name: Person's name (key)
            info: Updated person information
            
        Returns:
            True if updated successfully
        """
        try:
            if name in self.people_info:
                self.people_info[name].update(info)
            else:
                self.people_info[name] = info
            
            self.save_people_info()
            logger.info(f"Updated person: {name}")
            return True
        except Exception as e:
            logger.error(f"Error updating person {name}: {e}")
            return False
    
    def remove_person(self, name: str) -> bool:
        """
        Remove person information
        
        Args:
            name: Person's name to remove
            
        Returns:
            True if removed successfully
        """
        try:
            if name in self.people_info:
                del self.people_info[name]
                self.save_people_info()
                logger.info(f"Removed person: {name}")
                return True
            else:
                logger.warning(f"Person not found: {name}")
                return False
        except Exception as e:
            logger.error(f"Error removing person {name}: {e}")
            return False
    
    def get_all_people(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all people information
        
        Returns:
            Dictionary of all people information
        """
        return self.people_info.copy()
    
    def search_people(self, query: str) -> Dict[str, Dict[str, Any]]:
        """
        Search people by name or other attributes
        
        Args:
            query: Search query
            
        Returns:
            Dictionary of matching people
        """
        query = query.lower()
        results = {}
        
        for name, info in self.people_info.items():
            # Search in name, full_name, position, department
            searchable_text = ' '.join([
                name.lower(),
                info.get('full_name', '').lower(),
                info.get('position', '').lower(),
                info.get('department', '').lower()
            ])
            
            if query in searchable_text:
                results[name] = info
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the people database
        
        Returns:
            Statistics dictionary
        """
        total_people = len(self.people_info)
        departments = {}
        positions = {}
        
        for person_info in self.people_info.values():
            dept = person_info.get('department', 'Unknown')
            pos = person_info.get('position', 'Unknown')
            
            departments[dept] = departments.get(dept, 0) + 1
            positions[pos] = positions.get(pos, 0) + 1
        
        return {
            "total_people": total_people,
            "departments": departments,
            "positions": positions,
            "top_department": max(departments.items(), key=lambda x: x[1])[0] if departments else "N/A",
            "top_position": max(positions.items(), key=lambda x: x[1])[0] if positions else "N/A"
        }
    
    def _create_default_config(self):
        """Create a default configuration file"""
        default_config = {
            "example_person": {
                "full_name": "Example Person",
                "position": "Software Developer",
                "department": "IT Department", 
                "email": "example@company.com",
                "phone": "+84 123 456 789",
                "bio": "This is an example person profile. Replace with actual information.",
                "avatar": "dataset/example_person/main.jpg",
                "join_date": "2025-01-01",
                "employee_id": "EMP001",
                "skills": ["Python", "Machine Learning", "Computer Vision"],
                "projects": ["Face Recognition System", "AI Chat Bot"]
            }
        }
        
        self.people_info = default_config
        self.save_people_info()
    
    def export_to_csv(self, file_path: str) -> bool:
        """
        Export people information to CSV file
        
        Args:
            file_path: Path to export CSV file
            
        Returns:
            True if exported successfully
        """
        try:
            import csv
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'full_name', 'position', 'department', 'email', 'phone', 'bio']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for name, info in self.people_info.items():
                    row = {'name': name}
                    for field in fieldnames[1:]:
                        row[field] = info.get(field, '')
                    writer.writerow(row)
            
            logger.info(f"Exported people info to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def backup_data(self, backup_path: Optional[str] = None) -> bool:
        """
        Create backup of people information
        
        Args:
            backup_path: Optional custom backup path
            
        Returns:
            True if backup created successfully
        """
        try:
            if backup_path is None:
                timestamp = Path().cwd() / f"people_info_backup_{int(time.time())}.json"
                backup_path = timestamp
            
            import shutil
            shutil.copy2(self.config.PEOPLE_INFO_FILE, backup_path)
            
            logger.info(f"Created backup at {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False
