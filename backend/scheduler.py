#!/usr/bin/env python3
"""
Automated Briefing Generation Scheduler

This script generates briefings on a schedule:
- Data Analysis: Monday & Thursday (rotating reading levels)
- Article Summaries: Monday-Friday (rotating reading levels)

Run this script via cron job or task scheduler.
"""
import os
import sys
from datetime import datetime, timedelta
import requests
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import ReadingLevel

# API endpoint - use environment variable for production
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Reading level rotation for data analysis (4-week cycle)
DATA_ANALYSIS_LEVELS = [
    ReadingLevel.GRADE_6,
    ReadingLevel.GRADE_8,
    ReadingLevel.HIGH_SCHOOL,
    ReadingLevel.COLLEGE,
]

# Complementary levels for Thursday
COMPLEMENTARY_LEVELS = {
    ReadingLevel.GRADE_6: ReadingLevel.HIGH_SCHOOL,
    ReadingLevel.GRADE_8: ReadingLevel.COLLEGE,
    ReadingLevel.HIGH_SCHOOL: ReadingLevel.GRADE_6,
    ReadingLevel.COLLEGE: ReadingLevel.GRADE_8,
}

# Article summary reading levels by day of week
ARTICLE_LEVELS_BY_DAY = {
    0: ReadingLevel.GRADE_6,      # Monday
    1: ReadingLevel.GRADE_8,      # Tuesday
    2: ReadingLevel.HIGH_SCHOOL,  # Wednesday
    3: ReadingLevel.COLLEGE,      # Thursday
    4: ReadingLevel.GRADE_3,      # Friday
}

# Comprehensive health topics - rotating through major health areas
ARTICLE_TOPICS = [
    # Chronic Diseases
    "diabetes prevention and management",
    "heart disease and cardiovascular health",
    "hypertension and blood pressure control",
    "stroke prevention and recovery",
    "asthma and respiratory health",
    "COPD chronic obstructive pulmonary disease",
    "arthritis and joint health",
    "osteoporosis and bone health",
    "kidney disease and renal health",
    "liver disease and hepatic health",

    # Cancer
    "cancer prevention and screening",
    "breast cancer awareness",
    "lung cancer screening",
    "colorectal cancer prevention",
    "skin cancer and melanoma",
    "prostate cancer screening",

    # Mental Health
    "depression and mental health treatment",
    "anxiety disorders and coping strategies",
    "teen mental health and wellbeing",
    "stress management techniques",
    "addiction and substance abuse recovery",
    "PTSD and trauma recovery",
    "suicide prevention and mental health support",

    # Nutrition & Diet
    "healthy eating and nutrition guidelines",
    "weight management and obesity prevention",
    "plant-based diets and health",
    "food allergies and intolerances",
    "vitamin and mineral deficiencies",
    "eating disorders awareness",

    # Physical Activity
    "exercise benefits and recommendations",
    "fitness for different age groups",
    "injury prevention in sports",
    "physical therapy and rehabilitation",

    # Infectious Diseases
    "flu prevention and vaccination",
    "COVID-19 updates and prevention",
    "pneumonia prevention and treatment",
    "tuberculosis awareness",
    "HIV AIDS prevention and treatment",
    "sexually transmitted infections prevention",
    "Lyme disease and tick prevention",

    # Vaccines & Immunization
    "childhood vaccination schedule",
    "adult immunizations and boosters",
    "vaccine safety and efficacy",
    "travel vaccines and recommendations",

    # Women's Health
    "maternal health and pregnancy",
    "prenatal care and childbirth",
    "menopause and hormone health",
    "PCOS polycystic ovary syndrome",
    "endometriosis awareness",
    "cervical cancer screening",

    # Men's Health
    "prostate health screening",
    "testosterone and male health",
    "erectile dysfunction treatment",

    # Children's Health
    "pediatric health and development",
    "childhood obesity prevention",
    "ADHD attention deficit disorder",
    "autism spectrum disorders",
    "childhood vaccines schedule",

    # Senior Health
    "healthy aging and longevity",
    "Alzheimer's and dementia prevention",
    "fall prevention for seniors",
    "medication management for elderly",

    # Sleep & Rest
    "sleep disorders and insomnia",
    "sleep apnea treatment",
    "sleep hygiene and better rest",

    # Digestive Health
    "IBS irritable bowel syndrome",
    "Crohn's disease and colitis",
    "acid reflux and GERD",
    "celiac disease and gluten",
    "food poisoning prevention",

    # Eye & Ear Health
    "vision health and eye exams",
    "hearing loss prevention",
    "cataracts and glaucoma",

    # Dental Health
    "oral health and dental hygiene",
    "gum disease prevention",
    "tooth decay and cavities",

    # Skin Health
    "skin cancer prevention",
    "eczema and dermatitis",
    "acne treatment options",

    # Emergency & Safety
    "first aid basics",
    "CPR and emergency response",
    "fire safety and burn prevention",
    "poisoning prevention",

    # Public Health
    "antibiotic resistance and superbugs",
    "disease outbreak monitoring",
    "environmental health hazards",
    "air quality and respiratory health",
    "water safety and contamination",
    "climate change and health impacts",
]


