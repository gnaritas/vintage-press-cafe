#!/usr/bin/env python3
"""Render sweep for vintage-press-cafe demo host — local headless Chrome over CDP (port 9341,
unique user-data-dir; honey-bistro lineage). 10 pages x 2 viewports (1280 desktop, 390 mobile):
DOM-metrics gate + full-page capture."""
import asyncio, base64, io, json, os, subprocess, sys, time
import urllib.request
import websockets

O = "https://vintage-press-cafe-demo.up.railway.app"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "renders")
PAGES = ["index", "menu", "coffee-and-tea", "breakfast-and-lunch", "our-story",
         "visit", "contact", "privacy", "404", "thanks"]
VPS = [(1280, 900, False), (390, 844, True)]
PORT = 9341

GATE = """(() => {
  const vw = document.documentElement.clientWidth;
  const nm = e => (e.tagName + '.' + (typeof e.className === 'string' ? (e.className.split(' ')[0] || '') : '')).slice(0, 42);
  const bad = [];
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e);
    if (cs.position === 'fixed' || e.closest('.skip')) continue;
    const r = e.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (r.right > vw + 2 || r.left < -2) bad.push(nm(e) + ' w' + Math.round(r.width) + ' x' + Math.round(r.left) + '..' + Math.round(r.right));
  }
  const ovf = [];
  for (const e of document.querySelectorAll('main *, header *, footer *')) {
    if (e.scrollWidth > e.clientWidth + 2 && e.clientWidth > 0 && getComputedStyle(e).overflowX === 'visible' && e.tagName !== 'IFRAME') ovf.push(nm(e) + ' ' + e.scrollWidth + '>' + e.clientWidth);
  }
  let map = 'none';
  const m = document.querySelector('.mapwrap');
  if (m) { const fr = m.querySelector('iframe'); if (fr) { const r = fr.getBoundingClientRect(); map = Math.round(r.width) + 'x' + Math.round(r.height); } }
  return JSON.stringify({ vw, bad: bad.slice(0, 12), ovf: ovf.slice(0, 12), map, hs: document.documentElement.scrollHeight, bodysw: document.body.scrollWidth });
})()"""

async def main():
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=10) as r:
        ver = json.load(r)
    results = []
    async with websockets.connect(ver["webSocketDebuggerUrl"], max_size=60 * 1024 * 1024) as ws:
        mid = [0]
        events = {}
        sess = [None]
        async def send(method, params=None):
            mid[0] += 1
            payload = {"id": mid[0], "method": method, "params": params or {}}
            if sess[0] and not method.startswith("Target."):
                payload["sessionId"] = sess[0]
            await ws.send(json.dumps(payload))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("method") == "Page.loadEventFired":
                    events["load"] = True
                if msg.get("id") == mid[0]:
                    if "error" in msg:
                        raise RuntimeError(method + ": " + json.dumps(msg["error"])[:200])
                    return msg.get("result", {})
        tid = (await send("Target.createTarget", {"url": "about:blank"}))["targetId"]
        sess[0] = (await send("Target.attachToTarget", {"targetId": tid, "flatten": True}))["sessionId"]
        await send("Page.enable")
        await send("Runtime.enable")
        for (w, h, mobile) in VPS:
            await send("Emulation.setDeviceMetricsOverride",
                       {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": mobile})
            for pg in PAGES:
                url = O + ("/" if pg == "index" else "/" + pg)
                events.pop("load", None)
                await send("Page.navigate", {"url": url})
                t0 = time.time()
                while not events.get("load") and time.time() - t0 < 40:
                    try:
                        msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=2))
                        if msg.get("method") == "Page.loadEventFired":
                            events["load"] = True
                    except asyncio.TimeoutError:
                        pass
                grace = 3.2 if pg == "visit" else 1.4
                await asyncio.sleep(grace)
                ev = await send("Runtime.evaluate", {"expression": GATE, "returnByValue": True})
                gate = json.loads(ev["result"]["value"])
                cap_h = max(int(gate["hs"]), 850)
                cap_w = 1280 if not mobile else int(gate["vw"])
                shot = await send("Page.captureScreenshot",
                                  {"format": "jpeg", "quality": 78, "captureBeyondViewport": True,
                                   "clip": {"x": 0, "y": 0, "width": cap_w, "height": cap_h, "scale": 1}})
                data = base64.b64decode(shot["data"])
                vp = "d1280" if not mobile else "m390"
                path = os.path.join(OUT, f"{PAGES.index(pg):02d}-{pg}-{vp}.jpg")
                with open(path, "wb") as f:
                    f.write(data)
                try:
                    from PIL import Image
                    im = Image.open(io.BytesIO(data))
                    dims = im.size
                except Exception:
                    dims = (0, 0)
                results.append({"page": pg, "vp": vp, "gate": gate, "shot": path,
                                "shot_kb": len(data) // 1024, "dims": list(dims)})
                print(json.dumps({"page": pg, "vp": vp, "gate": gate, "kb": len(data)//1024, "dims": list(dims)}), flush=True)
        try:
            await send("Target.closeTarget", {"targetId": tid})
        except Exception:
            pass
    with open(os.path.join(OUT, "sweep_results.jsonl"), "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print("SWEEP_DONE", len(results))

asyncio.run(main())
