from scraping_lab.http import parse_products


HTML = """
<html>
  <body>
    <article class="product_pod">
      <h3><a href="catalogue/example_1/index.html" title="  Example   Book ">Example</a></h3>
      <p class="price_color">£12.34</p>
      <p class="availability"> In   stock </p>
    </article>
  </body>
</html>
"""


def test_parse_products_normalizes_public_demo_record() -> None:
    records = parse_products(HTML, "https://books.toscrape.com/")

    assert len(records) == 1
    assert records[0].title == "Example Book"
    assert str(records[0].price_gbp) == "12.34"
    assert records[0].availability == "In stock"
    assert str(records[0].source_url).endswith("/catalogue/example_1/index.html")
