# Holiday Planner AI

An AI-powered holiday planning application that generates personalized travel itineraries based on the user's destination, travel duration, budget, travel style, number of travelers, and selected interests.

The application uses Groq AI to generate the itinerary and Streamlit to provide an interactive web interface.

---

## Project Overview

Planning a holiday manually can require searching through many websites for destinations, activities, food, accommodation, travel routes, and estimated costs.

Holiday Planner AI simplifies this process by allowing users to enter their travel requirements and automatically generate a personalized holiday plan.

The application can generate:

- Destination-based travel plans
- Day-by-day itineraries
- Accommodation suggestions
- Food recommendations
- Travel planning suggestions
- Budget estimates
- Interest-based activities
- Travel tips
- AI-powered follow-up chat
- Downloadable PDF itinerary

---

## Features

### 1. Personalized Holiday Planning

Users provide:

- Destination
- Starting location
- Number of days
- Number of travelers
- Budget
- Travel style
- Interests

The AI uses these details to generate a personalized itinerary.

### 2. Interest-Based Planning

Available interests include:

- Beaches
- Food
- Culture & Heritage
- Shopping
- Nightlife
- Adventure
- Nature & Wildlife
- Temples & Spiritual
- Art & Museums
- Photography
- Water Sports
- Family Activities
- Romantic Places
- Cafés & Relaxation
- Trekking

The AI is instructed to focus on the interests selected by the user.

### 3. Day-by-Day Itinerary

The generated plan contains detailed daily activities.

Example:

```text
Day 1

Morning:
- Arrival at destination
- Hotel check-in

Afternoon:
- Visit nearby attractions

Evening:
- Local food and relaxation
```

### 4. Budget-Aware Planning

The AI considers the user's budget while generating the itinerary.

It is instructed not to create unrealistic prices simply to fit the user's budget.

If the budget is insufficient, the AI should provide a realistic minimum estimate.

### 5. Travel Consistency

The AI is instructed to maintain logical travel timing.

```text
Arrival
   |
   v
Hotel check-in
   |
   v
Activities
   |
   v
Dinner
   |
   v
Overnight stay
```

The application avoids placing activities before the traveler arrives.

### 6. AI Travel Assistant

After generating the itinerary, users can continue chatting with the AI.

Example:

```text
User:
Can I replace Day 2 with more photography locations?

AI:
Yes. Day 2 can be modified to focus on photography locations.
```

### 7. PDF Export

The generated itinerary can be downloaded as a PDF.

The application uses ReportLab for PDF generation.

### 8. Create New Holiday

The sidebar provides an action for creating a new holiday plan.

When a new plan is started:

- Current itinerary is cleared
- Current chat is cleared
- The user can enter new travel details

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application UI |
| Groq API | AI itinerary generation |
| python-dotenv | Environment variable management |
| ReportLab | PDF generation |

---

## Project Structure

```text
Holiday-Planner/
|
├── app.py
├── style.css
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## File Description

### app.py

Main application file containing:

- Streamlit interface
- User input form
- Groq API integration
- Holiday plan generation
- AI chat
- PDF generation
- Session state management

### style.css

Contains custom application styling for:

- Dark theme
- Sidebar
- Buttons
- Input fields
- Select boxes
- Multiselect
- Result page
- Expanders
- Chat interface
- PDF button
- Responsive layout

### requirements.txt

```txt
streamlit
groq
python-dotenv
reportlab
```

### .env

Example:

```env
GROQ_API_KEY="your_groq_api_key"
GROQ_MODEL="openai/gpt-oss-20b"
```

Never upload the `.env` file to GitHub.

### .gitignore

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Holiday-Planner.git
cd Holiday-Planner
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq API

Create a `.env` file in the project root:

```env
GROQ_API_KEY="your_groq_api_key"
GROQ_MODEL="openai/gpt-oss-20b"
```

Replace `your_groq_api_key` with your actual Groq API key.

### 5. Run the Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Application Workflow

```text
              User
                |
                v
       Enter Holiday Details
                |
                v
       Streamlit Interface
                |
                v
            Groq API
                |
                v
          AI Processing
                |
                v
     Personalized Holiday Plan
                |
        +-------+-------+
        |               |
        v               v
      AI Chat       PDF Export
```

---

## AI Prompt Personalization

The application sends the user's travel information to the Groq model.

The AI receives:

```text
Destination
Starting Location
Number of Days
Number of Travelers
Budget
Travel Style
Selected Interests
```

The prompt instructs the model to create a realistic and personalized itinerary.

---

## Interest Matching

A strict interest-matching rule is used.

For example:

```text
Beaches, Food, Photography
```

The AI is instructed:

```text
The following are the ONLY interests selected by the user.

