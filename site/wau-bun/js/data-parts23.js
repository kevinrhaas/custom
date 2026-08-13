/* Wau-Bun — Parts 2 and 3.
   These carry the part framing plus the real chapter spine (headings exactly as
   they stand in the text). Scene-by-scene detail is built one part at a time;
   Part 1 is complete, these are staged behind it. Nothing here is invented:
   every row is a chapter that exists, under its own heading. */
var WAUBUN_PART2 = {
  id: 'part2',
  number: 2,
  title: 'The Early Frontier',
  range: 'c. 1770s – 1816',
  chapters: 'Chapters XVIII–XXIII',
  status: 'outline',
  blurb: 'The story jumps back to the world that created the Kinzies: the Great Lakes fur trade, Native nations, early settlers, and the beginnings of Chicago. Growing conflict culminates in the War of 1812 and the Fort Dearborn massacre, followed by captivity, survival, and the rebuilding of Fort Dearborn.',
  acts: [],
  scenes: [],
  outline: [
    { chapter: 'XVIII', title: 'Massacre at Chicago' },
    { chapter: 'XIX', title: 'Narrative of the massacre, continued' },
    { chapter: 'XX', title: 'Captivity of J. Kinzie, Sen. — an amusing mistake' },
    { chapter: 'XXI', title: 'A sermon' },
    { chapter: 'XXII', title: 'The captives' },
    { chapter: 'XXIII', title: 'Second-sight — Hickory Creek' }
  ],
  leads: ['eleanor', 'kinziesen', 'margaret', 'billycaldwell']
};

var WAUBUN_PART3 = {
  id: 'part3',
  number: 3,
  title: 'Wau Bun',
  range: '1831 – 1833',
  chapters: 'Chapters XXIV–XXXVIII',
  status: 'outline',
  blurb: 'Juliette\'s story resumes in Chicago. She returns to Fort Winnebago and develops deeper relationships with Ho-Chunk people including Day-kau-ray, Four-Legs, Cut-Nose and White Crow. The Black Hawk War transforms the region, followed by displacement, hunger and upheaval. The series ends with Juliette and John leaving Fort Winnebago, closing the "early day" of the Northwest.',
  acts: [],
  scenes: [],
  outline: [
    { chapter: 'XXIV', title: 'Return to Fort Winnebago' },
    { chapter: 'XXV', title: 'Return journey, continued' },
    { chapter: 'XXVI', title: 'Four-Legs, the dandy' },
    { chapter: 'XXVII', title: 'The Cut-Nose' },
    { chapter: 'XXVIII', title: 'Indian customs and dances' },
    { chapter: 'XXIX', title: 'Story of the Red Fox' },
    { chapter: 'XXX', title: 'Story of Shee-shee-banze' },
    { chapter: 'XXXI', title: 'A visit to Green Bay — Ma-zhee-gaw-gaw swamp' },
    { chapter: 'XXXII', title: 'Commencement of the Sauk war' },
    { chapter: 'XXXIII', title: 'Fleeing from the Indians' },
    { chapter: 'XXXIV', title: 'Fort Howard — our return home' },
    { chapter: 'XXXV', title: 'Surrender of Winnebago prisoners' },
    { chapter: 'XXXVI', title: 'Escape of the prisoners' },
    { chapter: 'XXXVII', title: 'Agathe — Tomah' },
    { chapter: 'XXXVIII', title: 'Conclusion' }
  ],
  leads: ['juliette', 'john', 'daykauray', 'whitecrow', 'youngfourlegs']
};
