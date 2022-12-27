def remove_from_string(text, unwanted):
    new_text = text[:]
    for u in unwanted:
        new_text = new_text.replace(u, "")
    return new_text
