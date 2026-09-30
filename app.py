import os
import re
from io import BytesIO
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing in your .env file.")
    st.stop()

if not GROQ_MODEL:
    st.error("GROQ_MODEL is missing in your .env file.")
    st.stop()


groq_client = Groq(
    api_key=GROQ_API_KEY
)

st.set_page_config(
    page_title="Holiday Planner",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    """
    Load styling from style.css.
    """

    css_file = Path(__file__).parent / "style.css"

    if css_file.exists():

        with open(
            css_file,
            "r",
            encoding="utf-8"
        ) as file:

            css = file.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )


load_css()

if "holiday_plan" not in st.session_state:
    st.session_state["holiday_plan"] = None

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

def generate_holiday_plan(
    destination,
    starting_from,
    days,
    travelers,
    budget,
    travel_style,
    interests
):
    """
    Generate a personalized holiday plan using Groq.
    """

    interests_text = ", ".join(interests)

    if not interests_text:

        interests_text = (
            "General sightseeing, local food and relaxation"
        )


    prompt = f"""
You are an expert Indian travel planner.

Create a realistic, detailed and practical holiday itinerary.

USER INFORMATION
----------------
Destination: {destination}
Starting From: {starting_from}
Number of Days: {days}
Number of Travelers: {travelers}
Budget: ₹{budget}
Travel Style: {travel_style}

SELECTED INTERESTS
------------------
{interests_text}


IMPORTANT INTEREST RULE
-----------------------

The following are the ONLY interests selected by the user:

{interests_text}

You MUST use ONLY these selected interests.

NEVER:

- add an interest that the user did not select
- replace an interest with another interest
- reinterpret the user's selected interests
- introduce unrelated activities
- claim an activity matches an interest that was not selected

Every "Interest Focus" and "Interest Match" must contain ONLY
the interests selected by the user.

At least 70-80% of optional sightseeing and activities should
directly match the selected interests.


TRAVEL LOGIC
------------

- Keep the itinerary geographically logical.
- Do not place activities before arrival.
- Do not count the same travel period twice.
- Explain overnight travel clearly if required.
- Do not create impossible schedules.
- Include reasonable travel time between locations.
- Avoid excessive travel between distant places in one day.


BUDGET LOGIC
------------

- Give realistic Indian travel estimates.
- Do not invent unrealistically cheap prices just to fit the budget.
- Include transportation, accommodation, food and activities.
- If the budget is insufficient, clearly say so.
- Give a realistic minimum estimate when necessary.


OUTPUT FORMAT
-------------

# {destination} Holiday Plan


## Trip Overview

Include:

- Destination
- Duration
- Travelers
- Starting Location
- Travel Style
- Budget
- Selected Interests


## Transportation Plan

Explain:

- How to reach the destination from {starting_from}
- Recommended transportation
- Approximate travel time
- Approximate transportation cost


## Accommodation Suggestion

Give:

- Recommended area to stay
- Type of accommodation
- Approximate nightly price
- Why that area is suitable


## Day-by-Day Itinerary

For EVERY day use this structure:


### Day 1 - [Interesting Title]

**Morning**

- Activity
- Location
- Approximate timing
- Estimated cost


**Afternoon**

- Activity
- Location
- Approximate timing
- Estimated cost


**Evening**

- Activity
- Location
- Approximate timing
- Estimated cost


** Food Recommendation**

- Local food
- Restaurant/cafe type
- Approximate cost


** Interest Focus**

Only mention selected interests.


** Day Cost**

Give an estimated total cost for the day.


Repeat this structure for every day.


## Estimated Budget

Create this table:

| Category | Estimated Cost |
|---|---:|
| Transportation | ₹... |
| Accommodation | ₹... |
| Food | ₹... |
| Activities | ₹... |
| Local Transport | ₹... |
| Miscellaneous | ₹... |
| Total | ₹... |


## Travel Tips

Give useful destination-specific tips.


## Important Notes

Mention:

- Weather considerations
- Local transportation
- Booking considerations
- Safety considerations
- Important destination-specific information


Keep the itinerary realistic, practical and personalized.
"""


    try:

        response = groq_client.chat.completions.create(

            model=GROQ_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional travel planner. "
                        "Create realistic, practical and "
                        "personalized Indian travel itineraries."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,
            max_tokens=6000
        )


        return response.choices[0].message.content


    except Exception as e:

        return f"""
## Error Generating Holiday Plan

Something went wrong while contacting the AI.

**Error:**

{str(e)}
"""

