import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize, dirname } from 'node:path';
import { chromium } from 'playwright';
const ROOT = join(dirname(new URL(import.meta.url).pathname), '..', 'site', 'porchfest');
const PORT = 4192;
const MIME = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'};
const server = http.createServer(async (req,res)=>{ try{
  let p = normalize(decodeURIComponent(req.url.split('?')[0])).replace(/^(\.\.[/\\])+/,'');
  if(p.endsWith('/')) p+='index.html';
  const b = await readFile(join(ROOT,p));
  res.writeHead(200,{'Content-Type':MIME[extname(p)]||'application/octet-stream'}); res.end(b);
}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(PORT,r));
const at=p=>`http://localhost:${PORT}${p}`;
const out=join(ROOT,'..','..','porchfest','shots');
await (await import('node:fs/promises')).mkdir(out,{recursive:true});
const br = await chromium.launch();

// marketing, desktop dark
let ctx = await br.newContext({viewport:{width:1440,height:1000}});
let pg = await ctx.newPage();
await pg.goto(at('/index.html'),{waitUntil:'networkidle'});
await pg.screenshot({path:join(out,'1-marketing.png'),fullPage:false});
await ctx.close();

// app: plan a route, desktop dark
ctx = await br.newContext({viewport:{width:1600,height:1000}});
pg = await ctx.newPage();
await pg.goto(at('/app/'),{waitUntil:'networkidle'});
// dial in a taste so the result is interesting
await pg.evaluate(()=>{ document.querySelector('[data-preset="Loud & fast"]').click(); });
await pg.waitForTimeout(1600);
await pg.screenshot({path:join(out,'2-app-dark.png')});
await pg.click('#themeBtn'); await pg.waitForTimeout(400);
await pg.screenshot({path:join(out,'3-app-light.png')});
// exactly 4 bands, dark
await pg.click('#themeBtn'); await pg.waitForTimeout(200);
await pg.selectOption('#minB','4'); await pg.selectOption('#maxB','4');
await pg.waitForTimeout(1700);
await pg.screenshot({path:join(out,'8-exactly-4.png')});
await pg.selectOption('#minB','0'); await pg.selectOption('#maxB','0');
await pg.waitForTimeout(1500);
// bands browser
await pg.locator('[data-go="bands"]:visible').first().click();
await pg.waitForTimeout(900);
await pg.screenshot({path:join(out,'4-bands.png')});
await ctx.close();

// mobile: schedule + map
ctx = await br.newContext({viewport:{width:390,height:800},deviceScaleFactor:2});
pg = await ctx.newPage();
await pg.goto(at('/app/'),{waitUntil:'networkidle'});
await pg.evaluate(()=>document.querySelector('[data-preset="Family stroll"]').click());
await pg.waitForTimeout(1600);
await pg.screenshot({path:join(out,'5-mobile-schedule.png')});
await pg.locator('[data-go="map"]:visible').first().click();
await pg.waitForTimeout(500);
await pg.screenshot({path:join(out,'6-mobile-map.png')});
await pg.locator('[data-go="tune"]:visible').first().click();
await pg.waitForTimeout(300);
await pg.screenshot({path:join(out,'7-mobile-tune.png')});
await ctx.close();
await br.close(); server.close();
console.log('shots written');
