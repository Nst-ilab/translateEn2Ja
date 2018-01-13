# coding: UTF-8
import boto3
import urllib.request
import xml.etree.ElementTree as ET

#Region指定しないと、デフォルトのUSリージョンが使われる
client_lambda = boto3.client('lambda', region_name='ap-northeast-1')

def lambda_handler(event, context):

    # このサービスが動作するか決定する。英単語１つしか入ってないときに動かす
    line_text = event["lineMessage"]["events"][0]["message"]["text"]
    first_content = event["analysedMessage"]["tokens"][0]["text"]["content"]
    language = event["analysedMessage"]["language"]
    if line_text == first_content and language == "en":
        search_word = line_text
    else:
        return None
    
    # 検索
    item_id = get_item_id(search_word)
    translated_text = get_translated_text(item_id)

    #取得した翻訳結果を返す
    if translated_text is None:
        return None
    else:
        return { "message" : translated_text }

# 翻訳サービスが返すxmlから結果を抽出する
def get_xml_element_text(url, tag):
    try:
        xml = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print('error code : ' + str(e.code))
        print('error read : ' + str(e.read()))
        return ''
    tree = ET.parse(xml)
    root = tree.getroot()
    element = root.find('.//{http://btonic.est.co.jp/NetDic/NetDicV09}' + tag)
    text = element.text
    return text

# 翻訳サービスからワードのIDを取得
def get_item_id(search_word):
    head = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite?Dic=EJdict&Word='
    end = '&Scope=HEADWORD&Match=EXACT&Merge=OR&Prof=XHTML&PageSize=20&PageIndex=0'
    url = head + search_word + end
    return get_xml_element_text(url, 'ItemID')

# 翻訳サービスにワードIDを投げて結果を取得
def get_translated_text(item_id):
    head = 'http://public.dejizo.jp/NetDicV09.asmx/GetDicItemLite?Dic=EJdict&Item='
    end = '&Loc=&Prof=XHTML'
    url = head + item_id + end
    return get_xml_element_text(url, 'Body/div/div')