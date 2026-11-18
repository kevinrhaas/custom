// Device-local settings and approved tags. All Drive responses and invite keys
// are fixtures. No GitHub account, publishing token, or remote write is used.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { webcrypto } from 'node:crypto';
import { mkdir } from 'node:fs/promises';
import { sampleSettingsDocument, installConfigFixture } from './settings-test-fixture.mjs';
const {chromium}=createRequire(import.meta.url)('playwright');
const base=(process.env.ALBUM_TEST_URL || 'http://127.0.0.1:8765/memories/').replace(/\/?$/,'/');
if(!['localhost','127.0.0.1'].includes(new URL(base).hostname)) throw new Error('Use a local preview for fixture-key browser tests.');
const shots=process.env.SETTINGS_QA_SHOTS || '/tmp/memories-local-settings-qa';
await mkdir(shots,{recursive:true});
const pair=await webcrypto.subtle.generateKey({name:'ECDSA',namedCurve:'P-256'},true,['sign','verify']);
const publicKey=Buffer.from(await webcrypto.subtle.exportKey('spki',pair.publicKey)).toString('base64');
const privateKey=Buffer.from(await webcrypto.subtle.exportKey('pkcs8',pair.privateKey)).toString('base64');
const payload=Buffer.from(JSON.stringify({v:1,label:'Local QA',iat:Date.now(),exp:0,jti:'local-settings-qa'})).toString('base64url');
const signature=Buffer.from(await webcrypto.subtle.sign({name:'ECDSA',hash:'SHA-256'},pair.privateKey,new TextEncoder().encode(payload))).toString('base64url');
const invite=`${base}?invite=${payload}.${signature}`;
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium',args:['--no-sandbox']});
const reports=[],failures=[];
async function installMocks(context,githubRequests,driveRequests) {
  await installConfigFixture(context,publicKey,()=>sampleSettingsDocument());
  await context.route('**/memories/data/tags.json*',route=>route.fulfill({json:{version:1,photos:{}}}));
  await context.route('https://api.github.com/**',route=>{githubRequests.push(route.request().url());return route.abort();});
  await context.route('https://www.googleapis.com/drive/v3/**',route=>{
    const request=route.request(),url=new URL(request.url());
    driveRequests.push(url.pathname);
    assert.equal(request.headers().referer,new URL(base).origin+'/', 'restricted Drive key receives the site origin');
    const headers={'access-control-allow-origin':'*'};
    if(/\/files\/[^/]+$/.test(url.pathname)) return route.fulfill({headers,json:{id:url.pathname.split('/').pop(),name:'Local folder',mimeType:'application/vnd.google-apps.folder'}});
    const parent=/'([^']+)'/.exec(url.searchParams.get('q') || '')?.[1];
    const which=parent==='QA_LOCAL_FOLDER_A'?'A':'B';
    return route.fulfill({headers,json:{files:[{id:'drive-shared-id',name:`2001 - Folder ${which} photo.jpg`,mimeType:'image/jpeg',description:`A photo from folder ${which}.`}]}});
  });
  await context.route(/https:\/\/(?:lh3\.googleusercontent\.com|drive\.google\.com)\//,route=>route.fulfill({contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="#c6b69c"/></svg>'}));
}
async function status(page,selector,pattern) {
  await page.waitForFunction(({selector,pattern})=>new RegExp(pattern,'i').test(document.querySelector(selector)?.textContent || ''),{selector,pattern});
}
async function saveSettings(page) {
  await page.locator('#settingsSave').click();
  await status(page,'[data-settings-status]','^Saved on this device\\.');
}
async function openAdmin(page) {
  await page.goto(new URL('admin/',base).href,{waitUntil:'networkidle'});
  if(await page.locator('#unlockBtn').isVisible()) {
    await page.locator('#adminKey').fill(privateKey);
    await page.locator('#unlockBtn').click();
  }
  await page.locator('#albumTitleInput').waitFor({state:'visible'});
  await page.locator('[data-tag-controls]').waitFor({state:'visible'});
}
async function searchCount(context,query) {
  const page=await context.newPage();
  try {
    await page.goto(base+'#/search?q='+encodeURIComponent(query),{waitUntil:'networkidle'});
    await page.waitForFunction(()=>document.querySelector('#results')?.children.length);
    return await page.locator('#results [data-open]').count();
  } finally {await page.close();}
}
async function saveTags(page) {
  await page.locator('[data-tag-save]').click();
  await status(page,'[data-tag-status]','saved on this device');
}
async function blockStorage(page,prefix='') {
  await page.evaluate(prefix=>{
    window.__qaSetItem=Storage.prototype.setItem;
    Storage.prototype.setItem=function(key,value){if(String(key).startsWith(prefix))throw new DOMException('Fixture storage is full','QuotaExceededError');return window.__qaSetItem.call(this,key,value);};
  },prefix);
}
async function restoreStorage(page) {
  await page.evaluate(()=>{Storage.prototype.setItem=window.__qaSetItem;delete window.__qaSetItem;});
}
try {
  for(const viewport of [{width:390,height:780},{width:1280,height:800}]) {
    const context=await browser.newContext({viewport,reducedMotion:'reduce',serviceWorkers:'block'});
    context.setDefaultTimeout(15000);
    const githubRequests=[],driveRequests=[],errors=[];
    await installMocks(context,githubRequests,driveRequests);
    const page=await context.newPage();page.on('pageerror',error=>errors.push(error.message));
    try {
      console.log(`Testing local settings at ${viewport.width}px`);
      // Existing preferences must not prevent an admin's newly saved look, nor
      // lose the separately chosen dark mode or text size.
      await page.goto(base,{waitUntil:'networkidle'});
      await page.locator('.gate').waitFor({state:'visible'});
      await page.evaluate(()=>localStorage.setItem('memories.prefs',JSON.stringify({skin:'heirloom',mode:'dark',text:'large'})));
      await openAdmin(page);
      assert.equal(await page.locator('#albumTitleInput').isEnabled(),true);
      assert.equal(await page.locator('#settingsSave').isEnabled(),true);
      assert.equal(await page.locator('#publishingToken').count(),0);
      assert.doesNotMatch(await page.locator('#settingsCard').innerText(),/github|publishing token|repository|connect publishing/i);
      await page.locator('#albumTitleInput').fill('');
      await page.locator('#settingsSave').click();
      await status(page,'[data-settings-status]','title');
      const title=`José & June — this device ${viewport.width}`;
      await page.locator('#albumTitleInput').fill(title);
      await page.locator('[data-honoree-name]').first().fill('José Example');
      await page.locator('#albumDedicationInput').fill('A few moments we want to keep.');
      await page.getByText('More settings',{exact:true}).click();
      await page.locator('#albumPeopleInput').fill('José, June, Lauren');
      await page.locator('#albumSkinInput').selectOption('gallery');
      await saveSettings(page);
      const settingsKey=await page.evaluate(async()=> (await import('../js/settings.js')).LOCAL_SETTINGS_KEY);
      const saved=await page.evaluate(key=>JSON.parse(localStorage.getItem(key)),settingsKey);
      assert.equal(saved.settings.title,title);
      assert.deepEqual(saved.settings.people,['José','June','Lauren']);
      assert.ok(!JSON.stringify(saved).includes(privateKey));
      assert.equal(await page.evaluate(()=>document.documentElement.dataset.skin),'gallery');
      await page.reload({waitUntil:'networkidle'});
      await page.locator('#albumTitleInput').waitFor({state:'visible'});
      assert.equal(await page.locator('#albumTitleInput').inputValue(),title);
      await page.goto(base,{waitUntil:'networkidle'});
      await page.locator('.hero').waitFor({state:'visible'});
      assert.equal(await page.title(),title);
      assert.equal(await page.evaluate(()=>document.documentElement.dataset.skin),'gallery');
      assert.equal(await page.evaluate(()=>document.documentElement.dataset.mode),'dark');
      assert.equal(await page.evaluate(()=>document.documentElement.dataset.text),'large');
      await openAdmin(page);
      await blockStorage(page,'memories.settings.local.v1:');
      await page.locator('#albumTitleInput').fill('This edit cannot be saved');
      await page.locator('#settingsSave').click();
      await status(page,'[data-settings-status]','could not save');
      assert.equal(await page.evaluate(key=>JSON.parse(localStorage.getItem(key)).settings.title,settingsKey),title);
      await restoreStorage(page);
      await page.reload({waitUntil:'networkidle'});
      await page.locator('#albumTitleInput').waitFor({state:'visible'});
      assert.equal(await page.locator('#albumTitleInput').inputValue(),title,'failed storage does not claim a durable setting');

      // Approval stages a suggestion; only explicit Save makes it searchable.
      const tagId='walter-frank-fence-1930',draftId='june-baby-1925';
      const tag='LocalReviewHorse',draftTag='UnreviewedSunflower';
      await page.locator('#tagDraftFile').setInputFiles({name:'drafts.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({version:1,photos:{[tagId]:{tags:[tag]},[draftId]:{tags:[draftTag]}}}))});
      await status(page,'[data-tag-status]','drafts imported');
      await page.locator('#tagPhoto').selectOption(tagId);
      await page.locator('[data-tag-form] button[type=submit]').click();
      assert.equal(await searchCount(context,tag),0,'approval alone does not enter search');
      await saveTags(page);
      assert.equal(await searchCount(context,tag),1);
      assert.equal(await searchCount(context,draftTag),0,'unreviewed drafts remain out of search');
      await page.reload({waitUntil:'networkidle'});
      await page.locator('[data-tag-controls]').waitFor({state:'visible'});
      await page.locator('#tagPhoto').selectOption(tagId);
      assert.equal(await page.locator('#tagLabels').inputValue(),tag);
      await page.locator('#tagLabels').fill('UnsavedTagAfterStorageFailure');
      await page.locator('[data-tag-form] button[type=submit]').click();
      await blockStorage(page);
      await page.locator('[data-tag-save]').click();
      await status(page,'[data-tag-status]','could not save|not saved');
      await restoreStorage(page);
      assert.equal(await searchCount(context,'UnsavedTagAfterStorageFailure'),0);
      assert.equal(await searchCount(context,tag),1,'previous saved metadata survives failed Save');

      // Another browser has the published defaults and no private local edits.
      const other=await browser.newContext({viewport,reducedMotion:'reduce',serviceWorkers:'block'});
      await installMocks(other,githubRequests,driveRequests);
      const otherPage=await other.newPage();
      await otherPage.goto(base,{waitUntil:'networkidle'});
      await otherPage.locator('.gate').waitFor({state:'visible'});
      assert.equal(await otherPage.title(),sampleSettingsDocument().settings.title);
      assert.equal(await otherPage.evaluate(()=>document.documentElement.dataset.skin),'heirloom');
      assert.equal(await otherPage.evaluate(key=>localStorage.getItem(key),settingsKey),null);
      await otherPage.goto(invite,{waitUntil:'networkidle'});
      assert.equal(await searchCount(other,tag),0);
      await other.close();

      // Save accepts local Drive settings without a publishing service. The new
      // source mounts immediately, and folder-specific metadata cannot leak.
      await page.locator('#albumSourceInput').selectOption('drive');
      await page.getByText('Connection details',{exact:true}).click();
      await page.locator('#albumApiKeyInput').fill('AIza'+'x'.repeat(35));
      await page.locator('#albumFolderInput').fill('QA_LOCAL_FOLDER_A');
      await saveSettings(page);
      await page.waitForFunction(()=>document.querySelector('#tagPhoto option')?.textContent.includes('Folder A photo'));
      assert.equal(await page.locator('#tagPhoto option').count(),1);
      await page.locator('#tagLabels').fill('FolderOnlyApricot');
      await page.locator('[data-tag-form] button[type=submit]').click();
      await saveTags(page);
      assert.equal(await searchCount(context,'FolderOnlyApricot'),1);
      await page.locator('#albumFolderInput').fill('QA_LOCAL_FOLDER_B');
      await saveSettings(page);
      await page.waitForFunction(()=>document.querySelector('#tagPhoto option')?.textContent.includes('Folder B photo'));
      assert.equal(await page.locator('#tagLabels').inputValue(),'','new folder does not inherit local tags from the old one');
      assert.equal(await searchCount(context,'FolderOnlyApricot'),0);
      await page.locator('#albumSourceInput').selectOption('manifest');
      await saveSettings(page);
      await page.waitForFunction(()=>document.querySelector('#tagPhoto')?.options.length>1);
      assert.equal(await searchCount(context,tag),1,'returning to the sample source restores its separately saved metadata');
      assert.ok(driveRequests.length>0);
      assert.deepEqual(githubRequests,[],'no GitHub authorization, token, or network request is needed');
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
      assert.deepEqual(errors,[]);
      await page.screenshot({path:`${shots}/settings-${viewport.width}.png`,fullPage:false});
      reports.push({viewport,checks:['immediately editable after admin unlock','local settings survive reload','isolated browser keeps published defaults','no GitHub requests','truthful settings and metadata storage failures','saved skin preserves mode/text','approved-only saved tags enter search','Drive source remount and folder-specific tags'],pageErrors:errors});
    } catch(error) {
      failures.push({viewport,error:error.stack,pageErrors:errors});
      console.error(`Local settings QA failed at ${viewport.width}px: ${error.message}`);
      await page.screenshot({path:`${shots}/failure-${viewport.width}.png`,fullPage:false}).catch(()=>{});
    } finally {await context.close();}
  }
} finally {await browser.close();}
console.log(JSON.stringify({reports,failures,screenshots:shots},null,2));
if(failures.length)process.exitCode=1;
