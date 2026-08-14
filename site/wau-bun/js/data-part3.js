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
  status: 'complete',
  blurb: 'Juliette\'s story resumes in Chicago. She returns to Fort Winnebago and develops deeper relationships with Ho-Chunk people including Day-kau-ray, Four-Legs, Cut-Nose and White Crow. The Black Hawk War transforms the region, followed by displacement, hunger and upheaval. The series ends with Juliette and John leaving Fort Winnebago, closing the "early day" of the Northwest.',
  acts: [
    { id: 'c1', title: 'The Road Home', sub: 'Chicago → the Portage', note: 'Spring 1831' },
    { id: 'c2', title: 'The Agency', sub: 'Fort Winnebago', note: '1831' },
    { id: 'c3', title: 'The War\'s End', sub: 'Green Bay \u2192 the Portage', note: 'July\u2013December 1832' },
    { id: 'c4', title: 'The Dawn', sub: 'Fort Winnebago', note: '1833' }
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
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'josettegirl', 'harry', 'edwin', 'billycaldwell', 'robert', 'petaille', 'lecuyer'], offstage: ['ouilmette'], pivotal: true
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
      cast: ['juliette', 'john', 'harry', 'josettegirl', 'edwin', 'petaille', 'lecuyer', 'eleanor', 'margaret', 'foster'], offstage: [], pivotal: false
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
    },
    {
      id: 'p3s23', act: 'c2', chapter: 'XXIX', chapterTitle: 'Story of the Red Fox',
      title: 'How the fox got his black legs', date: 'Told at the Agency',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'The Indians of every tribe love telling and hearing stories, and keep professional storytellers who go from village to village with matter everyone already knows by heart — which is how the traditions come down unimpaired. Juliette has watched a man sit in his lodge and draw the whole Northwest in the ashes, lakes and rivers and distances in days\' journeys, accurate as far as Kentucky. The women prefer fiction, and she sets down two tales as specimens. In the first, a chief invites all the animals to a feast. The Red Fox, told the supper is corn porridge, turns up his sharp nose — he can get plenty of that at home. Told instead that there will be a fresh body cooked most delicately, he accepts warmly. The company, making common cause with their insulted friend, greet him at the door and pass him politely from seat to seat, each nearer the fire and the post of honour, until a dexterous shove puts him into the seething kettle.',
      points: [
        'His grandmother, dressing his scalded legs, gives him two reproofs: he returned insult for civility, and he was far too forward in taking the place of honour. Had he kept modestly to the seat by the door, none of it would have happened.',
        'The burns heal, but the legs stay black, and the fox — vain of his legs like many another brave — laments that the young girls will despise him.',
        'His revenge is to bark at the chief\'s lodge in the night, which foretells death; the chief\'s beautiful daughter sickens and dies, and he had loved her. He watches under the tree where she is hung night after night, leaving before dawn, until her beauty returns — and when the village comes to take her back for the Hart she slips off the Hart\'s back unnoticed and returns to him. "By his watchfulness and care he caressed her into life again, so she rightfully belongs to him."'
      ],
      cast: ['juliette'], offstage: [], pivotal: false
    },
    {
      id: 'p3s24', act: 'c2', chapter: 'XXX', chapterTitle: 'Story of Shee-shee-banze',
      title: 'Why those ducks fly in threes', date: 'Told at the Agency',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'The second specimen. A young man called Shee-shee-banze — the Little Duck — is paddling along the shore when two sisters call him over for a sail. In every Indian story with two sisters the elder is silly and disgusting and the younger wise and beautiful, and it is the elder who does the calling. Asked who he is, he claims to be Way-gee-mar-kin, the great chief — a fairy who, when he wishes to favour his followers, coughs slightly and sends silver brooches and ear-bobs flying from his mouth for them to scramble after. Told to cough, he produces a few he has stowed in his cheeks from scrambling. An elk comes down to drink and he calls it his hunting dog; a bear, and he calls it his servant; and when neither will come at his call he explains that the sight of her fills them with disgust.',
      points: [
        'The imposture runs on through murder, pursuit, and a taunting song — "Come, pretty widows, come and catch me" — sung to the women sent to lure him into the village.',
        'Cornered at last with two brides, he reaches his canoe; the pursuers overturn it in the river, and the moment they touch the water all three are turned into ducks and fly quacking away.',
        'Which is why water-fowl of that species are always found in companies of three, two females and a male — while the mallard and the wood duck fly in pairs, the wood duck being so constant that if he loses his mate he never takes another and goes mourning to the end of his days.'
      ],
      cast: ['juliette'], offstage: [], pivotal: false
    },
    {
      id: 'p3s25', act: 'c2', chapter: 'XXXI', chapterTitle: 'A visit to Green Bay',
      title: 'The mail that brought the wrong news', date: 'October 1831',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'Word comes that John\'s accounts as Agent never reached Washington. With the vouchers for past expenditure and the recent $15,000 annuity unaccounted for, his position could become awkward, so he decides to carry the duplicates east himself — and asks Juliette whether she would like to see her father and mother and show them how the West agrees with her. After a year\'s separation it is a joyful suggestion. Miss Brush comes with them to Green Bay, where the whole place from Fort Howard to Dickenson\'s is waiting on one of Mr. Newbery\'s schooners: friends for some, supplies for others, the fashions for the ladies, the news for the gentlemen, and the mail for the entire upper country. As Postmaster, John opens the bag himself. One letter says the missing accounts have turned up satisfactorily. Another says her parents have gone to Kentucky for the winter.',
      points: [
        'Not to any city or reachable place, but "up the Sandy" and over among the mountains of Virginia, hunting old land-claims of her grandfather\'s estate.',
        'Following them was hopeless, even with the directions an old settler once gave her father: "You must go up Tug, and down Troublesome, and fall over on to Kingdom-come."'
      ],
      cast: ['john', 'juliette', 'brush', 'stambaugh'], offstage: ['eleanor'], pivotal: false
    },
    {
      id: 'p3s26', act: 'c2', chapter: 'XXXI', chapterTitle: 'Ma-zhee-gaw-gaw swamp',
      title: '"No mortal woman has ever gone that road"', date: 'November 1831',
      place: 'Green Bay → the Portage', placeShort: 'Ma-zhee-gaw-gaw',
      summary: 'With the eastern journey abandoned, they must get home — and no boat is ready to ascend the river. Their old friend Hamilton promises one at once, and time passes, and none appears. It is the beginning of November. The days pass pleasantly enough with the Irwins, the Whitneys and Colonel Stambaugh, but the delay is vexatious. Juliette suggests riding home overland instead, and gets the same answer every time she raises it: no mortal woman has ever gone that road, unless some native on foot, nor ever could. The road in question runs through the Ma-zhee-gaw-gaw swamp.',
      points: ['The woman who had already been dumped into Duck Creek in March, lost on the prairie in a blizzard, and ferried across the Fox lying flat in the bottom of a canoe was not much impressed by the argument.'],
      cast: ['juliette', 'john', 'brush'], offstage: ['arndt'], pivotal: true
    },
    {
      id: 'p3s27', act: 'c2', chapter: 'XXXII', chapterTitle: 'Commencement of the Sauk war',
      title: 'Black Hawk recrosses the Mississippi', date: 'April 1832',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Juliette\'s brother Arthur arrives from Kentucky by way of the Mississippi at the end of April with uncomfortable news: Black Hawk has recrossed the river with the flower of his nation to take back the old homes and corn-fields. The Ho-Chunk come flocking in to confirm it and to promise they will stay faithful friends of the Americans. Then the Illinois Rangers reach the Rock River country and General Atkinson\'s regulars begin a pursuit of an enemy who will not stand and fight: the Sauks scatter through the country and wait for the lucky accident, and the army makes toilsome marches to the place they were expected to be and finds them gone to somewhere else entirely.',
      points: [
        'Wherever the war parties go, the course is marked by atrocities — though the worst of it has not reached the Portage yet.',
        'Juliette sets down plainly why young Ho-Chunk men might want white scalps: they had been dispossessed of the broad and beautiful country of their forefathers and hunted from place to place, and what they got in exchange was a few thousand a year in silver and presents, "together with the pernicious example, the debasing influence, and the positive ill treatment of too many of the new settlers upon their lands."'
      ],
      cast: ['arthur', 'juliette', 'john', 'eleanor'], offstage: ['blackhawk', 'atkinson'], pivotal: true
    },
    {
      id: 'p3s28', act: 'c2', chapter: 'XXXII', chapterTitle: 'Commencement of the Sauk war',
      title: 'Fifty lodges around the house', date: 'Spring 1832',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'About fifty lodges come and camp around the house at the beginning of the disturbances, saying that if the Sauks attack, it must be after killing them first — and, knowing these people, the household has perfect confidence in the assurance. But being surrounded by them is also being plugged into a channel of daily news, brought in by runners as the theatre of operations moves closer: that Captain Barney\'s head has been recognised in the Sauk camp, brought there the day before; that the Sauks are carrying Lieutenant Beall\'s head on a pole in front of them as they march. Some of it turns out to be true — among it the murder of M. St Vrain, the Sauks\' own Agent, at Kellogg\'s Grove, by the people who ought to have protected him.',
      points: [
        'Protection and terror arrive in the same bundle, which is the exact condition of that summer.',
        'Old Crély, Madame Paquette\'s father, rides express from Galena with news of the attack on Apple Fort, swearing he passed a bush with Sauks behind it and was saved by his horse smelling the sweet-scented grass they wear on a war party.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'crely', 'follett'], offstage: ['stvrain', 'blackhawk'], pivotal: true
    },
    {
      id: 'p3s29', act: 'c2', chapter: 'XXXII', chapterTitle: 'Commencement of the Sauk war',
      title: 'Seventy miles, and a council at the Four Lakes', date: 'Summer 1832',
      place: 'The Four Lakes', placeShort: 'Four Lakes',
      summary: 'After St Vrain\'s murder, John calls a council with every principal Ho-Chunk chief he can reach — at the Four Lakes, thirty-five miles off. He knows the Sauks will work on his people, and he is sure only of the older men. The household pleads with him not to go. It is his duty to assemble his people and talk to them, he says, and he must run the risk if there is one; he has perfect confidence in the Ho-Chunk, and the enemy by every account are far off at Kosh-ko-nong. He will leave early with Paquette, hold his council and be back the same evening. The day is impossible to describe; by night a drunken shout or a barking dog fills them with terror. Then, late, at the open window, the tramp of horses — Griffin and Jerry coming up the hill, and a cheerful shout to say all is well.',
      points: [
        'He and his interpreter had ridden seventy miles that day, on top of holding a long talk.',
        'The council promised to do their utmost to keep their young men quiet, and reported that every Rock River band but Win-no-sheek\'s was determined to stay clear of the Sauks — abandoning villages and corn-fields and moving north so that their Great Father should have no cause for dissatisfaction. For Win-no-sheek they could not answer.',
        'Then the murders of Auberry, Green and Force at Blue Mound, and the attack on Apple Fort.'
      ],
      cast: ['john', 'paquette', 'juliette', 'eleanor', 'margaret'], offstage: ['winnosheek', 'whitecrow', 'daykauray'], pivotal: true
    },
    {
      id: 'p3s30', act: 'c2', chapter: 'XXXIII', chapterTitle: 'Fleeing from the Indians',
      title: 'The Fourth of July, and the parting', date: '4 July 1832',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'The danger becomes imminent enough that John determines to send his family to Fort Howard, believed to be well out of the enemy\'s range. Juliette pleads to stay and he will not have it. He must not leave his post while there is danger — his going might be the signal for the Ho-Chunk to join the Sauks, and while he is here his presence restrains them. As for sharing his danger: alone, with friends in both tribes, he could hope to save his own life; surrounded by his family it would be impossible and they would all fall together. His plain duty is to send them somewhere safe. Paquette has a boat of furs going down to Green Bay, and it is fitted out as comfortably as an open boat can be — tent-cloth on a frame of hoop-poles, lined with a dark-green blanket — and they are committed to Juliette\'s brother Arthur and the blacksmith Mâtâ, with three trusted Ho-Chunk under Old Smoker as escort and six gay-hearted French engagés at the oars.',
      points: [
        'They leave on the Fourth of July. Nobody knows whether they will meet again, and some of that circle have experience of Indian warfare enough to justify the worst.',
        'Nor does the step guarantee anything: the Sauks might be on the other side of them, and this route might carry them into the middle of it.',
        'Only the Frenchmen are cheerful, laughing and cracking jokes and assuring Monsieur John that they will take Madame John and Madame Alum safe to the Bay in spite of Sauks or wind or weather.'
      ],
      cast: ['john', 'juliette', 'eleanor', 'margaret', 'arthur', 'mata', 'oldsmoker', 'edwin', 'julian'], offstage: ['paquette', 'blackhawk'], pivotal: true
    },
    {
      id: 'p3s31', act: 'c2', chapter: 'XXXIII', chapterTitle: 'Fleeing from the Indians',
      title: 'Three men step out on the bank', date: '6 July 1832',
      place: 'The Fox River', placeShort: 'The Fox',
      summary: 'At the noon pipe they discover that no bread was put aboard for the crew — everyone certain a quantity came from the garrison bakery that morning, one man having seen the sacks standing in Paquette\'s kitchen. Going back is out of the question, so their own oversupply is rationed out to the six Frenchmen as far as Powell\'s. They travel in silence from then on; a song or a loud laugh is forbidden until they are past the limits of country where the enemy might be. On the second forenoon they approach the point where the marshy meadows rise into firmer ground — the border of the Menomonee country, and exactly where the Sauks would be if they had fled north of the Wisconsin. Old Smoker is squatting in the bow staring at the wooded point. Three Indians step out and stand on the bank. If they are Sauks, the whole body is in that thicket. Nobody speaks; there is only the dip of the paddle.',
      points: [
        'Then he springs to his feet with a long shrill whoop — "Hoh! hoh! hoh! Neechee Muh-no-mo-nee!" — and everyone is forward to shake hands with men who are Menomonee and not Sauk.',
        'Later, told the woods are alive with pigeons they could almost knock down with sticks, the young people beg to shoot enough for supper and are refused: a gunshot would tell friend and foe alike where they are.',
        'At Powell\'s at the Butte des Morts there is not a loaf to be had and their own store is gone. All they can get is a bag of dark, bitter flour — and they leave the Hillock of the Dead feeling it has been the grave of their hopes.'
      ],
      cast: ['oldsmoker', 'juliette', 'arthur', 'mata', 'eleanor', 'margaret', 'edwin', 'julian'], offstage: [], pivotal: true
    },
    /* ---------------- Act 3 — The War's End ---------------- */
    {
      id: 'p3s32', act: 'c3', chapter: 'XXXIV', chapterTitle: 'Fort Howard — our return home',
      title: 'The man the Sauks nearly ate', date: 'July 1832',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'They arrive into a full-blown panic. Green Bay has convinced itself that the Sauks will come through on their way to Canada to put themselves under British protection — how they would get there, whether by stopping to build bark canoes or by chartering one of Mr. Newbery\'s schooners, nobody has troubled to work out. A portion of the citizens are nearly frightened to death and certain there is no safety outside the walls of the old dilapidated fort, from which nearly all the troops had been withdrawn and sent to Fort Winnebago some time before.',
      points: [
        'The fear is stoked by a traveller\'s report that he slept at night on the very spot where the Sauks breakfasted next morning — and since the Sauks were known to be on very short commons, he is held to have made a wonderful escape.',
        'The Kinzies\' own friends do not join in it: anyone who considers the country to be crossed and the numerous whites who would meet them there can see the movement is impossible.'
      ],
      cast: ['juliette', 'eleanor', 'margaret', 'arthur', 'edwin', 'julian'], offstage: ['blackhawk', 'john'], pivotal: false
    },
    {
      id: 'p3s33', act: 'c3', chapter: 'XXXIV', chapterTitle: 'Fort Howard — our return home',
      title: 'The Mariner', date: 'Early one morning',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'The schooner everyone has been waiting for comes in at last, and within an hour her news has run the whole length of the settlement: the cholera is in the country. It is in Detroit; it is among the troops on their way to the seat of war; whole companies have died of it in the river St. Clair and the survivors were put ashore at Port Gratiot to save their lives as best they might. They are shut in between the savage foe on one hand and the pestilence on the other.',
      points: [
        'The man who brings the news to the Kinzies is an officer of distinguished courage in the field and in private enterprises demanding unequalled daring. Having told them, he laid his head against the window-sill and wept like a child.',
        'Those with friends near and dear to the east leave in the Mariner. Everyone else decides their present home is the safest — and so it proves: the scourge does not visit Green Bay that season.'
      ],
      cast: ['juliette', 'eleanor', 'margaret'], offstage: [], pivotal: true
    },
    {
      id: 'p3s34', act: 'c3', chapter: 'XXXIV', chapterTitle: 'Fort Howard — our return home',
      title: 'Tapping on the bars', date: 'Summer 1832',
      place: 'Fort Howard', placeShort: 'Fort Howard',
      summary: 'Crossing the parade, their attention is sometimes drawn by a tapping on the bars of a dungeon. It is the murderer of Lieutenant Foster — the amiable young officer who had been their travelling companion from Chicago the year before. Some months after reaching Fort Howard, Foster had a soldier named Doyle confined for drunkenness. Doyle talked the sergeant of the guard into walking him up to the lieutenant\'s quarters to speak with him, asked what he was confined for, was told he knew his offence well enough and should return to his place of confinement — ran downstairs, wrenched the gun out of the sergeant\'s hands and discharged it into Foster\'s heart. Foster turned toward his inner room, said "Ah me!" and fell dead in the doorway.',
      points: [
        'Tried by a civil court, Doyle is now under sentence and shows not the slightest compunction. Asked by Major Clark whether he wants anything for his comfort, he would like a light and a copy of Byron\'s Works.',
        'Fearing he will make away with himself first, they take away everything that could serve as a weapon and serve his food in a wooden bowl in case a shard of crockery is used. He sends the commanding officer a present: a strong rope woven from strips of his blanket with a stout spike at the end, and the message that if he chose to put an end to himself he could find the means in spite of him.',
        'Led out past a stack of lumber for a new warehouse, he asks Captain Scott what they are going to build there. Told he has but a few moments to live and had better think about something else: "It is for that very reason, captain, that I am inquiring — as my time is short, I wish to gain all the information I can while it lasts."'
      ],
      cast: ['juliette', 'doyle', 'majorclark', 'captscott'], offstage: ['foster'], pivotal: true
    },
    {
      id: 'p3s35', act: 'c3', chapter: 'XXXIV', chapterTitle: 'Fort Howard — our return home',
      title: 'A lady at the front door', date: 'Two weeks later',
      place: 'Fort Howard', placeShort: 'Fort Howard',
      summary: 'They are not left long in suspense about the people they left behind. Old Smoker appears again inside a fortnight with letters: Generals Dodge, Henry and Alexander are all at Fort Winnebago recruiting men and horses worn out with scouring the country, and will march again for the head-waters of the Rock River as soon as they are fit. Not long after, Juliette is told a lady wishes to see her at the front door, and finds Madame Four-Legs — who puts both hands together over her forehead and parts them in a waving gesture, laughs, pats her arms, and draws a letter out of her bosom.',
      points: [
        'The letter reports the battle of the Wisconsin on the 21st: upwards of fifty of the enemy killed, one American killed and eight wounded, and the citizens well pleased it was done without any help from Old White Beaver.',
        '"The war must be near its close, for the militia and regulars together will soon finish the remaining handful of fugitives."'
      ],
      cast: ['juliette', 'oldsmoker', 'mmefourlegs'], offstage: ['john', 'gendodge', 'genhenry', 'genalexander', 'paquette', 'blackhawk'], pivotal: true
    },
    {
      id: 'p3s36', act: 'c3', chapter: 'XXXIV', chapterTitle: 'Fort Howard — our return home',
      title: 'The Grande Chûte', date: 'Late July 1832',
      place: 'The Grande Chûte, Fox River', placeShort: 'Grande Chûte',
      summary: 'Lieutenant Hunter takes leave of absence to escort them home. No Mackinac boat is to be had, so a Durham boat is got — longer, shallower, no way to rig an awning — and a party of eleven or twelve makes up its mind to close quarters. At the Grande Chûte the custom is to land at the foot of the rapids and walk round while the men haul the boat up through the foam. Juliette and one of the other ladies decide to stay aboard and be pulled up the Chûte. At the head of the cordel is a merry simpleton of a Frenchman, Robineau, who keeps turning his head to grin at their enjoyment — and, more occupied with the ladies than his duty, walks the boat straight into a sharp projecting tree hanging from the bank.',
      points: [
        'The first tug rips the side out of the boat. The two women jump for the nearest rocks showing above the foam and are carried ashore in the arms of Lieutenant Hunter and some Indians who came down the bank at a run.',
        'From the top of the bank: "Oh! my husband\'s new uniform!" — "Oh! the miniatures in the bottom of my trunk!" — "Oh! the silk dresses, and the ribbons, and the finery!" Nobody thinks of the provisions, though they had watched the barrel of bread and the tub of ice sail away on the waves.',
        'A box of loaf sugar splits and oozes white at the corners. Juliette points at the young Indian\'s hatchet, he does not need asking twice, and the scramble that follows — bowls, dippers, hands, the stoutest fragments of the blue sugar-paper — puts them all, the boys especially, into fits of laughter.',
        'Rain comes on; every bush is hung with mottled blue, green, red and black; the tent is pitched wet and the blankets wrung out and spread on the ground, and a Hamburg cheese is voted to Juliette for a pillow.'
      ],
      cast: ['juliette', 'hunter', 'mrshunter', 'missforsyth', 'eleanor', 'margaret', 'robineau', 'edwin', 'julian', 'arthur'], offstage: [], pivotal: true
    },
    {
      id: 'p3s37', act: 'c3', chapter: 'XXXIV', chapterTitle: 'Fort Howard — our return home',
      title: '"There is John!"', date: 'The next morning',
      place: 'The Fox River → the Portage', placeShort: 'Fox River',
      summary: 'The morning is hot and sultry, the mosquitoes making up for the night, the boat sunk halfway up the rapids and no way of getting anyone anywhere. In the middle of the consultation a whoop comes from beyond the hill — it is John, who, never having been told their plans, has come down with a boat to fetch them. They are transferred and pulling for Winnebago Lake in an incredibly short time.',
      points: [
        'They stop near the Little Butte to dry the wardrobe again, and have barely got the last ribbon spread when twenty-five horsemen ride into the middle of it — Colonel Stambaugh and Alexander Irwin with a company of young volunteers and a whooping band of Menomonee, bound for the war. They are comforted with the assurance that the victories are all won and the scalps taken, and ride on hoping for a few laurels left.',
        'Lake Winnebago is crossed by summer moonlight with just enough air to swell the sail; the whole company is packed into the centre of the boat in an arrangement nobody could have reassembled if it had once been disturbed.',
        'At Powell\'s there is nothing to be had, the wet bread has fermented in the July sun and the tea gone musty; at Gleason\'s, La Grosse Américaine cuts bread-and-butter for them like a parcel of children, and Mâtâ appears with the old calèche and a provident load of tea, coffee, fresh butter and eggs — "Good-morning, Madame Johns! How do you dos?"',
        'Margaret goes ahead with Josette to open the house, which has been headquarters for militia, Indians and stragglers all summer. They reach it at sunset to find it whitewashed roof to door-sill, scrubbed, carpets down, and a noble supper smoking on the board.'
      ],
      cast: ['john', 'juliette', 'hunter', 'mata', 'mrsarmstrong', 'stambaugh', 'irwin', 'margaret', 'josettegirl', 'eleanor', 'manaigre', 'edwin', 'julian', 'missforsyth', 'mrshunter'], offstage: [], pivotal: true
    },
    {
      id: 'p3s38', act: 'c3', chapter: 'XXXV', chapterTitle: 'Surrender of Winnebago prisoners',
      title: 'Three bottles of cologne-water', date: 'August 1832',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'News of the battle of the Bad Axe — regulars, militia and the steamboat Warrior together making an end of the remaining handful of Sauks — reaches them and restores tranquillity to the frontier. Juliette sets down why so small and ill-resourced an enemy required so vast a force: the difficulty was never in beating them but in finding them, and the training needed to pursue and catch Indians was something few even of the frontier militia could boast. The other difficulty was the want of concert between the two branches of the service — the regulars contemptuous of the militia\'s unprofessional movements, the militia scornful of the regulars\' dilatory formalities, each convinced things would go better without the other.',
      points: [
        'General Brady had spoken for every military man at the outset: "Give me two infantry companies mounted, and I will engage to whip the Sauks out of the country in one week!"',
        'The militia, being prompt to act, sometimes took matters into their own hands and brought on defeat and disgrace, as at Stillman\'s Run.',
        'The contempt ran all the way down. Asked to account for three bottles of cologne-water in the month\'s mess bill, little Yellow David answered respectfully that it was to sweeten up the dining-room and quarters after them milish\' officers were here visiting.'
      ],
      cast: ['juliette', 'yellowdavid'], offstage: ['brady', 'blackhawk'], pivotal: false
    },
    {
      id: 'p3s39', act: 'c3', chapter: 'XXXV', chapterTitle: 'Surrender of Winnebago prisoners',
      title: 'The canoes that were tied together', date: 'August 1832',
      place: 'Prairie du Chien', placeShort: 'Prairie du Chien',
      summary: 'Black Hawk and a few warriors who escaped north are captured shortly after by the One-eyed Day-kau-ray and his party and brought as prisoners to General Street at Prairie du Chien. The women and children of the band had been put into canoes and sent down the Mississippi in hopes of being allowed to cross and reach the rest of the tribe. The canoes had been tied together; many upset, and the children drowned, their mothers too weak and exhausted to save them. The survivors were taken prisoner and brought in starving.',
      points: [
        'The Kinzies\' mother is at the fort when they arrive, and describes their condition as more wretched and reduced than anything she has ever seen.',
        'One woman who spoke a little Chippewa gave her the account: after eating such horses as could be spared they had lived on acorns, elm-bark and grass, and the dead were found lying in their trail by the pursuing whites. She had lost her husband in battle and all her children in the upset canoe, and her only wish now was to go and join them.',
        'Juliette\'s comment is one line long: "Poor Indians! who can wonder that they don\'t love the whites?"'
      ],
      cast: ['eleanor', 'saukmother', 'oneeyeddaykauray', 'blackhawk'], offstage: ['juliette'], pivotal: true
    },
    {
      id: 'p3s40', act: 'c3', chapter: 'XXXV', chapterTitle: 'Surrender of Winnebago prisoners',
      title: '"Bad news, madam! Have you heard it?"', date: 'Autumn 1832',
      place: 'Fort Winnebago / Rock Island', placeShort: 'Fort Winnebago',
      summary: 'John is summoned to collect the principal chiefs and meet General Scott and Governor Reynolds at Rock Island, where a treaty is proposed for the purchase of all the land east and south of the Wisconsin. He has been gone a fortnight when Juliette, crossing the hall of the quarters to visit her sister, meets Lieutenant Lacy coming the other way. "Bad news, madam! Have you heard it? The cholera has broken out at Rock Island, and they are dying by five hundred a day." He vanishes without waiting for a question. She cannot get the sentinel to leave his post, and Mrs. Lacy\'s servant girl does not like to go to the young officers\' quarters — until Dr. Finley appears of his own accord: on his way home, madam, safe and sound.',
      points: [
        'He was in fact seized with cholera on the journey, and recovered by the care of Paquette and the chicken-broth of the poor woman at whose cabin he stopped — coming home by way of Prairie du Chien and bringing his mother back with him.',
        'The nation consented to the sale. Juliette explains why they generally do: hold the land and you end up surrounded and hemmed in by white settlers, which is worse than giving it up, so you give it up and take care to make the best bargain you can. The price was a tract reaching into the interior of Iowa and ten thousand dollars a year.',
        'One stipulation of the treaty was that the Ho-Chunk surrender certain of their own people accused of joining the Sauks in murders on the frontier, to be tried by American law.'
      ],
      cast: ['juliette', 'lacy', 'finley', 'margaret'], offstage: ['john', 'genscott', 'reynolds', 'paquette', 'eleanor'], pivotal: true
    },
    {
      id: 'p3s41', act: 'c3', chapter: 'XXXV', chapterTitle: 'Surrender of Winnebago prisoners',
      title: 'The hostage, and two kegs of whiskey', date: 'Autumn 1832',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Persuading the seven accused men to put themselves into white hands takes time: the trial of Red Bird and his lingering death in prison are still fresh, and it needs resolution as well as a strong conviction of innocence. Nothing is forced — the nation would never have used force to fulfil its own stipulation. Meanwhile Wau-kaun-kah, the Little Snake, gives himself voluntarily as a hostage until the seven appear to redeem him, and is marched over and confined at the fort. A solemn talk is held at the Agency with the principal chiefs, most of the nation being camped nearby on Governor Porter\'s notice that he will bring the annuity money himself this year instead of leaving it to the Agent.',
      points: [
        'Those who had not been at Rock Island are loud in their condemnation of the sale. Foremost is Wild-Cat, weeping over the loss of his home on the blue waters of Winnebago Lake, and certain that if he had not been accidentally stopped on his way to the treaty he would never have permitted the bargain.',
        'Their Father, who knows the stopping was a desperate frolic, replies gravely that he had heard of the chief\'s misfortune: ascending the Fox, a couple of kegs of whiskey came floating down the stream and ran foul of his canoe with such force that he was obliged to lay up several days at the Mee-kan to repair damages. The laughter is contagious enough that Wild-Cat joins in and treats his own misfortune as a joke.',
        'Every time the Kinzies come inside the walls they are hailed from the guard-room window: "Do you hear anything of those Indians? When are they coming, that I may be let out?"'
      ],
      cast: ['john', 'juliette', 'waukaunkah', 'wildcat', 'paquette'], offstage: ['redbird', 'porter', 'doty', 'prisoners'], pivotal: true
    },
    {
      id: 'p3s42', act: 'c3', chapter: 'XXXV', chapterTitle: 'Surrender of Winnebago prisoners',
      title: 'White cotton, and a death-song', date: 'A bright autumn morning',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'At ten o\'clock a moving concourse can be made out along the Portage road — brilliant colour, glittering arms, and, closer, white objects of unusual appearance. General Dodge, Major Plympton and one or two other officers take seats with John on the platform in front of the door; the women watch from the window. First come the principal chiefs in their most brilliant array. Then the prisoners, all in white cotton in token of their innocence, girdled at the waist, wearing no paint and no ornament, chanting their death-song to the drum and the shee-shee-qua, their faces grave and thoughtful. Behind them a long train of the nation in holiday garb. It is a grand and solemn sight.',
      points: [
        'The chiefs shake hands; the prisoners shake hands with the officers; and when they offer their hands to their Father he declines. "You have come here accused of great crimes. When you have been tried by the laws of the land, and been proved innocent, then your Father will give you his hand." They look more serious still, step back, and seat themselves in a row on the ground.',
        'White Crow, deputed to deliver them, says that although his countrymen assert their innocence they are quite willing to be tried by the laws of white men — and hopes they will not be detained long, but will come out of it clear and white.',
        'He then asks leave to transfer the President\'s medal from his own neck to his son\'s, the nation having chosen the young man to fill the office he wishes to resign. Juliette thinks no one could have witnessed it unmoved.',
        'She watches the prisoners\' faces throughout. With one exception they are open and calm; one is remarkably fine-looking; one is a boy of certainly not more than seventeen, who follows the business of the medal with an air of childlike interest and satisfaction. When it is over they are marched off by a file of soldiers to the dungeon of the guard-house.'
      ],
      cast: ['john', 'juliette', 'prisoners', 'whitecrow', 'whitecrowson', 'gendodge', 'plympton', 'paquette', 'eleanor', 'margaret'], offstage: ['waukaunkah'], pivotal: true
    },
    {
      id: 'p3s43', act: 'c3', chapter: 'XXXVI', chapterTitle: 'Escape of the prisoners',
      title: 'Waiting for the silver', date: 'September–October 1832',
      place: 'The Portage', placeShort: 'The Portage',
      summary: 'The nation does not disperse after the surrender: they stay near the Portage expecting the annuity money they were summoned for, and Governor Porter puts off the journey to fetch it from week to week. Had he foreseen what the delay would cause he might have been prompter. Having abandoned their homes that spring to avoid any appearance of fraternising with the Sauks, they had planted no gardens and no corn-fields, and had nothing in hand for the winter but a scant supply of wild rice — which now goes on being eaten during the detention. The rations the Agent had sometimes been permitted to issue are cut off by scarcity in the Commissary\'s department, drained by the summer\'s levies and the troops brought up from Fort Howard.',
      points: [
        'John saw it coming and, the moment the war ended, commissioned Mr. Kercheval at Fort Howard to buy two boat-loads of corn for distribution. There was none to be had in Michigan; it had to come from Ohio; and by the time it reached Green Bay the navigation of the Fox had closed for the winter.',
        'Advised at last to disperse to their hunting grounds and be summoned back the moment the silver arrives, they go.',
        'While they were near, they more than once asked leave to dance the scalp-dance before the door — the most heart-curdling exhibition imaginable, scalps stretched on hoops and brandished on poles, the women rushing in to seize and toss them with the screams of demons. Juliette has seen forty or fifty scalps in one dance; one carried near her had long fair hair, evidently a woman\'s; another man carried the skin of a human hand, stretched and prepared as carefully as a costly jewel. By moonlight they are peculiarly horrid.'
      ],
      cast: ['john', 'juliette'], offstage: ['porter', 'cutler'], pivotal: true
    },
    {
      id: 'p3s44', act: 'c3', chapter: 'XXXVI', chapterTitle: 'Escape of the prisoners',
      title: 'Guns toward the Wisconsin', date: 'One evening at tea',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Amid so much of a painful character there is occasionally something that borders on the ludicrous. Firing is heard from the direction of the Wisconsin; everyone starts up and prepares instinctively for the garrison. Outside, the whole bluff and meadow are in commotion — Indians running with guns and spears toward the sound, women and children standing in front of their lodges looking anxiously that way, groups of French and half-breeds fleeing for the bridge and the new pickets. As one company hurries past, a carelessly carried weapon catches one of the party on the side of the head: "Oh! I am killed! an Indian has tomahawked me!" — she is reassured on discovering she can still run as fast as the best of them.',
      points: [
        'On the parade-ground they cannot help laughing at the figure they cut: some without hats or shawls, some clutching valuables snatched up at the door, one still holding the bread-and-butter she had not had the presence of mind to put down.',
        'The alarm turns out to be a party from one of the Barribault villages, leaving home for a season and going through the ceremony of burying the scalps they and their fathers had taken — closing the solemnity, like a military funeral, with volleys over the grave of their trophies.'
      ],
      cast: ['juliette', 'john', 'margaret', 'eleanor', 'edwin', 'julian'], offstage: [], pivotal: false
    },
    {
      id: 'p3s45', act: 'c3', chapter: 'XXXVI', chapterTitle: 'Escape of the prisoners',
      title: 'The badgers', date: 'December 1832',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Governor Porter arrives with the annuity money at the beginning of November, two months after the appointed time; the payment is made, the people lay in more ammunition than usual against a winter they know they must hunt hard in, and go. The Kinzies move into the new Agency House at last. They have been settled a few weeks when Lieutenant Davies appears at breakfast with a face full of consternation: the prisoners have escaped from the black-hole, and Colonel Cutler wants Mr. Kinzie to come over and counsel with him.',
      points: [
        'They had begun almost at once. Meals came three times a day and the rest of the time they were left alone; they dug with their knives, spread the earth on the floor, and kept a blanket over the hole with one man sitting on it — so that the soldier in charge always found them seated and smoking in the most orderly and quiet manner.',
        'They had never read the memoirs of Baron Trenck, but they had watched badgers. Working the shaft spirally, they came out beyond the walls of the fort in about six weeks — leaving their blankets behind so as not to be encumbered, and taking to the woods in bitter December in nothing but calico shirts and leggings.',
        'Juliette declines, on grounds of her own reputation as a loyal and patriotic citizen, to say how the news was received in her house.',
        'Asked to help get them back, the chiefs assembled on New-Year\'s Day answer that if they see the young men they will tell them what the officers would like; they can do nothing themselves. They fulfilled their engagement by bringing them once and putting them into the officers\' hands. "The Government had had them in its power once and could not keep them — it must now go and catch them itself." The Government, having had some experience that summer in catching Indians, wisely dropped the matter.'
      ],
      cast: ['john', 'juliette', 'davies', 'prisoners'], offstage: ['porter', 'cutler', 'daykauray'], pivotal: true
    },
    {
      id: 'p3s46', act: 'c3', chapter: 'XXXVI', chapterTitle: 'Escape of the prisoners',
      title: 'Ten days in the snow', date: 'Winter 1832–33',
      place: 'Toward Sugar Creek', placeShort: 'Sugar Creek',
      summary: 'Robineau arrives on a very cold day to get medical aid for Mâtâ\'s eldest daughter Sophy, who fell on the ice at Sugar Creek and has been feverish and suffering for two or three days with her father away at Prairie du Chien. The commanding officer will not spare the surgeon but cheerfully grants leave to Currie, the hospital steward; Madame Bellaire is engaged as nurse and Agathe, Day-kau-ray\'s daughter, goes as aid and companion. Forty miles, a horse packed with rice, crackers, tea and sugar for the invalid, and two days expected. On the fourth day Turcotte walks in from Sugar Creek to ask why no help has come.',
      points: [
        'Robineau had guided them as ill as he guided the boat at the Grande Chûte, keeping doggedly to a track Agathe had known from the first was wrong until it brought them out at the Rock River.',
        'Ten days later a searching party finds them at Hastings\'s Woods, twelve miles out, feeble and on the right road at last; their provisions had given out two days before, and they had seriously discussed killing and eating the horse — deterred only by Currie\'s inability to walk and the dread of leaving him in the woods to perish.',
        'Agathe had carried her hatchet, as her people do, so they had a fire every night and boughs against the storms. Without that they must have perished.',
        'Two things stir more than sympathy: Robineau demanding of Currie first his money and then his watch as the price of leading them back into a path he claimed to know perfectly well, and Bellaire giving his kind, excellent wife a hearty flogging for going off on such a fool\'s errand. The second culprit is out of the Agency\'s jurisdiction; the first is discharged on the spot and told he may think himself happy to escape a prosecution for swindling.',
        'Sophy is quite recovered by the time her father gets back from the Prairie.'
      ],
      cast: ['robineau', 'currie', 'mmebellaire', 'agathe', 'turcotte', 'john', 'juliette'], offstage: ['sophy', 'mata', 'cutler', 'bellaire'], pivotal: false
    },
    /* ---------------- Act 4 — The Dawn ---------------- */
    {
      id: 'p3s47', act: 'c4', chapter: 'XXXVII', chapterTitle: 'Agathe — Tomah',
      title: 'What was done to Agathe', date: 'Some years earlier',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Agathe is the daughter of the man known as Rascal Day-kau-ray, brother to the grand old chief and as unlike him as men of one blood can be. The Day-kau-rays are a handsome family and she is remarkable even among them — tall, a round sweet face, the soft melodious voice of the women of her people, and a pensive expression that makes strangers want her history. Mrs. Paquette tells it to Juliette. A young officer at the fort saw her and set his mind on her, and applied to Paquette to negotiate what he called a marriage. Paquette knew perfectly well the sin of the false representations he was making to her family and the misery he was bringing on her, and did it anyway.',
      points: [
        'She had been betrothed to a young man of her own people, and the attachment on both sides was very strong. Juliette explains why that matters more here than a white reader may assume: with few objects to spend feeling on, all feeling is concentrated, and among the women family ties engross the whole of it. Marriage is a sacred and indissoluble tie, female propriety the strictest trait of the nation — a woman who transgresses is said to have "forgotten herself," and is cast off and forgotten in return.',
        'She rejects outright the notion, then being written into a historical report, that temporary marriages between white men and native women were common and carried no scandal: investigate such cases, she says, and you will generally find deceit and misrepresentation added to the other sins, and the woman a victim rather than a willing participant.',
        'The father would not have exposed himself to the contempt of his whole nation by selling a daughter to be any man\'s mistress. The connection was understood to be true and lasting; he was moved as much by the honour he thought it carried as by the presents.',
        'There were no ladies in the garrison at that time. Had there been, Juliette observes, the step would hardly have been ventured.',
        'The girl was torn from her lover and transferred from her father\'s lodge to the officer\'s quarters. Then he left the post, as he said, on furlough. Word came in time that he was married, and when he rejoined his regiment it was at another post.'
      ],
      cast: ['agathe', 'youngofficer', 'mmepaquette', 'juliette', 'paquette', 'rascaldaykauray'], offstage: [], pivotal: true
    },
    {
      id: 'p3s48', act: 'c4', chapter: 'XXXVII', chapterTitle: 'Agathe — Tomah',
      title: 'Her little brother', date: '1833',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Every tie was broken for her but the one to her child. She never went back to her father\'s lodge — being deserted, she felt she was dishonoured — and her whole ambition became to bring the child up like a white child, dressing it in the costume of the French children, bright calico with a matching cap trimmed in narrow black lace. It was a fine child, and the only time Juliette ever saw her smile was when someone praised or petted it. Even that she had to give up: while the family was at Green Bay and the Sauks were in the neighbourhood, the child was taken violently ill. Paquette\'s house, which was her home, was thronged with people and noisy, so John had a place prepared under the Agency roof where she could be quiet and the post physician could attend. Nothing could save it.',
      points: [
        'Her agony over it was described to Juliette as truly heart-rending, and the parting almost more than nature could bear. There were friends, not of her own nation or colour, who tried to comfort her.',
        'Did the father ever send a thought or an inquiry after the fate of his child, or of the young being whose life he had made dark and desolate? "We will hope that he did."',
        'Months after the child\'s death she came with several of the half-breed women to pay a visit of congratulation on the birth of the young Shaw-nee-aw-kee. Taking her "little brother\'s" soft tiny hand in her own, the tears stood in her eyes and she said some little words of tenderness that showed her heart was full — and Juliette could scarcely keep from mingling her own tears with them, thinking on all the sorrow and desolation that one man\'s selfishness had occasioned.'
      ],
      cast: ['agathe', 'juliette', 'babykinzie', 'agathechild', 'john'], offstage: ['youngofficer', 'mazzuchelli', 'mmepaquette'], pivotal: true
    },
    {
      id: 'p3s49', act: 'c4', chapter: 'XXXVII', chapterTitle: 'Agathe — Tomah',
      title: '"Stick!" "Stuck!"', date: 'February 1833',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'John and Lieutenant Hunter go down to Chicago with one or two others: the place has become so much of a town — it contains maybe fifty inhabitants — that the proprietors of Kinzie\'s Addition must lay out lots and open streets through their property, and this is done during the visit. Out on the ground with the surveyor, John\'s attention is caught by a very bright-looking boy in Indian costume hopping along beside the chainman and mimicking his cries of "Stick!" "Stuck!" Asking who he is, he learns to his surprise that the lad is the brother of the old family servants Victoire, Genevieve and Baptiste. Tomah has never worn anything but blanket and leggings and has always lived in a wigwam. Would he like to go to Fort Winnebago and learn to be a white boy? The idea pleases him very much; his mother gives her sanction; and he is packed into the wagon with the two gentlemen and their travelling gear.',
      points: [
        'Near the Aux Plaines, approaching Glode Laframboise\'s where he knows he will meet acquaintances, Tomah asks leave to get out and walk a little way.',
        'When the gentlemen next see him he is in full Pottawatomie costume. It is bitter winter weather, and he has put his uncomfortable native dress back on rather than let his old friends see him in a state of transformation.'
      ],
      cast: ['john', 'hunter', 'tomah'], offstage: ['juliette', 'laframboise', 'victoire', 'genevieve'], pivotal: true
    },
    {
      id: 'p3s50', act: 'c4', chapter: 'XXXVII', chapterTitle: 'Agathe — Tomah',
      title: 'Ask Tomah — he will tell you', date: 'Spring 1833',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'Their first care is a complete wardrobe, put in a box in his sleeping room and placed under his own charge; words cannot express his delight, and every spare moment goes to contemplating it. Now and then Tomah is missing, and is invariably found sitting beside his little trunk folding and refolding the clothes, laying them now lengthwise, now crosswise, the happiest of mortals. The next step is to teach him to be useful — at which point it is noticed that whenever there is anything in the shape of work, Tomah slips off to bed, even before supper.',
      points: [
        'Given fish to scale at dusk he retires as usual, and has to be sent for. Told in Pottawatomie that there are some fish and they want him to scale them: "Now? It is very late." Miss Rolette, who understands the language, bursts out laughing at the simplicity of it and the rest join in; Tomah looks a little indignant, then, learning that it is the white custom to scale fish at night and put salt and pepper on them, is soon reconciled to his duty.',
        'The best china is used only for company, and the best teaspoons live in a locked bureau drawer upstairs with the key under a small clock on the mantelpiece. The next time visitors are expected Juliette explains that the good china must be used — and walks through the dining-room to find the company silver already on the table. He got it where it was kept. Was the drawer open? No, he opened it with a key. Was the key in the drawer? No, it was under that thing on the shelf. How did he know? That Mr. Tomah declined to say.',
        'Nobody ever saw him in that part of the house, and yet there was hardly an article he did not know the whereabouts of. If anyone was puzzled to find a thing it was always "Ask Tomah — he will tell you."',
        'At the tea-party for all the families and young officers he is given a white apron with long sleeves and acquits himself to perfection, never having any difficulty in imitating what he sees another do. Afterwards Lieutenant Van Cleve tells Juliette to look behind her: there sits Tom between two of the company, apron smoothed down, hands clasped, listening to the music on the best possible terms with himself and all around him. It is voted unanimously that he may stay and enjoy the pleasures of society for one evening — and, with characteristic restlessness, he gets tired the moment the music stops and takes his leave unceremoniously.'
      ],
      cast: ['tomah', 'juliette', 'john', 'missrolette', 'vancleve', 'eleanor', 'josettegirl', 'mary', 'julian', 'edwin'], offstage: [], pivotal: false
    },
    {
      id: 'p3s51', act: 'c4', chapter: 'XXXVIII', chapterTitle: 'Conclusion',
      title: 'The road to the Portage', date: 'Spring 1833',
      place: 'The Portage', placeShort: 'The Portage',
      summary: 'What they had long anticipated of the sufferings of the Indians begins to show itself as spring draws on, and they learn its extent from the little parties who come in begging for food. The Agent issues occasional rations as long as it is possible, but the Commissary\'s stores are so reduced that Colonel Cutler cannot justify anything beyond a scanty relief in extreme cases. The household has used the greatest economy all winter, even buying sour flour condemned by the commissary and making a very palatable bread of it with plenty of saleratus and a due proportion of potatoes. But having given to party after party as they came, the time arrives when they have nothing to give.',
      points: [
        'The half-breed families, who shared as long as their own stock lasted, are obliged to refuse too, and come instead to lament with the Kinzies over the accounts from the wintering grounds.',
        'It had been a very open winter with scarcely enough snow at any time to track deer — and the game had all been driven off by troops and war-parties scouring the country the preceding summer.',
        'They hear of people dying by companies of pure starvation, and lying stretched in the road to the Portage as they tried to drag their exhausted frames toward it. Soup made of slippery-elm bark, or stewed acorns, is all many have had for weeks.',
        'The Agency itself is now drawing daily rations from the garrison — there is no possibility of obtaining a barrel of flour at a time. After every meal Juliette goes into the pantry and carefully collects every remaining particle of food to set aside for the applicants who constantly throng the house.'
      ],
      cast: ['juliette', 'john'], offstage: ['cutler', 'mmepaquette'], pivotal: true
    },
    {
      id: 'p3s52', act: 'c4', chapter: 'XXXVIII', chapterTitle: 'Conclusion',
      title: 'The dish that came back untasted', date: 'Spring 1833',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'One day, while Juliette is at that work in the pantry, a face she once knew well appears at the window: the pretty daughter of the elder Day-kau-ray, who used to visit often and watch with great interest whatever was being done — the sewing, the weeding and cultivating of the garden, the reading. Juliette had tried many times to give her some idea of reading, showing her the plates in the Family Bible and doing her best to explain them; but she had quite lost sight of her lately. Now she is changed and wan. To the ordinary greeting — "Tshah-ko-zhah?", what is it — she gives a sigh that is almost a sob. She does not beg. Her face speaks volumes.',
      points: [
        'Juliette hands her the dish, expecting her to devour it eagerly. Instead she takes it, makes a sign that she will soon return, and walks away.',
        'When she brings it back, Juliette is almost sure she has not tasted a morsel herself.'
      ],
      cast: ['juliette', 'daykauraydaughter'], offstage: ['daykauray'], pivotal: true
    },
    {
      id: 'p3s53', act: 'c4', chapter: 'XXXVIII', chapterTitle: 'Conclusion',
      title: '"If his people could not be relieved"', date: 'Spring 1833',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'They are soon obliged to keep the doors and windows fast to shut out a misery they cannot relieve. If a door is opened to let a member of the family in, some wretched mother rushes in with it, takes the hand of Juliette\'s infant, places her own famishing child\'s hand inside it and tells them pleadingly that he is imploring his little brother for food. It is in vain that they screen the lower half of the windows with curtains: they climb up outside, and tier upon tier of gaunt faces peer in over the top to watch and see whether the family really is as ill provided as it says.',
      points: [
        'The noble old Day-kau-ray comes down from the Barribault to report his village: more than forty of his people have now gone many days on nothing but bark and roots. John takes him to the commanding officer to tell it himself and find out what can be had.',
        'The result is the promise of a small allowance of flour, enough to relieve the cravings of his own family. When this is explained to him the chief turns away. If his people could not be relieved, he said, he and his family would starve with them — and he refuses, for those nearest and dearest to him, until all can share alike.'
      ],
      cast: ['daykauray', 'john', 'juliette', 'babykinzie'], offstage: ['cutler'], pivotal: true
    },
    {
      id: 'p3s54', act: 'c4', chapter: 'XXXVIII', chapterTitle: 'Conclusion',
      title: 'The boats are in sight', date: 'Spring 1833',
      place: 'The Portage', placeShort: 'The Portage',
      summary: 'The announcement that the boats are in sight is a thrilling and most joyful sound. Hundreds of people assemble on the bank to watch them come, and their slow approach by the winding course of the river through the open prairie is torture to everyone looking on. As the first boat touches the land, the watchers at the house can scarcely keep from laughing: old Wild-Cat — somewhat fallen off in his huge amount of flesh — seizes the Washington Woman in his arms and hugs and dances with her in the ecstasy of his delight.',
      points: [
        'Their Father signs to them all to fall to with the hatchets they have long held ready, and in an incredibly short time barrel after barrel of corn is broken open and emptied, the little children carrying off pans and kettles full to the fires blazing round about to parch and cook what they have seized.',
        'From that time forward there is no more destitution. Supplies for the Commissary\'s department arrive immediately after, and, refreshed and invigorated, the people go back to their villages to get their crops ready for the coming season.'
      ],
      cast: ['wildcat', 'washingtonwoman', 'john', 'juliette'], offstage: [], pivotal: true
    },
    {
      id: 'p3s55', act: 'c4', chapter: 'XXXVIII', chapterTitle: 'Conclusion',
      title: 'Coffee, and the man in the doorway', date: 'Spring 1833',
      place: 'The Agency', placeShort: 'The Agency',
      summary: 'In the course of the spring the Rev. Mr. Kent and Mrs. Kent visit from Galena, and the large parlour of the hospital is fitted up for the first service ever preached at Fort Winnebago according to the Protestant faith — after nearly three years without a public service of praise and thanksgiving, they say gladly to one another, "Let us go to the house of the Lord!" They take it as an omen of better times, and the little sewing society works with renewed industry toward a fund that might one day secure a missionary permanently. Not long after, on a fine spring morning at breakfast, a party of Indians comes into the parlour. Two pass through onto the portico; the third stands in the doorway nearly opposite Juliette, and, in spite of his changed dress and the paint covering him, she knows him at once.',
      points: [
        'She goes on pouring the coffee and says to her husband, "The one behind you, with whom you are speaking, is one of the escaped prisoners."',
        'Without turning his head John goes on listening to their directions about the guns and traps they want left for the blacksmith, then turns carelessly toward the door and answers the man speaking to him. When he addresses her again it is to say: "You are right, but it is no affair of ours. We are none of us to look so as to give him notice that we suspect anything. They are undoubtedly innocent, and have suffered enough already."',
        'Contrary to his usual custom their Father does not ask their names. He writes out their directions, ties them to their implements, and sends them to deliver them to M. Morrin themselves.',
        'The rest of the circle are greatly pleased at the young fellow\'s audacity, and quite long to tell the officers that they could have caught one of their fugitives for them if they had had a mind.'
      ],
      cast: ['juliette', 'john', 'escapedprisoner', 'kent', 'mrskent'], offstage: ['morrin', 'prisoners'], pivotal: true
    },
    {
      id: 'p3s56', act: 'c4', chapter: 'XXXVIII', chapterTitle: 'Conclusion',
      title: '"I never, never, never shall I find such friends again"', date: '1 July 1833',
      place: 'The Portage', placeShort: 'The Portage',
      summary: 'The time comes when they begin to think seriously of leaving their pleasant home and taking up residence at Detroit while arrangements are made for a permanent settlement at Chicago. The news brings out great lamentations from their Winnebago children, who come flocking in from the surrounding country to ask whether the tidings are true and to petition earnestly that the Kinzies will go on living and dying among them.',
      points: [
        'No one seems so overwhelmed as Elizabeth, the Cut-Nose, who sits for hours in one spot wiping the tears down her cheeks with the corner of the chintz shawl pinned across her bosom. "No! I never, never, never shall I find such friends again. You will go away, and I shall be left here all alone."',
        'Wild-Cat — the fat, jolly Wild-Cat — gives way to the most audible lamentations, insisting on taking the baby on his fat dirty knee on the morning of the departure: "Oh, my little brother, you will never come back to see your poor brother again!" Having taken an extra glass on the occasion, he weeps like an infant.',
        'On the morning of the 1st of July they bid adieu to the long train that follows them down to the boat waiting to take them to Green Bay, where they are to meet Governor Porter and Mr. Brush and go on under their escort to Detroit.',
        'The farewells finished, the crowd turns to walk with their Father across the Portage on his road to Chicago — and long afterwards the Kinzies can still see them winding along the road, and hear their loud lamentations at a parting they foresee will be forever.'
      ],
      cast: ['juliette', 'john', 'cutnose', 'wildcat', 'babykinzie', 'eleanor', 'margaret', 'edwin', 'julian'], offstage: ['porter', 'daykauray', 'tomah', 'agathe'], pivotal: true
    }
  ],
  outline: [],
  leads: ['juliette', 'john', 'daykauray', 'whitecrow', 'youngfourlegs']
};
