import bs4


def clean(html_string):
    soup = bs4.BeautifulSoup(html_string, 'html.parser')
    anchors = soup.find_all('a')
    for anchor in anchors:
        del anchor['id']
    return str(soup)
