import re
import mistune
import json
import os
import sys

def md_to_latex(md_text):
    """Convert Markdown to LaTeX with support for titles, bold, italic, lists, images, and tables."""
    at_pattern = re.compile(r"(\@\@\@.*?\@\@\@)", re.DOTALL)
    ats = at_pattern.findall(md_text)

    for i, atat in enumerate(ats):
        placeholder = f"@@ATAT_{i}@@"
        md_text = md_text.replace(atat, placeholder)

    # Step 1: Protect math formulas
    math_pattern = re.compile(r"(\$\$.*?\$\$|\$.*?\$)", re.DOTALL)
    formulas = math_pattern.findall(md_text)

    # Replace formulas with placeholders
    for i, formula in enumerate(formulas):
        placeholder = f"@@FORMULA_{i}@@"

        md_text = md_text.replace(formula, placeholder)

    markdown = mistune.Markdown(escape=False)
    html_text = markdown(md_text)

    # Step 4: Restore math formulas from placeholders
    for i, formula in enumerate(formulas):
        placeholder = f"@@FORMULA_{i}@@"
        html_text = html_text.replace(placeholder, formula)

    for i, atat in enumerate(ats):
        placeholder = f"@@ATAT_{i}@@"
        # print(atat)
        html_text = html_text.replace(placeholder, atat[3:-3])

    html_text = re.sub(r"&gt;", ">", html_text)  # Replace &gt; with >
    html_text = re.sub(r"&lt;", "<", html_text)  # Replace &lt; with <
    html_text = re.sub(r"&amp;", "&", html_text)  # Replace &amp; with &
    html_text = re.sub(r"&quot;", '"', html_text)  # Replace &quot; with "
    html_text = re.sub(r"&apos;", "'", html_text)  # Replace &apos; with '
    html_text = re.sub(r"&nbsp;", " ", html_text)  # Replace &nbsp; with space

    # print(html_text)
    # Convert HTML to LaTeX
    html_to_latex = [
        (r"<h1>(.*?)</h1>", r"\\section{\1}"),
        (r"<h2>(.*?)</h2>", r"\\subsection{\1}"),
        (r"<h3>(.*?)</h3>", r"\\subsubsection{\1}"),
        (r"<h4>(.*?)</h4>", r"\\paragraph{\1}"),
        (r"<h5>(.*?)</h5>", r"\\subparagraph{\1}"),
        (r"<p>(.*?)</p>", r"\1\n"),
        (r"<p>(.*?)</p>", r"\1\n"),
        (r"<blockquote>(.*?)</blockquote>", r"\1\n"),
        (r"<strong>(.*?)</strong>", r"\\textbf{\1}"),
        (r"<em>(.*?)</em>", r"\\textit{\1}"),
        (r"<ul>(.*?)</ul>", r"\\begin{itemize}\1\\end{itemize}\n"),
        (r"<ol>(.*?)</ol>", r"\\begin{enumerate}\1\\end{enumerate}\n"),
        (r"<li>(.*?)</li>", r"\\item \1"),
        (r'<a href=".*?">(.*?)</a>', r"\1"),
        (
            r'<pre><code class=".*?">(.*?)</code></pre>',
            r"\\begin{verbatim}\1\\end{verbatim}",
        ),
        (r"<pre><code>(.*?)</code></pre>", r"\\begin{verbatim}\1\\end{verbatim}"),
    ]

    latex_text = html_text
    for pattern, repl in html_to_latex:
        latex_text = re.sub(pattern, repl, latex_text, flags=re.DOTALL)

    image_pattern = re.compile(r'<img src="(.*?)" alt="(.*?)" ?/?>')

    # 处理 alt 文本，提取 `@0.8@` 的数值，并去掉它
    def process_caption(match):
        src = match.group(1)  # 图片路径
        alt = match.group(2)  # 原始 alt 文字

        # 匹配末尾的 `@数字@`，提取数值并去掉 `alt` 中的这个部分
        size_match = re.search(r"@(.*?)@$", alt)
        if size_match:
            size = size_match.group(1)  # 提取 @0.8@ 里面的 0.8
            alt = re.sub(r"@(.*?)@$", "", alt)  # 去掉 `@0.8@`
        else:
            size = "1-htbp!"  # 默认大小

        n_s = size.split("-")

        if len(n_s) >= 2:
            n_size, n_pos = n_s[:2]  # 取前两个值，避免重复 split
        elif len(n_s) == 1:
            n_size, n_pos = n_s[0], "htbp!"  # 只有一个参数时，n_size 取值，n_pos 设默认
        else:
            n_size, n_pos = "1", "htbp!"  # 兜底默认值

        # 防止 n_size 或 n_pos 为空
        n_size = n_size or "1"
        n_pos = n_pos or "htbp!"

        # 替换为 LaTeX 代码
        return f"""\n\n\\begin{{figure}}[{{{n_pos}}}]
                        \\centering
                        \\includegraphics[width={n_size}\\textwidth]{{../{src}}}
                        \\caption{{\\textbf{{{alt}}}}}
                        \\end{{figure}}\n\n"""

    latex_text = image_pattern.sub(process_caption, latex_text)

    # 正则表达式匹配表格、行和单元格
    table_pattern = re.compile(r"<table>(.*?)</table>", re.DOTALL)
    row_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
    cell_pattern = re.compile(r"<t[dh]>(.*?)</t[dh]>")

    def convert_table(match):
        rows = row_pattern.findall(match.group(1))
        num_cols = (
            len(cell_pattern.findall(rows[0])) if rows else 2
        )  # 计算列数，默认 2 列
        col_format = "c " * num_cols  # 生成相应列数的格式（c 表示居中）
        # col_format = 'p{\\dimexpr \\linewidth / ' + str(num_cols) + '}' * num_cols  # 让列等宽填充整个页宽
        table_latex = (
            "\\begin{table}[ht]\n"
            "  \\renewcommand{\\arraystretch}{1.3}  % 调整行距，使表格更易读\n"
            "  \\captionsetup{justification=centering}\n"
            f"  \\caption{{\\textbf{{{cell_pattern.findall(rows[-1])[0]}}}}}\n"  # 加粗表格标题
            "  \\centering\n"
            "  \\setlength{\\tabcolsep}{10pt}  % 调整列间距，避免挤在一起\n"
            "  \\begin{tabular}{" + col_format + "}\n"
            "    \\toprule\n"
        )

        # 处理表头
        header_cells = cell_pattern.findall(rows[0])
        table_latex += (
            "    "
            + " & ".join(f"\\textbf{{{cell.strip()}}}" for cell in header_cells)
            + " \\\\\n"
        )
        table_latex += "    \\midrule\n"

        # 处理数据行
        for row in rows[1:-1]:
            cells = cell_pattern.findall(row)
            table_latex += (
                "    " + " & ".join(cell.strip() for cell in cells) + " \\\\\n"
            )

        table_latex += "    \\bottomrule\n"
        table_latex += "  \\end{tabular}\n"
        table_latex += "\\end{table}\n"

        return table_latex

    latex_text = table_pattern.sub(convert_table, latex_text)

    return latex_text

