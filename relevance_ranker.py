def score_text_block(text_block, persona_keywords, job_keywords):
    score = 0
    text = text_block["text"].lower()

    # Match job keywords more strongly
    for keyword in job_keywords:
        if keyword.lower() in text:
            score += 3
        elif any(k in text for k in keyword.lower().split()):
            score += 1  # partial match

    # Match persona keywords less strongly
    for keyword in persona_keywords:
        if keyword.lower() in text:
            score += 2
        elif any(k in text for k in keyword.lower().split()):
            score += 1

    # Small bonus if early in doc
    if text_block.get("page", 999) <= 3:
        score += 1

    # Bonus for large font size (likely heading or important)
    if text_block.get("avg_font_size", 0) >= 10:
        score += 1

    return score


def rank_text_blocks(blocks, persona_keywords, job_keywords):
    for block in blocks:
        block["score"] = score_text_block(block, persona_keywords, job_keywords)
    sorted_blocks = sorted(blocks, key=lambda b: b["score"], reverse=True)
    return sorted_blocks
