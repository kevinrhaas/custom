// Local regression tests. Generates an ephemeral key and replaces only the
// browser's config response; the repository's production invite key is untouched.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { webcrypto } from 'node:crypto';
import { readFile, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const base = (process.env.ALBUM_TEST_URL || 'http://127.0.0.1:8765/memories/').replace(/\/?$/, '/');
if (!['localhost', '127.0.0.1'].includes(new URL(base).hostname)) throw new Error('Run fixture-key tests against a local preview only.');
const shots = process.env.QA_SHOTS || '/tmp/memories-tagging-qa';
await mkdir(shots, { recursive: true });
const pair = await webcrypto.subtle.generateKey({name:'ECDSA', namedCurve:'P-256'}, true, ['sign','verify']);
const publicKey = Buffer.from(await webcrypto.subtle.exportKey('spki', pair.publicKey)).toString('base64');
const privateKey = Buffer.from(await webcrypto.subtle.exportKey('pkcs8', pair.privateKey)).toString('base64');
const browser = await chromium.launch({ headless:true, executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium', args:['--no-sandbox'] });
const failures = [];
const reports = [];

async function visible(page, selector) { await page.locator(selector).first().waitFor({state:'visible'}); }
async function hidden(page, selector) { await page.locator(selector).waitFor({state:'hidden'}); }
async function noOverflow(page, label) {
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth + 1), false, label + ' has horizontal page overflow');
}
async function checked(page, selector, attribute, expected) {
  await page.waitForFunction(({selector,attribute,expected})=>document.querySelector(selector)?.getAttribute(attribute) === expected, {selector,attribute,expected});
}
function zipNames(bytes) {
  const names=[];
  for(let i=0;i<bytes.length-46;i++) if(bytes.readUInt32LE(i) === 0x02014b50) {
    const nameSize=bytes.readUInt16LE(i+28), extraSize=bytes.readUInt16LE(i+30), commentSize=bytes.readUInt16LE(i+32);
    names.push(bytes.subarray(i+46,i+46+nameSize).toString('utf8'));
    i += 45+nameSize+extraSize+commentSize;
  }
  return names;
}

try {
  for (const viewport of [{width:390,height:780},{width:1280,height:800}]) {
    const context=await browser.newContext({viewport,reducedMotion:'reduce',acceptDownloads:true});
    context.setDefaultTimeout(10000);
    const page=await context.newPage();
    const errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await context.route('**/memories/js/config.js', async route=>{
      const response=await route.fetch();
      const source=await response.text();
      assert.match(source,/publicKey:\s*'[^']*'/);
      await route.fulfill({response,body:source.replace(/publicKey:\s*'[^']*'/,`publicKey: '${publicKey}'`)});
    });
    const published={version:1,photos:{'june-baby-1925':{tags:['QA-only-object'],people:['QA Person']}}};
    await context.route('**/memories/data/tags.json',route=>route.fulfill({json:published}));
    try {
      console.log('Testing viewport',viewport.width);
      await page.goto(base,{waitUntil:'networkidle'});
      await visible(page,'.gate');
      await noOverflow(page,'Invite gate');
      await page.goto(new URL('admin/',base).href,{waitUntil:'networkidle'});
      await page.locator('#adminKey').fill(privateKey);
      await page.locator('#unlockBtn').click();
      await visible(page,'#makeCard');
      await page.locator('#who').fill('Local QA fixture');
      await page.locator('#makeForm button[type="submit"]').click();
      await visible(page,'#result');
      const invite=await page.locator('#resultLink').inputValue();
      assert.ok(new URL(invite).searchParams.get('invite'));
      // Clear the earlier grant so this visit consumes a signed test invite.
      await page.evaluate(()=>localStorage.removeItem('memories.access'));
      await page.goto(invite,{waitUntil:'networkidle'});
      await hidden(page,'.gate');
      await visible(page,'[data-play="all"]');
      await noOverflow(page,'Home');
      assert.ok(!new URL(page.url()).searchParams.has('invite'));
      await page.screenshot({path:resolve(shots,`home-${viewport.width}.png`),fullPage:false,timeout:30000});

      console.log('Testing viewer');
      await page.locator('.moment-img[data-open]').click();
      await visible(page,'#viewer');
      const firstTitle=await page.locator('#vTitle').innerText();
      await page.keyboard.press('ArrowRight');
      assert.notEqual(await page.locator('#vTitle').innerText(),firstTitle);
      await page.keyboard.press('ArrowLeft');
      assert.equal(await page.locator('#vTitle').innerText(),firstTitle);
      await page.locator('[data-v="fav"]').click();
      await checked(page,'[data-v="fav"]','aria-pressed','true');
      await page.locator('[data-v="zoom"]').click();
      await checked(page,'[data-v="zoom"]','aria-pressed','true');
      await page.keyboard.press('Escape');
      await checked(page,'[data-v="zoom"]','aria-pressed','false');
      await page.goBack();
      await hidden(page,'#viewer');

      console.log('Testing slideshow');
      await page.locator('[data-play="all"]').click();
      await visible(page,'#show');
      await page.locator('[data-s="toggle"]').click();
      assert.equal(await page.locator('.s-toggle-label').innerText(),'Play');
      const firstSlide=await page.locator('#sCaption').innerText();
      await page.locator('[data-s="next"]').click();
      assert.notEqual(await page.locator('#sCaption').innerText(),firstSlide);
      await page.locator('[data-s="close"]').click();
      await hidden(page,'#show');

      console.log('Testing preferences');
      await page.locator('#lookButton:visible, [data-look]:visible').click();
      await visible(page,'#lookSheet');
      for(const [size,pixels] of [['regular','18px'],['large','21px'],['xl','24px']]) {
        await page.locator(`button[data-text="${size}"]`).click();
        await page.waitForFunction(expected=>getComputedStyle(document.documentElement).fontSize === expected,pixels);
        assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).fontSize),pixels);
      }
      for(const mode of ['dark','light']) {
        await page.locator(`button[data-mode="${mode}"]`).click();
        await checked(page,'html','data-scheme',mode);
      }
      await page.locator('button[data-text="regular"]').click();
      await page.locator('[data-close-sheet]').click();
      await hidden(page,'#lookSheet');

      console.log('Testing search');
      await page.goto(base+'#/search?q=horse',{waitUntil:'networkidle'});
      await visible(page,'#results [data-open]');
      assert.match(await page.locator('#resultCount').innerText(),/photo/);
      await noOverflow(page,'Search');
      for(const query of ['QA-only-object','QA Person','Where it all began']) {
        await page.goto(base+'#/search?q='+encodeURIComponent(query),{waitUntil:'networkidle'});
        await visible(page,'#results [data-open]');
        assert.ok(await page.locator('#results [data-open="june-baby-1925"]').count(),query+' should find the matching photo');
      }
      await page.goto(base+'#/years',{waitUntil:'networkidle'});
      await visible(page,'[data-decade]');
      await noOverflow(page,'Years');

      // A chapter must yield exactly one ZIP containing only its own photos.
      console.log('Testing ZIP');
      const library=await (await context.request.get(new URL('data/library.json',base).href)).json();
      const chapter=library.chapters[0];
      const expected=library.photos.filter(photo=>photo.chapter === chapter.id);
      await page.goto(base+'#/chapter/'+chapter.id,{waitUntil:'networkidle'});
      await visible(page,'[data-zip="chapter"]');
      const downloads=[];
      page.on('download',download=>downloads.push(download));
      const downloadWait=page.waitForEvent('download');
      await page.locator('[data-zip="chapter"]').click();
      const download=await downloadWait;
      const names=zipNames(await readFile(await download.path()));
      assert.equal(names.length,expected.length,'ZIP should contain only the chosen chapter');
      assert.deepEqual(names.sort(),expected.map(photo=>photo.downloadName || photo.title+'.jpg').sort());
      await page.waitForTimeout(250);
      assert.equal(downloads.length,1,'Save all must trigger exactly one download');

      console.log('Testing tagging');
      // Suggestions are unapproved until explicitly reviewed; exports contain
      // approved additions only and never AI provenance or face descriptors.
      await page.goto(new URL('admin/',base).href,{waitUntil:'networkidle'});
      await visible(page,'[data-tag-controls]');
      await noOverflow(page,'Tagging admin');
      const draftId='walter-frank-fence-1930';
      const suggestion={version:1,photos:{[draftId]:{tags:['Ferris wheel'],caption:'A draft to review.'},'unknown-id':{tags:['Skip me']}},provenance:{[draftId]:{sha256:'not-published'}}};
      await page.locator('#tagDraftFile').setInputFiles({name:'drafts.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(suggestion))});
      await page.waitForFunction(()=>document.querySelector('[data-tag-status]').textContent.includes('drafts imported'));
      const exportJSON=async()=>{
        const next=page.waitForEvent('download');
        await page.locator('[data-tag-export]').click();
        return JSON.parse(await readFile(await (await next).path(),'utf8'));
      };
      assert.deepEqual(await exportJSON(),published,'Importing AI drafts must not approve them');
      await page.locator('#tagPhoto').selectOption(draftId);
      assert.equal(await page.locator('#tagCaption').inputValue(),'A draft to review.');
      await page.locator('#tagLabels').fill('Ferris wheel, family picnic');
      await page.locator('#tagPeople').fill('Confirmed June');
      await page.locator('#tagCaption').fill('The family at the fair.');
      // Edits survive a reload but are still drafts.
      await page.reload({waitUntil:'networkidle'});
      await visible(page,'[data-tag-controls]');
      await page.locator('#tagPhoto').selectOption(draftId);
      assert.equal(await page.locator('#tagPeople').inputValue(),'Confirmed June');
      assert.deepEqual(await exportJSON(),published);
      await page.locator('[data-tag-form] button[type="submit"]').click();
      const approved=await exportJSON();
      assert.deepEqual(approved.photos[draftId],{tags:['Ferris wheel','family picnic'],people:['Confirmed June'],caption:'The family at the fair.'});
      assert.deepEqual(Object.keys(approved).sort(),['photos','version']);
      assert.ok(!Object.hasOwn(approved.photos,'unknown-id'));
      assert.deepEqual(approved.photos['june-baby-1925'],published.photos['june-baby-1925']);
      await page.screenshot({path:resolve(shots,`tagging-${viewport.width}.png`),fullPage:false,timeout:30000});
      page.once('dialog',dialog=>dialog.accept());
      await page.locator('[data-tag-clear]').click();
      assert.deepEqual(await exportJSON(),published,'Clearing local work restores the published baseline');
      await page.locator('#tagApprovedFile').setInputFiles({name:'tags.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(approved))});
      await page.waitForFunction(()=>document.querySelector('[data-tag-status]').textContent.includes('approved additions restored'));
      assert.deepEqual(await exportJSON(),approved);
      assert.deepEqual(errors,[]);
      reports.push({viewport,passed:['gate','admin unlock and signed invite','home','viewer keys, love, zoom, back','slideshow','text sizes and color modes','search incl. published tags, people and chapter','years','chapter ZIP','AI draft import remains unapproved','draft reload persistence','individual approval and exact export','clear and restore approved metadata'],pageErrors:errors});
    } catch(error) {
      console.error('Failed viewport', viewport.width, error.message);
      failures.push({viewport,error:error.stack,pageErrors:errors});
      await page.screenshot({path:resolve(shots,`failure-${viewport.width}.png`),fullPage:false,timeout:30000}).catch(()=>{});
    } finally { await context.close(); }
  }
} finally { await browser.close(); }
console.log(JSON.stringify({reports,failures,screenshots:shots},null,2));
if(failures.length) process.exitCode=1;
