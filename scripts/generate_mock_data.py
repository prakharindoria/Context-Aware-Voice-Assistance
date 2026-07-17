#!/usr/bin/env python3
"""
generate_mock_data.py

Generate mock voice assistant JSON datasets.

Usage:
    python generate_mock_data.py

Output:
    mock_data/

Features:
    - Generate sample voice assistant data
    - Create category-based JSON files
    - Generate combined all_samples.json
    - Supports multimodal assistant examples
"""

import json
from pathlib import Path


OUTPUT_DIR = Path("mock_data")


DATASETS = {

    "basic_queries": [
        {
            "query": "Hello",
            "intent": "greeting",
            "entities": {},
            "response": "Hello! How can I help you today?"
        },
        {
            "query": "What can you do?",
            "intent": "general_question",
            "entities": {},
            "response": "I can help with navigation, weather, reminders, and device tasks."
        }
    ],

    "navigation": [
        {
            "query": "Navigate to the airport",
            "intent": "navigate",
            "entities": {
                "destination": "airport"
            },
            "response": "Starting navigation to the airport."
        },
        {
            "query": "Find restaurants near me",
            "intent": "find_place",
            "entities": {
                "place_type": "restaurant",
                "location": "nearby"
            },
            "response": "Finding nearby restaurants."
        }
    ],

    "weather": [
        {
            "query": "What's the weather today?",
            "intent": "weather_current",
            "entities": {
                "date": "today"
            },
            "response": "Fetching today's weather."
        },
        {
            "query": "Will it rain today?",
            "intent": "rain_forecast",
            "entities": {},
            "response": "Checking rain forecast."
        }
    ],

    "reminders": [
        {
            "query": "Remind me to call John at 6 PM",
            "intent": "set_reminder",
            "entities": {
                "task": "call John",
                "time": "6 PM"
            },
            "response": "Reminder set for 6 PM."
        }
    ],

    "accent": [
        {
            "query": "Use a British accent",
            "intent": "change_voice_accent",
            "entities": {
                "accent": "British"
            },
            "response": "Voice accent changed to British English."
        }
    ],

    "background_noise": [
        {
            "query": "Reduce background noise",
            "intent": "noise_reduction",
            "entities": {
                "level": "high"
            },
            "response": "Background noise reduction enabled."
        }
    ],

    "gps": [
        {
            "query": "My GPS is showing wrong location",
            "intent": "gps_drift_issue",
            "entities": {
                "issue": "incorrect_location"
            },
            "response": "Checking GPS accuracy."
        }
    ],

    "multimodal": [
        {
            "query": "Where am I?",
            "intent": "audio_location_query",
            "modality": "audio",
            "entities": {
                "location_source": "gps"
            },
            "response": "Finding your current location."
        },
        {
            "query": "What is the weather here?",
            "intent": "weather_location_query",
            "modality": "multimodal",
            "entities": {
                "location_source": "current_location"
            },
            "response": "Fetching weather for your location."
        },
        {
            "query": "What time is it here?",
            "intent": "time_location_query",
            "modality": "multimodal",
            "entities": {
                "location_source": "current_location"
            },
            "response": "Checking current local time."
        }
    ]
}


def add_ids(samples):
    """Add unique IDs."""

    for index, sample in enumerate(
        samples,
        start=1
    ):
        sample["id"] = index

    return samples


def save_dataset(name, samples):
    """Save individual dataset."""

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    data = {
        "dataset_name": name,
        "version": "1.0",
        "samples": add_ids(samples)
    }

    file_path = OUTPUT_DIR / f"{name}.json"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Created {file_path}"
    )


def create_combined_dataset():
    """Create all_samples.json."""

    combined = []

    for category, samples in DATASETS.items():

        for sample in samples:

            item = sample.copy()

            item["category"] = category

            combined.append(
                item
            )

    combined = add_ids(
        combined
    )

    data = {
        "dataset_name": "voice_assistant_all_samples",
        "version": "1.0",
        "total_samples": len(combined),
        "samples": combined
    }

    file_path = (
        OUTPUT_DIR /
        "all_samples.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Created {file_path}"
    )


def main():

    print(
        "Generating voice assistant mock datasets..."
    )

    for name, samples in DATASETS.items():

        save_dataset(
            name,
            samples
        )

    create_combined_dataset()

    print(
        "\nMock dataset generation completed."
    )


if __name__ == "__main__":
    main()
