def extract_sequences(text):
    import re

    # Merge hyphenated sequences
    text = re.sub(r'(?<=\w)-(?!\w)', '', text)

    # Set to keep track of seen sequences
    seen_sequences = set()
    # Regex pattern to match sequences with limited context
    pattern = r'(?<!\w)(\w{0,2})?(\w+)(\w{0,2})(?!\w)'
    matches = re.finditer(pattern, text)
    results = []

    for match in matches:
        sequence = match.group(2)
        # Avoid adding repeated sequences
        if sequence not in seen_sequences:
            # Deduplicate and add context
            context_before = match.group(1) if match.group(1) else ''
            context_after = match.group(3) if match.group(3) else ''
            results.append(f'{context_before}{sequence}{context_after}')
            seen_sequences.add(sequence)

    return results