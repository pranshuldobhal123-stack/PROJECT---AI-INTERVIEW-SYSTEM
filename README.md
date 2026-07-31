# PROJECT---AI-INTERVIEW-SYSTEM

This repository contains an AI interview system with a Python backend and a Next.js frontend.

## Repository layout

- `ai-interview-system/backend/` - Python backend service
- `ai-interview-system/frontend/` - Next.js frontend application

> Note: the actual project files are currently located inside the nested `ai-interview-system/` folder in this repository.

## Backend

The backend is built with Python and uses the files in `ai-interview-system/backend/`.

### Setup

```bash
cd ai-interview-system/backend
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## Frontend

The frontend is a Next.js application in `ai-interview-system/frontend/`.

### Setup

```bash
cd ai-interview-system/frontend
npm install
```

### Run

```bash
npm run dev
```

### Build

```bash
npm run build
```

## Notes

- If you want the repository root to be the actual project root, the nested `ai-interview-system/` folder should be flattened.
- The current GitHub default branch is `main`. 