You MUST use ONLY these selected interests.

NEVER add an interest that the user did not select.

NEVER change, replace, or reinterpret the user's interests.

Every Interest Focus / Interest Match must contain only selected interests.

At least 70-80% of optional sightseeing and activities
should directly match selected interests.
```

This helps prevent unrelated activities from being generated.

---

## Budget Handling

The AI is instructed:

```text
Do not invent unrealistically cheap prices just to fit budget.

If budget is insufficient, say so and give realistic minimum estimate.
```

This helps keep travel cost estimates realistic.

---

## Travel Consistency

The AI is instructed:

```text
Do not show activity before arrival.

Do not count the same travel period twice.

Keep overnight travel logically consistent.
```

---

## PDF Generation

The application uses ReportLab.

```text
Generated AI Plan
       |
       v
Clean Text
       |
       v
Convert Markdown/HTML
       |
       v
ReportLab
       |
       v
A4 PDF
       |
       v
Download
```

The application also cleans unsupported characters such as:

```text
₹
–
—
•
→
←
✓
✗
```

HTML line breaks such as `<br>`, `<br/>`, and `<br />` are converted into ReportLab-compatible line breaks.

---

## AI Chat

Example questions:

```text
Can you make Day 2 cheaper?

Suggest more food places.

Can I add another day?

Which activities are best for photography?

Can you make this trip suitable for a family?

Can you reduce travel time?
```

The AI uses the generated holiday plan as context when answering.

---

## User Interface

The application uses a dark theme based on:

```text
Background:
#080f1c

Sidebar:
#0b1424

Card:
#111c2d

Input:
#0f1a2b

Primary Blue:
#2563eb

Cyan:
#22d3ee

Text:
#f8fafc

Secondary Text:
#94a3b8
```

---

## Security

The Groq API key is stored in `.env`.

```env
GROQ_API_KEY="your_api_key"
```

The `.env` file should be excluded from Git:

```gitignore
.env
```

Never hard-code the API key inside `app.py`.

---

## Components Not Used

The simplified version intentionally does not use:

- MongoDB
- LangChain
- LangGraph
- FAISS
- ChromaDB
- MySQL
- RailRadar API
- External train APIs
- PDF parsing
- Resume parsing

The project is intentionally kept small and focused.

---

## Future Improvements

Possible future improvements include:

- Interactive maps
- Weather information
- Real hotel availability
- Flight information
- Live train information
- Currency conversion
- Nearby attractions
- User ratings
- Destination images
- User accounts
- Saved itineraries
- Mobile-friendly application
- Cloud deployment

---

## Testing

### User Input

- [ ] Destination
- [ ] Starting location
- [ ] Number of days
- [ ] Number of travelers
- [ ] Budget
- [ ] Travel style
- [ ] Interests

### AI Generation

- [ ] Itinerary generated successfully
- [ ] Selected interests respected
- [ ] Budget considered
- [ ] Travel timing is logical
- [ ] Day-by-day plan generated

### PDF

- [ ] PDF generates successfully
- [ ] Special characters do not break PDF
- [ ] `<br>` tags do not cause errors
- [ ] PDF can be downloaded
- [ ] PDF content is readable

### Chat

- [ ] Chat input works
- [ ] AI receives itinerary context
- [ ] New holiday clears previous chat

---

## Common Errors

### Groq API Key Error

If you see:

```text
GROQ_API_KEY is missing
```

check your `.env` file:

```env
GROQ_API_KEY="your_actual_key"
```

### Model Error

Check:

```env
GROQ_MODEL="openai/gpt-oss-20b"
```

### PDF Generation Error

If ReportLab reports an error involving `paraparser`, check the generated AI text for unsupported HTML.

The `clean_pdf_text()` function converts HTML line breaks and unsupported characters before sending text to ReportLab.

### Streamlit Not Found

If:

```text
streamlit is not recognized
```

activate the virtual environment:

```bash
venv\Scripts\activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

---

## License

This project is created for educational and academic purposes.

You may modify and extend the project according to your requirements.

---

## Author

Shourya Basu

Holiday Planner AI

Built using:

```text
Python
Streamlit
Groq AI
ReportLab
```

---

## Project Summary

Holiday Planner AI is a lightweight AI-powered travel planning application that transforms user travel preferences into a personalized holiday itinerary.

The application combines:

```text
User Preferences
       +
Groq AI
       +
Streamlit
       +
ReportLab
       |
       v
Personalized Holiday Plan
```

The goal is to make holiday planning faster, simpler, and more personalized through generative AI.
