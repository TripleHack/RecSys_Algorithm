# RecSys_Algorithm

信息过载，用户实际需求不明确；强依赖于用户行为。  

## 1.Collaborative Filtering
### item CF

给用户推荐他之前喜欢物品相似的物品  
电商场景下更看重实际转化  
信息流场景下更看重点击率  

$u(i)$表示对item i有行为的用户集合  
$u(j)$表示对item j有行为的用户集合  
分子部分表示user的重合程度，分母则是做了归一化  

$$s_{ij} = \frac {u(i)\cap u(j)} {\sqrt{|u(i)|\cup |u(j)|}}$$  
$$p_{uj} = \sum_{i\in N(u) \cap s(j,k)} {s_{ij} * r_{ui}}$$  
$r_{ui}$表示用户u对物品i的行为得分  
$s_{ij}$表示物品的相似度  
对user u进行item j推荐的得分是根据item i来计算的  
i 是 user u行为过的物品，并且取与item i最相似的k个item  
  
公式升级1：活跃用户应该被降低在相似度公式中的贡献度  
例如：某个电商系统，user a是批发商，买了很多物品，比如啤酒和书刊，但是不能反映他的兴趣，user b是普通用户，只买了啤酒和书刊，这可以反映他的兴趣。按照之前的公式，a与b的贡献度是一样的，我们需要降低user a的贡献度。  
<div align=center><img src="https://github.com/TripleHack/RecSys_Algorithm/blob/master/RecSys公式/2.1.3.png" width="300" height="120" /></div>  
  
公式升级2：用户在不同时间对item的操作应给予时间衰减惩罚  
<div align=center><img src="https://github.com/TripleHack/RecSys_Algorithm/blob/master/RecSys公式/2.1.4.png" width="300" height="230" /></div>  

### user CF
给用户推荐相似兴趣用户感兴趣的物品  
如何评价相似兴趣用户集合  
找到集合用户感兴趣的而目标用户没行为过的item  
  
$$s_{uv} = \frac {N(u)\cap N(v)} {\sqrt{|N(u)|\cup |N(v)|}}$$  
$N(u)$表示用户u有过行为的item集合  
$N(v)$表示用户v有过行为的item集合  
分子部分是item的重合程度  
$$p_{ui} = \sum_{v\in s(u,k) \cap u(i)} {s_{uv} * r_{vi}}$$  
  
公式升级1：降低异常活跃物品对用户相似度的贡献  
例如：电商系统中，user a与user b都购买了新华词典这本书，user a与user c都购买了机器学习，并且他们都只有这一本书重合，这时a与b，a与c重合度都是1，显然是不合理的，因为购买新华字典不能反映真实的兴趣，而机器学习大概率可以反应，因为这本书的购书群体较窄。  
<div align=center><img src="https://github.com/TripleHack/RecSys_Algorithm/blob/master/RecSys公式/2.1.5.png" width="300" height="120" /></div>  
  
公式升级2：不同用户对同一item行为的时间段不同应给予时间惩罚  
<div align=center><img src="https://github.com/TripleHack/RecSys_Algorithm/blob/master/RecSys公式/2.1.6.png" width="300" height="260" /></div>  
  
user cf，是基于用户相似度矩阵来推荐，因此user本身的行为并不会造成自己的推荐结果发生改变；对于item cf来说，产生了新的行为，推荐结果则会立刻发生改变  
user cf，新用户需要等用户有了一定的行为，并得到与其他用户的相似度矩阵之后才可以推荐，但是新物品在被点击之后，则可以推荐给相似用户；对于item cf，新用户一旦完成了点击，便可以推荐相似物品，但是因为新物品还没有进入物品相似度矩阵的计算，因此无法进行新物品的推荐  
user cf，推荐结果略难以解释；item cf的推荐理由有较好的可解释性  
  
user cf不适用于user非常多的场景，item cf适用于item远小于user的场景，实战中更倾向于item cf  
user cf适用于物品需要及时下发，且个性化领域不太强的推荐，item cf适用于长尾物品丰富，且个性化需求强烈的场景，由于真实场景中会有一些召回算法解决新物品下发问题，从个性化层面考虑也更倾向于item cf  
  
## 2.Latent Factor Model  
<div align=center><img src="https://github.com/TripleHack/RecSys_Algorithm/blob/master/formula/3.1.png"/></div>  
<div align=center><img src="https://github.com/TripleHack/RecSys_Algorithm/blob/master/formula/3.2.png"/></div>  
<div align=center><img src="https://github.com/TripleHack/RecSys_Algorithm/blob/master/formula/3.3.png"/></div>  
隐特征个数F(10-32)，正则化参数α(0.01-0.05)，learning rate β(0.01-0.05)  
LFM是传统的监督学习方法，根据样本的label设定损失函数，利用最优化方法使损失函数最小化，特征为隐特征，不是那么直观  
CF是利用公式建模，缺少学习的过程，理论完备性弱于LFM  
item CF需要的空间为item^2  
LFM只需要存储item向量和user向量，LFM需要的空间更少  
LFM需要迭代，耗时略高于CF，但是是同一量级  
item CF可以将矩阵写入内存或redis，可以较好响应用户行为  
LFM，如果将向量写入内存或redis，但是就不能对用户行为及时感知 
