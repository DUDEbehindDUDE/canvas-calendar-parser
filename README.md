# 📅 Canvas Calendar Assignment Parser

A simple Python script I made that takes an export of your Canvas calendar and generates a list of assignments due. Great when you have an assignment where you have to do exactly this. Optimized for UNC Charlotte students.

## 🎯 Purpose

This script was created because I had an assignment where I had to list every assignment for all the courses I was taking (30+ per week). It takes a Canvas calendar export and transforms it into a format where I could easily copy it by day.

## ✨ Features

- Groups assignments by due date
- Cleans up course names and assignment titles
- Filters out non-assignment events (like PAL sessions and training)
- Displays assignments in a clear, chronological format
- Handles multiple course sections elegantly

## 📋 Prerequisites

- Python 3.7 or higher
- `ics` library (should install with `pip instal -r requirements.txt`)

## 💾 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/dudebehinddude/canvas-calendar-parser
   cd canvas-calendar-parser
   ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Export your Canvas calendar:

   - Go to Calendar in Canvas
   - Select "Calendar Feed" (bottom left)
   - Click the "Click to view Calendar Feed" link to download the .ics file
   - Save the file as `canvas_export.ics` in the same directory as the script

2. Run the script:

   ```bash
   python canvas_parser.py
   ```

   Or, if you named/placed it something else:

   ```bash
   python canvas_parser.py path/to/your/calendar.ics
   ```

## 📝 Example Output

```bash
-- January 14, 2025 (Tuesday) --
CTCM-2530-H74: What is a hero?

-- January 15, 2025 (Wednesday) --
ITSC-2214-001: M0 - Course Structures and Policies Quiz

-- January 16, 2025 (Thursday) --
CTCM-2530-H74: Participation 1/16
ITSC-2214-001: M0 - PREPARE - CodeWorkout
ITSC-2214-001: M0 - PROBLEM SOLVE - Intro to CodeWorkout

-- January 17, 2025 (Friday) --
ITSC-2214-001: M0 - Computing Background Survey
MATH-2164-006: Hmwk 1
MATH-2164-006: Hmwk 2
```

## ⚠️ Known Limitations

- Only processes assignment events (intentionally filters out other calendar items)
- Works best for classes containing DEPT-1234-001 (dept-class-section)
  - It will attempt to filter out extraneous information if this isn't found, but results might be unsatisfactory
- Calendar export must be in .ics format

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.
