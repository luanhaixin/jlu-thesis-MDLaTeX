# 如何组织章节

章节组织通过 page\\\_config.json 配置文件控制，共包含以下字段：

- pagesInsertAtStart：插入在文档开头的 PDF 页面，如封面、声明页。
- summaryPage：摘要部分（可为中英文），支持多个 Markdown 文件。
- customPage：正文章节，用户自定义内容和顺序，支持多个 Markdown 文件。
- noHeadPage：不带章节号的结尾章节，如参考文献、致谢等。

## 示例配置

```json
{
  "pagesInsertAtStart": [
    { "path": "./word/cover.pdf", "name": "封面" },
    { "path": "./word/originStatement.pdf", "name": "原创性声明" },
    { "path": "./word/authorizationStatement.pdf", "name": "使用授权声明" }
  ],
  "summaryPage": [
    { "path": "./md/summaryCN.md", "name": "摘要" },
    { "path": "./md/summaryEN.md", "name": "Abstract" }
  ],
  "customPage": [
    { "path": "./md/Introduction.md" },
    { "path": "./md/charpter2.md" }
  ],
  "noHeadPage": [
    { "path": "./md/Reference.md", "name": "参考文献" },
    { "path": "./md/Acknowledgement.md", "name": "致谢" }
  ]
}
```


## page\\\_config.json 配置详解

这个配置文件定义了论文的整体结构与各个部分的内容来源。其核心作用是**描述哪些页面要被插入、按什么顺序插入、文件路径在哪里、是否要生成书签和目录条目等信息**。

### pagesInsertAtStart

**作用**：定义在正文（摘要与目录）开始之前插入的**PDF 页面**，通常用于封面、声明等已有格式的页面。

**每项对象字段**：

* path ：PDF 文件的路径，相对于项目根目录；
* name ：插入该 PDF 时在目录书签中显示的名称（如“封面”、“原创性声明”等）。

### summaryPage

**作用**：指定论文摘要部分的内容，支持多个摘要（例如中文摘要、英文摘要），会被渲染为 LaTeX 的 abstract 环境。

**每项对象字段**：

* path ：Markdown 格式的摘要文件路径；
* name ：显示在目录和书签中的名称，自动用于设置章节名字


### customPage

**作用**：指定论文正文部分的内容，通常是每章的 Markdown 文件，将转换为 LaTeX 正文章节。

**每项对象字段**：

* path ：Markdown 文件路径；
* **无需 "name" 字段**：章节标题由 Markdown 文件中的 #（如 # 第二章 xxx）自动决定。


### noHeadPage

**作用**：处理文档末尾的特殊章节，如“参考文献”和“致谢”，这些部分通常不带章节编号。

**每项对象字段**：

* path ：Markdown 文件路径；
* name ：章节显示名称，用于设置章节名字、PDF 书签、目录等。

## 项目目录

### asset
用于存放项目使用的 **图片** 资源。可以按需放入 .png、.jpg 文件，在 Markdown 和 LaTeX 中都可以引用。

### latex
此目录用于存放最终生成的 LaTeX 文件，包括目录结构控制文件、排版模板、自动生成的中间结果等。

* pages.tex ：根据 page\\\_config.json 自动生成，负责导入用户的章节文件。
* pagesInsertAtStart.tex ：根据 page\\\_config.json 自动生成，负责导入用户的插页配置（如封面、声明）。
* settings.tex ：全局排版设置（如字体、间距、页眉页脚等）。
* main.tex ：Latex 程序入口。


### latex/article
存放每一章具体内容对应的 .tex 文件，**由 Markdown 自动转换生成**。

### md
用于撰写论文主要内容的 **Markdown 原稿目录**。

该文件夹预留了 SummaryCN.md, SummaryEN.md, Introduction.md, Reference.md,Acknowledgement.md 。 这些文件都不可以被删除，其中 Reference.md 不可以改动其中的内容。

### word
用于存放无法用 Markdown 编辑的 **PDF 文件**，例如学校要求的：

* 封面 cover.pdf
* 原创性声明 originStatement.pdf 
* 授权声明 authorizationStatement.pdf 
