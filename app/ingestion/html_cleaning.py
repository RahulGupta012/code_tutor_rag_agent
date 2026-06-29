from bs4 import BeautifulSoup


def clean_html(html_text: str) -> str:

    soup = BeautifulSoup(html_text, "lxml")

    # Preserve code blocks
    for code in soup.find_all("code"):
        code.replace_with(
            f"\n[CODE]\n{code.get_text()}\n[/CODE]\n"
        )

    cleaned_text = soup.get_text(separator="\n")

    cleaned_text = "\n".join(
        line.strip()
        for line in cleaned_text.splitlines()
        if line.strip()
    )

    return cleaned_text