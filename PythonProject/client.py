import xmlrpc.client

# 连接到RPC服务器
server = xmlrpc.client.ServerProxy("http://localhost:8000")

# 添加笔记
def add_note():
    topic = input("Enter topic: ")
    text = input("Enter text: ")
    timestamp = input("Enter timestamp: ")
    if server.add_note(topic, text, timestamp):
        print("Note added successfully!")
    else:
        print("Failed to add note.")

# 查询笔记
def get_notes():
    topic = input("Enter topic to search: ")
    notes = server.get_notes_by_topic(topic)
    if notes:
        print(f"Notes for topic '{topic}':")
        for note in notes:
            print(f"Text: {note['text']}, Timestamp: {note['timestamp']}")
    else:
        print(f"No notes found for topic '{topic}'.")

# 查询Wikipedia并追加到笔记
def query_wikipedia():
    topic = input("Enter topic to search on Wikipedia: ")
    result = server.query_wikipedia(topic)
    if result:
        print(f"Wikipedia result: {result['title']} - {result['link']}")
        text = f"Wikipedia info: {result['link']}"
        timestamp = "Wikipedia query"
        if server.add_note(topic, text, timestamp):
            print("Wikipedia result appended to notes!")
    else:
        print("No Wikipedia results found.")

# 主菜单
def main():
    while True:
        print("\n1. Add Note\n2. Get Notes by Topic\n3. Query Wikipedia\n4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_note()
        elif choice == "2":
            get_notes()
        elif choice == "3":
            query_wikipedia()
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()