def get_week_number():
    """Get the current week number (1-4 cycle for rotation)."""
    # Get ISO week number and cycle through 1-4
    week = datetime.now().isocalendar()[1]
    return (week % 4) + 1


def generate_data_analysis_briefing(reading_level: str):
    """Generate a data analysis briefing."""
    print(f"Generating data analysis briefing at {reading_level} level...")

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/briefings/generate",
            json={
                "source_type": "data_analysis",
                "use_mock_data": True,
                "reading_level": reading_level,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        print(f"✓ Created: {data['briefing']['title']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def generate_article_summary_briefing(topic: str, reading_level: str):
    """Generate an article summary briefing."""
    print(f"Generating article summary on '{topic}' at {reading_level} level...")

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/briefings/generate",
            json={
                "source_type": "article_summary",
                "topic": topic,
                "reading_level": reading_level,
            },
            timeout=120,
        )

        # Handle duplicate detection
        if response.status_code == 409:
            print(f"⚠ Duplicate detected for '{topic}'. Trying next topic...")
            # Try the next topic in the list
            current_index = ARTICLE_TOPICS.index(topic) if topic in ARTICLE_TOPICS else 0
            next_topic = ARTICLE_TOPICS[(current_index + 1) % len(ARTICLE_TOPICS)]
            print(f"Trying alternate topic: '{next_topic}'")

            response = requests.post(
                f"{API_BASE_URL}/api/briefings/generate",
                json={
                    "source_type": "article_summary",
                    "topic": next_topic,
                    "reading_level": reading_level,
                },
                timeout=120,
            )

        response.raise_for_status()
        data = response.json()
        print(f"✓ Created: {data['briefing']['title']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_monday_schedule():
    """Run Monday's scheduled briefings."""
    print("=== MONDAY SCHEDULE ===")

    # Data Analysis - Rotating level based on week
    week = get_week_number()
    data_level = DATA_ANALYSIS_LEVELS[week - 1]
    print(f"Week {week} of 4-week cycle")
    generate_data_analysis_briefing(data_level.value)

    # Article Summary - Grade 6
    topic_index = datetime.now().timetuple().tm_yday % len(ARTICLE_TOPICS)
    topic = ARTICLE_TOPICS[topic_index]
    generate_article_summary_briefing(topic, ReadingLevel.GRADE_6.value)


def run_tuesday_schedule():
    """Run Tuesday's scheduled briefings."""
    print("=== TUESDAY SCHEDULE ===")

    # Article Summary - Grade 8
    topic_index = datetime.now().timetuple().tm_yday % len(ARTICLE_TOPICS)
    topic = ARTICLE_TOPICS[topic_index]
    generate_article_summary_briefing(topic, ReadingLevel.GRADE_8.value)


def run_wednesday_schedule():
    """Run Wednesday's scheduled briefings."""
    print("=== WEDNESDAY SCHEDULE ===")

    # Article Summary - High School
    topic_index = datetime.now().timetuple().tm_yday % len(ARTICLE_TOPICS)
    topic = ARTICLE_TOPICS[topic_index]
    generate_article_summary_briefing(topic, ReadingLevel.HIGH_SCHOOL.value)


def run_thursday_schedule():
    """Run Thursday's scheduled briefings."""
    print("=== THURSDAY SCHEDULE ===")

    # Data Analysis - Complementary level to Monday
    week = get_week_number()
    monday_level = DATA_ANALYSIS_LEVELS[week - 1]
    thursday_level = COMPLEMENTARY_LEVELS[monday_level]
    print(f"Week {week} - Complementary to Monday's {monday_level.value}")
    generate_data_analysis_briefing(thursday_level.value)

    # Article Summary - College
    topic_index = datetime.now().timetuple().tm_yday % len(ARTICLE_TOPICS)
    topic = ARTICLE_TOPICS[topic_index]
    generate_article_summary_briefing(topic, ReadingLevel.COLLEGE.value)


def run_friday_schedule():
    """Run Friday's scheduled briefings."""
    print("=== FRIDAY SCHEDULE ===")

    # Article Summary - Grade 3
    topic_index = datetime.now().timetuple().tm_yday % len(ARTICLE_TOPICS)
    topic = ARTICLE_TOPICS[topic_index]
    generate_article_summary_briefing(topic, ReadingLevel.GRADE_3.value)


def main():
    """Main scheduler function."""
    print(f"\n{'='*60}")
    print(f"EazyHealth Briefing Scheduler")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Get current day of week (0 = Monday, 6 = Sunday)
    day_of_week = datetime.now().weekday()

    # Run appropriate schedule based on day
    if day_of_week == 0:  # Monday
        run_monday_schedule()
    elif day_of_week == 1:  # Tuesday
        run_tuesday_schedule()
    elif day_of_week == 2:  # Wednesday
        run_wednesday_schedule()
    elif day_of_week == 3:  # Thursday
        run_thursday_schedule()
    elif day_of_week == 4:  # Friday
        run_friday_schedule()
    else:
        print("Weekend - No briefings scheduled")

    print(f"\n{'='*60}")
    print("Scheduler completed")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
