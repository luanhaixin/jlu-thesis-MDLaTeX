# 吉林大学毕业论文快速生成大法

这个项目的目的就是为了**减轻 人类 写论文的压力**，能专注在论文的**内容**上，而不是被各种**格式**搞得焦头烂额！

通过这个项目，你只需要**一行命令**，就能生成格式完全正确的 PDF 论文。**格式问题？放心，已经帮你搞定了！** 最后只需要提交 PDF 文件，绝对没问题！

该项目基于的是吉林大学硕士论文模板奥！！！！！！！！

---

## 项目所需环境

想让这个工具跑起来，你需要准备以下环境：

- **Windows 电脑**
- **LaTeX 环境**
- **Markdown 文档编辑器**
- **Python 3**

### LaTeX 环境安装

**LaTeX 环境理论上不算好配**，但别担心，我已经帮你简化了流程：

1. 先去 LaTeX 官网瞅一眼：[https://www.latex-project.org/](https://www.latex-project.org/)
2. 懒得麻烦？直接去这个链接：[https://miktex.org/download](https://miktex.org/download) 下载 Windows 版本
3. 下载好之后，安装过程一路点击“确定”就行，完全不用多想

到这一步，简易 LaTeX 环境就装好了，可以直接开搞！

---

## 打开项目包，开始操作

项目解压出来，目录结构长这样：

```
thesis
├── asset
├── latex
│   └── article
├── md
├── py
├── word
├── page_config.json
├── reference.bib
└── run.ps1
```


### 主要目录

1. asset：用于存放项目使用的 **图片** 资源。可以按需放入 .png、.jpg 文件，在 Markdown 和 LaTeX 中都可以引用。

2. latex：此目录用于存放最终生成的 LaTeX 文件，包括目录结构控制文件、排版模板、自动生成的中间结果等。

	* pages.tex ：根据 page\\\_config.json 自动生成，负责导入用户的章节文件。
	* pagesInsertAtStart.tex ：根据 page\\\_config.json 自动生成，负责导入用户的插页配置（如封面、声明）。
	* settings.tex ：全局排版设置（如字体、间距、页眉页脚等）。
	* main.tex ：Latex 程序入口。

3. latex/article： 存放每一章具体内容对应的 .tex 文件，**由 Markdown 自动转换生成**。

4. md：用于撰写论文主要内容的 **Markdown 原稿目录**，我们主要在这里写论文内容。该文件夹预留了 SummaryCN.md, SummaryEN.md, Introduction.md, Reference.md,Acknowledgement.md 。 这些文件都不可以被删除，其中 Reference.md 不可以改动其中的内容。

5. word：用于存放无法用 Markdown 编辑的 **PDF 文件**，例如学校要求的：
	* 封面 cover.pdf
	* 原创性声明 originStatement.pdf
	* 授权声明 authorizationStatement.pdf


### 主要文件

1. page_config.json：这个 JSON 格式的配置文件是您论文自动化排版系统的“**蓝图**” 。它**定义了论文的整体结构和各个部分的内容来源** 。其核心作用在于**描述哪些页面将被插入到最终文档中，它们应按什么顺序排列，各自对应的文件路径在哪里，以及是否需要为这些页面生成 PDF 书签和目录条目等关键信息** 。通过编辑此文件，用户可以灵活地自定义论文的章节组织、插页顺序（如封面、声明页）、摘要以及无章节号的末尾部分（如参考文献、致谢） 。
2.  reference.bib ：`reference.bib` 是一个标准的 **BibTeX 格式的参考文献数据库文件**。它集中存储了您论文中所有引用的文献信息，包括书籍、期刊文章、会议论文等各种类型 。每条文献记录都包含唯一的引用键（如 `HAGBERG2008`），以及作者、标题、年份、出版物等详细元数据 。
3. run.ps1：`run.ps1` 是一个 **PowerShell 脚本文件**，专为 Windows 操作系统设计。它充当了整个论文自动化编译流程的**执行入口和调度器** 。

### 快速开始

**直接在项目根目录中运行：**

```powershell
./run.ps1
```

运行完后，`main.pdf` 会自动生成在当前文件夹里，**格式直接齐活**！

中间不管弹出来啥，同意就完了！

---
## 如何组织章节

  
章节组织通过 page_config.json 配置文件控制，共包含以下字段：

- pagesInsertAtStart：插入在文档开头的 PDF 页面，如封面、声明页。
- summaryPage：摘要部分（可为中英文），支持多个 Markdown 文件。
- customPage：正文章节，用户自定义内容和顺序，支持多个 Markdown 文件。
- noHeadPage：不带章节号的结尾章节，如参考文献、致谢、附录等。

示例配置

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

  
### page_config.json 配置详解

这个配置文件定义了论文的整体结构与各个部分的内容来源。其核心作用是描述哪些页面要被插入、按什么顺序插入、文件路径在哪里、是否要生成书签和目录条目等信息。

#### pagesInsertAtStart

**作用**：定义在正文（摘要与目录）开始之前插入的 PDF 页面，通常用于封面、声明等已有格式的页面。

**每项对象字段**：
* path ：PDF 文件的路径，相对于项目根目录；
* name ：插入该 PDF 时在目录书签中显示的名称（如“封面”、“原创性声明”等）。

#### summaryPage

**作用**：指定论文摘要部分的内容，支持多个摘要（例如中文摘要、英文摘要），会被渲染为 LaTeX 的 abstract 环境。

**每项对象字段**：

* path ：Markdown 格式的摘要文件路径；
* name ：显示在目录和书签中的名称，自动用于设置章节名字


#### customPage

**作用**：指定论文正文部分的内容，通常是每章的 Markdown 文件，将转换为 LaTeX 正文章节。

**每项对象字段**：

* path ：Markdown 文件路径；
* **无需 "name" 字段**：章节标题由 Markdown 文件中的 #（如 # 第二章 xxx）自动决定。

  
#### noHeadPage

**作用**：处理文档末尾的特殊章节，如“参考文献”和“致谢”，这些部分通常不带章节编号。

**每项对象字段**：

* path ：Markdown 文件路径；
* name ：章节显示名称，用于设置章节名字、PDF 书签、目录等。


---
## Markdown 语法介绍（超级阉割版）

找一个markdown编辑器，我建议 obisidan 奥，很简单

### 标题

在行首输入 `#` 加空格，当前行就会被识别为标题：

- `#` 一级标题 (**章节标题**)
- `##` 二级标题 (**小节标题**)
- `###` 三级标题 (**子小节标题**)

### 加粗

- `**`符号包裹 加粗 (**加粗**)

### 斜体

- `_`符号包裹 斜体 (_斜体_)

### 开启新段落

段落中间多按一个回车奥

第一段

第二段

### 符号避嫌

有一些符号是 markdown 或者 latex 的语法。以下符号出现在正文中，要注意。公式，latex源码有自己的解析方法，不用管。

```markdown
% 请写成 \% 
_ 请写成 \\\_ 
\ 请写成 \textbackslash
~ 请写成 \\~
# 请写成 \# 
$ 请写成 \$ 
& 请写成 \&
```

这里细究不得啊，因为这个文件被转了将近 3 次码，中间转义好几次，假如说某个符号不对劲，咱就加\试试，基本上都能试出来。出问题，转义就完了！

### 插入图片

插入图片也很简单，用这个格式：

```markdown
![\label{pic}我是图片的标题@0.5@](../asset/placeholder.png)
```

- 图片路径必须写成 `../asset/图片名字`
- `\label{pic}` 和 `\ref{pic}` 是一对命令，`\label` 给图片打标签，`\ref` 在文中引用
- `我是图片的标题` 会自动生成图片标题和编号，引用时还能自动调用，**再也不用手动改图号啦！**
- `@0.5@` 是使用一对@包裹的一个数字，大小是百分比，例如 0.5 为 50\%, 1.1为 110\%
 
### 插入表格

表格结构分为三部分：**表头**、**对齐方式** 和 **内容**。

**表头**：用 `|` 分隔每一列

**对齐方式**：
  - `---`：左对齐
  - `:---`：左对齐
  - `---:`：右对齐
  - `:---:`：居中对齐
**内容部分**：跟表头一样，按行输入

**示例：**

```markdown
|左对齐标题|右对齐标题|居中对齐标题|
|:---|---:|:---:|
|居左|居右|居中|
|测试文本|测试文本|测试文本|
|\label{pic}表格的标题|||
```

- **自动生成表格标题**：在最后一行加 `\label{}`，方便在正文中引用
- **默认表格样式**：输出的论文表格默认使用三线表，内容默认左对齐。如果有更高需求，后续可以提供定制服务 😎

### 插入数学公式

我们支持 **LaTeX 数学公式编辑**，用起来相当顺手：

- **行内公式**：用 `$ ... $` 包裹  
    例子：`$\sum_{i=1}^n a_i=0$`
    
- **独立公式**：用 `$$ ... $$` 包裹  
    例子：`$$\sum_{i=1}^n a_i=0$$`
    

**更多公式写法参考**：[MathJax 教程](https://1024th.github.io/MathJax_Tutorial_CN)

**在线公式编辑器推荐**：[LaTeX Live](https://www.latexlive.com/)

注意一下，$$,$,@@@包裹的内容，会被提前处理，不用考虑转义问题。

### 插入 Latex 源码
我们支持使用一对 @@@ 进行包裹以实现插入 Latex 源码的功能。例如

```latex
@@@
\begin{enumerate}
\item 基本符号
\begin{itemize}
\item $x$：观测序列。
\item $x_i$：第 $i$ 个观测符号。
\item $N$：观测序列长度。
\item $P(x)$：整个观测序列的概率。
\item $K$ ：模型长度。
\end{itemize}
\item 状态表示符号
\begin{itemize}
\item $S$：起始状态。
\item $E$：终止状态。
\item $M_k$：第 $k$ 个状态位的匹配状态 (Match State)。
\item $I_k$：第 $k$ 个状态位的插入状态(Insert State)。
\item $D_k$：第 $k$ 个状态位的删除状态 (Delete State)。
\end{itemize}
\end{enumerate}
@@@
```

注意一下，$$,$,@@@包裹的内容，会被提前处理，不用考虑转义问题。

### 插入文献

**引用文献？简单！** 直接用 `\cite{}` 命令即可。

**示例：**

```markdown
本章节将介绍 DAG-TPHMM \cite{lai_accurate_2024} 的算法细节，本文将对算法进行优化。
```

**那 `\cite{}` 里该写啥？**

别忘了 `reference.bib` 文件，里面存着你的参考文献。每条文献都有一个唯一标识符（citation key），比如这样：

```bibtex
@online{gpts2023,
  title = {Introducing GPTs},
  author = {OpenAI},
  date = {2023-11-06},
  url = {https://openai.com/index/introducing-gpts/},
  urldate = {\today}
}
```

这里的 `gpts2023` 就是文献的标识符。想引用这篇文献？ 直接在 `\cite{}` 里写上 `gpts2023`：

```markdown
\cite{gpts2023}
```

**想引用多篇文献？**

用英文逗号隔开多个标识符，程序会自动帮你格式化引用：

```markdown
\cite{gpts2023,lewis2020retrieval}
```

**生成的 PDF 会自动调整文献格式和排序，完全不用你手动操心！**

## `reference.bib` 文件怎么来的

### 直接在根目录中添加 `reference.bib` 条目

为了简化文献管理流程，建议直接将 BibTeX 格式的条目统一添加至项目根目录下的 `reference.bib` 文件中。这样可以在不借助外部文献管理工具的前提下，快速维护引用文献。

#### 推荐方法：通过 DOI 获取 BibTeX

大多数正式发表的论文都会提供 DOI（数字对象唯一标识符），我们可以通过 DOI 快速获取对应的 BibTeX 条目，操作流程如下：

1. 打开网址：[doi-to-bibtex-converter](https://www.bibtex.com/c/doi-to-bibtex-converter/)
2. 将论文的 DOI 粘贴进输入框，点击转换按钮
3. 复制生成的 BibTeX 条目
4. 将条目粘贴至项目中的 `reference.bib` 文件末尾即可


### 使用 Zotero 生成 `.bib` 文件

Zotero 是一款强大的文献管理工具，能帮你轻松收集、整理和引用参考文献。接下来，我们一步步教你如何使用 Zotero 生成 `.bib` 文件，然后在论文中愉快地引用文献。

####  安装 Zotero

- 访问 Zotero 官网：[https://www.zotero.org/download/](https://www.zotero.org/download/)
- 下载并安装适合你系统的版本（Windows、macOS 或 Linux）
- 建议安装浏览器插件（Zotero Connector），方便直接从网页上一键保存文献。

#### 添加文献到 Zotero

1. 使用浏览器插件添加： 
    打开你要引用的文献网页，点击浏览器右上角的 Zotero 图标（看起来像个文件夹或文献图标）。Zotero 会自动识别并保存文献信息到你的文献库。
    
2. 手动添加文献：
    打开 Zotero，点击左上角的绿色 “+” 按钮，选择 “添加条目”，然后填写文献信息（标题、作者、出版日期等）。
    
3. 导入已有文献：
    如果你已经有文献的 PDF 文件，直接拖进 Zotero，Zotero 会自动识别并提取元数据。
    
#### 生成 `.bib` 文件

1. 选择要导出的文献： 
    在 Zotero 中，选中你需要引用的文献（可以按住 `Ctrl` 键多选）。
    
2. 导出为 `.bib` 文件：
    - 右键点击选中的文献，选择 “导出文献”（Export Items）。
    - 在弹出的对话框中，选择 BibTeX 格式。
    - 勾选 “仅导出选定的条目”，然后点击确定。
    - 选择保存位置，保存文件名为 `reference.bib`，点击保存。
3. 批量导出整个文献库：  
    如果你想导出整个文献库，直接右键点击左侧的“我的文库”，选择“导出文献库”，同样选择 BibTeX 格式保存即可。

4. 将生成的 `reference.bib` 文件放入项目根目录下。


## 关于双面打印的问题

该框架默认是单面打印的模式。如果要双面打印，需要去自己去折腾一下 `latex/setting.tex` 和 `latex/main.tex` 去弄一下奇偶页的问题，毕竟有各种要求吗，例如正文开始页码必须是奇数页的问题。 

## 最后说明

本项目的 LaTeX 源码派生自 [JLU-SE-Thesis-Template](https://github.com/OceanPresentChao/JLU-SE-Thesis-Template)，我做了一些魔改，目的就是让大家少折腾格式，多专注在内容上。一行命令出 PDF，论文写作从未如此轻松！🎉
