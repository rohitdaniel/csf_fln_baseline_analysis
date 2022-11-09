def extract_name(string):
    name = re.findall(r'\w+', string)
    return name
