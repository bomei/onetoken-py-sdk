import asyncio
import onetoken
import pytest


@pytest.mark.asyncio
async def test_tick_quote():
    q = await onetoken.quote.get_client()

    happen = False

    async def update(tk):
        nonlocal happen
        happen = True
        assert tk.contract == 'okef/btc.usd.q'
        print('tick updated')

    await q.subscribe_tick('okef/btc.usd.q', on_update=update)
    for _ in range(60):
        await asyncio.sleep(1)
    await q.close()
    assert happen


@pytest.mark.asyncio
async def test_candle_quote():
    happen = False

    async def update(candle):
        nonlocal happen
        happen = True
        assert candle.contract == 'okef/btc.usd.q'
        assert candle.duration == '1m'
        print('candle updated')

    await onetoken.quote.subscribe_candle('okef/btc.usd.q', '1m', on_update=update)
    await onetoken.quote.subscribe_candle('okef/btc.usd.q', '1m', on_update=update)
    for _ in range(60):
        await asyncio.sleep(1)
    assert happen

if __name__ == "__main__":
    #asyncio.ensure_future(test_tick_quote())
    asyncio.ensure_future(test_candle_quote())
    asyncio.get_event_loop().run_forever()