def chat_with_holiday_ai(
    question,
    holiday_plan
):
    """
    Answer questions using the generated holiday itinerary.
    """

    prompt = f"""
You are a helpful travel assistant.

The user has generated the following holiday plan:

------------------------------
{holiday_plan}
------------------------------

Answer the user's question using the itinerary above.

Rules:

- Stay consistent with the itinerary.
- Do not contradict the itinerary.
- Do not invent information that conflicts with the plan.
- If information is not available in the itinerary,
  clearly say so.
- Give practical travel advice.
- Keep the answer concise but useful.

User Question:

{question}
"""


    try:

        response = groq_client.chat.completions.create(

            model=GROQ_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful holiday planning "
                        "assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,
            max_tokens=2000
        )


        return response.choices[0].message.content


    except Exception as e:

        return f" Chat error: {str(e)}"


# ============================================================
# PDF TEXT CLEANING
# ============================================================

def clean_pdf_text(text):
    """
    Safely clean AI-generated text for ReportLab Paragraph.
    """

    if not text:
        return ""

    text = str(text)

    # Normalize line breaks
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    # Remove any remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Escape XML-sensitive characters
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    # Convert normal newlines into ReportLab line breaks
    text = text.replace("\n", "<br/>")

    return text.strip()

# ============================================================
# PDF GENERATOR
# ============================================================

def create_pdf(holiday_plan):
    """
    Convert the generated itinerary into a PDF.
    """

    buffer = BytesIO()


    # --------------------------------------------------------
    # DOCUMENT
    # --------------------------------------------------------

    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,

        title="Holiday Planner",
        author="Holiday Planner AI"
    )


    # --------------------------------------------------------
    # STYLES
    # --------------------------------------------------------

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "HolidayTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=8
    )


    subtitle_style = ParagraphStyle(
        "HolidaySubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=16
    )


    h1_style = ParagraphStyle(
        "HolidayH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=12,
        spaceAfter=8
    )


    h2_style = ParagraphStyle(
        "HolidayH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0891B2"),
        spaceBefore=10,
        spaceAfter=6
    )


    h3_style = ParagraphStyle(
        "HolidayH3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1D4ED8"),
        spaceBefore=8,
        spaceAfter=4
    )


    body_style = ParagraphStyle(
        "HolidayBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=5
    )


    bullet_style = ParagraphStyle(
        "HolidayBullet",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-8,
        spaceAfter=4
    )


    story = []
    story.append(
        Paragraph(
            "Holiday Planner",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI Generated Travel Itinerary",
            subtitle_style
        )
    )
    lines = holiday_plan.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Empty line

        if not line:
            story.append(
                Spacer(1, 4)
            )
            i += 1
            continue

        if line.startswith("|"):
            table_rows = []

            while (
                i < len(lines)
                and lines[i].strip().startswith("|")
            ):
                current_line = lines[i].strip()
                cells = [
                    cell.strip()
                    for cell in
                    current_line.strip("|").split("|")
                ]

                # Skip separator row
                is_separator = all(
                    re.fullmatch(
                        r":?-{2,}:?",
                        cell
                    )
                    for cell in cells
                )

                if not is_separator:
                    table_rows.append(
                        cells
                    )
                i += 1

            if table_rows:
                pdf_rows = []
                for row in table_rows:
                    pdf_row = []
                    for cell in row:
                        cell = re.sub(
                            r"\*\*(.*?)\*\*",
                            r"<b>\1</b>",
                            cell
                        )

                        pdf_row.append(
                            Paragraph(
                                clean_pdf_text(cell),
                                body_style
                            )
                        )

                    pdf_rows.append(
                        pdf_row
                    )

                table = Table(
                    pdf_rows,
                    repeatRows=1,
                    hAlign="LEFT"
                )

                table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, 0),
                                colors.HexColor("#2563EB")
                            ),
                            (
                                "TEXTCOLOR",
                                (0, 0),
                                (-1, 0),
                                colors.white
                            ),
                            (
                                "FONTNAME",
                                (0, 0),
                                (-1, 0),
                                "Helvetica-Bold"
                            ),
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.5,
                                colors.HexColor("#CBD5E1")
                            ),
                            (
                                "BACKGROUND",
                                (0, 1),
                                (-1, -1),
                                colors.HexColor("#F8FAFC")
                            ),
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP"
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                5
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                5
                            ),
                        ]
                    )
                )
                story.append(table)
                story.append(
                    Spacer(1, 10)
                )
            continue

        if line.startswith("# ") and not line.startswith("## "):
            text = line[2:].strip()
            story.append(
                Paragraph(
                    clean_pdf_text(text),
                    h1_style
                )
            )
            i += 1
            continue

        if line.startswith("## "):

            text = line[3:].strip()

            story.append(
                Paragraph(
                    clean_pdf_text(text),
                    h2_style
                )
            )

            i += 1

            continue

        if line.startswith("### "):

            text = line[4:].strip()

            story.append(
                Paragraph(
                    clean_pdf_text(text),
                    h3_style
                )
            )

            i += 1

            continue

        if line.startswith("- "):
            text = line[2:].strip()
            text = re.sub(
                r"\*\*(.*?)\*\*",
                r"<b>\1</b>",
                text
            )
            story.append(
                Paragraph(
                    "- " + clean_pdf_text(text),
                    bullet_style
                )
            )
            i += 1
            continue

        if re.match(
            r"^\d+\.\s",
            line
        ):
            text = re.sub(
                r"\*\*(.*?)\*\*",
                r"<b>\1</b>",
                line
            )
            story.append(
                Paragraph(
                    clean_pdf_text(text),
                    bullet_style
                )
            )
            i += 1
            continue

        text = re.sub(
            r"\*\*(.*?)\*\*",
            r"<b>\1</b>",
            line
        )

        story.append(
            Paragraph(
                clean_pdf_text(text),
                body_style
            )
        )

        i += 1

    def add_page_number(
        canvas,
        doc
    ):

        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8
        )

        canvas.setFillColor(
            colors.HexColor("#64748B")
        )

        canvas.drawCentredString(
            A4[0] / 2,
            10 * mm,
            f"Holiday Planner AI  •  Page {doc.page}"
        )

        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )


    buffer.seek(0)

    return buffer.getvalue()

