# 🏠 Smart Property Finder

Smart Property Finder is a **Model Context Protocol (MCP)** tool built for the **Puch AI WhatsApp bot**. It helps users discover real-estate listings and get intelligent property insights directly in chat.

Using **[Firecrawl](https://firecrawl.dev)** for web scraping and **Groq LLM** for deep contextual analysis, this project allows users to retrieve personalized property recommendations from platforms like **99acres** and **SquareYards**.

---

## ✨ Features
- 🔍 **Scrape property listings** using Firecrawl based on user queries.  
- 🧠 **LLM-powered analysis** of property data and location context via Groq API.  
- 💬 **Delivered on WhatsApp** using Puch AI’s conversational interface.  

---

## 🛠️ How It Works

```mermaid
graph TD
    A[User input on WhatsApp] -->|via Puch AI| B[MCP Tool]
    B --> C[Firecrawl<br/>Web scraping]
    C --> D[Raw property JSON]
    D --> E[Groq LLM analysis]
    E --> F[Insights + Summary]
    F --> G[Reply to user via WhatsApp]