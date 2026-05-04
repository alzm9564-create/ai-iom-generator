# AI IOM Generator

This is a web-based tool that generates engineering IOM documents using AI.

## Demo

![demo](docs/demo.gif)

## Live Demo
Coming soon (deploying)

## What it does
- Generate structured IOM documents from inputs
- Store history (SQLite)
- Delete records
- Download as .txt

## Why this project
Built to demonstrate AI integration into manufacturing workflows (IOM automation).

## Features
- Generate structured engineering documents
- Store history in database
- Delete records
- Download generated documents

## Tech Stack
- Python (Flask)
- OpenAI API
- SQLite

## How to Run

1. Install dependencies
   pip install -r requirements.txt

2. Set API key
   set OPENAI_API_KEY=your_api_key

3. Run
   python app.py

4. Open browser
   http://127.0.0.1:5000

## Project Structure

app.py  
templates/index.html