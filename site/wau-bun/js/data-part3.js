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
  outlineNote: 'Scenes so far cover chapters XXIV–XXVIII. The chapters below are next, and are listed here exactly as they stand in the narrative.',
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
    },
    {
      id: 'p3s14', act: 'c2', chapter: 'XXVII', chapterTitle: 'The Cut-Nose',
      title: 'The Cut-Nose', date: '1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Their greatest favourite among the women of the tribe is a daughter of one of the Day-kau-rays — fair-complexioned and soft-haired from a French cross some generations back, with a noble forehead, full expressive eyes and fine teeth, and, unlike most women of her people, not gone brown and haggard with age. But for one feature she would be called beautiful. She had married a Fox, who by custom came to live among his wife\'s family; no children came, he grew tired of her relations and homesick for the Mississippi, and when she would not go he flew into a passion. If you will not come with me, I will leave you — but you shall never be another man\'s wife. I will mark you. And he bit off the end of her nose, the usual punishment for infidelity and the greatest disgrace a woman can carry, and fled to his own people.',
      points: [
        'His revenge fell short: Day-kau-ray was too well known and too universally respected for disgrace to attach to anyone in his family.',
        'Crippled with rheumatism and much relieved by a remedy the household gave her, she walked the ten miles from the Barribault every two or three weeks just to sit and look at them, laugh at whatever was new or strange, stroke them as they passed and sometimes lift a hand to her lips.',
        '"The Cut-Nose is coming!" was always a joyful announcement. In time they learned to call her Elizabeth, her baptismal name — she too was one of Father Mazzuchelli\'s converts.'
      ],
      cast: ['cutnose', 'juliette', 'eleanor', 'margaret'], offstage: ['musquakee', 'daykauray', 'mazzuchelli'], pivotal: true
    },
    {
      id: 'p3s15', act: 'c2', chapter: 'XXVII', chapterTitle: 'The Cut-Nose',
      title: 'Fan, and the green parasol', date: '1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'She comes one day with a half-grown boy carrying a young fawn as a present. Juliette, who has heard "as wild as a fawn" all her life, expects nothing — and finds that it follows her like a dog, lies at her feet under the breakfast table, and shows affection by gnawing all the trimming off her black silk apron while pretending to nuzzle her. A great rattling of crockery one day turns out to be Fan up on a dresser shelf two feet off the ground, trying to make herself comfortable among the plates: what she wants is the shelf overhead. After that a large green parasol is opened on the matting in the corner at nap time, and at "Fan, Fan" she comes and nestles under it and falls fast asleep.',
      points: [
        'One morning she is missing — garden, cattle enclosure, the Frenchmen\'s houses, the hill toward Paquette\'s, nothing — and they conclude she has gone back to the woods.',
        'At dinner-time she rushes in panting violently, throws herself on her side with her feet out and her mouth foaming, and in a few minutes is dead. Whether the greyhounds had chased her or she had eaten something poisonous and come to her best friends for help, they never knew.'
      ],
      cast: ['cutnose', 'juliette'], offstage: [], pivotal: false
    },
    {
      id: 'p3s16', act: 'c2', chapter: 'XXVII', chapterTitle: 'The Cut-Nose',
      title: 'White Crow brings word of Black Hawk', date: 'Summer 1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Shortly after John leaves for the annuity silver, White Crow, the Little Priest and several other principal Rock River chiefs arrive and are plainly disappointed to find their Father from home. Paquette is sent for to interpret. Black Hawk and his band, who had moved west of the Mississippi under a former treaty, have come back to their old homes and hunting grounds and mean to keep them and drive off the white settlers — which he has already begun. He is said to have brought some Potawatomi with him, and there is reason to fear he may draw Ho-Chunk after them. These chiefs have come to counsel with their Father and to promise they will do everything in their power to keep their young men quiet. They have heard that troops are being raised down in Illinois, and they ask that the soldiers be kept from meddling with people who stay quiet and behave as friends.',
      points: [
        'White Crow is particularly anxious that Juliette understand that if any danger arises while Shaw-nee-aw-kee is away, he will come with his people and protect her and her family — and she believes him, having always found him upright and honourable.',
        'This is the Black Hawk War arriving as a rumour, a full year before it arrives as a war.'
      ],
      cast: ['whitecrow', 'littlepriest', 'juliette', 'paquette', 'eleanor', 'margaret'], offstage: ['blackhawk', 'john'], pivotal: true
    },
    {
      id: 'p3s17', act: 'c2', chapter: 'XXVII', chapterTitle: 'The Cut-Nose',
      title: 'Krissman scrowged out of his place', date: '1831',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'They part with Major Twiggs and his family with real regret, and he leaves Juliette a last report on her protégé. Going into the barracks about dinner-time he had found a great six-foot soldier standing against the window-frame crying and blubbering. What on earth does this mean? "Why, that fellow there," said Krissman, "has scrowged me out of my place!" A pretty soldier your protégé will make, madam. Louisa is disposed of too: an opportunity offering, the Major puts her in the charge of a person going to Buffalo to be returned to her parents. In compliment to her new acquaintances she shortens her skirts and mounts a pair of scarlet leggings embroidered with porcupine quills — and hands her escort sixty dollars for safe keeping, saved out of wages of a dollar a week through the winter.',
      points: [
        'Whether Krissman went on to display his prowess against the Seminoles and the Mexicans or went home to the German Flats to blow his boatman\'s horn, Juliette never heard.',
        'The demure fifteen-year-old who could not be kept from watching Sunday inspection had, it turns out, been quietly banking most of her wages the whole time.'
      ],
      cast: ['twiggs', 'mrstwiggs', 'juliette'], offstage: ['krissman', 'louisa'], pivotal: false
    },
    {
      id: 'p3s18', act: 'c2', chapter: 'XXVII', chapterTitle: 'The Cut-Nose',
      title: 'The little Sunday school', date: '1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Soon after settling in they start a small Sunday school. Edwin, Harry and Josette are the reliable scholars; besides them come the two little Manaigres, Thérèse Paquette, and her mother\'s half-sister Florence Courville, a pretty girl of fifteen. None of the girls knows her letters, and all of them speak only the Canadian patois, so every word has to be given twice — its sound and its meaning, which they are careful to ask for. On top of that there is the ignorance and superstition to work against. They do their best, and have the satisfaction of seeing real progress with the spelling-book and something better besides.',
      points: [
        'Then Florence begins missing class: her sister cannot always spare her, wanting her to keep house while she goes over on Sundays to visit the Roys on the Wisconsin. Offered a weekday lesson instead, Madame Paquette says she will see. Nothing improves.',
        'Manaigre is persuaded to send his children to Mr. Cadle\'s mission school at Green Bay, Thérèse goes with them, Florence stops coming altogether, and the teaching is confined from then on to their own household.'
      ],
      cast: ['juliette', 'edwin', 'harry', 'josettegirl', 'therese', 'florence', 'mmepaquette', 'manaigre'], offstage: ['cadle'], pivotal: false
    },
    {
      id: 'p3s19', act: 'c2', chapter: 'XXVIII', chapterTitle: 'Indian customs and dances',
      title: '"À cette heure, pour le régal!"', date: 'Summer 1831',
      place: 'The new house', placeShort: 'The Agency',
      summary: 'A message comes inviting her up to the new house — they have deliberately stayed away a few days, expecting exactly this. Plante is sitting astride a small keg on the roof beside the kitchen chimney, on the very top of which he has planted a green bough, holding on with one hand and waving the other: "Eh bien, Madame John! à cette heure, pour le régal!" He gets his treat, and is quite content that Pillon and Manaigre share it. Then they leave the old log tenement for the new house, small and insignificant as it is, and Juliette has the luxury of a real bedchamber after more than two months of sleeping on the parlour floor.',
      points: [
        'The clay chimney will not hold trammel and pot-hooks, so the cooking is done on sticks laid across the andirons — and if one burns through, down comes the whole arrangement, kettles, saucepans, brands and cinders together.',
        'In a hard shower the rain comes down the chimney onto a hearth that slopes the wrong way and puts the fire out, and through the bark roof besides, so that there is nothing for it but to snatch up the dinner and tuck it under the table until fair weather.',
        'John gets back at the end of August, astonished to find them moved and settled, and brings with him Juliette\'s young brother Julian, met at Fort Gratiot — a companion at last for the solitary Edwin.'
      ],
      cast: ['plante', 'juliette', 'pillon', 'manaigre', 'john', 'julian', 'edwin', 'eleanor', 'margaret'], offstage: [], pivotal: true
    },
    {
      id: 'p3s20', act: 'c2', chapter: 'XXVIII', chapterTitle: 'Indian customs and dances',
      title: 'A hundred winters, counting her silver', date: 'Payment, autumn 1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Among the crowd at that year\'s payment is someone Juliette has never seen: the mother of the elder Day-kau-ray. Nobody can name her age and everyone agrees on upwards of a hundred winters — eyes almost white, face dark and withered like a baked apple, voice feeble except when she raises it at her graceless grandsons. She goes on all fours, having no strength to stand. Having drawn her portion she hides it in the corner of her blanket, crawls to the doorstep and spreads her silver out to count, unobserved as she thinks. Two of her descendants come on her suddenly, beg, are angrily repulsed, and one makes a swoop and takes a handful. She cannot rise to chase him and can only clutch what is left and scream with rage — until the boys look up, see the women watching from the window, laugh, throw the half-dollars back and run off to the pay-ground.',
      points: [
        'She is fond of them regardless, and can never come to her Father without begging something to give them.',
        'She crawls into the parlour one morning, straightens up against the door-frame and cries piteously, "Shaw-nee-aw-kee! Wau-tshob-ee-rah Thsoonsh-koo-nee-noh!" — Silver-man, I have no looking-glass. "Do you wish to look at yourself, mother?" he asks in the same tone, and she laughs until she has to sit down on the floor.',
        'Then she finds she has no comb; then no knife; then no calico shawl — and it ends, as it generally does, with Shaw-nee-aw-kee paying pretty dearly for his joke.'
      ],
      cast: ['granddaykauray', 'john', 'juliette', 'margaret'], offstage: ['daykauray'], pivotal: false
    },
    {
      id: 'p3s21', act: 'c2', chapter: 'XXVIII', chapterTitle: 'Indian customs and dances',
      title: 'Complimentary dances, and a platform over the graves', date: 'Autumn 1831',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'The payment brings its dances. Permission is asked of the person to be complimented; then faces and bare shoulders are painted after the approved pattern and every ornament that can be found goes into the hair, with an eagle feather for each scalp taken — and for the less fortunate, wild turkey, or the first unlucky rooster to hand, which is why Juliette\'s fowls are thoroughly plucked every payment. The dancers come marching to the appointed place behind drum and shee-shee-qua, form a circle and dance with violent gesticulation until their strength is quite gone, the women standing a little apart and mingling their voices with the instruments. Then presents are piled in the middle by order of the party complimented, equitably divided by one of their number, and everyone retires.',
      points: [
        'The medicine dance is rarer, and celebrates the medicine-man\'s skill in curing. He is priest so far as he makes propitiatory offerings and prophet so far as he instructs, but he claims no power to foretell events.',
        'Some very unsightly pickets round two or three graves in front of the house are, after delicate negotiation with Mrs. Pawnee Blanc, replaced with a neat low wooden platform — and it is touching to see two or three old women come every evening at sunset to sit and gossip over the ashes of their people, and to see a group there on moonlit nights, since they hold that the moon was made to give light to the dead.',
        'Juliette records the Ho-Chunk principles — worship of the Great Spirit, brotherly love, parental affection, honesty, temperance, chastity — and then records that practice departs from them further every year under the debasing influence of nearness to the whites, a thing no one admits with more sorrow than the people who knew them before.'
      ],
      cast: ['mrspawneeblanc', 'juliette', 'john'], offstage: [], pivotal: true
    },
    {
      id: 'p3s22', act: 'c2', chapter: 'XXVIII', chapterTitle: 'Indian customs and dances',
      title: '"Why, you\'re dead!"', date: 'After the payment, 1831',
      place: 'Near Swan Lake', placeShort: 'Swan Lake',
      summary: 'Word of a death is a signal for general mourning, and sometimes — where the means can be found — the apology for a general carouse. A deputation comes to their Father to report one and to beg presents to help them, as they put it, dry up their tears. The deceased is a drunken little Indian the French call Old Boilvin, after the Agent at Prairie du Chien: he had been fishing on one of the little lakes near the Portage, had taken a little too much whiskey, and had fallen in and drowned. Nothing of him was found but his blanket on the bank, so there can be no funeral — but his friends are prepared to lament him thoroughly. Tobacco, knives, calico and looking-glasses are given out in proportion to what their grief for such a worthless vagabond might reasonably amount to, a keg is obtained from a trader despite every prohibition, and the mourning begins in a circle around it.',
      points: [
        'The more they drink the louder the grief and the faster the tears.',
        'Into the middle of it comes a small bent figure, staggering, covered in mud, full of wonder and sympathy: "Why? what? what? Who\'s dead?" — "Why, you\'re dead! You were drowned in Swan Lake! Didn\'t we find your blanket there? Come, sit down and help us mourn."',
        'He did not wait for a second invitation, and wept and drank as bitterly as any of them for as long as anyone could still articulate or any of the whiskey was left.'
      ],
      cast: ['oldboilvinind', 'john'], offstage: ['juliette'], pivotal: false
    }
  ],
  outline: [
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
