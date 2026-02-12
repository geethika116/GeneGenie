import re

def extract_sequences(text):
    seen_sequences = set()
    pattern = r'(?<=\n|^)(\S+(?:\s+\S+){0,2})(?=\s+\S+(?:\s+\S+){0,2}|$)'
    matches = re.findall(pattern, text, re.MULTILINE)

    filtered_sequences = []
    for seq in matches:
        if seq not in seen_sequences:
            seen_sequences.add(seq)
            filtered_sequences.append(seq.strip())

    return filtered_sequences