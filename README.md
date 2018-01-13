# translateEn2Ja


    data={}
    data['Dic'] = 'EJDict'
    data['Word'] = searchWord
    data['Scope'] = 'HEADWORD'
    data['Match'] = 'EXACT'
    data['Merge'] = 'OR'
    data['Prof'] = 'XHTML'
    data['PageSize'] = '10'
    data['PageIndex'] = '0'
    url_values = parse.urlencode(data)
    url = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite'
    full_url = url + '?' + url_values
    data = request.urlopen(full_url)

    tree = ET.parse(data)
    root = tree.getroot()
    element = root.find()
