
# LL1

### LL(1)文法

什么是LL1文法?

- 第一个L代表从左至右
- 第二个L代表产生最左推导
- 1代表每一步中只需要向前看一个输入符号就可以决定语法分析动作

之前我们提到了如何计算FIRST集和FOLLOW集,既然我们已经知道了在某一状态的开头的字符都是什么,后面跟着字符都可能是什么,那么我们就可以做出预测分析.

由此引出了`可选集-SELECT集`的概念


SELECT集是指选用该产生式时的输入符号的集合


SELECT集的求法也比较简单

- 当产生式非空时,将首终结符加入SELECT集中,如果首字符是非终结符那么将该非终结符的FIRST集加入SELECT集中
- 当产生式为空时,将FOLLOW集加入SELECT集中


这里值得注意的一点是,现在得到的文法很有可能是多个 | 连接起来的,在计算SELECT集的时候我们需要把它们都拆开,
比如 A -> aBc | ST | c,应该分解为 A->aBc,A->ST,A->c. 在分别计算它们的SELECT(A->aBc),SELECT(A->ST),SELECT(A->c)

FIRST集和SELECT集中是可以有ε的,只有FOLLOW集中没有ε,应该说是没有出现的必要.



对于之前的例子



```txt
S -> (L) | a
L -> SL'
L' -> ,SL' | ε
```



|FIRST集|元素|FOLLOW集|元素|
|:--:|:--:|:--:|:--:|
|FIRST(S)|{(,a}|FOLLOW(S)|{$,`,`,)}|
|FIRST(L)|{(,a}|FOLLOW(L)|{$,)}|
|FIRST(L')|{`,`,ε}|FOLLOW(L')|{$,)}|


记得拆开 | 哦~


|SELECT|ITEM|
|:--:|:--:|
|SELECT(S->(L))|{(}|
|SELECT(S->a)|{a}|
|SELECT(L->SL')|{(,a}|
|SELECT(L'->,SL')|{,}|
|SELECT(L'->ε)|{$,)}|

对于具有相同左部的SELECT集,只要它们不相交,那么我们可以根据它SELECT集中的元素唯一的选择一个产生式由于推断,这样就避免了回溯,这就是LL1文法的优势.

这样我们就得到了一个表格,我们可以把它画出来


横坐标中的输入符号就是所有出现在SELECT集后面的元素
纵坐标就是所有的左部的非终结符


|非终结符|(|)|,|a|$|
|:--:|:--:|:--:|:--:|:--:|:--:|
|S|S->(L)|||S->a||
|L|L->SL'|L->SL'|||
|L'||L'->ε|L'->,SL'||L'->ε|


那么这个分析表应该怎么用呢


我们不妨先来做一道题,我会将我的解答放在下面,不过建议你先独立做完这道题再看

![20220428201954](https://raw.githubusercontent.com/learner-lu/picbed/master/20220428201954.png)

1. 试写出 ¬(a→a)$ 的一个最左推导

   ```txt
   F -> ¬F
   F -> ¬(F)
   F -> ¬(F→F)
   F -> ¬(a→F)
   F -> ¬(a→a)
   ```

2. 消除左递归和左公因子

   ```txt
   F -> ¬FT | (F)T | aT
   T -> →FT | ε
   ```

3. 求FIRST集 FOLLOW集

   |FIRST|ITEM|FOLLOW|ITEM|
   |:--:|:--:|:--:|:--:|
   |FIRST(F)|{¬,(,a}|FOLLOW(F)|{$,),→}|
   |FIRST(T)|{→,ε}|FOLLOW(T)|{$,),→}|

4. LL1分析表

   |SELECT|ITEM|
   |:--:|:--:|
   |SELECT(F->¬FT)|{¬}|
   |SELECT(F->(F)T)|{(}|
   |SELECT(F->aT)|{a}|
   |SELECT(T->→FT)|{→}|
   |SELECT(T->ε)|{$,),→}|

   |非终结符|¬|(|a|$|)|→|
   |:--:|:--:|:--:|:--:|:--:|:--:|:--:|
   |F|F->¬FT|F->(F)T|F->aT|
   |T||T->ε|T->ε|T->ε|T->ε|T->→FT\|ε|

   当输入为→且非终结符为T时,存在两个产生式,SELECT(T->→FT)与SELECT(T->ε)存在交集.所以不是LL1文法

5. ¬(a→a)的推导过程

   
   推导过程就是一个根据分析表一步步解析,消减的过程,如下
   

   |剩余串|分析栈|分析动作|
   |:--:|:--:|:--:|
   |¬(a→a)$|F$|F->¬FT|
   |¬(a→a)$|¬FT$||
   |(a→a)$|FT$|F->(F)T|
   |(a→a)$|(F)TT$||
   |a→a)$|F)TT$|F->aT|
   |a→a)$|aT)TT$||
   |→a)$|T)TT$|T->→FT|
   |→a)$|→FT)TT$||
   |a)$|FT)TT$|F->aT|
   |a)$|aTT)TT$||
   |)$|TT)TT$|T->ε|
   |)$|T)TT$|T->ε|
   |)$|)TT$||
   |$|TT$|T->ε|
   |$|T$|T->ε|
   |$|$||
