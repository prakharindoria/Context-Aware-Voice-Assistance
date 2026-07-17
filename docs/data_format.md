# Voice Assistant Data Format Documentation

## Overview

This document describes the JSON data format used for the voice assistant mock dataset. The format is designed for intent classification, entity extraction, multimodal processing, and assistant response generation.

---

# Dataset Structure

A voice assistant dataset contains multiple samples grouped by categories such as:

- Basic queries
- Navigation
- Weather
- Reminders
- Voice settings
- Background noise handling
- GPS/location services
- Multimodal interactions

Example:

```json
{
  "dataset_name": "voice_assistant_all_samples",
  "version": "1.0",
  "samples": []
}
