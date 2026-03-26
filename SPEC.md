# Athena-Revision - Project Specification

## Overview

Athena-Revision is an AI-powered study revision tool designed for Athena, a student. It allows teachers/parents (Cui) to capture textbook content and generate personalized practice questions.

## User Flow

### Step 1: Content Capture (Cui)
- Send photo of textbook page to Goblin via Discord
- Goblin uses AI vision to extract text
- Content stored as Markdown in `content/` folder
- Organized by subject and chapter

### Step 2: Quiz Selection (Athena)
- Open app at subject/chapter selection
- Choose desired quiz type
- Set difficulty level (Easy/Medium/Hard)

### Step 3: Practice (Athena)
- Receive generated questions
- Answer and submit
- Get instant feedback with explanations

## Features

### Content Management
- [ ] Image upload via Discord
- [ ] AI text extraction (OCR via vision model)
- [ ] Markdown formatting and storage
- [ ] Subject/chapter organization
- [ ] Content versioning (git)

### Quiz Generation
- [ ] Multiple Choice Questions (MCQ)
- [ ] True/False questions
- [ ] Fill-in-the-blank
- [ ] Short answer questions
- [ ] Essay questions
- [ ] Difficulty levels

### App Interface
- [ ] Subject selection
- [ ] Chapter navigation
- [ ] Quiz type selector
- [ ] Question display
- [ ] Answer input
- [ ] Score tracking
- [ ] Progress history

## Data Structure

### Content Format (Markdown)
```markdown
# Chapter 1: Introduction to Biology

## Key Concepts
- Cell: The basic unit of life
- DNA: Deoxyribonucleic acid

## Important Terms
- **Prokaryote**: Cell without nucleus
- **Eukaryote**: Cell with nucleus
```

### Quiz Format (JSON)
```json
{
  "chapter": "1",
  "subject": "biology",
  "questions": [
    {
      "type": "mcq",
      "question": "What is the basic unit of life?",
      "options": ["Atom", "Cell", "Molecule", "Organ"],
      "answer": "Cell",
      "explanation": "The cell is the smallest unit that can carry out all life processes."
    }
  ]
}
```

## Technical Implementation

### Frontend
- HTML5/CSS3/JavaScript (Vanilla)
- Responsive design for tablet/mobile
- LocalStorage for progress tracking

### Backend/AI
- Goblin AI for content extraction
- Claude API for question generation
- GitHub for content storage

### Security
- Content is private (Athena's study materials)
- GitHub repo is public but content is generic educational material

## Future Enhancements

- [ ] Spaced repetition learning
- [ ] Progress analytics dashboard
- [ ] Study timer/pomodoro
- [ ] Voice input/output
- [ ] Export to PDF/flashcards
- [ ] Multi-language support

---

*Created by Goblin for Cui and Athena 👺*
*Last Updated: 2026-03-26*
