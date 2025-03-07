import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta


# 假设有一个函数可以获取沪深300成分股数据和资金流数据
# 这里用伪数据替代，实际需接入真实数据源（如tushare、akshare等）

class MoneyFlowStrategy(bt.Strategy):
    params = (
        ('hold_period', 15),  # 最大持有天数
        ('portfolio_size', 5),  # 组合持有5只股票
        ('lookback_days', 5),  # 查看过去5天的资金流入
    )

    def __init__(self):
        self.stocks = self.datas  # 所有沪深300股票数据
        self.positions = {}  # 记录持仓天数
        self.kdj = {d._name: bt.indicators.Stochastic(d) for d in self.datas}  # KDJ指标
        self.macd = {d._name: bt.indicators.MACD(d) for d in self.datas}  # MACD指标

    def next(self):
        # 当前日期
        current_date = self.datas[0].datetime.date(0)

        # 1. 计算过去5天资金净流入排名
        money_flow_ranking = {}
        for data in self.stocks:
            if len(data) >= self.params.lookback_days:
                money_flow = 0
                for i in range(-self.params.lookback_days + 1, 1):
                    # 假设data.money_flow是资金流数据，需替换为真实字段
                    money_flow += data.get(ago=i, size=1)[0]
                money_flow_ranking[data._name] = money_flow

        # 按资金流入排序，取前5
        sorted_stocks = sorted(money_flow_ranking.items(), key=lambda x: x[1], reverse=True)
        top_5_stocks = [stock[0] for stock in sorted_stocks[:self.params.portfolio_size]]

        # 2. 检查当前持仓并处理卖出逻辑
        for stock in list(self.positions.keys()):
            position = self.getpositionbyname(stock)
            if position.size > 0:
                days_held = self.positions[stock]['days'] + 1
                self.positions[stock]['days'] = days_held

                kdj = self.kdj[stock]
                macd = self.macd[stock]

                # 卖出条件：KDJ超买(MACD死叉) 或 持有超过15天
                sell_signal = (
                        (kdj.percK[-1] > 80 and macd.macd[-1] < macd.signal[-1]) or
                        days_held >= self.params.hold_period
                )

                if sell_signal:
                    self.sell(data=self.getdatabyname(stock), size=position.size)
                    del self.positions[stock]
                    print(f"{current_date}: Sold {stock}")

        # 3. 买入逻辑：补齐到5只股票
        current_holdings = len(self.positions)
        available_slots = self.params.portfolio_size - current_holdings

        if available_slots > 0:
            for stock_name in top_5_stocks:
                if stock_name not in self.positions and available_slots > 0:
                    data = self.getdatabyname(stock_name)
                    cash = self.broker.getcash()
                    size = int((cash / available_slots) / data.close[0])  # 等额分配现金
                    if size > 0:
                        self.buy(data=data, size=size)
                        self.positions[stock_name] = {'days': 0}
                        available_slots -= 1
                        print(f"{current_date}: Bought {stock_name}")


# 数据加载函数（示例）
def load_data():
    cerebro = bt.Cerebro()

    # 假设沪深300股票列表和数据，这里用随机数据模拟
    hs300_stocks = ['stock1', 'stock2', 'stock3', ..., 'stock300']  # 替换为真实沪深300代码
    for stock in hs300_stocks:
        df = pd.DataFrame({
            'open': ...,  # 需填充真实数据
            'high': ...,
            'low': ...,
            'close': ...,
            'volume': ...,
            'money_flow': ...,  # 资金流数据
        }, index=pd.date_range(start='2020-01-01', end='2025-03-06', freq='D'))

        data = bt.feeds.PandasData(dataname=df, name=stock)
        cerebro.adddata(data)

    return cerebro


# 主函数
if __name__ == '__main__':
    cerebro = load_data()
    cerebro.addstrategy(MoneyFlowStrategy)
    cerebro.broker.setcash(1000000)  # 初始资金100万
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)  # 每笔交易固定股数，可调整

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # 可视化结果
    cerebro.plot()