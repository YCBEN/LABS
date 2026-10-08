"""Tank simulator. Coil 0 = pump command (written by PLC).
Input register 0 = tank level x10 (read by PLC). Modbus/TCP on 502."""
import asyncio, random
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import (ModbusSequentialDataBlock,
                                ModbusSlaveContext, ModbusServerContext)

def log(*a):
    print(*a, flush=True)

async def process(store):
    level = 50.0
    store.setValues(4, 0, [int(level * 10)])
    n = 0
    while True:
        try:
            pump = store.getValues(1, 0, 1)[0]
            level += (2.0 if pump else -1.0) + random.uniform(-0.3, 0.3)
            level = max(0.0, min(100.0, level))
            store.setValues(4, 0, [int(level * 10)])
            n += 1
            if n % 10 == 0:
                log(f"level={level:.1f} pump={pump}")
        except Exception as e:
            log("process error:", repr(e))
        await asyncio.sleep(1)

async def main():
    blk = lambda: ModbusSequentialDataBlock(0, [0] * 16)
    store = ModbusSlaveContext(di=blk(), co=blk(), hr=blk(), ir=blk(),
                               zero_mode=True)
    task = asyncio.create_task(process(store))
    log("field-sim starting on port 502")
    await StartAsyncTcpServer(
        context=ModbusServerContext(slaves=store, single=True),
        address=("0.0.0.0", 502))
    await task

asyncio.run(main())
