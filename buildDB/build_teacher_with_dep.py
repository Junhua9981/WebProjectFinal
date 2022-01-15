import json
from tqdm import tqdm
def main():
    file = 'output.json'
    teachers = []
    with open(file, 'r', encoding="UTF-8") as obj:
        classdata = json.load(obj)
    with open('teachers.json', 'r', encoding="UTF-8") as f:
        teacherdata = json.load(f)
    for t in teacherdata:
        teachers.append({'name': t, 'classes': [], 'department': []})
    for classes in tqdm(classdata):
        for(i, t) in enumerate(teachers):
            if classes['professor'] == t['name']:
                if(classes['name'] not in teachers[i]['classes']):
                    teachers[i]['classes'].append(classes['name'])
                if(classes['department'] not in teachers[i]['department']):
                    teachers[i]['department'].append(classes['department'])
                break
    with open('result.json', 'w', encoding="UTF-8") as s:
        json.dump(teachers, s, ensure_ascii=False)


if __name__ == '__main__':
    main()