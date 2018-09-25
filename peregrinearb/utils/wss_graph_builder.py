import logging
import math


__all__ = [
    'wss_add_market',
    'wss_update_graph',
]


adapter = logging.getLogger(__name__)


def wss_add_market(graph, symbol, market_data):
    base, quote = symbol.split('/')
    graph.add_edge(base, quote, weight=float('Inf'), depth=float('Inf'), market_name=symbol,
                   fee=float(market_data['taker_fee']), volume=0, no_fee_rate=-float('Inf'), trade_type='SELL')
    graph.add_edge(quote, base, weight=float('Inf'), depth=float('Inf'), market_name=symbol,
                   fee=float(market_data['taker_fee']), volume=0, no_fee_rate=float('Inf'), trade_type='BUY')


def wss_update_graph(graph, symbol, side, price, volume, *args):
    base, quote = symbol.split('/')
    fee_scalar = 1 - graph[base][quote]['fee']
    if side == 'sell':
        opp_could_exist = price > graph[base][quote]['no_fee_rate']
        graph[base][quote]['weight'] = -math.log(price * fee_scalar)
        graph[base][quote]['depth'] = -math.log(volume)
        graph[base][quote]['volume'] = volume
        graph[base][quote]['no_fee_rate'] = price
    else:
        opp_could_exist = price < graph[base][quote]['no_fee_rate']
        graph[quote][base]['weight'] = -math.log(fee_scalar * 1 / price)
        graph[quote][base]['depth'] = -math.log(volume * price)
        graph[quote][base]['volume'] = volume
        graph[quote][base]['no_fee_rate'] = price

    return opp_could_exist
