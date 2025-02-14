#%% md
## 行情数据(单日数据)

* 开盘收盘最高最低

* 数据的精度

* 前后复权

https://www.akshare.xyz/index.html

股票数据复权

1.为何要复权：由于股票存在配股、分拆、合并和发放股息等事件，会导致股价出现较大的缺口。 若使用不复权的价格处理数据、计算各种指标，将会导致它们失去连续性，且使用不复权价格计算收益也会出现错误。 为了保证数据连贯性，常通过前复权和后复权对价格序列进行调整。

2.前复权：保持当前价格不变，将历史价格进行增减，从而使股价连续。 前复权用来看盘非常方便，能一眼看出股价的历史走势，叠加各种技术指标也比较顺畅，是各种行情软件默认的复权方式。 这种方法虽然很常见，但也有两个缺陷需要注意。

2.1 为了保证当前价格不变，每次股票除权除息，均需要重新调整历史价格，因此其历史价格是时变的。 这会导致在不同时点看到的历史前复权价可能出现差异。

2.2 对于有持续分红的公司来说，前复权价可能出现负值。

3.后复权：保证历史价格不变，在每次股票权益事件发生后，调整当前的股票价格。 后复权价格和真实股票价格可能差别较大，不适合用来看盘。 其优点在于，可以被看作投资者的长期财富增长曲线，反映投资者的真实收益率情况。

4.在量化投资研究中普遍采用后复权数据。

* 其他行情数据接口

#%% md
## 基于pyecharts的k线图

## 股票中的均线

* talib

TA-Lib，全称“Technical Analysis Library”, 即技术分析库，是Python金融量化的高级库，涵盖了150多种股票、期货交易软件中常用的技术分析指标，如MACD、RSI、KDJ、动量指标、布林带等等。TA-Lib可分为10个子板块：Overlap Studies(重叠指标)，Momentum Indicators(动量指标)，Volume Indicators(交易量指标)，Cycle Indicators(周期指标)，Price Transform(价格变换)，Volatility Indicators(波动率指标)，Pattern Recognition(模式识别)，Statistic Functions(统计函数)，Math Transform(数学变换)和Math Operators(数学运算)，

链接：https://www.jianshu.com/p/7ecc7962d638

TA-LIB 200多个技术指标含有及计算式:

https://blog.csdn.net/MARY197011111/article/details/79622184

重叠指标

https://www.jianshu.com/p/7ecc7962d638


更多的例子：

https://gallery.pyecharts.org/#/Candlestick/README

* k线图的基本意义
