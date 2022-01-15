import json
from tqdm import tqdm
def main():
    file = 'output.json'
    teachers = []
    with open(file, 'r', encoding="UTF-8") as obj:
        data = json.load(obj)
    for classes in tqdm(data):
        if classes['professor'] not in teachers:
            teachers.append(classes['professor'])
        # for teacher in classes['professor']:
        #     for i in range(len(teachers)):
        #         if teacher['name'] == teachers[i]['name']:
        #             teachers[i]['classes'].append(classes['name'])
        #             break
        #     else:
        #         teachers.append({'name': teacher['name'], 'classes': [classes['name']]})
    with open('teachers.json', 'w', encoding="UTF-8") as obj:
        json.dump(teachers, obj, ensure_ascii=False)


if __name__ == '__main__':
    main()