#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刷新 00_目录与阅读进度.md 里所有派生数字。

用法：  python3 _scripts/refresh_progress.py

真相来源 = 文件里「阅读清单」的复选框。勾选后跑一次，以下内容全部自动重算：
  · 进度条、已读/剩余时长
  · 各星级档「（N 篇，已读 M）」
  · 「下一步读什么」推荐表（按未读 + 星级 + 时长）
  · 总表的 ✅ 状态列
  · 主题串读里的 ~~删除线~~
  · 每篇详情标题后的 ✅ 已读 / ⬜ 未读
脚本不改动任何正文、摘要或链接，只动这些派生视图。
"""
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, '..', 'Engineering全集_逐句对照', '00_目录与阅读进度.md')

# 未读篇目在推荐表里显示的理由（可自行增删）
RATIONALE = {
    "01": "RAG／记忆检索的底子，检索失败率降 49% 的经典方法。",
    "03": "Anthropic 极简脚手架哲学的源头，双工具就是 Claude Code 的雏形。",
    "04": "低成本提升长工具链可靠性；注意文首更新说明——官方现在更推荐扩展思考。",
    "07": "只有要分发 MCP 服务器时才需要；注意后缀已从 .dxt 改为 .mcpb。",
    "09": "推理基础设施故障的一线复盘，理解采样精度与路由如何影响输出质量。",
    "11": "Skills 的三层渐进式披露，以及它和 MCP 的互补关系。",
    "12": "文件系统 + 网络双重隔离，少一个都不算有效沙箱。",
    "14": "工具搜索、程序化调用、调用示例三件套，解决工具规模化瓶颈。",
    "17": "模型 vs 人类的能力边界案例，偏招聘评估设计，当故事读。",
    "18": "16 个智能体并行写出 10 万行编译器，多智能体工程实录。",
    "19": "跑 agentic 评估前的必要提醒：光资源配置就能造成 6 个百分点差距。",
    "20": "模型自己识破评估并解密答案，跑联网 benchmark 前值得一读。",
    "22": "生产级安全护栏的完整设计取舍，公开了真实误报／漏报数据。",
    "23": "性价比最高：10 分钟拿到平台级抽象设计思路。",
    "24": "产品层配置如何在不改模型的情况下拖垮质量，反面教材。",
    "25": "承接沙箱那篇，补齐安全侧完整架构与四起真实事故。",
}

STARS = {5: "★★★★★", 4: "★★★★☆", 3: "★★★☆☆", 2: "★★☆☆☆", 1: "★☆☆☆☆"}
CHAINS = ["Agent 架构基础", "上下文与工具", "评估体系", "安全与运维"]


def hm(m):
    return f"{m // 60} 小时 {m % 60} 分钟" if m >= 60 else f"{m} 分钟"


def main():
    path = os.path.normpath(DOC)
    if not os.path.exists(path):
        sys.exit(f'找不到 {path}')
    txt = open(path, encoding='utf-8').read()

    # ── 1. 从清单复选框读出真相 ──
    items = {}   # num -> {read, mins, cn}
    for m in re.finditer(r'^- \[([ x])\] \*\*(\d\d)\*\*\s*\[([^\]]+)\][^\n]*?`(\d+) 分钟`', txt, re.M):
        items[m.group(2)] = {'read': m.group(1) == 'x', 'cn': m.group(3), 'mins': int(m.group(4))}
    if not items:
        sys.exit('没在文件里找到阅读清单复选框，格式可能被改动过')

    # 星级：从清单所在的档位标题推断
    star_of = {}
    cur = None
    for line in txt.splitlines():
        hm_ = re.match(r'^### (★+☆*)\s', line)
        if hm_:
            cur = {v: k for k, v in STARS.items()}.get(hm_.group(1))
        m = re.match(r'^- \[[ x]\] \*\*(\d\d)\*\*', line)
        if m and cur:
            star_of[m.group(1)] = cur
    for k in items:
        items[k]['star'] = star_of.get(k, 3)

    n = len(items)
    read = {k for k, v in items.items() if v['read']}
    total_min = sum(v['mins'] for v in items.values())
    done_min = sum(v['mins'] for k, v in items.items() if v['read'])
    left_min = total_min - done_min

    # ── 2. 进度条与统计行 ──
    filled = round(len(read) / n * 24)
    txt = re.sub(r'`█*░*`　\*\*\d+ / \d+ 篇\*\*',
                 f"`{'█' * filled}{'░' * (24 - filled)}`　**{len(read)} / {n} 篇**", txt, count=1)
    txt = re.sub(r'- 已读约 [^\n]*（全集精读约 [^\n]*）',
                 f'- 已读约 {hm(done_min)}，剩余约 {hm(left_min)}（全集精读约 {hm(total_min)}）', txt, count=1)

    def tier(s):
        tot = [k for k, v in items.items() if v['star'] == s]
        return len([k for k in tot if k in read]), len(tot)

    d5, t5 = tier(5)
    d4, t4 = tier(4)
    lo = [k for k, v in items.items() if v['star'] <= 3]
    txt = re.sub(r'- ★★★★★ 必读档：[^\n]*',
                 f'- ★★★★★ 必读档：**{d5} / {t5}**　｜　★★★★☆ {d4} / {t4}　｜　'
                 f'★★★☆☆ 及以下 {len([k for k in lo if k in read])} / {len(lo)}', txt, count=1)

    # ── 3. 各档标题「（N 篇，已读 M）」 ──
    def fix_tier_head(m):
        s = {v: k for k, v in STARS.items()}[m.group(1)]
        d, t = tier(s)
        return f'### {m.group(1)}　{m.group(2)}（{t} 篇，已读 {d}）'
    txt = re.sub(r'^### (★+☆*)　([^（\n]+)（\d+ 篇，已读 \d+）', fix_tier_head, txt, flags=re.M)

    # ── 4. 「下一步读什么」推荐表 ──
    todo = sorted([(k, v) for k, v in items.items() if not v['read']],
                  key=lambda kv: (-kv[1]['star'], kv[1]['mins']))
    lines = ['### 下一步读什么', '']
    if not todo:
        lines += ['全集读完了 🎉', '']
    else:
        hi = [k for k, v in todo if v['star'] == 5]
        if hi:
            lines += [f'★★★★★ 必读档还剩 **{len(hi)}** 篇未读。', '']
        else:
            lines += [f'★★★★★ **必读档已全部读完（{t5}/{t5}）**，'
                      '下面按重要度和时长排出性价比最高的几篇。', '']
        lines += ['| 顺序 | 篇目 | 重要度 | 时长 | 为什么读 |', '|:--:|---|:--:|--:|---|']
        for i, (k, v) in enumerate(todo[:5], 1):
            lines.append(f"| {i} | **{k}** {v['cn']} | {STARS[v['star']]} | {v['mins']} 分钟 "
                         f"| {RATIONALE.get(k, '')} |")
        lines.append('')
    txt = re.sub(r'### 下一步读什么\n.*?(?=### 通用阅读路线)', '\n'.join(lines) + '\n', txt, count=1, flags=re.S)

    # ── 5. 总表 ✅ 列 ──
    def fix_row(m):
        return f"| {m.group(1)} | {'✅' if m.group(1) in read else '　'} |"
    txt = re.sub(r'\| (\d\d) \| (?:✅|　) \|', fix_row, txt)

    # ── 6. 主题串读删除线 ──
    def fix_chain(m):
        nums = re.findall(r'\d\d', m.group(2))
        cells = ' → '.join(f'~~{x}~~' if x in read else f'**{x}**' for x in nums)
        return f'| {m.group(1)} | {cells} |'
    txt = re.sub(r'\| (' + '|'.join(CHAINS) + r') \| ([^|]+) \|', fix_chain, txt)

    # ── 7. 详情标题的已读标记 ──
    def fix_detail(m):
        return f"### {m.group(1)}　{m.group(2)}　<sub>{'✅ 已读' if m.group(1) in read else '⬜ 未读'}</sub>"
    txt = re.sub(r'### (\d\d)　([^\n　]+)　<sub>(?:✅ 已读|⬜ 未读)</sub>', fix_detail, txt)

    open(path, 'w', encoding='utf-8').write(txt)
    print(f'已刷新：{len(read)}/{n} 篇　｜　必读档 {d5}/{t5}　｜　'
          f'已读 {hm(done_min)}，剩余 {hm(left_min)}')
    if todo:
        print('下一篇推荐：' + f"{todo[0][0]} {todo[0][1]['cn']}（{todo[0][1]['mins']} 分钟）")


if __name__ == '__main__':
    main()
