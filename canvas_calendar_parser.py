import re
import sys
from pathlib import Path
from typing import Dict, List
from ics import Calendar
from collections import defaultdict
from datetime import date

class CanvasCalendarParser:
    """Parser for Canvas ICS calendar files that extracts and formats assignment information."""
    
    def __init__(self, file_path: str):
        """Initialize the parser with the path to an ICS file.
        
        Args:
            file_path (str): Path to the ICS file to parse
        """
        self.file_path = Path(file_path)
        
    def parse_calendar(self) -> Dict[date, List[str]]:
        """Parse the ICS file and return events grouped by day.
        
        Returns:
            Dict[date, List[str]]: Dictionary mapping dates to lists of formatted event strings
            
        Raises:
            FileNotFoundError: If the specified ICS file doesn't exist
            ValueError: If the file isn't a valid ICS file
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Could not find ICS file: {self.file_path}")
            
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                calendar = Calendar(f.read())
        except Exception as e:
            raise ValueError(f"Failed to parse ICS file: {e}")
        
        events_by_day = defaultdict(list)
        
        for event in calendar.events:
            event_date = event.begin.date()
            event_details = event.name
            
            # Skip PAL sessions and assignments from training courses
            to_skip = ["PAL", "Training"]
            if any(item in event_details for item in to_skip):
                continue
                
            event_details = self._format_event(event_details)
            events_by_day[event_date].append(event_details)
            
        return events_by_day
    
    def _format_event(self, event_name: str) -> str:
        """Format a Canvas calendar event name into a cleaner representation.
        
        Args:
            event_name (str): Raw event name from the calendar
            
        Returns:
            str: Formatted event string
        """
        # Extract class name from brackets
        class_name_matches = re.findall(r'(?<=\[)[^\[\]]+(?=\])', event_name)
        if not class_name_matches:
            return event_name
            
        class_name = class_name_matches[-1]
        assignment = event_name.replace(f"[{class_name}]", '').strip()
        
        # Extract course code (e.g., MATH-2164-001)
        class_slug_match = re.search(
            r'([A-Z]{3,4}[- ]\d{4}(?:[- ][A-Z\d]{0,3}(?=[- :])){0,1})',
            class_name
        )
        
        if class_slug_match:
            return self._format_with_slug(class_slug_match.groups(), assignment)
            
        # Clean up common patterns
        return self._clean_class_name(class_name, assignment)
    
    def _format_with_slug(self, slugs: tuple, assignment: str) -> str:
        """Format event with course code/slug.
        
        Args:
            slugs (tuple): Extracted course code components
            assignment (str): Assignment description
            
        Returns:
            str: Formatted event string
        """
        slugs = [s.replace(" ", "-") for s in slugs if s]
        
        if len(slugs) == 1:
            return f"{slugs[0]}: {assignment}"
            
        # Handle multi-section courses
        base_code = slugs[0][:8]
        if all(s.startswith(base_code) for s in slugs):
            return f"{base_code.rstrip('-')}: {assignment}"
            
        # There are multiple different courses found, just return the first
        return f"{slugs[0]}: {assignment}"
    
    def _clean_class_name(self, class_name: str, assignment: str) -> str:
        """Clean up a class name by removing common unnecessary patterns.
        
        Args:
            class_name (str): Raw class name
            assignment (str): Assignment description
            
        Returns:
            str: Cleaned up event string
        """
        patterns = [
            r"[- ]*[A-Za-z]*\d[A-Za-z\d]{5,}[- ]*",  # Random IDs
            r"[- ]*[A-Z][a-z]+[- ]\d{4}[- ]*",       # Semester identifiers
            r"_Combined"                             # Combined section markers
        ]
        
        for pattern in patterns:
            class_name = re.sub(pattern, "", class_name)
            
        return f"{class_name}: {assignment}"

def main():
    """Main entry point for the script."""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "canvas_export.ics"
        
    try:
        parser = CanvasCalendarParser(file_path)
        events = parser.parse_calendar()
        
        # Print events sorted by date
        for day, day_events in sorted(events.items()):
            print(f"\n-- {day.strftime('%B %d, %Y (%A)')} --")
            for event in sorted(day_events):
                print(f"{event}")
                
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        if (f"{e}" == "Could not find ICS file: canvas_export.ics"):
            print("Specify a file or rename it to 'canvas_export.ics' and place in this directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()