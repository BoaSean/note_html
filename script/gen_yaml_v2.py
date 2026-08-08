#!/usr/bin/env python3
"""
v2 规则：
  - # 始终为纯目录
  - ## ~ ##### 有子标题做目录，无子标题做叶子 + file
  - ######+ 始终做叶子 + file
  - --dry 按缩进打印标题树

用法：
    python3 script/gen_yaml_v2.py docs/<folder>/<file>.md --dry
    python3 script/gen_yaml_v2.py docs/<folder>/<file>.md
    python3 script/gen_yaml_v2.py docs/<folder>/ --dry
    python3 script/gen_yaml_v2.py docs/<folder>/
"""

import os, sys, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(BASE, 'docs')
TITLE = os.path.join(BASE, 'title')

LEAF_CUTOFF = 6  # ###### 及以上始终为叶子


def parse_all(filepath):
    """返回 [(level, text, line_no), ...]"""
    headings = []
    with open(filepath, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            m = re.match(r'^(#{1,})\s+(.+)', line)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                headings.append((level, text, i))
    return headings


def build_tree(headings):
    """扁平标题 → 嵌套树 [{title, h_level, children?}]"""
    if not headings:
        return []

    root = []
    stack = []  # [(level, node), ...]

    for level, text, _ in headings:
        node = {'title': text, 'h_level': level}

        while stack and stack[-1][0] >= level:
            stack.pop()

        if not stack:
            root.append(node)
        else:
            parent = stack[-1][1]
            parent.setdefault('children', []).append(node)

        stack.append((level, node))

    return root


def dry_print(nodes, depth=0):
    """按缩进打印标题树"""
    for node in nodes:
        indent = '  ' * (node['h_level'] - 1)
        prefix = '#' * node['h_level']
        print(f'{indent}{prefix} {node["title"]}')
        if 'children' in node:
            dry_print(node['children'])


def attach_files(nodes, md_filename):
    """按规则加 file：
       - # 不加（始终纯目录）
       - ##~##### 有 children 不加，无 children 加
       - ######+ 有 children 也加 + 叶子也加
    """
    for node in nodes:
        h = node['h_level']
        has_kids = 'children' in node

        if has_kids:
            attach_files(node['children'], md_filename)

        if h < LEAF_CUTOFF and has_kids:
            # #~##### 且有子 → 目录，不加 file
            continue
        # ######+ 或 无子标题 → 叶子
        node['file'] = md_filename + '#' + node['title']


def emit_yaml(nodes, depth=0):
    """生成 YAML，depth 对应标题级数"""
    out = ''
    pad = '  ' * depth
    for node in nodes:
        out += pad + '- title: ' + _q(node['title']) + '\n'
        children = node.get('children')
        if children:
            if 'file' in node:
                out += pad + '  file: ' + _q(node['file']) + '\n'
            out += pad + '  items:\n'
            out += emit_yaml(children, depth + 1)
        elif 'file' in node:
            out += pad + '  file: ' + _q(node['file']) + '\n'
    return out


def _q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def generate(path, dry_run=False):
    target = os.path.join(BASE, path) if not os.path.isabs(path) else path.rstrip('/')

    if os.path.isfile(target):
        if dry_run:
            _process_file(target, dry_run)
        else:
            result = _process_file(target, dry_run)
            if result:
                tree, folder, md_filename = result
                yaml = 'name: ' + _q(folder) + '\ntree:\n' + emit_yaml(tree)
                md_name = os.path.splitext(md_filename)[0]
                out_name = 'file_' + md_name + '_default.yaml'
                out_path = os.path.join(TITLE, out_name)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(yaml)
                print(f'已生成 title/{out_name}')
    elif os.path.isdir(target):
        _process_folder(target, dry_run)
    else:
        print(f'错误：{path} 不是有效的文件或目录')
        sys.exit(1)


def _process_file(md_path, dry_run):
    rel = os.path.relpath(md_path, DOCS)
    folder = rel.split(os.sep)[0]
    md_filename = os.path.basename(md_path)

    headings = parse_all(md_path)
    if not headings:
        print(f'警告：{md_filename} 未找到标题')
        return None

    tree = build_tree(headings)
    attach_files(tree, md_filename)

    if dry_run:
        print(f'# {md_filename}')
        dry_print(tree)
        print()
        return None
    return tree, folder, md_filename


def _process_folder(folder_path, dry_run):
    folder = os.path.basename(folder_path.rstrip('/'))
    md_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.md')],
        key=lambda x: x.lower()
    )

    if not md_files:
        print(f'警告：{folder} 下没有 .md 文件')
        return

    all_sections = []

    for md_file in md_files:
        md_path = os.path.join(folder_path, md_file)
        headings = parse_all(md_path)
        if not headings:
            continue

        tree = build_tree(headings)
        attach_files(tree, md_file)

        if dry_run:
            print(f'# {md_file}')
            dry_print(tree)
            print()
        else:
            all_sections.extend(tree)

    if dry_run:
        return

    if not all_sections:
        print('警告：未找到有效标题')
        return

    yaml = 'name: ' + _q(folder) + '\ntree:\n' + emit_yaml(all_sections)
    out_path = os.path.join(TITLE, folder + '_default.yaml')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(yaml)
    print(f'已生成 title/{folder}_default.yaml ({len(md_files)} 个 .md 文件)')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='v2: 根据单个 md 文件生成 YAML')
    parser.add_argument('file', help='md 文件路径，如 docs/tool/linux_cmd.md')
    parser.add_argument('--dry', action='store_true', help='只打印标题树预览')
    args = parser.parse_args()
    generate(args.file, dry_run=args.dry)
