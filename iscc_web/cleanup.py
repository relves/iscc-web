# -*- coding: utf-8 -*-
import asyncio
import time
import iscc_web as iw
from loguru import logger as log
from aiofiles.os import scandir, path


async def cleanup_task():
    while True:
        log.debug("Running cleanup session ...")
        for fp in await scandir(iw.opts.media_path):
            if fp.name in ["061knt35ejv6o", ".gitignore"]:
                continue
            dir_time = int(await path.getctime(fp.path))
            cur_time = int(time.time())
            if cur_time > (dir_time + iw.opts.storage_expiry):
                log.debug(f"Deleting expired {fp.name}")
                await iw.rmtree(fp.path)
        await asyncio.sleep(iw.opts.cleanup_interval)
