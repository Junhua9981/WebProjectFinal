import json
def main():
    file = 'output.json'
    teachers = []
    with open(file, 'r', encoding="UTF-8") as obj:
        data = json.load(obj)
    print(len(data))


if __name__ == '__main__':
    main()