import json
import os
from opencc import OpenCC

DATA_DIR = '.'
SRC_FILE = os.path.join(DATA_DIR, 'tang300.json')
WUYAN_FILE = os.path.join(DATA_DIR, 'wuyan.json')
QIYAN_FILE = os.path.join(DATA_DIR, 'qiyan.json')

cc = OpenCC('t2s')  # 繁体转简体

def clean_line(line):
    # 转简体，去掉逗号和句号
    line = cc.convert(line.strip())
    line = line.replace('，', '').replace('。', '').replace('.', '')
    return line

def main():
    with open(SRC_FILE, encoding='utf-8') as f:
        poems = json.load(f)
    wuyan, qiyan = [], []
    for idx, p in enumerate(poems):
        author = p.get('author', '未知')
        title = p.get('title', '无题')
        if 'paragraphs' in p:
            para = p['paragraphs']
        elif 'content' in p:
            para = p['content']
        else:
            print(f"[{idx}] 跳过无正文诗: {title} - {author}")
            continue
        for line_idx, line in enumerate(para):
            clean = clean_line(line)
            length = len(clean)
            log_msg = f"[{idx}-{line_idx}] {title} - {author} | 长度: {length} | 内容: {clean}"
            if length == 10:
                wuyan.append(clean)
                print(log_msg + " -> 五言")
            elif length == 14:
                qiyan.append(clean)
                print(log_msg + " -> 七言")
            else:
                print(log_msg + " -> 跳过")
    with open(WUYAN_FILE, 'w', encoding='utf-8') as f:
        json.dump(wuyan, f, ensure_ascii=False, indent=2)
    with open(QIYAN_FILE, 'w', encoding='utf-8') as f:
        json.dump(qiyan, f, ensure_ascii=False, indent=2)
    print(f'五言数量: {len(wuyan)}，七言数量: {len(qiyan)}')
    print('已保存为 wuyan.json 和 qiyan.json')

if __name__ == '__main__':
    main() 