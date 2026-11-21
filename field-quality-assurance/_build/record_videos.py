# -*- coding: utf-8 -*-
"""Record each scenario of the segment protocol demo as an MP4, in real time, through Edge's DevTools protocol.
Usage: python _build/record_videos.py <training_folder> <out_dir> [lang] [scenario ...]
Needs Microsoft Edge, the websockets package and imageio-ffmpeg."""
import asyncio
import base64
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

import imageio_ffmpeg
import requests
import websockets

ROOT, OUT = sys.argv[1], sys.argv[2]
LANG = sys.argv[3] if len(sys.argv) > 3 else 'fr'
ONLY = sys.argv[4:]
SCEN = ['basic', 'quota1', 'flood', 'empty', 'river', 'danger', 'swamp', 'two', 'below', 'emptypsu', 'g1']
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PORT = 9333
W, H = 1280, 720
DEMO = pathlib.Path(ROOT, '04_Segment_protocol_demo', 'segment_protocol_demo.html').resolve().as_uri()
FF = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs(OUT, exist_ok=True)


class CDP:
    def __init__(self, ws):
        self.ws, self.n, self.pending, self.events = ws, 0, {}, asyncio.Queue()

    async def reader(self):
        async for msg in self.ws:
            m = json.loads(msg)
            if 'id' in m and m['id'] in self.pending:
                self.pending.pop(m['id']).set_result(m)
            elif 'method' in m:
                await self.events.put(m)

    async def call(self, method, **params):
        self.n += 1
        fut = asyncio.get_event_loop().create_future()
        self.pending[self.n] = fut
        await self.ws.send(json.dumps({'id': self.n, 'method': method, 'params': params}))
        return (await fut).get('result', {})


async def record(cdp, sid, variant):
    frames = []
    tmp = tempfile.mkdtemp()
    url = f'{DEMO}?video=1&s={sid}&v={variant}&lang={LANG}&speed=5'
    await cdp.call('Page.navigate', url=url)
    await asyncio.sleep(1.5)
    await cdp.call('Page.startScreencast', format='jpeg', quality=82, maxWidth=W, maxHeight=H, everyNthFrame=1)
    t_start = time.time()

    async def grab():
        while True:
            ev = await cdp.events.get()
            if ev['method'] == 'Page.screencastFrame':
                p = ev['params']
                f = os.path.join(tmp, f'{len(frames):05d}.jpg')
                with open(f, 'wb') as fh:
                    fh.write(base64.b64decode(p['data']))
                frames.append((time.time(), f))
                await cdp.call('Page.screencastFrameAck', sessionId=p['sessionId'])

    g = asyncio.create_task(grab())
    await asyncio.sleep(1.0)
    await cdp.call('Runtime.evaluate', expression='play()')
    while True:
        await asyncio.sleep(0.5)
        r = await cdp.call('Runtime.evaluate', expression='idx>=steps.length && !playing', returnByValue=True)
        if r.get('result', {}).get('value') or time.time() - t_start > 240:
            break
    await asyncio.sleep(3.0)
    await cdp.call('Page.stopScreencast')
    g.cancel()
    # constant 15 fps: repeat the latest frame until the next one arrives
    fps, t0, t1 = 15, frames[0][0], frames[-1][0] + 1.5
    seq = os.path.join(tmp, 'seq')
    os.makedirs(seq)
    k, j = 0, 0
    t = t0
    while t < t1:
        while j + 1 < len(frames) and frames[j + 1][0] <= t:
            j += 1
        shutil.copyfile(frames[j][1], os.path.join(seq, f'{k:06d}.jpg'))
        k += 1
        t += 1 / fps
    out = os.path.join(OUT, f'{sid}_{variant}_{LANG}.mp4')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(seq, '%06d.jpg'),
                    '-vf', f'scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:white',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '27', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f'{out}: {k / fps:.0f} s, {os.path.getsize(out) / 1e6:.1f} MB', flush=True)


async def main():
    prof = tempfile.mkdtemp()
    proc = subprocess.Popen([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--remote-debugging-port={PORT}',
                             f'--user-data-dir={prof}', f'--window-size={W},{H}', '--allow-file-access-from-files', 'about:blank'])
    try:
        for _ in range(40):
            try:
                pages = requests.get(f'http://127.0.0.1:{PORT}/json/list', timeout=1).json()
                page = next(p for p in pages if p['type'] == 'page')
                break
            except Exception:
                time.sleep(0.5)
        async with websockets.connect(page['webSocketDebuggerUrl'], max_size=50_000_000) as ws:
            cdp = CDP(ws)
            rd = asyncio.create_task(cdp.reader())
            await cdp.call('Page.enable')
            await cdp.call('Runtime.enable')
            await cdp.call('Emulation.setDeviceMetricsOverride', width=W, height=H, deviceScaleFactor=1, mobile=False)
            for sid in (ONLY or SCEN):
                for v in ('correct', 'wrong'):
                    await record(cdp, sid, v)
            rd.cancel()
    finally:
        proc.terminate()


asyncio.run(main())
