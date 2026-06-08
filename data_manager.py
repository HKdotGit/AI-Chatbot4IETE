import os
import json

class DataManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Locate relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "data", "database.json")
        
        self.db_path = db_path
        self.data = {}
        self.load_database()

    def load_database(self):
        """Loads and parses the database JSON file."""
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Database file not found at {self.db_path}. Using empty database.")
            self.data = {}
        except json.JSONDecodeError as e:
            print(f"Error parsing database JSON: {e}")
            self.data = {}

    def get_organization_info(self):
        return self.data.get("organization", {})

    def get_statistics(self):
        return self.data.get("statistics", {})

    def get_core_values(self):
        return self.data.get("core_values", [])

    def get_events(self):
        return self.data.get("events", [])

    def get_team_structure(self):
        return self.data.get("team_structure", {})

    def find_event(self, name):
        """Searches for an event by name."""
        for event in self.get_events():
            if name.lower() in event.get("name", "").lower():
                return event
        return None

    def find_department(self, name):
        """Searches for a department by name."""
        team = self.get_team_structure()
        for dept in team.get("departments", []):
            if name.lower() in dept.get("name", "").lower():
                return dept
        return None

    def generate_system_instruction(self):
        """
        Dynamically constructs the system instruction prompt for the Gemini AI.
        Formats the loaded JSON database into the markdown prompt structure.
        """
        org = self.get_organization_info()
        stats = self.get_statistics()
        values = self.get_core_values()
        events = self.get_events()
        team = self.get_team_structure()
        supercore = team.get("supercore", {})
        departments = team.get("departments", [])

        # Build prompt string
        lines = []
        lines.append("You are the official IETE-SF AI Chatbot. Your primary role is to provide information about the tech community IETE-SF MPSTME based on the following official database.")
        lines.append("[IETE-SF DATABASE START]")
        
        lines.append(f"Motto: {org.get('motto', 'For the Engineers, By the Engineers')}.")
        lines.append(f"About: {org.get('about', '')}")
        lines.append(f"Stats: {stats.get('members', '220+')} Team Members, {stats.get('incentives', '100K+')} Incentives, {stats.get('alumni', '1,200+')} Alumni, {stats.get('followers', '2,500+')} Followers.")
        
        lines.append("Mission Core Values:")
        for val in values:
            lines.append(f"- {val.get('name')}: {val.get('description')}")
            
        lines.append("Events:")
        for ev in events:
            lines.append(f"- {ev.get('name')}: {ev.get('description')}")
            
        lines.append("\nTeam Structure & Departments:")
        lines.append("Supercore:")
        for role, name in supercore.items():
            role_title = role.replace("_", "-").title()
            lines.append(f"- {role_title}: {name}")
            
        lines.append("\nDepartments & Heads:")
        for dept in departments:
            heads_str = ", ".join(dept.get("heads", []))
            subheads_str = ", ".join(dept.get("sub_heads", []))
            lines.append(f"- {dept.get('name')}: {heads_str} (Sub-Heads: {subheads_str})")
            
        lines.append("\nGeneral Info & Contact:")
        lines.append(f"- Website: {org.get('website')}")
        lines.append(f"- Established: {org.get('established')}")
        lines.append(f"- Email: {org.get('email')}")
        lines.append(f"- Location: {org.get('location')}")
        
        mentors_str = ", ".join(org.get("faculty_mentors", []))
        lines.append(f"- Faculty Mentors: {mentors_str}")
        lines.append("[IETE-SF DATABASE END]")
        
        lines.append("""
Rules:
1. When asked about IETE-SF, answer gracefully and enthusiastically using the database above. If asked who you are, introduce yourself.
2. Provide concise, friendly answers and format them beautifully using markdown.
3. You are a highly versatile AI. If asked about general tech, coding, or any topics unrelated to IETE-SF, seamlessly answer them utilizing your broader Gemini knowledge base. Do not force the conversation back to IETE-SF or sound overly self-centered about the organization.""")

        return "\n".join(lines)

if __name__ == "__main__":
    # Test script output
    manager = DataManager()
    print("--- Loaded Organization ---")
    print(manager.get_organization_info())
    print("\n--- Generated System Prompt Excerpt ---")
    prompt = manager.generate_system_instruction()
    print("\n".join(prompt.split("\n")[:25]))
    print("...")
