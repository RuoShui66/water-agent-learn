#!/usr/bin/env python3
"""Extract claude.com/blog article body (u-rich-text-blog) to markdown + image manifest.

Usage: python3 extract_blog.py raw_<slug>.html
Writes: extracted_<slug>.md  (title/date/meta header + body markdown, images as remote URLs)
Prints: image URL list
"""
import re, sys, html
from html.parser import HTMLParser

class Node:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []  # Node or str

class TreeParser(HTMLParser):
    VOID = {'img','br','hr','meta','link','input','source','embed','wbr','col','area','base','track','param'}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root', [])
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].children.append(n)
        if tag not in self.VOID:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def find_all(node, pred, out=None):
    if out is None: out = []
    if isinstance(node, Node):
        if pred(node): out.append(node)
        for c in node.children:
            find_all(c, pred, out)
    return out

def text_of(node):
    if isinstance(node, str): return node
    return ''.join(text_of(c) for c in node.children)

images = []

def inline_md(node):
    if isinstance(node, str):
        return node
    t = node.tag
    inner = ''.join(inline_md(c) for c in node.children)
    if t == 'strong' or t == 'b':
        s = inner.strip()
        return f'**{s}**' if s else inner
    if t == 'em' or t == 'i':
        s = inner.strip()
        return f'*{s}*' if s else inner
    if t == 'code':
        return f'`{inner}`'
    if t == 'a':
        href = node.attrs.get('href','')
        if href.startswith('/'): href = 'https://claude.com' + href
        return f'[{inner}]({href})' if inner.strip() else ''
    if t == 'br':
        return '\n'
    if t == 'img':
        src = node.attrs.get('src','')
        alt = node.attrs.get('alt','').replace('\n',' ')
        if src and not src.startswith('data:'):
            images.append(src)
            return f'\n\n![{alt}]({src})\n\n'
        return ''
    if t == 'sup':
        return f'^{inner}'
    return inner

def block_md(node, depth=0):
    out = []
    if isinstance(node, str):
        s = node.strip()
        if s: out.append(s)
        return out
    t = node.tag
    if t in ('h1','h2','h3','h4','h5','h6'):
        level = int(t[1])
        out.append('#'*level + ' ' + inline_md(node).strip())
    elif t == 'p':
        s = inline_md(node).strip()
        if s: out.append(s)
    elif t in ('ul','ol'):
        idx = 1
        for li in [c for c in node.children if isinstance(c, Node) and c.tag=='li']:
            # separate nested lists from inline content
            nested = [c for c in li.children if isinstance(c, Node) and c.tag in ('ul','ol')]
            own = Node('li', [])
            own.children = [c for c in li.children if not (isinstance(c, Node) and c.tag in ('ul','ol'))]
            marker = '-' if t=='ul' else f'{idx}.'
            s = inline_md(own).strip()
            out.append('  '*depth + f'{marker} {s}')
            for nl in nested:
                out.extend(block_md(nl, depth+1))
            idx += 1
    elif t == 'blockquote':
        inner = []
        for c in node.children:
            inner.extend(block_md(c))
        out.append('\n'.join('> ' + l for chunk in inner for l in chunk.split('\n')))
    elif t == 'pre':
        code = text_of(node)
        out.append('```\n' + code.strip('\n') + '\n```')
    elif t == 'img':
        s = inline_md(node).strip()
        if s: out.append(s)
    elif t == 'figure':
        for c in node.children:
            out.extend(block_md(c, depth))
    elif t == 'figcaption':
        s = inline_md(node).strip()
        if s: out.append(f'*图注：{s}*')
    elif t == 'table':
        rows = find_all(node, lambda n: n.tag=='tr')
        md_rows = []
        for r_i, r in enumerate(rows):
            cells = [c for c in r.children if isinstance(c, Node) and c.tag in ('td','th')]
            md_rows.append('| ' + ' | '.join(inline_md(c).strip().replace('\n',' ') for c in cells) + ' |')
            if r_i == 0:
                md_rows.append('|' + '---|'*len(cells))
        out.append('\n'.join(md_rows))
    else:
        for c in node.children:
            out.extend(block_md(c, depth))
    return out

def main(path):
    global images
    raw = open(path).read()
    p = TreeParser()
    p.feed(raw)
    # meta
    def meta(pat):
        m = re.search(pat, raw)
        return html.unescape(m.group(1)) if m else ''
    title = meta(r'<meta property="og:title" content="([^"]*)"') or meta(r'<title>([^<]*)</title>').replace(' | Claude', '').strip()
    desc = meta(r'<meta property="og:description" content="([^"]*)"')
    ogimg = meta(r'<meta property="og:image" content="([^"]*)"')
    # published date: look for datetime attr or "Published" text
    date = ''
    m = re.search(r'datetime="([^"]+)"', raw)
    if m: date = m.group(1)
    else:
        m = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', raw)
        if m: date = m.group(1)
    blocks = find_all(p.root, lambda n: 'u-rich-text-blog' in n.attrs.get('class','') and 'w-dyn-bind-empty' not in n.attrs.get('class',''))
    body_parts = []
    seen = set()
    for b in blocks:
        for chunk in block_md(b):
            body_parts.append(chunk)
    slug = re.sub(r'^raw_|\.html$', '', path.split('/')[-1].replace('.html',''))
    slug = path.split('/')[-1][4:-5]
    outp = f'extracted_{slug}.md'
    with open(outp, 'w') as f:
        f.write(f'# {title}\n\n')
        f.write(f'> URL: https://claude.com/blog/{slug}\n> Date: {date}\n> og:description: {desc}\n> og:image: {ogimg}\n\n---\n\n')
        f.write('\n\n'.join(body_parts) + '\n')
    print(f'{slug}: {len(body_parts)} blocks, {len(images)} inline images -> {outp}')
    for u in dict.fromkeys(images):
        print('  IMG', u)
    images = []

if __name__ == '__main__':
    for path in sys.argv[1:]:
        main(path)
