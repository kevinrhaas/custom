/* Wau-Bun — Part 3: Wau Bun (1831–1833), chapters XXIV–XXXVIII.
   Being built the same way Parts 1 and 2 were: read the chapters, break them
   into scenes, name who is in each one. `scenes` covers the chapters done so
   far; `outline` lists the chapters still to be broken up, exactly as they
   stand in the narrative. The app shows both, and says which is which. */
var WAUBUN_PART3 = {
  id: 'part3',
  number: 3,
  title: 'Wau Bun',
  range: '1831 – 1833',
  chapters: 'Chapters XXIV–XXXVIII',
  status: 'partial',
  blurb: 'Juliette\'s story resumes in Chicago. She returns to Fort Winnebago and develops deeper relationships with Ho-Chunk people including Day-kau-ray, Four-Legs, Cut-Nose and White Crow. The Black Hawk War transforms the region, followed by displacement, hunger and upheaval. The series ends with Juliette and John leaving Fort Winnebago, closing the "early day" of the Northwest.',
  outlineNote: 'Scenes so far cover chapters XXIV–XXVI. The chapters below are next, and are listed here exactly as they stand in the narrative.',
  acts: [
    { id: 'c1', title: 'The Road Home', sub: 'Chicago → the Portage', note: 'Spring 1831' },
    { id: 'c2', title: 'The Agency', sub: 'Fort Winnebago', note: '1831' }
  ],
  scenes: [
    /* ---------------- Act 1 — The Road Home ---------------- */
    {
      id: 'p3s1', act: 'c1', chapter: 'XXIV', chapterTitle: 'Return to Fort Winnebago',
      title: 'Masks of brown linen', date: 'Spring 1831',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'With the family seen safely aboard the Napoleon, the Kinzies turn for home. Travelling with them are Josette, a bright bound-girl of ten — daughter of Ouilmette and a Potawatomi mother, lately at the St. Joseph mission school — and Harry, the boy brought up from Kentucky, whose position on crossing into a free state became that of an indentured servant, and who, told to choose his own guardian, looked round the parlour and picked Master John. Three women are going: the mother, Mrs. Helm and Juliette. Against the sun and the prairie wind Juliette has made each of them a mask of brown linen fitted to the face, with eyebrows, lashes and a ring around the mouth worked in black silk, gathered under the chin and tied above and below. Nothing more hideous can be imagined, and the competition is over who shall be called ugliest.',
      points: [
        'Billy Caldwell, Robert Kinzie and Gholson Kercheval ride out with them as far as the Aux Plaines.',
        'Their mother, at sixty, gives her place in the carriage to anyone who wants it — she has travelled so many years on horseback that any other way tires her — and mounts a pacer with the activity of a girl of sixteen.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'josettegirl', 'harry', 'edwin', 'billycaldwell', 'robert', 'gholson', 'petaille', 'lecuyer'], offstage: ['ouilmette'], pivotal: true
    },
    {
      id: 'p3s2', act: 'c1', chapter: 'XXIV', chapterTitle: 'Return to Fort Winnebago',
      title: '"Manitou!"', date: 'First day out',
      place: 'Barney Lawton\'s, the Aux Plaines', placeShort: 'Lawton\'s',
      summary: 'There is nobody at Lawton\'s but a Frenchman and a few Indians. The two women dismount and walk in at the open door, and two men sitting on the floor smoking look up into the masks. One of them lets his pipe fall. Their eyes start; they raise their open hands as if to wave the thing away, and say slowly, "Manitou" — a spirit. The masks come up, the faces underneath are recognised, and the cry that follows is pure delight: "Bon-jour, bon-jour, Maman!" They plunge straight out of doors to tell the others what has happened.',
      points: ['The afternoon\'s ride is over empty prairie under wheeling flocks of curlew, whose shrieking "crack, crack, crack — rackety, rackety, rackety" becomes almost unbearable at close range.'],
      cast: ['juliette', 'margaret', 'john', 'eleanor'], offstage: [], pivotal: false
    },
    {
      id: 'p3s3', act: 'c1', chapter: 'XXIV', chapterTitle: 'Return to Fort Winnebago',
      title: 'The horses that came back on their own', date: 'Second morning',
      place: 'A wooded knoll on the prairie', placeShort: 'The prairie',
      summary: 'They camp on a knoll so covered in flowers that nobody can bear to fell a tree among them, with the hickory and sassafras in bud and the birds going at full strength. The children are in ecstasies and make themselves useful piling saddles and breaking boughs. In the morning the Frenchmen go for the horses and do not come back; the day wears on, searchers return wet to the knees with dew and no news. Could the Indians have stolen them? Hardly — these people rarely rob in peacetime, and never this family. A council sends Grignon back to Chicago for fresh horses. An hour after he leaves, the missing animals come hopping demurely out of a point of woods every searcher swore he had been through twice, and seem rather surprised to be scolded instead of patted.',
      points: ['Half an hour to strike the tent, pack the mats and kettles and saddle up — the camp routine of Part 1, now second nature.'],
      cast: ['juliette', 'john', 'harry', 'josettegirl', 'edwin', 'petaille', 'lecuyer', 'eleanor', 'margaret', 'foster'], offstage: ['gholson'], pivotal: false
    },
    {
      id: 'p3s4', act: 'c1', chapter: 'XXIV', chapterTitle: 'Return to Fort Winnebago',
      title: 'The bed of yellow clay', date: 'Second day',
      place: 'The Fox River', placeShort: 'Fox River',
      summary: 'At the Fox the question is not the depth but the bottom. Three riders cross to test it and find it firm until near the far bank, where it yields a little — one more step and they are on dry ground. "Est-il beau?" calls John, driving. Come just here, it is perfectly good. No — go a little farther down, see the white gravel, it will be firmer. He takes the second advice, and one step short of the bank both horses go down until little more than their backs show. The white gravel is a bed of treacherous yellow clay gleaming up through the water. The horses fight the harness, nearly suffocating; he springs out on the pole and calls for a knife, and Juliette is back in the water handing him hers from the scabbard at her neck.',
      points: [
        '"Whatever you do, don\'t cut the traces," calls his mother.',
        'A plunge rears one horse nearly over backwards with him between them; he comes up out of the mud, and Harry goes out along the pole and cuts the head-couplings with his jack-knife.',
        'The freed horses wrench the pole apart, carry it off across the river in triumph, and stand on the far bank waiting to see what will be done next. Margaret, hauled out of the wagon, goes into a fit of the ague — cured, homoeopathically, by a rattlesnake gliding within three inches of her mother\'s feet.'
      ],
      cast: ['john', 'juliette', 'harry', 'eleanor', 'margaret', 'edwin', 'petaille', 'lecuyer'], offstage: [], pivotal: true
    },
    {
      id: 'p3s5', act: 'c1', chapter: 'XXIV', chapterTitle: 'Return to Fort Winnebago',
      title: 'Why the little rail has a hollow back', date: 'That evening',
      place: 'Crystal Lake', placeShort: 'Crystal Lake',
      summary: 'The delays leave only a short ride, ending at a lake whose surface is covered with loons and poules d\'eau. The Indians, Juliette observes, have Aesop\'s genius for animal character, and a story for every peculiarity of every creature. Nan-nee-bo-zho, the spirit whose business is punishing what is amiss, calls a flock of ducks ashore to be taught to dance. Inside the lodge he hangs an open-mouthed sack at his shoulders, rings them round him, and tells them to shut their eyes tight — anyone who opens them will have something dreadful happen. He plays his flute. The music keeps stopping, and each time there is a smothered "qu-a-a-ck." One small duck risks one eye, sees him stooping to throttle the nearest bird and stuff it into the bag, edges toward the door and screams the warning.',
      points: [
        'She got out with his hand already on her back, and saved her life at the cost of her beauty: ever since, the little rail carries the shape she was forced into — back pressed hollow, neck stretched forward.',
        'This is the first of the Ho-Chunk stories Juliette sets down, and the pattern for the ones that follow: a moral, an animal, and a debt that shows in the body.'
      ],
      cast: ['juliette'], offstage: [], pivotal: false
    },
    {
      id: 'p3s6', act: 'c1', chapter: 'XXV', chapterTitle: 'Return journey, continued',
      title: 'The fawn, and the soldiers\' camp', date: 'Third day',
      place: 'Toward Big-foot Lake', placeShort: 'Big-foot Lake',
      summary: 'A day without a single mishap: balmy air, fresh forest, clear brooks. Stopping at noon at the edge of a thicket they are startled by a bleating, and a dappled fawn breaks through the branches looking for its mother, so unacquainted with man that it is not frightened of them at all — until the children\'s delight sends it bounding back into the woods and ends all hope of a pet. Toward sunset they come over a ridge above an oak-opening where the soldiers\' cattle and horses are browsing, white tents pitched by a clear stream, and the camp-fires already lit. Lieutenant Foster comes out delighted and rejoins their mess for as long as the two parties travel together.',
      points: [
        'Mrs. Gardiner, the hospital matron, brings over a kettle of fresh milk, and supper is a cheerful business.',
        'None of Foster\'s party knows the road, so from here the Kinzies undertake to blaze a tree or set up a chip at every doubtful place — and later plant cut sticks with a cross-piece through a cleft as guide-boards.'
      ],
      cast: ['juliette', 'john', 'foster', 'gardiner', 'eleanor', 'margaret', 'edwin', 'josettegirl'], offstage: [], pivotal: false
    },
    {
      id: 'p3s7', act: 'c1', chapter: 'XXV', chapterTitle: 'Return journey, continued',
      title: 'Hauling the carriage out of Big-foot\'s village', date: 'Fourth day',
      place: 'Big-foot Lake', placeShort: 'Big-foot village',
      summary: 'They come by a sudden turn on the lake the French call Gros-pied and the Ho-Chunk Maunk-suck — bold hills jutting into blue water, a gravelled beach, neat wigwams and gardens on a rise beneath a bluff. The whole party shouts at the sight of it. The villagers, who have watched them come for miles, are drawn up in front of the lodges to meet whatever this is; Shaw-nee-aw-kee and his mother — known through the tribe as "Our friend\'s wife" — are welcomed warmly. The village sits in an amphitheatre of hills so steep that getting a four-wheeled carriage out of it looks impossible. Juliette goes up first, clinging round Jerry\'s neck, almost perpendicularly up the dry bed of a torrent full of loose stones. Then the horses are taken out, the luggage carried up on young men\'s shoulders, ropes made fast to the sides, and a whole bevy of Potawatomi headed by the two Frenchmen haul while others hold it from behind.',
      points: [
        'Shouting, clapping from both sexes, one or two wavering moments when carriage and men look like going over backwards — and then the table-land, and everyone paid to their satisfaction.',
        'Juliette spends the visit constructing a romance around a young man in a lemon-yellow shirt with one blue legging and one scarlet, carrying a flute — the recognised signs of a man in love who is not being refused.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'bigfoot', 'petaille', 'lecuyer'], offstage: ['shawbeenay', 'billycaldwell', 'robinson', 'wolcott'], pivotal: true
    },
    {
      id: 'p3s8', act: 'c1', chapter: 'XXV', chapterTitle: 'Return journey, continued',
      title: 'Kosh-ko-nong: the lake we live on', date: 'Fifth day',
      place: 'Man-Eater\'s village, Kosh-ko-nong', placeShort: 'Kosh-ko-nong',
      summary: 'A morning of forest so tangled that Grignon and Lecuyer go ahead with axes, then low prairie cut by deep narrow channels that the carriage must be pushed and pulled across. The wooded banks of the Kosh-ko-nong were never more welcome. Five or six miles through oak openings bring them to Man-Eater\'s village — neat bark wigwams with wide fields of corn, beans and squashes just planted and already promising. They are among their own people again, and an arrangement is made to cross half a mile above. The party goes over by canoe, the horses swim, and the carriage is stood inside two long canoes lashed side by side and ferried across, swaying enough to draw a shout from the bank each time.',
      points: [
        'Kosh-ko-nong means "the lake we live on" — a name Juliette says is made doubly affecting by what later became of the people who lived on it.',
        'Half a mile on is a swamp two to three feet deep. John comes back in duck trousers, barefoot, to carry his wife across on his shoulders; Petaille takes his mother and a tall Ho-Chunk named To-shun-nuck takes Margaret. Juliette alone takes off her own boots and stockings first, is laughed at for it, and is the only one who rides on dry-shod.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'petaille', 'lecuyer'], offstage: [], pivotal: false
    },
    {
      id: 'p3s9', act: 'c1', chapter: 'XXV', chapterTitle: 'Return journey, continued',
      title: 'The Twenty-mile Prairie, and home', date: 'Sixth day',
      place: 'The Portage', placeShort: 'Fort Winnebago',
      summary: 'The last morning is the hardest: the Twenty-mile Prairie under a sun making up for two months of seclusion, no tree, no living thing, no stream to answer the thirst, and no way to carry an umbrella on horseback. Their mother\'s energy holds her in the saddle until this day and then gives out, and she takes the wagon. Knoll after knoll rises and shows nothing. Take courage — very soon you will begin to see the timber. Another hour. Now, from the rising ground just ahead, look sharp. Nothing. Then a whoop from Shaw-nee-aw-kee: "Le voilà!" — a faint blue strip on the horizon that grows until the fatigue is gone. Hastings\'s Woods, Duck Creek (crossed now without the ice that dumped her in it in March), and a four-mile ride bringing them to the fort with the sun throwing its last light over the landscape.',
      points: [
        'Margaret, on the perverse little Brunet, is carried out of her depth and rides it out perched on top of the saddle with her feet drawn up, steering him to shore.',
        'They are taken straight to Major Twiggs\'s roof by the friends waiting at the ferry.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'edwin', 'petaille', 'lecuyer', 'twiggs'], offstage: ['foster'], pivotal: true
    },

    /* ---------------- Act 2 — The Agency ---------------- */
    {
      id: 'p3s10', act: 'c2', chapter: 'XXVI', chapterTitle: 'Four-Legs, the dandy',
      title: 'A very grand name for a very small concern', date: 'Summer 1831',
      place: 'The Agency, Fort Winnebago', placeShort: 'The Agency',
      summary: 'The First Infantry is ordered to the Mississippi as soon as the Fifth relieves it, and since many of the incoming officers are married, every quarter in the fort will be wanted. So, despite Major Twiggs pressing them to stay, the Kinzies set up at "the Agency" — a laughably grand name for what it is. Washington promised a comfortable house as soon as Congress appropriated for it, and Congress has now ignored them for two sessions. What they have is the old log barracks, taken down and re-erected on the little hill opposite the fort, with dairy, stable and smoke-house of tamarack logs from the swamp: four rooms in a row, none opening into another, each with its own door to the outside, one small window cut through the logs front and back.',
      points: [
        'Mats on the floor, the piano in its place and a few pictures on the logs make it homelike — until the first heavy rain finds the crevices, and everything that can be spoiled goes up into what they dignify with the name of attic.',
        'The greatest inconvenience is having to wear a straw bonnet all day going from bedroom to parlour to kitchen — and sometimes forgetting to take it off at table.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'twiggs'], offstage: [], pivotal: true
    },
    {
      id: 'p3s11', act: 'c2', chapter: 'XXVI', chapterTitle: 'Four-Legs, the dandy',
      title: 'A green bough on the chimney top', date: 'Summer 1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Permission comes to build a house for the government blacksmith, and since Isidore Morrin is a bachelor quite content to go on boarding with Louis Manaigre, the Kinzies plan and hurry it forward entirely on their own account. Then word arrives that the annuity money is waiting at Detroit, and John has to leave at once. The hired workmen can carry on, but the kitchen is the Frenchmen\'s job and the bourgeois will be gone for weeks. So Juliette puts it to them: the logs are cut and hauled, the women have brought the bark for the roof — what is to prevent us finishing the house and surprising Monsieur John? "Ah, to be sure, Madame John," says Plante, who is always the spokesman, "provided the one who plants a green bough on the chimney-top is to have a treat."',
      points: [
        'A log house is built by laying and jointing the logs, framing the chimney with four poles wickered with branches, then filling it with "clay cats" — wisps of hay soaked in clay mortar and shaped by hand — and smoothing the whole with wet clay.',
        'Between the wall logs small bits of wood are driven close together (the "chinking"), clay cats worked in and plastered over, and when it dries the whole is whitewashed.',
        'Around the chimney they lay a few of the palisades left over from Mr. Peach\'s fencing of the garden, which was the pride and wonder of the settlement and the wigwams alike.'
      ],
      cast: ['juliette', 'plante', 'pillon', 'manaigre', 'morrin'], offstage: ['john', 'peach'], pivotal: false
    },
    {
      id: 'p3s12', act: 'c2', chapter: 'XXVI', chapterTitle: 'Four-Legs, the dandy',
      title: 'The Dandy takes a chair', date: 'A Sunday morning, 1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'First and most frequent of their visitors is young Four-Legs, the Dandy, who arrives one fine morning with two women he introduces as his wives — in full finery, brooches, wampum, fan and looking-glass, his face and chest painted with evident care. He takes a chair, as he saw done at Washington, and signs to the women to sit on the floor. Finding the household reading and everything quiet, he asks why, and their mother explains the day of rest and the command to keep it. He nods his approval: that is quite right, he is glad to see people doing their duty, he is very religious himself and likes to see it in others — he always takes care that his wives attend to their duties too. Not reading, perhaps, but such duties as the Great Spirit likes and he thinks becoming.',
      points: [
        'He has no appetite whatever for hearing where the two views differ.',
        'Juliette records the standing Ho-Chunk answer to missionaries plainly: look at you — always toiling and striving, always with a brow of care, shut up in houses, afraid of the wind and the rain, suffering when the comforts are taken away. What should we gain by changing ourselves into white men?'
      ],
      cast: ['youngfourlegs', 'eleanor', 'juliette'], offstage: [], pivotal: true
    },
    {
      id: 'p3s13', act: 'c2', chapter: 'XXVI', chapterTitle: 'Four-Legs, the dandy',
      title: 'Charlotte scours her crucifix', date: '1831',
      place: 'The Agency kitchen', placeShort: 'The Agency',
      summary: 'Father Mazzuchelli visits the Portage with Miss Elizabeth Grignon interpreting, and about forty Ho-Chunk consent to be baptized, pleased with their Christian names and with the little plated crucifixes the women wear at their necks. One of them, given the name Charlotte, asks through Madame Paquette to come on washing-day and learn how it is done in a white household. A tub is found and the servants show her by signs. Curious about how it is going, Juliette comes into the kitchen to find her at the tub scouring and rubbing away — at her crucifix, which she has been polishing for half an hour, watched by two other women sitting on the floor. "She\'ll never learn to wash," says Josette, out of patience. Then Charlotte falls to in earnest, as if she would tear her arms off.',
      points: [
        'Thinking her exhausted, Juliette goes to the closet to do what every housekeeper then did on washing-day and fetch her a glass of something. The cupboard is Mother Hubbard\'s: nothing but orange shrub.',
        'Charlotte takes it with pleasure, stops it halfway to her lips, says "Whiskey!", hands it straight back, points to her crucifix and returns to the tub.',
        '"It was the first time in my life that I had ever seen spirituous liquors rejected upon a religious principle, and it made an impression upon me that I never forgot."'
      ],
      cast: ['charlotte', 'juliette', 'mazzuchelli', 'elizgrignon', 'mmepaquette', 'josettegirl'], offstage: [], pivotal: true
    }
  ],
  outline: [
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
