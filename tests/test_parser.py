from parsers.site1_parser import parse_quotes

def test_parser():
    sample_html = """
    <div class="quote">
        <span class="text">Test Quote</span>
        <small class="author">Author</small>
    </div>
    """

    data = parse_quotes(sample_html)

    assert data[0]["author"] == "Author"