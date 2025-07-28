import os
import json
from datetime import datetime
from extract_text import extract_text_from_pdfs
from relevance_ranker import rank_text_blocks

if __name__ == "__main__":
    # Persona and job-to-be-done keywords
    persona_keywords = [
        "python", "html", "css", "javascript", "unity", "mysql", "git",
        "large language model", "rag", "software testing"
    ]

    job_keywords = [
        "project", "structure", "main.py", "utils.py", "dockerfile", "requirements.txt",
        "tools", "skills", "experience", "workflow"
    ]

    # Step 1: Extract text blocks
    text_blocks = extract_text_from_pdfs("pdfs")
    print(f"\n✅ Extracted {len(text_blocks)} blocks from PDFs")

    # Step 2: Rank them by relevance
    ranked = rank_text_blocks(text_blocks, persona_keywords, job_keywords)

    # Step 3: Print top 10 ranked blocks
    for i, item in enumerate(ranked[:10], start=1):
        print(f"\n{i}. [Score: {item['score']}] (Page {item['page']}) — {item['document']}")
        print(item['text'][:300] + "...")

    # Step 4: Build output JSON
    output = {
        "metadata": {
            "input_documents": list(set([b["document"] for b in ranked])),
            "persona": "Software Engineering Student focusing on resume and portfolio building",
            "job_to_be_done": "Understand how to structure project sections and highlight relevant skills",
            "timestamp": datetime.now().isoformat()
        },
        "sections": []
    }

    for item in ranked[:10]:
        output["sections"].append({
            "document": item["document"],
            "page": item["page"],
            "section_title": item["text"][:40] + "...",
            "importance_rank": item["score"],
            "refined_text": item["text"]
        })

    # Step 5: Write output to JSON file
    output_path = os.path.join(os.getcwd(), "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Output written to: {output_path}")
