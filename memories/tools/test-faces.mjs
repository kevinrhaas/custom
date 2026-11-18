import assert from 'node:assert/strict';
import { descriptorDistance, groupFaces, collectPeople } from '../../site/memories/admin/face-engine.js';
import { matchPhotoFile } from '../../site/memories/admin/faces.js';

assert.equal(descriptorDistance([0, 0], [3, 4]), 5);
assert.equal(descriptorDistance([0], [0, 1]), Infinity);
assert.equal(descriptorDistance([NaN], [1]), Infinity);
const faces = [
  { id: 'a', photoId: '1', descriptor: [0] },
  { id: 'b', photoId: '2', descriptor: [0.4] },
  { id: 'c', photoId: '3', descriptor: [0.8] },
  { id: 'd', photoId: '1', descriptor: [0.05] },
];
const groups = groupFaces(faces, 0.5);
assert.deepEqual(groups.map(group => group.map(face => face.id)), [['a', 'b'], ['c'], ['d']], 'no transitive or same-photo matches');
const names = collectPeople([
  { name: 'June', faces: [{photoId: '1'}, {photoId: '2', name: 'Walter'}, {photoId: '3', excluded: true}] },
  { name: 'june', faces: [{photoId: '1'}] },
  { name: '', faces: [{photoId: '4'}] },
]);
assert.deepEqual(JSON.parse(JSON.stringify(names)), {'1': {people: ['June']}, '2': {people: ['Walter']}});
assert.equal(JSON.stringify(names).includes('descriptor'), false);
assert.equal(matchPhotoFile('Portrait.JPG', [{id:'p1',filename:'portrait.jpg'}]), 'p1');
assert.equal(matchPhotoFile('Portrait.JPG', [{id:'p1',filename:'portrait.jpg'}, {id:'p2',filename:'portrait.jpg'}]), '', 'ambiguous names require a choice');
assert.equal(matchPhotoFile('missing.jpg', [{id:'p1',filename:'portrait.jpg'}]), '');
console.log('Face grouping tests passed: strict clusters, same-photo exclusion, reviewed names, duplicate filenames.');
