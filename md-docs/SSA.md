
# SSA

## DU UD

O(M * N)

du chain: <<x, <B2, 1>>, {<B4, 1>, <B5, 1>}>

ud chain: <<x, <B5, 1>>, {<B2, 1>, <B3, 1>}>

## SSA

图的边使用前驱和后继, 树的边使用父亲和儿子

静态单赋值是一种比较新的中间代码表示, 它能够有效地将程序中运算的值与他们的存储位置分开, 从而使得若干优化能具有更有效的形式

如果在某个过程内赋值的每一个变量作为赋值的目标只出现一次, 我们说这个过程是静态单赋值(SSA, static single-assignment)的形式

结点 x 的必经结点边界(dominance frontier)是所有符合下面条件的结点 w 的集合: x 是 w 的前驱的必经结点, 但不是 w 的严格必经结点

$DF_{local}[n]$: 不以 n 为严格必经结点的 n 的后继

$DF_{up}[n]$: 属于 n 的必经结点边界, 但是不以 n 的直接必经结点作为严格必经结点的结点

$DF[n] = DF_{local}[n] \cup \bigcup\limits_{c \in children[n]} DF_{up}[c]$

children[n] 是以 n 作为直接必经结点的所有结点, 从支配树上来看就是 n 的所有儿子结点

## 参考

- [Wiki 静态单赋值形式](https://zh.wikipedia.org/wiki/%E9%9D%99%E6%80%81%E5%8D%95%E8%B5%8B%E5%80%BC%E5%BD%A2%E5%BC%8F)
- [程序分析与优化 - 7 静态单赋值(SSA)](https://www.cnblogs.com/zhouronghua/p/16390138.html)