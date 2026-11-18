// Focused regression for the real Kevin-and-Lee album copy. Read the actual
// shared settings; only the photo source and invite key are replaced locally.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { readFile, mkdir } from 'node:fs/promises';
import { webcrypto } from 'node:crypto';
import { installConfigFixture } from './settings-test-fixture.mjs';
const { chromium } = createRequire(import.meta.url)('playwright');
const base = (process.env.ALBUM_TEST_URL || 'http://127.0.0.1:8765/memories/').replace(/\/?$/, '/');
if (!['localhost','127.0.0.1'].includes(new URL(base).hostname)) throw new Error('Use a local preview for fixture-key browser tests.');
const published = JSON.parse(await readFile(new URL('../../site/memories/data/settings.json', import.meta.url), 'utf8'));
assert.equal(published.settings.title, 'Our Life in Pictures');
assert.deepEqual(published.settings.honorees, [{name:'Kevin',years:''},{name:'Lee',years:''}]);
const unwanted = /in loving memory|\bmemorial\b|grandkids|grandchildren|\b(?:18|19|20)\d{2}\b/i;
assert.doesNotMatch(published.settings.dedication, unwanted);
const fixture = structuredClone(published);
Object.assign(fixture.settings, {source:'manifest',sample:true,drive:{apiKey:'',folderId:''}});
const pair = await webcrypto.subtle.generateKey({name:'ECDSA',namedCurve:'P-256'},true,['sign','verify']);
const publicKey = Buffer.from(await webcrypto.subtle.exportKey('spki',pair.publicKey)).toString('base64');
const privateKey = Buffer.from(await webcrypto.subtle.exportKey('pkcs8',pair.privateKey)).toString('base64');
const payload = Buffer.from(JSON.stringify({v:1,label:'A friend',iat:Date.now(),exp:0,jti:'living-couple-qa'})).toString('base64url');
const signature = Buffer.from(await webcrypto.subtle.sign({name:'ECDSA',hash:'SHA-256'},pair.privateKey,new TextEncoder().encode(payload))).toString('base64url');
const invite = `${base}?invite=${payload}.${signature}`;
const shots = process.env.LIVING_COUPLE_QA_SHOTS || '/tmp/memories-living-couple-qa';
await mkdir(shots,{recursive:true});
const browser = await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium',args:['--no-sandbox']});
const reports=[];
try {
  for (const viewport of [{width:390,height:780},{width:1280,height:800}]) {
    const context=await browser.newContext({viewport,reducedMotion:'reduce',serviceWorkers:'block',colorScheme:viewport.width===390?'light':'dark'});
    context.setDefaultTimeout(15000);
    await installConfigFixture(context,publicKey,()=>fixture);
    const page=await context.newPage();
    const errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    try {
      await page.goto(base,{waitUntil:'networkidle'});
      await page.locator('.gate').waitFor({state:'visible'});
      assert.equal(await page.title(),published.settings.title);
      assert.deepEqual(await page.locator('.gate-name').allTextContents(),['Kevin','Lee']);
      assert.equal(await page.locator('.gate-years').count(),0);
      assert.equal(await page.locator('.gate-kicker').innerText(),'Our story, so far');
      assert.doesNotMatch(await page.locator('.gate').innerText(),unwanted);
      const defaults=await page.evaluate(async()=>{
        const {DEFAULT_SETTINGS}=await import('./js/config.js');
        return {title:DEFAULT_SETTINGS.title,honorees:DEFAULT_SETTINGS.honorees,dedication:DEFAULT_SETTINGS.dedication};
      });
      assert.deepEqual(defaults,{title:published.settings.title,honorees:published.settings.honorees,dedication:published.settings.dedication},'bootstrap fallback keeps the same living-couple copy');
      await page.screenshot({path:`${shots}/gate-${viewport.width}.png`,fullPage:false});

      await page.goto(invite,{waitUntil:'networkidle'});
      await page.locator('.hero').waitFor({state:'visible'});
      assert.match(await page.locator('.hero-names').innerText(),/Kevin\s*&\s*Lee/);
      assert.equal(await page.locator('.hero-years').count(),0,'blank years produce no empty lifespan row');
      assert.equal(await page.locator('.hero-dedication').innerText(),published.settings.dedication);
      assert.doesNotMatch(await page.locator('.hero').innerText(),unwanted);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
      await page.screenshot({path:`${shots}/home-${viewport.width}.png`,fullPage:false});

      await page.goto(new URL('admin/',base).href,{waitUntil:'networkidle'});
      await page.locator('#adminKey').fill(privateKey);
      await page.locator('#unlockBtn').click();
      await page.locator('#settingsCard').waitFor({state:'visible'});
      await page.locator('#albumTitleInput').waitFor({state:'visible'});
      assert.match(await page.locator('#settingsCard').innerText(),/Names on the album/);
      assert.match(await page.locator('#settingsCard').innerText(),/Welcome message/);
      assert.doesNotMatch(await page.locator('#settingsCard').innerText(),/in loving memory|\bmemorial\b|grandkids|grandchildren|People the album remembers/i);
      assert.deepEqual(await page.locator('[data-honoree-name]').evaluateAll(inputs=>inputs.map(input=>input.value)),['Kevin','Lee']);
      assert.deepEqual(await page.locator('[data-honoree-years]').evaluateAll(inputs=>inputs.map(input=>input.value)),['','']);
      assert.equal(await page.locator('#albumDedicationInput').inputValue(),published.settings.dedication);
      assert.deepEqual(errors,[]);
      reports.push({viewport,colorScheme:viewport.width===390?'light':'dark',checks:['actual shared/default Kevin and Lee settings','neutral welcome gate','no lifespan row','living-couple home welcome','neutral admin labels'],pageErrors:errors});
    } finally {await context.close();}
  }
} finally {await browser.close();}
console.log(JSON.stringify({reports,screenshots:shots},null,2));
