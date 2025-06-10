# 具体语法示例演示

在这里，请看渲染出本文的.md文件的写法，具体语法教程请看配套 pdf

## 图片插入

![\label{pic}zzzz](../asset/placeholder.png)

## 三线表格插入

|水果|价格|
|---|---|
|苹果|8|
|西瓜|2|
|\label{table}水果价格意识图||


## 公式插入

行内公式 $a\times b=c$

行间公式

$$
\begin{equation}
\begin{array}{l}
E_{M_k}(a) = \dfrac{1}{P(x)} \displaystyle\sum_{i \mid x_i = a} f_{M_k}(i) \, b_{M_k}(i)\\[10pt]

E_{I_k}(a) = \dfrac{1}{P(x)} \displaystyle\sum_{i \mid x_i = a} f_{I_k}(i) \, b_{I_k}(i)
\end{array}
\label{eq:phmm-em1-eq}
\end{equation}
$$


## 引用一下

我要引用图 \ref{pic} 

我要引用表 \ref{table}

我要引用公式 \ref{eq:phmm-em1-eq}

我要引用文献 \cite{NetworkX}

我要引用多个文献 \cite{NetworkX,LEDA}

###  使用 latex 源码

这里使用 latex 源码 渲染一张复杂表格
@@@
\begin{table}[H]
    \centering
    \caption{\label{tab:complex_results}不同实验条件下模型性能对比}
    \vspace{1ex} % 标题和表格之间增加一点垂直空间
    \resizebox{\textwidth}{!}{ % 尝试将表格缩放到文本宽度，如果表格过宽
    \begin{tabular}{l ccc ccc c} % 定义列格式：l-左对齐，c-居中对齐，根据需要调整数量
        \toprule
        \multirow{2}{*}{\textbf{模型配置}} & \multicolumn{3}{c}{\textbf{数据集 A}} & \multicolumn{3}{c}{\textbf{数据集 B}} & \multirow{2}{*}{\textbf{平均得分}} \\
        \cmidrule(lr){2-4} \cmidrule(lr){5-7} % 局部横线，(lr)表示左右稍作修剪
        & 准确率 (\%) & 召回率 (\%) & F1-Score & 准确率 (\%) & 召回率 (\%) & F1-Score & \\
        \midrule
        基准模型 (Baseline) & 85.2 & 80.1 & 82.6 & 88.5 & 82.3 & 85.3 & 84.0 \\
        \addlinespace % 增加行间距
        \textit{改进模型 1} & 87.5 & 83.2 & 85.3 & 90.1 & 85.0 & 87.5 & 86.4 \\
        \quad + 特征增强\textsuperscript{a} & 88.3 & 84.5 & 86.4 & 91.0 & 86.2 & 88.5 & 87.5 \\
        \addlinespace
        \textit{改进模型 2} & 89.0 & 85.0 & 87.0 & 91.5 & 87.0 & 89.2 & 88.1 \\
        \quad + 优化算法\textsuperscript{b} & \textbf{90.5} & \textbf{86.3} & \textbf{88.3} & \textbf{92.8} & \textbf{88.5} & \textbf{90.6} & \textbf{89.4} \\
        \bottomrule
    \end{tabular}
    } % \resizebox 结束
    \par\vspace{1ex} % 表格和脚注之间增加一点垂直空间
    \small % 脚注文字使用小一号字体
    \textsuperscript{a} 特征增强具体方法请参考第二章2.1节。\par
    \textsuperscript{b} 优化算法采用自适应学习率策略，具体参数见附录A。
\end{table}
@@@

这里使用 latex 源码 渲染一个嵌套列表
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