with st.sidebar:

    if st.button(
        "NEW",
        key="new_holiday_button",
        help="Create a new holiday plan"
    ):
        st.session_state["holiday_plan"] = None
        st.session_state["chat_messages"] = []
        st.rerun()


if st.session_state["holiday_plan"] is None:


    st.markdown(
        '<div class="hp-title">'
        ' Holiday '
        '<span class="hp-title-accent">Planner</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hp-subtitle">'
        'Create a personalized holiday itinerary with AI.'
        '</div>',
        unsafe_allow_html=True
    )


    left_space, form_column, right_space = st.columns(
        [1, 3, 1]
    )


    with form_column:
        with st.form("holiday_form"):

            st.markdown(
                "###  Trip Details"
            )

            st.caption(
                "Tell us where you want to go and how you want to travel."
            )

            col1, col2 = st.columns(2)


            with col1:

                destination = st.text_input(
                    "Destination",
                    placeholder="Example: Goa"
                )


            with col2:

                starting_from = st.text_input(
                    "Starting From",
                    placeholder="Example: Kolkata"
                )

            col1, col2 = st.columns(2)


            with col1:

                days = st.number_input(
                    " Number of Days",
                    min_value=1,
                    max_value=30,
                    value=5
                )


            with col2:

                travelers = st.number_input(
                    " Number of Travelers",
                    min_value=1,
                    max_value=20,
                    value=2
                )

            col1, col2 = st.columns(2)


            with col1:

                budget = st.number_input(
                    " Total Budget (₹)",
                    min_value=1000,
                    max_value=1000000,
                    value=30000,
                    step=1000
                )


            with col2:

                travel_style = st.selectbox(
                    " Travel Style",

                    [
                        "Relaxing",
                        "Budget",
                        "Comfort",
                        "Luxury",
                        "Adventure",
                        "Family",
                        "Romantic",
                        "Backpacking"
                    ]
                )


            st.markdown(
                "###  Your Interests"
            )

            st.caption(
                "Select everything you are interested in."
            )


            interests = st.multiselect(
                "Select your interests",

                [
                    " Beaches",
                    " Food",
                    " Culture & Heritage",
                    " Shopping",
                    " Nightlife",
                    " Adventure",
                    " Nature & Wildlife",
                    " Temples & Spiritual",
                    " Art & Museums",
                    " Photography",
                    " Water Sports",
                    " Family Activities",
                    " Romantic Places",
                    " Cafés & Relaxation",
                    " Trekking"
                ]
            )
            st.write("")

            generate_button = st.form_submit_button(
                " Generate My Holiday Plan",
                use_container_width=True
            )

        if generate_button:
            if not destination:
                st.warning(
                    " Please enter your destination."
                )

            elif not starting_from:
                st.warning(
                    " Please enter your starting location."
                )

            else:
                with st.spinner(
                    " Creating your personalized holiday plan..."
                ):

                    holiday_plan = generate_holiday_plan(
                        destination=destination,
                        starting_from=starting_from,
                        days=days,
                        travelers=travelers,
                        budget=budget,
                        travel_style=travel_style,
                        interests=interests
                    )

                st.session_state["holiday_plan"] = (
                    holiday_plan
                )
                st.session_state["chat_messages"] = []

                st.rerun()

