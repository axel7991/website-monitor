# 🔍 Website Change Monitor

An AI-powered SaaS tool that automatically monitors websites for changes and delivers intelligent summaries of what changed.

## 🚀 Features

- **Automated Monitoring** — tracks any website on a schedule
- **Change Detection** — instantly detects what was added or removed
- **AI Summaries** — Claude AI generates human-readable summaries of changes
- **Visual Dashboard** — real-time charts and graphs of change history
- **Change History** — full log of every change detected over time

## 🛠️ Tech Stack

- **Python** — core language
- **BeautifulSoup** — web scraping
- **Streamlit** — dashboard and UI
- **Plotly** — interactive charts
- **Anthropic Claude API** — AI-powered summaries
- **AWS** — cloud deployment

## ⚙️ Installation

```bash
git clone https://github.com/axel7991/website-monitor
cd website-monitor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Usage

**Run the monitor:**
```bash
python monitor.py
```

**Launch the dashboard:**
```bash
streamlit run dashboard.py
```

## 📊 Dashboard

The dashboard shows:
- Total checks and changes detected
- Line graph of changes over time
- Bar chart of lines added vs removed
- Full change history table

## 🔮 Roadmap

- [ ] Email alerts when changes detected
- [ ] Multi-URL monitoring
- [ ] Stripe payments and user accounts
- [ ] AWS Lambda deployment
- [ ] Claude AI summaries

## 👨‍💻 Author

Built by Axel — MS Computer Science student building AI-powered SaaS tools.