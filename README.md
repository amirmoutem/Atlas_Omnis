# The AtlasOmnis Firm

AtlasOmnis is an AI agent orchestration composed of seven "experts" each one with a specific specialization revolving around Moroccan and Global Economics. The goal is to produce two coherent detailed reports (same content just one in French the other in Arabic) on a specific topic about Economics or Econometrics.

## The Problem

Economics is a very complex field, which contains topics and questions that require immense reasoning. So, delegating a request containing these advanced concepts to one LLM, will produce poor outputs that only cover the surface of that specific topic. This explains the need of multiple LLMs or agents that cover different niches (i.e OSINT research, economic and legal analysis, strategic synthesis etc...) to produce together a detailed and rich document. And that is what AtlasOmnis is for. 

## AtlasOmnis Architecture

Atlas Omnis is composed of  7 different agents each with a specific goal and role. They all work together to produce the final bilingual reports, this diagram explains thoroughly the role of each agent and how they cooperate.

```mermaid
graph TD
    A["User Query on Economics"] -->|Submit| B["OSINT & Research"]
    B -->|Gather Data| C{"Multi-Agent Analysis"}
    C -->|Financial Analysis| D1["Financial Agent"]
    C -->|Judicial Analysis| D2["Judicial Agent"]
    C -->|Quantitative Analysis| D3["Quantitative Agent"]
    D1 -->|Compile Results| E["Synthesis & Writing in French"]
    D2 -->|Compile Results| E
    D3 -->|Compile Results| E
    E -->|Generate Document| F["Arabic Translation"]
    F -->|Preserve Content| G["Quality Audit"]
    G -->|Approved| H["Bilingual PDF Report"]
    G -->|Rejected| B
    H -->|Deliver| I["French + Arabic Output"]

    classDef userInput fill:#f0f9ff,stroke:#38bdf8
    classDef research fill:#f0fdf4,stroke:#4ade80
    classDef analysis fill:#fdf4ff,stroke:#e879f9
    classDef agent fill:#fff7ed,stroke:#fb923c
    classDef synthesis fill:#f5f3ff,stroke:#a78bfa
    classDef translation fill:#ecfeff,stroke:#22d3ee
    classDef audit fill:#fef2f2,stroke:#f87171
    classDef output fill:#f7fee7,stroke:#a3e635

    class A userInput
    class B research
    class C analysis
    class D1 agent
    class D2 agent
    class D3 agent
    class E synthesis
    class F translation
    class G audit
    class H output
    class I output
```

We use the CrewAI framework to orchestrate this process. We implemented the sequential process to avoid some earlier problems related to the hierarchical process, which boiled down to the manager doing all the work and not delegating tasks. The sequential process means that the agents work in order seen in the diagram, one by one. We chose the bilingual PDF output (French+Arabic) because those two languages are essential in the Moroccan MEF. 

## The Seven Agents

| Agent           | Role                          | Responsibility                                           |
| --------------- | ----------------------------- | -------------------------------------------------------- |
| Researcher   | OSINT & Economic research | Collects extensive and detailed contextual Moroccan data                 |
| Jurist       | Moroccan Legal Analyst           | Analyzes Moroccan laws and Dahirs                        |
| Statistician | Quantitative Analyst          | Develops KPIs and quantitative models                    |
| Financier    | Financial Analyst             | Analyzes financial, macro and microeconomic impacts             |
| Writer       | French Writer and summarizer       | Synthesizes the expert outputs into the strategic report |
| Translator   | Arabic Translator      | Translates the report into Classical Arabic              |
| Auditor      | Quality & Final Audit         | Checks and consolidates the final bilingual output       |

This table explains thoroughly the role and responsibility of each agent. The separation of tasks enable better outputs, since instead of forcing one agent to do all the responsibilities, we spread it out to 7 different agents to give more focus and attention to each niche.

## How a mission works

A **mission** is just the process of all the agents working together. As said before, a mission is sequential, which means the agents work one by one. This diagram will explain the mechanics of a **mission**:

