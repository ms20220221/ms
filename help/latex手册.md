* 空白距离
  1. 空格和制表符都被看作相同的空白距离。多个空白字符等于一个空白字符。多个空行也认为是一个空行。
* 特殊字符\#,\$,\%,\^,\_,\{,\},在前面加反斜杠才能正常显示。特例：反斜杠不能通过在前面加反斜杠得到，双反斜杠是换行。如果要打出反斜杠，在数学环境中输入反斜杠+backlash

* latex命令
  由反斜杠开始。如果不想命令吃掉后面的空格，可以加大括号

* 注释：百分号

* 源文件结构：
\documentclass{...}

\usepackage{....}  加入宏包

\begin{document}  文档开头

\end{document}文档结束，后面的内容会被忽略

* -：连字号；--：破折号；---：长破折号
* \ldots :省略号
* 每一句的结尾要加个空格，增加可读性。除非是缩写如A.W.J


## 标题和章节
1. 一级标题：\section{标题}
2. 二级标题：\subsection{}
3. 三级标题：\subsubsection{}
4. 四级标题：\paragraph{}
5. 五级标题：\subparagraph{}

* 把文档分为几个部分而不影响章节序号：\part{}
* 插入目录：\tableofcontents
* 如果加上星号，则标题不出现于目录，也不带序号。\section*{dd}
* \title{},\author{}\and{},date{}
* \maketitle:整篇文章的标题

## 交叉引用
\label{marker1}

\ref{marker1}

脚注：\footnote{}
## 强调
\undreline{text}

\emph{text}斜体

## 环境：
\begin{environment} text \end{environment}

* itemize:无标号列表
* enumerate：有序号列表
* description：带描述的列表

>\flushleft
\begin{enumerate}
\item You can mix the list
environments to your taste:
\begin{itemize}
\item But it might start to
look silly.
\item[-] With a dash.
\end{itemize}
\item Therefore remember:
\begin{description}
\item[Stupid] things will not
become smart because they arec
in a list.
\item[Smart] things, though,
can be presented beautifully
in a list.
\end{description}
\end{enumerate}

* flushleft:左对齐
* lushright:右对齐
* cener:居中

* quote:引用
* abstract:摘要

## 原文打印：
* verbatim环境
* \verb|xxx|

## 表格
* tabular环境
* \begin{tabular}[pos]{table spec}
* 表格总是在同一页上，如果要排一个长表格，可以看supertabular和longtabular环境
## 浮动体
* figure环境或table环境
* \begin{table}[!hbp]
* 