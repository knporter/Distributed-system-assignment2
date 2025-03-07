from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import requests
from xml.dom import minidom


# 加载或创建XML数据库
XML_FILE = "notes.xml"

def load_or_create_xml():
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    except FileNotFoundError:
        root = ET.Element("notes")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)
    return tree, root

# 添加笔记到XML数据库
def add_note(topic, text, timestamp):
    tree, root = load_or_create_xml()
    note = ET.SubElement(root, "note")
    ET.SubElement(note, "topic").text = topic
    ET.SubElement(note, "text").text = text
    ET.SubElement(note, "timestamp").text = timestamp

    # 将 XML 转换为字符串
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")

    # 使用 minidom 美化输出
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="\t")

    # 写入文件
    with open(XML_FILE, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    return True

# 根据主题查询笔记
def get_notes_by_topic(topic):
    tree, root = load_or_create_xml()
    notes = []
    for note in root.findall("note"):
        if note.find("topic").text == topic:
            notes.append({
                "text": note.find("text").text,
                "timestamp": note.find("timestamp").text
            })
    return notes

# 查询Wikipedia API并返回结果
def query_wikipedia(topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": topic,
        "limit": 1,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if len(data) > 1 and len(data[1]) > 0:
        return {
            "title": data[1][0],
            "link": data[3][0]
        }
    return None


server = SimpleXMLRPCServer(("localhost", 8000))
print("Server listening on port 8000...")


server.register_function(add_note, "add_note")
server.register_function(get_notes_by_topic, "get_notes_by_topic")
server.register_function(query_wikipedia, "query_wikipedia")

server.serve_forever()