```mermaid

flowchart TD
    A["Atlas-Omnis"] --> B["Initialize seven specialized agents"]

    subgraph R["Research and Analysis"]
        direction TD
        C["OSINT Research Agent"]
        D["Serper Web Research"]
        E["Analyst Agents"]
        C -->|Uses| D
        C -->|OSINT findings| E
    end

    subgraph P["Report Production"]
        direction TD
        F["Writer Agent"]
        G["Translator Agent"]
        F -->|Strategic report| G
    end

    subgraph V["Validation and Delivery"]
        direction TD
        H["Auditor Agent"]
        I["Extract [FRANCAIS] and [ARABE] sections"]
        J["WeasyPrint"]
        K["French PDF"]
        L["Arabic PDF"]
        M["Interface preview and files"]

        H --> I --> J
        J --> K & L
        K & L --> M
    end

    B --> C
    E -->|Sequential CrewAI workflow| F
    F --> H
    G --> H

    classDef core stroke:#818cf8,fill:#eef2ff
    classDef research stroke:#2dd4bf,fill:#f0fdfa
    classDef production stroke:#fb923c,fill:#fff7ed
    classDef validation stroke:#a78bfa,fill:#f5f3ff
    classDef output stroke:#4ade80,fill:#f0fdf4

    class A,B core
    class C,D,E research
    class F,G production
    class H,I,J validation
    class K,L,M output

    style R fill:#f0fdfa,stroke:#2dd4bf
    style P fill:#fff7ed,stroke:#fb923c
    style V fill:#f5f3ff,stroke:#a78bfa
```


## Intelligence Pipeline

The Osint Researcher agent is a core member of the firm. He is the only agent with the serper search tool, and that is to separate the ability to search, from the ability of analysis. And that is for the goal to allow each agent to only focus on one area, the researcher extracts copious amounts of information and context from the web around a specific topic, which is then transferred to each of the three analysts.

## Report generation

The Final Output is first translated by the translator to Arabic, then the html changes the format the PDF to RTL (right to left) and vice versa if in French. The auditor also puts specific tags in the final text for each language to make detection easier.

## Tech Stack 

This is our Tech stack for this project which is quite compact:

| Technology         | Why?                                                    |
| ------------------ | ------------------------------------------------------- |
| **Python**         | Core language for the entire system and agent logic     |
| **CrewAI**         | Orchestrates the specialized AI agents and workflows    |
| **Gemini 3 Flash** | Powers the AI reasoning, analysis, and generation       |
| **Serper**         | Provides fast, reliable web search for research         |
| **Gradio**         | Provides a simple interactive interface                 |
| **WeasyPrint**     | Generates polished PDF reports from the agents' outputs |

## Project Structure

We intentionally used one file since the projects code is compact and efficient. We have also included a specific font since it is compatible with both languages. In the future, when more features will be added, the architecture will be changed accordingly.

## User base

Atlas Omnis has been used by an Administrator in the MEF who reported increased efficiency and  detailed outputs compared to other LLMs, the user implemented Atlas Omnis in his workflow regarding banking, external finance and regulations.

## Limitations

The project includes many limitations across many features:
- There have been some problems with the formatting of the Arabic pdfs, where random characters appear in the middle of the text. This is occasional.
- LLM generated content isn't always correct, and hallucinations may happen
- Critical Legal and Economic conclusions always need human verification
- Research quality depends on the sources
- The Sequential process is expensive and slow
- The simulation is not in any way a replacement of real analysts and writers

## Future Ambitions

Near Term:

- Better Source verification
- More rigorous fact checking
- Agent cross-examination
- Better report formatting

Long Term:

- More specialized agents
- Using a faster and more efficient process
- Mission history
- More sophisticated simulation


## Thank You!

Thank you for checking out and reading my project, you are welcome to contribute and send me any suggestions.

Written by: Mohamed Amir Moutem
Age: 15
email: amirmoutem19@gmail.com
GitHub: I think you already know :)
