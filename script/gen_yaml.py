#!/usr/bin/env python3
"""
根据 docs/<folder> 下的所有 .md 文件，自动生成 title/<folder>_default.yaml

用法：
    python3 script/gen_yaml.py <folder>        → title/<folder>_default.yaml
    python3 script/gen_yaml.py <folder> --dry   → 只打印预览，不写文件

映射规则：
    - 文件中最高级别的标题 → YAML depth-0（一级分组）
      有子标题 → 带 items | 无子标题 → 带 file
    - 次级标题 → YAML depth-1+
      有子标题 → 带 file + items（可点击+可展开）
      无子标题 → 带 file（叶子）
"""

import os, sys, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(BASE, 'docs')
TITLE = os.path.join(BASE, 'title')


def parse_headings(md_path):
    """提取标题: [(level, text), ...]  level: 1=#, 2=##, 3=###, 4=####"""
    headings = []
    with open(md_path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^(#{1,4})\s+(.+)', line)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                headings.append((level, text))
    return headings


def build_tree(headings):
    """扁平标题列表 → 嵌套树 [{title, children?, file?}, ...]"""
    if not headings:
        return []

    min_level = min(h[0] for h in headings)

    root = []
    stack = []  # [(depth, node), ...]  depth 是归一化后的

    for level, text in headings:
        depth = level - min_level  # 0=root, 1=child, 2=grandchild
        node = {'title': text, 'h_level': level}  # h_level 保留原始 # 级数

        while stack and stack[-1][0] >= depth:
            stack.pop()

        if not stack:
            root.append(node)
        else:
            parent = stack[-1][1]
            parent.setdefault('children', []).append(node)

        stack.append((depth, node))

    return root


def emit_yaml(nodes, depth=0):
    """h_level >= 3 的叶子才带 file；h_level <= 2 始终为纯目录"""
    out = ''
    pad = '  ' * depth
    for node in nodes:
        out += pad + '- title: ' + _q(node['title']) + '\n'
        children = node.get('children')
        h = node.get('h_level', 0)
        if children:
            out += pad + '  items:\n'
            out += emit_yaml(children, depth + 1)
        elif h >= 3:
            # 三级及以上：叶子带 file
            out += pad + '  file: ' + _q(node.get('file', '')) + '\n'
        # h <= 2 且无 children：纯标题，不加 file（用户后续手动补内容）
    return out


def attach_files(nodes, md_filename):
    """只给 H3+ 叶子节点添加 file"""
    for node in nodes:
        if 'children' in node:
            attach_files(node['children'], md_filename)
        elif node.get('h_level', 0) >= 3:
            node['file'] = md_filename + '#' + node['title']


def _q(s):
    """YAML 安全的引号"""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def generate(folder, dry_run=False):
    folder_path = os.path.join(DOCS, folder)
    if not os.path.isdir(folder_path):
        print(f'错误：docs/{folder} 目录不存在')
        sys.exit(1)

    md_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.md')],
        key=lambda x: x.lower()
    )

    if not md_files:
        print(f'警告：docs/{folder} 下没有 .md 文件')
        return

    all_sections = []

    for md_file in md_files:
        headings = parse_headings(os.path.join(folder_path, md_file))
        if not headings:
            continue

        tree = build_tree(headings)
        attach_files(tree, md_file)
        all_sections.extend(tree)

    if not all_sections:
        print(f'警告：未找到有效标题')
        return

    yaml = 'name: ' + _q(folder) + '\ntree:\n' + emit_yaml(all_sections)
    out_path = os.path.join(TITLE, folder + '_default.yaml')

    if dry_run:
        print(f'--- 预览 title/{folder}_default.yaml ---')
        print(yaml)
    else:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(yaml)
        print(f'已生成 title/{folder}_default.yaml ({len(md_files)} 个 .md 文件)')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='根据 md 文件生成 YAML 导航')
    parser.add_argument('folder', help='docs 下的目录名')
    parser.add_argument('--dry', action='store_true', help='只预览不写文件')
    args = parser.parse_args()
    generate(args.folder, dry_run=args.dry)
