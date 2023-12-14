def decode_str(string):
    return string.encode().decode("unicode-escape").encode("latin1").decode("utf-8")


def get_page_sentence(page, count: int = 10):
    # find all paragraphs
    paragraphs = page.split("\n")
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # find all sentence
    sentences = []
    for p in paragraphs:
        sentences += p.split(". ")
    sentences = [s.strip() + "." for s in sentences if s.strip()]
    # get first `count` number of sentences
    return " ".join(sentences[:count])
