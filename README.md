![Llamita Sincera App](static/screenshot-llamitasincera.jpg)

## Features

- AI-Powered Chats: "Llamita Sincera" uses the advanced Llama 2 AI model, creating more genuine and context-aware conversations.
- Offline Privacy: This app lets you train your AI using personal data offline. No need for internet access, keeping your information secure.

## Requirements

- Python 3.9
- Node 18

## Installation

1. Install Python dependencies:

```
pip install -r requirements.txt
```

2. Install Node.js dependencies:

```
npm install
```

3. Download a language model and place it in the `models` folder. [List of LLMs](models/README.md)

## Run

1. Start the backend server using one of the following commands, depending on your Python version:

```
python -i main.py
```

or 

```
python3 -i main.py
```

2. Once the backend is up and running, start the frontend development server with the following command: 

```
npm run dev
```

## Backend

- Llama 2
- Chroma DB
- Sentence Transformers
- Langchain
- Python
- Flask

## Frontend

- SvelteKit
- TypeScript
- Tailwind CSS
- Skeleton

## Roadmap

- [x] Linux version
- [x] Windows version
- [ ] Mac version
- [x] .md file type supported
- [x] .pdf file type supported
- [ ] .doc file type supported