else:

    holiday_plan = st.session_state["holiday_plan"]

    st.markdown(
        '<div class="hp-title">'
        ' Your '
        '<span class="hp-title-accent">Holiday Plan</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hp-subtitle">'
        'Your personalized itinerary is ready.'
        '</div>',
        unsafe_allow_html=True
    )


    try:

        pdf_file = create_pdf(
            holiday_plan
        )


        col1, col2, col3 = st.columns(
            [1, 1, 1]
        )


        with col2:

            st.download_button(

                label=" Save Holiday Plan as PDF",

                data=pdf_file,

                file_name="holiday_plan.pdf",

                mime="application/pdf",

                use_container_width=True
            )


    except Exception as e:

        st.warning(
            f"PDF could not be generated: {str(e)}"
        )


    st.divider()


    # --------------------------------------------------------
    # ITINERARY
    # --------------------------------------------------------

    st.markdown(
        holiday_plan
    )


    st.divider()


    # ========================================================
    # DETAILED DAYS
    # ========================================================

    st.subheader(
        " Explore Your Days in More Detail"
    )

    st.caption(
        "Open a day to see the complete schedule, "
        "food recommendations and estimated costs."
    )


    lines = holiday_plan.split("\n")

    day_sections = []

    current_day = None

    current_content = []


    for line in lines:


        if line.strip().startswith(
            "### Day"
        ):


            if current_day is not None:

                day_sections.append(
                    (
                        current_day,
                        "\n".join(
                            current_content
                        )
                    )
                )


            current_day = line.strip()

            current_content = []


        elif current_day is not None:

            current_content.append(
                line
            )


    if current_day is not None:

        day_sections.append(
            (
                current_day,
                "\n".join(
                    current_content
                )
            )
        )


    if day_sections:


        for (
            day_title,
            day_content
        ) in day_sections:


            clean_title = day_title.replace(
                "### ",
                ""
            )


            with st.expander(
                f" {clean_title}",
                expanded=False
            ):

                st.markdown(
                    day_content
                )


    else:

        st.info(
            "Detailed day sections could not be separated "
            "from the generated itinerary."
        )


    st.divider()


    st.subheader(
        " Ask Your Travel Assistant"
    )

    st.caption(
        "Ask questions about your itinerary and get "
        "AI-powered answers."
    )


    for message in st.session_state[
        "chat_messages"
    ]:


        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    user_question = st.chat_input(
        "Ask something about your holiday..."
    )


    if user_question:

        st.session_state[
            "chat_messages"
        ].append(
            {
                "role": "user",
                "content": user_question
            }
        )


        with st.chat_message(
            "user"
        ):

            st.markdown(
                user_question
            )

        with st.chat_message(
            "assistant"
        ):


            with st.spinner(
                "Thinking..."
            ):

                answer = chat_with_holiday_ai(

                    question=user_question,

                    holiday_plan=holiday_plan
                )


            st.markdown(
                answer
            )


        st.session_state[
            "chat_messages"
        ].append(
            {
                "role": "assistant",
                "content": answer
            }
        )