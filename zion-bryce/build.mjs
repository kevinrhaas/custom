import { cp, mkdir, readdir, rm } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = dirname(fileURLToPath(import.meta.url));
const sourceRoot = join(projectRoot, 'src');
const destinationRoot = join(dirname(projectRoot), 'site', 'zion-bryce');

const sourceFiles = (await readdir(sourceRoot, { withFileTypes: true }))
  .filter((entry) => entry.isFile())
  .map((entry) => entry.name)
  .sort();

await rm(destinationRoot, { recursive: true, force: true });
await mkdir(destinationRoot, { recursive: true });
await Promise.all(sourceFiles.map((file) => cp(join(sourceRoot, file), join(destinationRoot, file))));

console.log(`Built site/zion-bryce/ from ${sourceFiles.length} source files.`);
