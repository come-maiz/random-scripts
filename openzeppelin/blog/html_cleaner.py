import bs4


def clean(html_string):
    soup = bs4.BeautifulSoup(html_string, 'html.parser')
    soup = _clean_anchors(soup)
    soup = _clean_classes(soup)
    return str(soup)

def _clean_anchors(soup):
    anchors = soup.find_all('a')
    for anchor in anchors:
        _remove_blank_target_from_anchors(anchor)
        _remove_attributes_from_anchor(anchor)
    return soup

def _remove_blank_target_from_anchors(anchor):
    if anchor.has_attr('target'):
        if anchor['target'] == '_blank':
            del anchor['target']

def _remove_attributes_from_anchor(anchor):
    attributes = ['rel', 'data-href']
    for attribute in attributes:
        if anchor.has_attr(attribute):
            del anchor[attribute]

def _clean_classes(soup):
    classes = ['graf', 'graf--p', 'graf--h3', 'graf-after--p', 'graf--h4']
    for class_ in classes:
        elements = soup.select('.' + class_)
        for element in elements:
            element['class'].remove(class_)
            if element['class'] == []:
                del element['class']
    return soup
