import os
import sys
import json
import re
from md2tex import md_to_latex

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
