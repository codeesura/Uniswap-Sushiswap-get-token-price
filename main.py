from web3 import Web3, HTTPProvider
import json
import asyncio

URL = "INFURA_LINK"
UNISWAP_FACTORY_ADDRESS = "0x1F98431c8aD98523631AE4a59f267346ea31F984" 
SUSHISWAP_FACTORY_ADDRESS = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" 
WETH_ADDRESS ="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

with open("/abis/UniswapV3Factory.json", "r") as f:
    uniswap_factory_abi = json.loads(f.read())
with open("/abis/UniswapV3Pool.json", "r") as f:
    uniswap_pool_abi = json.loads(f.read())
with open("/abis/SushiswapFactory.json", "r") as f:
    sushiswap_factory_abi = json.loads(f.read())
with open("/abis/SushiswapPool.json", "r") as f:
    sushiswap_pool_abi = json.loads(f.read())

w3 = Web3(HTTPProvider(URL))

async def uniswap():
    factory = w3.eth.contract(address = UNISWAP_FACTORY_ADDRESS , abi = uniswap_factory_abi)

    pool_address = factory.functions.getPool(USDC_ADDRESS, WETH_ADDRESS, 500).call()
    pool = w3.eth.contract(address = pool_address , abi = uniswap_pool_abi)

    slot0 = pool.functions.slot0().call()
    sqrtPriceX96 = slot0[0]

    price = sqrtPriceX96**2 / 2**192
    price = 1/price * 10**12
    print("Uniswap ETH price:", price - (price*0.05/100))

async def sushiswap():
    factory = w3.eth.contract(address = SUSHISWAP_FACTORY_ADDRESS , abi = sushiswap_factory_abi)

    pool_address = factory.functions.getPair(USDC_ADDRESS, WETH_ADDRESS).call()
    pool = w3.eth.contract(address = pool_address , abi = sushiswap_pool_abi)

    reserves = pool.functions.getReserves().call()
    reserve_0 = reserves[0]
    reserve_1 = reserves[1]
    a = reserve_0 / reserve_1

    print("Sushiswap ETH price:",(a - a * 0.31 /100 )*10**12 + 0.05)

async def main_uniswap():
    await uniswap()

async def main_sushiswap():
    await sushiswap()

asyncio.run(main_uniswap())
asyncio.run(main_sushiswap())
