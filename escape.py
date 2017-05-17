def escape_html(s):
    """Escaping html"""
    html_entities = {
        '"': "&quot;",
        ">": "&gt;",
        "&": "&amp;",
        "'": "&apos;",
        "<": "&lt;", }

    return "".join(html_entities.get(c, c) for c in s)