def load_config_file(config_file_path):
    # 加载用户页面配置
    try:
        with open(config_file_path, "r", encoding="utf-8") as f:
            pages = json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：解析 '{config_file_path}' 失败。请检查 JSON 格式是否有误：{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误：读取 '{config_file_path}' 时发生未知错误：{e}", file=sys.stderr)
        sys.exit(1)


    # ... 在加载json后 ...
    required_keys = ["pagesInsertAtStart", "summaryPage", "customPage", "noHeadPage"]
    for key in required_keys:
        if key not in pages or not isinstance(pages[key], list):
            print(f"错误：'{config_file_path}' 中缺少或 '{key}' 键的格式不正确（应为列表）。", file=sys.stderr)
            sys.exit(1)


    # 对列表中的每个字典项也进行校验，例如：
    for page_list_name in required_keys:
        for i, item in enumerate(pages[page_list_name]):
            if not isinstance(item, dict):
                print(f"错误：'{config_file_path}' 中 '{page_list_name}' 列表的第 {i+1} 项不是有效的字典。", file=sys.stderr)
                sys.exit(1)
            if "path" not in item:
                print(f"错误：'{config_file_path}' 中 '{page_list_name}' 列表的第 {i+1} 项缺少 'path' 键。", file=sys.stderr)
                sys.exit(1)
            # 进一步检查 path 是否存在
            full_path = item["path"] # 假设这里已经是正确相对路径
            if not os.path.exists(full_path):
                print(f"错误：配置文件中指定的路径 '{full_path}' 不存在。请检查文件是否存在。", file=sys.stderr)
                sys.exit(1)
            # 特别检查 "name" 字段是否必须，例如 pagesInsertAtStart 和 noHeadPage 需要
            if page_list_name in ["pagesInsertAtStart", "summaryPage", "noHeadPage"] and "name" not in item:
                print(f"错误：'{config_file_path}' 中 '{page_list_name}' 列表的第 {i+1} 项缺少 'name' 键。", file=sys.stderr)
                sys.exit(1)
    return pages




if __name__ == "__main__":

    latex_path = "./latex"
    latex_article_path = "./latex/article"
    md_path = "./md"
    config_file_path = "./page_config.json"

    # 检查主要目录是否存在
    for path_var in [latex_path, latex_article_path, md_path,config_file_path]:
        if not os.path.exists(path_var):
            print(f"错误：必要目录或文件 '{path_var}' 不存在。请创建或检查路径。", file=sys.stderr)
            sys.exit(1) 


    print(f"加载配置文件：{config_file_path}")

    pages=load_config_file(config_file_path)


    print("开始向 latex 注册文件 ...")

    # 向 latex 那边输送要在最开始插入的页面配置
    latex_pages_insert_at_start_content = ""
    for pa in pages["pagesInsertAtStart"]:
        print(f"  正在注册插入页面：{pa['path']}")
        filename = os.path.basename(pa["path"])
        name_only = os.path.splitext(filename)[0]
        rel_path = os.path.relpath(pa["path"], start=latex_path)
        latex_pages_insert_at_start_content += "\\pdfbookmark[1]{{{0}}}{{{1}}}\n\\includepdf[pages=-, linktodoc=true, bookmarks=true]{{{2}}}\n".format(
            pa["name"], name_only, rel_path.replace("\\", "/")
        )


    latex_pages_insert_at_start_path = os.path.join(
        latex_path, "pagesInsertAtStart.tex"
    )
    with open(latex_pages_insert_at_start_path, "w", encoding="utf-8") as f:
        f.write(latex_pages_insert_at_start_content)

    # 向 latex 那边输送要进行渲染的 普通页面 配置
    latex_pages_content = ""
    for pa in pages["customPage"]:
        print(f"  正在注册页面：{pa['path']}")
        filename = os.path.basename(pa["path"])
        name_only = os.path.splitext(filename)[0]
        latex_pages_content += "\\include{{article/{}}}\n".format(name_only)

    for pa in pages["noHeadPage"]:
        print(f"  正在注册页面：{pa['path']}")
        filename = os.path.basename(pa["path"])
        name_only = os.path.splitext(filename)[0]
        latex_pages_content += "\\include{{article/{}}}\n".format(name_only)


    latex_pages_path = os.path.join(latex_path, "pages.tex")
    with open(latex_pages_path, "w", encoding="utf-8") as f:
        f.write(latex_pages_content)

    # 从这里开始处理正文内容
    #
    print(f"开始将 .md 文件 转换成 .tex 文件 ...")
    # 处理摘要
    for pa in pages["summaryPage"]:
        print(f"  正在转换页面：{pa['path']}")
        filename = os.path.basename(pa["path"])
        name_only = os.path.splitext(filename)[0]

        with open(pa["path"], "r", encoding="utf-8") as f:
            md_text = f.read()

        latex_text = md_to_latex(md_text)
        latex_text = (
            "\\renewcommand{\\abstractname}{"
            + pa["name"]
            + "}\\begin{abstract}"
            + "\n".join(latex_text.splitlines()[1:])
            + "\\newpage\\end{abstract}"
        )

        with open(
            os.path.join(latex_article_path, name_only + ".tex"), "w", encoding="utf-8"
        ) as f:
            f.write(latex_text)

    # 处理正常的页面
    for pa in pages["customPage"]:
        print(f"  正在转换页面：{pa['path']}")
        filename = os.path.basename(pa["path"])
        name_only = os.path.splitext(filename)[0]

        with open(pa["path"], "r", encoding="utf-8") as f:
            md_text = f.read()

        latex_text = md_to_latex(md_text)

        with open(
            os.path.join(latex_article_path, name_only + ".tex"), "w", encoding="utf-8"
        ) as f:
            f.write(latex_text)

    # 处理尾部的页面
    for pa in pages["noHeadPage"]:
        print(f"  正在转换页面：{pa['path']}")
        filename = os.path.basename(pa["path"])
        name_only = os.path.splitext(filename)[0]

        with open(pa["path"], "r", encoding="utf-8") as f:
            md_text = f.read()

        latex_text = md_to_latex(md_text)

        ack = (
            "\\phantomsection\n"
            "\\addcontentsline{{toc}}{{section}}{{{0}}}\n"
            "\\markboth{{{0}}}{{{1}}}\n"
            "\\section*{{{0}}} \n"
        ).format(pa["name"], name_only)

        latex_text = ack + "\n".join(latex_text.splitlines()[1:])

        with open(
            os.path.join(latex_article_path, name_only + ".tex"), "w", encoding="utf-8"
        ) as f:
            f.write(latex_text)
        # ...
    print("所有文件转换完成。")
