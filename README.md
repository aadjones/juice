# Demby Analytics™

A personal dashboard for tracking your creative energy and mental state. 

## What is it?

Demby Analytics helps you track two key metrics:
- **Juice** (0-10): Your creative energy and motivation
- **Anxiety** (0-10): Your stress or resistance level

From these, it calculates several derived metrics like Gumption Quotient (GQ) and Focus Flux to help you understand your creative patterns.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to the URL shown (usually http://localhost:8501)

4. On first visit, pick a nickname to start your own log. Or use the demo data to explore.

## Features

- 📊 Daily logging of Juice and Anxiety levels
- 📈 Interactive charts showing trends
- 🗓️ Calendar heatmap of your energy patterns
- 📱 Mobile-friendly interface
- 📑 Export KPI reports as PowerPoint decks

## Privacy

Your data is stored locally in CSV files under the `data/` directory. No data is sent to any server.

## Development

To run the test suite:

```bash
# Install in development mode
pip install -e .

# Run tests
pytest
```

## License

MIT