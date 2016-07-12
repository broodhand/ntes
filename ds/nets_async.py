
import logging;logging.basicConfig(level=logging.DEBUG)
import aiohttp


# 通过网易代码异步获取网易api数据，最大限制1000数据
async def __asyncgetnvalue(sessions, future, *codes):
    fronturl = 'http://api.money.126.net/data/feed/'
    backurl = ',money.api'
    codelist = list()

    logging.info('__asyncgetnvalue:Input data number %s' % len(codes))

    if len(codes) > 1010:
        raise ValueError('Too many code input: %s' % len(codes))

    for code in codes:
        codelist.append(str(code))

    url = fronturl + ','.join(codelist) + backurl
    with aiohttp.Timeout(10):
        async with sessions.get(url) as response:
            future.set_result(await response.text())