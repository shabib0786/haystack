
def validateNumber(testString):
    import re
    pattern = re.compile('(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}')
    result = pattern.search(testString)
    return result