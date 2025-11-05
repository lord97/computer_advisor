# AI Computer Advisor (Django + LLM)

---

## Project Overview

This project implements an **AI-powered computer recommendation system**, combining:

- Python
- Django (frontend + backend)
- Gemini API (LLM inference)
- Prompt engineering
- SQLite database lookup

The user interacts with a chat-style web interface (Q&A style), and the AI recommends suitable computers based on:

- Budget
- Usage type (e.g., gaming, business, student, editing, etc.)
- Device specs stored in the DB

Example query:

> "I am a gamer, and my budget is under 5000 EUR"

The system performs:

1. Semantic interpretation (Gemini) — understand domain intent
2. Query the local DB (SQLite) — filter by price + category
3. Return final recommended devices

---

## Author

**SANOU Mohamed Bachir**

- Software Engineering Student @ 中国科学技术大学 (USTC), China
- Interests: AI / Machine Learning / Software Development
- Email: [**sanoumohamed@mail.ustc.edu.cn**](mailto\:sanoumohamed@mail.ustc.edu.cn)
- GitHub: [**https://github.com/lord97**](https://github.com/lord97)
- Portfolio: [**https://lord97.github.io/my-portfolio/**](https://lord97.github.io/my-portfolio/)

---

## Tech Stack

| Component          | Technology                    |
| ------------------ | ----------------------------- |
| Frontend Framework | Django Templates + Bootstrap  |
| Backend            | Python 3 + Django             |
| LLM                | Gemini API                    |
| Prompting          | Multi‑turn prompt engineering |
| Database           | SQLite                        |

---

## Features

- Chat-like UI to interact with the advisor
- LLM interprets user needs using prompt engineering
- Automatic DB filtering (budget + category)
- Returns final ranked recommendations
- Simple extensible schema for more products

---



---

## Example Prompt Flow

**User:** *"I'm a gamer, budget < 5000 EUR"*

**LLM:** *identify category = gaming*

---

## Future Improvements

- Add JWT Auth for user profiles
- Add ranking based on performance/price ratio
- Move DB to PostgreSQL or Cloud SQL
- Deploy on Render or HuggingFace Spaces

---

## Run Locally (simple)

```bash
pip install -r requirements.txt
python manage.py runserver
```

---

## License

MIT

