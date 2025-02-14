# pandas 来做数据分析
## 目的
1. 统一数据的格式，减少不必要的学习成本
2. 方便数据的处理，能够进行跨不同平台的数据分析
3. 自定义数据可视化

## 如何使用pandas和backtrader结合
1. 使用pandas读取数据 分析买卖时机
2. 通过时机数据，生成交易信号
3. 通过交易信号，使用backtrader进行回测

MACD的计算公式如下：

### 1. **MACD线**
MACD线是12日指数移动平均线（EMA）减去26日EMA的结果。

\[ \text{MACD线} = \text{12日EMA} - \text{26日EMA} \]

### 2. **信号线（Signal Line）**
信号线是MACD线的9日EMA。

\[ \text{信号线} = \text{MACD线的9日EMA} \]

### 3. **柱状图（Histogram）**
柱状图是MACD线与信号线的差值。

\[ \text{柱状图} = \text{MACD线} - \text{信号线} \]

### 指数移动平均线（EMA）的计算
EMA的计算公式为：

\[ \text{EMA}_{today} = \left( \text{Price}_{today} \times \left( \frac{2}{N+1} \right) \right) + \left( \text{EMA}_{yesterday} \times \left( 1 - \frac{2}{N+1} \right) \right) \]

其中：
- \( \text{Price}_{today} \) 是当天的价格。
- \( \text{EMA}_{yesterday} \) 是前一天的EMA值。
- \( N \) 是EMA的周期（例如12日、26日或9日）。

### 示例
假设某股票的12日EMA为50，26日EMA为45，9日EMA为48：

1. **MACD线**：
\[ \text{MACD线} = 50 - 45 = 5 \]

2. **信号线**：
\[ \text{信号线} = 48 \]

3. **柱状图**：
\[ \text{柱状图} = 5 - 48 = -43 \]

### 总结
MACD的计算涉及12日EMA、26日EMA和9日EMA，通过这些公式可以得出MACD线、信号线和柱状图，进而用于技术分析。


### 策略
1. 30日均线突破
2. MACD 快慢线的差异，增强版均线。反映趋势
3. RSI 强弱
4. kdj 
5. mtm 动量；上涨的时候，下跌的时候，量能的关系（可能有假）
6. 唐奇安通道
7. 布林带

### 目标
1. 手动+自动 的系统 --- 纯自动
2. 防止亏损的保底策略
3. 有组合的策略，能够稳健投资； 衡量组合的风险，夏普，回测
4. 分仓，不同风险承担不同的组合
5. 手续费的观测
6. 融资融券的费率和规则机制


# 基于backtrader的量化交易策略


* 从量化平台（掘金量化，米筐，聚宽，优矿）到开源库

* backtrader的安装

pip install backtrader[plotting] -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

* 解决无法作图的办法：

https://blog.csdn.net/weixin_41494909/article/details/119427922


## backtrader的交易策略编写逻辑

https://blog.csdn.net/qq_41578115/article/details/122525397

https://blog.csdn.net/h00cker/article/details/120911268

* 编写形式，class(next) addstrategy

* 交易策略的真实逻辑：以bar（交易日）为周期，重复运行next函数，对应的就是导入的data序列，每一对应一次next函数的重复运行（当前序列始终对应的是0）

* 为了提供交易的进行与记录，底层提供若干函数（self.order，self.sell）和变量可以调取（self.position，self.datetime）

