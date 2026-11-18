// Public sample data only. Production family settings and invite keys are never
// changed by browser tests; every fixture response is local to its test context.
export function sampleSettingsDocument() {
  return { version: 1, revision: 'qa-sample-settings', settings: {
    title: 'Our Family Album',
    honorees: [{name: 'Walter Hale', years: '1921 – 2019'}, {name: 'June Hale', years: '1924 – 2011'}],
    dedication: 'The family stories, gathered for everyone.',
    keeper: 'Lauren', helper: 'Kevin',
    people: ['Walter', 'June', 'Margaret', 'Robert', 'Eleanor', 'Grandma Rose', 'Uncle Frank', 'Peggy', 'Danny'],
    sample: true, source: 'manifest', drive: { apiKey: '', folderId: '' }, defaultSkin: 'heirloom',
  } };
}

export async function installConfigFixture(context, publicKey, getDocument) {
  await context.route('**/memories/js/config.js', async route => {
    const response = await route.fetch();
    let source = await response.text();
    if (!/publicKey:\s*'[^']*'/.test(source)) throw new Error('Expected the unchanged immutable invite public-key bootstrap.');
    source = source.replace(/publicKey:\s*'[^']*'/, `publicKey: '${publicKey}'`)
      .replace(/sample:\s*(?:true|false)/, 'sample: true')
      .replace(/source:\s*'(?:manifest|drive)'/, "source: 'manifest'")
      .replace(/apiKey:\s*'[^']*'/, "apiKey: ''")
      .replace(/folderId:\s*'[^']*'/, "folderId: ''");
    await route.fulfill({ response, body: source });
  });
  await context.route('**/memories/data/settings.json*', route => route.fulfill({ json: getDocument() }));
}
