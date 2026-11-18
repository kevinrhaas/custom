// Tests shared publishing against a mock of GitHub's Contents API. No production
// write, real publishing token, real invite key, or real Drive request is used.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { webcrypto } from 'node:crypto';
import { mkdir, readFile } from 'node:fs/promises';
import { sampleSettingsDocument, installConfigFixture } from './settings-test-fixture.mjs';
const { chromium } = createRequire(import.meta.url)('playwright');
const base = (process.env.ALBUM_TEST_URL || 'http://127.0.0.1:8765/memories/').replace(/\/?$/, '/');
if (!['localhost', '127.0.0.1'].includes(new URL(base).hostname)) throw new Error('Use a local preview for fixture-key browser tests.');
const shots = process.env.SETTINGS_QA_SHOTS || '/tmp/memories-settings-qa';
await mkdir(shots, { recursive: true });
const pair = await webcrypto.subtle.generateKey({name:'ECDSA', namedCurve:'P-256'}, true, ['sign','verify']);
const publicKey = Buffer.from(await webcrypto.subtle.exportKey('spki', pair.publicKey)).toString('base64');
const privateKey = Buffer.from(await webcrypto.subtle.exportKey('pkcs8', pair.privateKey)).toString('base64');
const token = 'github_pat_qa_fixture_never_live_0123456789012345678901234567890';
const endpoint = 'https://api.github.com/repos/kevinrhaas/custom/contents/site/memories/data/settings.json';
const metadataEndpoint = endpoint.replace('settings.json','tags.json');
const hash = number => number.toString(16).padStart(40, '0');
const browser = await chromium.launch({headless:true, executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium', args:['--no-sandbox']});
const reports = [];
const failures = [];
async function statusIncludes(page, expression) {
  await page.waitForFunction(source => new RegExp(source, 'i').test(document.querySelector('[data-settings-status]')?.textContent || ''), expression);
}
async function fits(page, label) {
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), false, `${label} overflows horizontally`);
}
try {
  for (const viewport of [{width:390,height:780}, {width:1280,height:800}]) {
    const context = await browser.newContext({viewport,reducedMotion:'reduce',serviceWorkers:'block'});
    context.setDefaultTimeout(15000);
    let publicDocument = sampleSettingsDocument();
    let repositoryDocument = structuredClone(publicDocument);
    let generation = 1;
    let repositorySha = hash(generation);
    let rejectAuth = false;
    const writes = [], metadataWrites = [], requests = [], errors = [];
    let publicMetadata = {version:1,photos:{}};
    let repositoryMetadata = structuredClone(publicMetadata);
    let metadataSha = hash(1000);
    let metadataConflict = false;
    let driveRequests = 0;
    await installConfigFixture(context, publicKey, () => publicDocument);
    await context.route('**/memories/data/tags.json*', route => route.fulfill({json:publicMetadata}));
    await context.route('https://www.googleapis.com/drive/v3/**', route => {
      driveRequests++;
      assert.equal(route.request().headers().referer, new URL(base).origin+'/', 'Drive restriction receives the site origin');
      return route.fulfill({status:404,headers:{'access-control-allow-origin':'*'},json:{error:{code:404,message:'Fixture folder not shared'}}});
    });
    await context.route('https://api.github.com/**', async route => {
      const request = route.request();
      const method = request.method();
      const url = new URL(request.url());
      requests.push({method, path:url.pathname});
      const isMetadata = url.origin + url.pathname === metadataEndpoint;
      assert.ok(isMetadata || url.origin + url.pathname === endpoint, 'publishing target is fixed');
      assert.ok(!request.url().includes(token));
      const headers = {'access-control-allow-origin':'*','access-control-allow-methods':'GET,PUT,OPTIONS','access-control-allow-headers':'authorization,content-type,x-github-api-version,accept'};
      if (method === 'OPTIONS') return route.fulfill({status:204,headers});
      if (rejectAuth || request.headers().authorization !== `Bearer ${token}`) {
        return route.fulfill({status:401,headers,json:{message:`Mock rejected ${token}`}});
      }
      if (method === 'GET') {
        assert.equal(url.searchParams.get('ref'), 'main');
        return route.fulfill({headers,json:{type:'file',encoding:'base64',sha:isMetadata ? metadataSha : repositorySha,content:Buffer.from(JSON.stringify(isMetadata ? repositoryMetadata : repositoryDocument)).toString('base64')}});
      }
      assert.equal(method, 'PUT');
      const body = request.postDataJSON();
      assert.equal(body.branch, 'main');
      const document = JSON.parse(Buffer.from(body.content, 'base64').toString('utf8'));
      if (isMetadata) {
        assert.deepEqual(Object.keys(document).sort(), ['photos','version']);
        assert.ok(!JSON.stringify(document).includes(token));
        assert.ok(!JSON.stringify(document).includes(privateKey));
        if (metadataConflict) {
          metadataConflict=false; metadataSha=hash(1500);
          repositoryMetadata={version:1,photos:{'walter-frank-fence-1930':{tags:['Another keeper tag']}}};
          return route.fulfill({status:409,headers,json:{message:'Concurrent metadata update'}});
        }
        if (body.sha !== metadataSha) return route.fulfill({status:409,headers,json:{message:'Metadata revision changed'}});
        metadataWrites.push(document); repositoryMetadata=structuredClone(document); metadataSha=hash(1000+metadataWrites.length);
        return route.fulfill({headers,json:{content:{sha:metadataSha},commit:{sha:hash(2000+metadataWrites.length)}}});
      }
      assert.deepEqual(Object.keys(document).sort(), ['revision','settings','version']);
      assert.ok(!JSON.stringify(document).includes(token));
      assert.ok(!JSON.stringify(document).includes(privateKey));
      assert.ok(!Object.hasOwn(document.settings, 'access'));
      if (body.sha !== repositorySha) return route.fulfill({status:409,headers,json:{message:'The saved revision changed.'}});
      writes.push(document);
      repositoryDocument = structuredClone(document);
      repositorySha = hash(++generation);
      return route.fulfill({headers,json:{content:{sha:repositorySha},commit:{sha:hash(100+generation)}}});
    });
    const page = await context.newPage();
    page.on('pageerror',error=>errors.push(error.message));
    try {
      console.log(`Testing shared settings at ${viewport.width}px`);
      await page.goto(new URL('admin/',base).href,{waitUntil:'networkidle'});
      await page.locator('#adminKey').fill(privateKey);
      await page.locator('#unlockBtn').click();
      await page.locator('#settingsCard').waitFor({state:'visible'});
      await fits(page,'Settings admin');
      assert.equal(await page.locator('#settingsSave').isDisabled(), true, 'saving needs publishing authorization');

      // Invalid credentials cannot unlock publishing, and provider error text
      // containing credentials must never be reflected in the page.
      await page.locator('#publishingToken').fill('bad-fixture-credential');
      await page.locator('#publishingConnect').click();
      await statusIncludes(page,'rejected|expired|valid');
      assert.equal(await page.locator('#settingsSave').isDisabled(), true);
      assert.ok(!(await page.locator('body').innerText()).includes(token));
      await page.locator('#publishingToken').fill(token);
      await page.locator('#publishingConnect').click();
      await page.waitForFunction(()=>!document.querySelector('#settingsSave').disabled);
      assert.equal(await page.locator('#publishingToken').inputValue(), '');
      assert.equal(await page.locator('#albumTitleInput').inputValue(), repositoryDocument.settings.title);
      const stored = await page.evaluate(()=>JSON.stringify({local:{...localStorage},session:{...sessionStorage}}));
      assert.ok(!stored.includes(token), 'publishing credential is not persisted');

      // A blank required title blocks the write, preserving the last saved doc.
      await page.locator('#albumTitleInput').fill('');
      await page.locator('#settingsSave').click();
      assert.equal(writes.length,0);
      const title = `June & José — shared album ${viewport.width}`;
      await page.locator('#albumTitleInput').fill(title);
      await page.locator('#albumSourceInput').selectOption('drive');
      await page.locator('#settingsSave').click();
      assert.equal(writes.length,0,'invalid Drive settings cannot be saved');
      assert.equal(driveRequests,0,'invalid Drive settings fail before network access');
      await page.locator('#albumApiKeyInput').fill('AIza'+'x'.repeat(35));
      await page.locator('#albumFolderInput').fill('QA_FOLDER_12345');
      await page.locator('#settingsSave').click();
      await statusIncludes(page,'could not be verified');
      assert.equal(writes.length,0,'an unverified new folder cannot replace the album source');
      assert.ok(driveRequests>0);
      await page.locator('#albumApiKeyInput').fill('');
      await page.locator('#albumFolderInput').fill('');
      await page.locator('#albumSourceInput').selectOption('manifest');
      await page.locator('[data-honoree-name]').first().fill('José Example');
      await page.locator('#albumDedicationInput').fill('Our stories, saved for every relative.');
      await page.locator('#albumPeopleInput').fill('José, June, Lauren');
      await page.locator('#settingsSave').click();
      await page.waitForFunction(()=>/saved/i.test(document.querySelector('[data-settings-status]').textContent));
      assert.equal(writes.length,1);
      assert.equal(repositoryDocument.settings.title,title);
      assert.equal(publicDocument.settings.title,'Our Family Album','saved and deployed are distinct states');
      assert.deepEqual(repositoryDocument.settings.people,['José','June','Lauren']);
      assert.notEqual(repositoryDocument.revision,'qa-sample-settings');
      await fits(page,'Saved settings admin');

      // Simulate Pages finishing the publication. A completely separate browser
      // profile sees the shared document; it never receives admin browser state.
      publicDocument = structuredClone(repositoryDocument);
      await page.locator('#settingsCheckLive').click();
      await statusIncludes(page,'published|now live|is live|are live');
      const visitor = await browser.newContext({viewport,reducedMotion:'reduce',serviceWorkers:'block'});
      await installConfigFixture(visitor,publicKey,()=>publicDocument);
      const visitorPage = await visitor.newPage();
      visitorPage.on('pageerror',error=>errors.push(error.message));
      await visitorPage.goto(base,{waitUntil:'networkidle'});
      assert.equal(await visitorPage.title(),title);
      assert.match(await visitorPage.locator('.gate').innerText(),/José Example/);
      assert.equal(await visitorPage.evaluate(()=>localStorage.getItem('memories.adminkey')),null);
      await fits(visitorPage,'Fresh visitor gate');
      await visitor.close();

      // Approved additions save through the same connection. Unreviewed AI
      // drafts are excluded, and pending publication survives a page reload.
      const tagId='walter-frank-fence-1930', draftOnlyId='june-baby-1925';
      await page.locator('#tagDraftFile').setInputFiles({name:'drafts.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({version:1,photos:{[tagId]:{tags:['Approved search object']},[draftOnlyId]:{tags:['Unreviewed object']}}}))});
      await page.waitForFunction(()=>document.querySelector('[data-tag-status]').textContent.includes('drafts imported'));
      await page.locator('#tagPhoto').selectOption(tagId);
      await page.locator('[data-tag-form] button[type=submit]').click();
      await page.locator('[data-tag-save]').click();
      await page.waitForFunction(()=>document.querySelector('[data-tag-status]').textContent.includes('saved for the whole album'));
      assert.equal(metadataWrites.length,1);
      assert.deepEqual(Object.keys(repositoryMetadata.photos),[tagId]);
      assert.equal(publicMetadata.photos[tagId],undefined,'metadata is durably saved before Pages catches up');
      await page.reload({waitUntil:'networkidle'});
      await page.locator('[data-tag-controls]').waitFor({state:'visible'});
      await page.locator('#tagPhoto').selectOption(tagId);
      assert.match(await page.locator('[data-tag-review-state]').innerText(),/Approved/);
      assert.equal(await page.locator('#tagLabels').inputValue(),'Approved search object');
      const backupWait=page.waitForEvent('download');
      await page.locator('[data-tag-export]').click();
      const backup=JSON.parse(await readFile(await (await backupWait).path(),'utf8'));
      assert.deepEqual(backup,repositoryMetadata,'backup retains a pending saved publication after reload');
      await page.locator('#publishingToken').fill(token);
      await page.locator('#publishingConnect').click();
      await page.waitForFunction(()=>!document.querySelector('#settingsSave').disabled);
      await page.locator('#tagLabels').fill('Revised approved object');
      await page.locator('[data-tag-form] button[type=submit]').click();
      await page.locator('[data-tag-save]').click();
      await page.waitForFunction(()=>document.querySelector('[data-tag-status]').textContent.includes('saved for the whole album'));
      assert.equal(metadataWrites.length,2,'a pending first publication does not create a false conflict on the next save');
      await page.reload({waitUntil:'networkidle'});
      await page.locator('[data-tag-controls]').waitFor({state:'visible'});
      page.once('dialog',dialog=>dialog.accept());
      await page.locator('[data-tag-clear]').click();
      const clearedBackupWait=page.waitForEvent('download');
      await page.locator('[data-tag-export]').click();
      const clearedBackup=JSON.parse(await readFile(await (await clearedBackupWait).path(),'utf8'));
      assert.deepEqual(clearedBackup,repositoryMetadata,'clearing local work retains already saved tags while deployment is pending');
      await page.reload({waitUntil:'networkidle'});
      await page.locator('[data-tag-controls]').waitFor({state:'visible'});
      await page.locator('#tagPhoto').selectOption(tagId);
      assert.equal(await page.locator('#tagLabels').inputValue(),'Revised approved object','a second reload retains saved pending tags after clear');
      await page.locator('#publishingToken').fill(token);
      await page.locator('#publishingConnect').click();
      await page.waitForFunction(()=>!document.querySelector('#settingsSave').disabled);
      await page.locator('#tagLabels').fill('Conflicting object');
      await page.locator('[data-tag-form] button[type=submit]').click();
      metadataConflict=true;
      await page.locator('[data-tag-save]').click();
      await page.waitForFunction(()=>/changed|review|conflict/i.test(document.querySelector('[data-tag-status]').textContent));
      assert.equal(metadataWrites.length,2,'metadata conflict does not claim a successful new save');
      assert.equal(metadataConflict,false,'the test exercised a race at PUT, not only a pre-read conflict');
      assert.match(await page.locator('#tagLabels').inputValue(),/Conflicting object/);

      // Another keeper changes the saved document while this form is open.
      repositorySha = hash(++generation);
      repositoryDocument = {...repositoryDocument,revision:'changed-by-another-keeper',settings:{...repositoryDocument.settings,title:'Another keeper’s title'}};
      await page.locator('#albumTitleInput').fill('Unsaved conflicting title');
      await page.locator('#settingsSave').click();
      await statusIncludes(page,'changed|reload|revision');
      assert.equal(writes.length,1,'a stale SHA cannot overwrite shared settings');
      assert.equal(await page.locator('#albumTitleInput').inputValue(),'Unsaved conflicting title','conflict preserves edits for review');
      page.once('dialog',dialog=>dialog.accept());
      await page.locator('#settingsReload').click();
      await page.waitForFunction(()=>document.querySelector('#albumTitleInput').value === 'Another keeper’s title');
      rejectAuth = true;
      await page.locator('#albumTitleInput').fill('Should not be saved');
      await page.locator('#settingsSave').click();
      await statusIncludes(page,'rejected|expired|valid');
      assert.equal(writes.length,1,'revoked credentials cannot report a new save');
      assert.ok(!(await page.locator('body').innerText()).includes(token));
      rejectAuth = false;
      await page.screenshot({path:`${shots}/settings-${viewport.width}.png`,fullPage:false});

      page.once('dialog',dialog=>dialog.accept());
      await page.locator('#lockBtn').click();
      await page.locator('#lockedView').waitFor({state:'visible'});
      assert.equal(await page.evaluate(async()=>{const {publisher}=await import('./publishing.js');return publisher.isConnected();}),false,'locking destroys the in-memory publishing credential');
      assert.equal(await page.locator('#settingsCard').isVisible(),false);
      assert.ok(!(await page.evaluate(()=>JSON.stringify({local:{...localStorage},session:{...sessionStorage}}))).includes(token));
      assert.deepEqual(errors,[]);
      reports.push({viewport,writes:writes.length,checks:['approved metadata shared save and pending reload','Drive validation blocks invalid source','authorized shared save','Unicode metadata','separate visitor loads published JSON','saved versus published state','required fields','stale revision conflict','credential failures','token not stored or published','lock disconnect','no horizontal overflow'],pageErrors:errors});
    } catch (error) {
      failures.push({viewport,error:error.stack,pageErrors:errors});
      console.error(`Settings QA failed at ${viewport.width}px: ${error.message}`);
      await page.screenshot({path:`${shots}/failure-${viewport.width}.png`,fullPage:false}).catch(()=>{});
    } finally { await context.close(); }
  }
} finally { await browser.close(); }
console.log(JSON.stringify({reports,failures,screenshots:shots},null,2));
if (failures.length) process.exitCode=1;
