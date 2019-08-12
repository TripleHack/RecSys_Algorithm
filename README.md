# RecSys_Algorithm

信息过载，用户实际需求不明确；强依赖于用户行为。
给用户推荐他之前喜欢物品相似的物品
电商场景下更看重实际转化
信息流场景下更看重点击率

#### Collaborative Filtering
##### item CF

$u(i)$表示对item i有行为的用户集合
$u(j)$表示对item j有行为的用户集合
分子部分表示user的重合程度，分母则是做了归一化

$$s_{ij} = \frac {u(i)\cap u(j)} {\sqrt{|u(i)|\cup |u(j)|}}$$
