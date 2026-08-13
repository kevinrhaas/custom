/* Wau-Bun — Part 1: Journey West (September 1830 – March 1831).
   Chapters I–XVII of Juliette Kinzie's narrative, broken into scenes.
   Each scene records where it happens, what happens, the pivotal turns, and
   exactly who is on stage: `cast` = present in the scene, `offstage` = spoken
   of, remembered, or acting at a distance. The chart derives first/last
   appearances from these lists — nothing is hand-numbered. */
var WAUBUN_PART1 = {
  id: 'part1',
  number: 1,
  title: 'Journey West',
  range: '1830 – March 1831',
  chapters: 'Chapters I–XVII',
  status: 'complete',
  blurb: 'Newlywed Juliette Kinzie leaves Detroit for the remote Northwest, travelling through Mackinac and Green Bay to Fort Winnebago. After a winter among soldiers, traders, settlers and Ho-Chunk communities, she undertakes a dangerous overland journey across Wisconsin and Illinois. The part ends with Juliette arriving in tiny Chicago.',
  acts: [
    { id: 'a1', title: 'The Lakes', sub: 'Detroit → Green Bay', note: 'September 1830' },
    { id: 'a2', title: 'Up the Fox', sub: 'Green Bay → the Portage', note: 'October 1830' },
    { id: 'a3', title: 'The Winter Post', sub: 'Fort Winnebago', note: 'Oct 1830 – Mar 1831' },
    { id: 'a4', title: 'Overland', sub: 'The Portage → Chicago', note: 'March 1831' },
    { id: 'a5', title: 'Chicago', sub: 'What she found there', note: '1831 · and how it began' }
  ],
  scenes: [
    /* ---------------- Act 1 — The Lakes ---------------- */
    {
      id: 's1', act: 'a1', chapter: 'I', chapterTitle: 'Departure from Detroit',
      title: 'The Henry Clay casts off', date: 'A dark, rainy evening, September 1830',
      place: 'Detroit', placeShort: 'Detroit',
      summary: 'Juliette and John Kinzie board the steamer Henry Clay for Green Bay, congratulated by every friend in Detroit on being spared the little schooners — one relative once took three months to reach Chicago. They ride to the quay in a cart, the only vehicle that can navigate the unpaved streets, and descend a perpendicular stairway into the Ladies\' Cabin. For a day it is delightful: officers among the passengers, books, reading aloud, cigars and euchre.',
      points: [
        'Juliette is not merely visiting the "Indian country" — she is going to live in the land that has been her region of romance since childhood.',
        'The frontier is measured in delays: three months for a journey a sail-vessel can sometimes make in four days.'
      ],
      cast: ['juliette', 'john'], offstage: [], pivotal: true
    },
    {
      id: 's2', act: 'a1', chapter: 'I', chapterTitle: 'Departure from Detroit',
      title: 'Storm on Thunder Bay', date: 'Days later, September 1830',
      place: 'Lake Huron', placeShort: 'Lake Huron',
      summary: 'Thunder Bay lives up to its name. Rain drives through every seam of the deck, saturating carpet and bedding, and the ladies are driven first into the Gentlemen\'s Cabin and then into the berths, where they spend the livelong day and are served dinner on their pillows. The gentlemen sit under raised umbrellas telling amusing anecdotes until, at nine in the evening, word comes that they have reached the pier at Mackinac.',
      points: ['The first lesson of the journey: the discomfort you prepared for is never the discomfort that arrives.'],
      cast: ['juliette', 'john'], offstage: [], pivotal: false
    },
    {
      id: 's3', act: 'a1', chapter: 'I', chapterTitle: 'Departure from Detroit',
      title: 'A haven at the Stuarts\'', date: 'Night of arrival, Mackinac',
      place: 'Mackinac Island', placeShort: 'Mackinac',
      summary: 'Robert and Mrs. Stuart receive the drenched travellers with affectionate cordiality into a house where they have been expected for days. A bright fire, kind faces, and then the servants assembled, the chapter of God\'s word read, the hymn chanted, the prayer offered, before the guests are conducted to their rest.',
      points: ['Juliette declines to attempt a portrait of Robert Stuart — an abler pen should write the biography of the head of the American Fur Company.'],
      cast: ['juliette', 'john', 'stuart', 'mrsstuart'], offstage: [], pivotal: false
    },
    {
      id: 's4', act: 'a1', chapter: 'II', chapterTitle: 'Michilimackinac',
      title: '"Bon-jour, Monsieur John"', date: 'The following morning',
      place: 'Mackinac Island', placeShort: 'Mackinac',
      summary: 'Mackinac in the morning sun: the bay dotted with fishing canoes, Ottawa lodges scattered along the beach, and a shout of welcome as the inmates recognise Shaw-nee-aw-kee, known to every individual from a seven years\' residence. Canadian engagés trot up to pay their respects to "Monsieur John" and shower felicitations in an incomprehensible patois on "Madame John" — of which she understands only the hope that she will be happy in her vie sauvage.',
      points: [
        'Juliette meets her husband\'s other name for the first time; from here on he is Shaw-nee-aw-kee wherever they land.',
        'The Indians greet white men in French — a fashion learned from the traders, not a language of their own.'
      ],
      cast: ['juliette', 'john', 'voyageurs'], offstage: [], pivotal: true
    },
    {
      id: 's5', act: 'a1', chapter: 'II', chapterTitle: 'Michilimackinac',
      title: 'The mission school and the Fur Company', date: 'Morning, Mackinac',
      place: 'Mackinac Island', placeShort: 'Mackinac',
      summary: 'They visit the Presbyterian mission school, the beloved child of the island\'s small Protestant community and the particular interest of the Stuarts. Around it turns the whole northwest trade: Mackinac is the entrepôt where a hundred canoes at a time bring furs, maple sugar, wild rice and quill-work, and where the tribes buy the goods their British presents at Fort Malden do not include. Walking the white gravel road, Juliette is shown Madame Laframboise\'s house — the Ottawa woman who took over her murdered husband\'s trading posts and runs them herself.',
      points: [
        'Juliette records the philanthropic hope of the hour — that education and Christianity would raise "the red brethren" — and then, writing a quarter-century later, records what actually happened: the lands cajoled or wrested away, the graves turned up by the ploughshare.',
        'This is the book\'s first sustained note of elegy, and it is set down at the height of the trade\'s prosperity.'
      ],
      cast: ['juliette', 'john', 'stuart', 'mrsstuart', 'ferry'], offstage: ['laframboise'], pivotal: true
    },
    {
      id: 's6', act: 'a1', chapter: 'II', chapterTitle: 'Michilimackinac',
      title: 'Dinner at the Mitchells\'; the Big Turtle recedes', date: 'Two o\'clock, Mackinac',
      place: 'Mackinac Island', placeShort: 'Mackinac',
      summary: 'With her head aching from the boat, Juliette dines at Mr. Mitchell\'s and is struck by his wife — part French, part Sioux, once the belle of Fort Crawford — and by the soft musical voice she will come to recognise. A visiting lady asks whether she does not dread the entire deprivation of religious privileges in so distant a home; Juliette answers that she will have her Prayer-Book. Then the bell sounds, and Mackinac slides astern in its perfect outline: Mich-i-li-mack-i-nac, the Big Turtle.',
      points: [
        'The Prayer-Book answer is planted deliberately — it is called back on the worst night of the journey.',
        'Point St. Ignace and old Mackinac pass in view, with the story of the ball game that took the old fort in the days of Pontiac.'
      ],
      cast: ['juliette', 'john', 'mitchell'], offstage: ['stuart', 'mrsstuart'], pivotal: false
    },
    {
      id: 's7', act: 'a1', chapter: 'II', chapterTitle: 'Michilimackinac',
      title: 'Aground on the flats', date: 'Night, late September 1830',
      place: 'Below Green Bay', placeShort: 'Green Bay flats',
      summary: 'Equinoctial weather catches them again at the mouth of Green Bay and the little steamer grounds fast and hard three miles below the settlement. Almost everyone prefers braving wind, rain and darkness in the open boat to another night cooped up, and in due time they reach the shore.',
      points: ['A week aboard has been enough; the passengers would rather row through a storm than stay.'],
      cast: ['juliette', 'john'], offstage: [], pivotal: false
    },
    {
      id: 's8', act: 'a1', chapter: 'III', chapterTitle: 'Green Bay',
      title: 'The crowded hotel, and General Root\'s dispatches', date: 'Night of arrival, Green Bay',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'They arrive in the middle of a treaty with the Menomonees and Waubanakees: commissioners, clerks, traders, claimants, travellers and idlers innumerable, all crammed into the only hotel. The landlady has turned her own family out of their quarters but contrives a little nook. Through a slight board partition, General Root — deaf, weak-eyed — has every dispatch read aloud twice by his secretaries at the top of their voices, and coughing and knocking over furniture does nothing to stop it.',
      points: ['Had the Kinzies been politicians, they would have had all the secrets of the working-men\'s party to make capital of.'],
      cast: ['juliette', 'john', 'root'], offstage: [], pivotal: false
    },
    {
      id: 's9', act: 'a1', chapter: 'III', chapterTitle: 'Green Bay',
      title: 'A somersault into the river', date: 'The next morning, Green Bay',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'The gentlemen row out to the grounded steamer for the luggage — not least the boxes of silver for the Winnebago annuities. Watching from the piazza, Juliette sees a passenger standing in the stern turn a complete somersault backward into the water. The party puts back to shore, and only when one of them steps out dripping and laughing does she recognise him as her own peculiar property. Then a vehicle drives up: Judge Doty has heard of their arrival and carries them off to his house, where Mrs. Doty receives them with sisterly kindness.',
      points: [
        'John treats it as a joke; Juliette thinks it rather a sad beginning of Western experience.',
        'The annuity silver — the thing the whole journey is built around — is nearly in the river before it leaves Green Bay.'
      ],
      cast: ['juliette', 'john', 'doty', 'mrsdoty'], offstage: [], pivotal: false
    },
    {
      id: 's10', act: 'a1', chapter: 'III', chapterTitle: 'Green Bay',
      title: 'The morning hymn below the window', date: 'First light, Green Bay',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'Juliette wakes in terror at a plaintive, monotonous chant rising and falling beneath her room — something wild and unearthly. John explains: it is the morning salutation of the Indians to the opening day. Some Menomonees given shelter in the kitchen have sung their unvarying hymn and gone back to sleep. Their listener does not.',
      points: ['"What a lesson did it preach to the civilized, Christianized world" — the first time Juliette measures her own people against her hosts and finds them wanting.'],
      cast: ['juliette', 'john'], offstage: [], pivotal: true
    },
    {
      id: 's11', act: 'a1', chapter: 'III', chapterTitle: 'Green Bay',
      title: 'The evening party — and the serpents', date: 'Evening, Green Bay',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'The whole circle of Green Bay society is assembled to do honour to the strangers. Mr. and Miss Cadle call, full of anticipation for a school and chapel not yet built. M. Rolette\'s famous mid-lake conversation is retold — the new house, the chimney, the harvest, the mill, the horse Whip, all satisfactorily gone over before he thinks to shout after the departing boat, "And how are Madame Rolette and the children?" Then the Miss Grignons, hearing Juliette\'s impatience to see her new home, open a wholly new field of apprehension: "Vous n\'avez donc pas peur des serpens?"',
      points: ['Rattlesnakes and copperheads at the Portage, "all sorts" — the first thing about her new home Juliette learns from someone who has been there.'],
      cast: ['juliette', 'john', 'doty', 'mrsdoty', 'cadle', 'grignons'], offstage: ['rolette'], pivotal: false
    },
    {
      id: 's12', act: 'a1', chapter: 'III', chapterTitle: 'Green Bay',
      title: 'A real Western hop', date: 'Before departure, Green Bay',
      place: 'Green Bay', placeShort: 'Green Bay',
      summary: 'Everybody on Green Bay gathers at Mrs. Baird\'s: desks cleared from the office wing for dancing, the young officers up from Fort Howard in uniform, long-hoarded finery brought to light, even the kitchen made fit for company in case a visitor prefers to sit and smoke there. A clumsy little man waddles over to introduce himself to Juliette without ceremony, then turns to a beautiful woman nearby and tells her she is the prettiest in the room and dances the handsomest — such is the penalty of being too charming. Meanwhile Captain Harney\'s boat arrives, the mess-basket is stowed, three voyageurs are engaged, and a messenger is sent ahead to the Kakalin for Wish-tay-yun.',
      points: [
        'Society in a new country: the number of the company matters more than the quality, and the good humour is genuine.',
        'The expedition up the Fox is assembled here — boat, crew, provisions, and the best guide on the river bespoken in advance.'
      ],
      cast: ['juliette', 'john', 'doty', 'mrsdoty', 'harney', 'grignons'], offstage: ['wishtayyun'], pivotal: false
    },

    /* ---------------- Act 2 — Up the Fox ---------------- */
    {
      id: 's13', act: 'a2', chapter: 'IV', chapterTitle: 'Voyage up Fox River',
      title: 'Pousse au large — the boat, the piano, and the silver', date: 'A bright morning, October 1830',
      place: 'Fox River', placeShort: 'Fox River',
      summary: 'A thirty-foot Mackinac boat with a canvas roof like a stage-coach, a crew of soldiers and three voyageurs. Amidships stands the box holding Juliette\'s piano, with a mattress on top for a divan by day and a bed by night; next to it the boxes of annuity silver; then the mess-basket and two covered baskets bought from the New York Indians. Judge Doty rides with them as far as Butte des Morts, an admirable companion with a vast fund of anecdote — Réaume the justice who settled a suit by fining both parties a load of hay and a load of wood, and Old Boilvin of Prairie du Chien, who tried a soldier by shaking his fist at him and inviting the company to take a little quelque-chose.',
      points: [
        'The Canadians sing to keep the oars in time, and measure the river not in miles but in pipes — a stop to rest and smoke every five or six miles.',
        'Juliette sees a gentleman in a coloured shirt for the first time in her life, and finds her divan pillows in patchwork.'
      ],
      cast: ['juliette', 'john', 'doty', 'harney', 'voyageurs', 'kilgour'], offstage: [], pivotal: false
    },
    {
      id: 's14', act: 'a2', chapter: 'IV', chapterTitle: 'Voyage up Fox River',
      title: 'The Kakalin: "Bon-jour, maman"', date: 'Second morning on the river',
      place: 'The Kakalin rapids', placeShort: 'Kakalin',
      summary: 'The boat is poled and dragged up the Kakalin while Juliette is jolted round the portage in an ox-cart. At the head of the rapids their Menomonee guide comes forward to be presented: Wish-tay-yun, stalwart, open-faced, faintly roguish, who laughs "Bon-jour, bon-jour, maman." Surprised at the title, she learns from her husband what her position now is — that as the Agent he is "father" to the Winnebago by office and to the Chippewas, Ottawas, Potawatomi and others by courtesy, and that she is therefore their mother. As they push off, Mr. Marsh and the Rev. Eleazar Williams row over from the far bank for news from the east countrie.',
      points: [
        'Juliette is given her role in the story: mother to a very numerous and well-grown family.',
        'Asked what she means to do among them, she can claim no plan beyond general good-will and a hope of making them her friends.'
      ],
      cast: ['juliette', 'john', 'doty', 'wishtayyun', 'marsh', 'williams', 'voyageurs'], offstage: [], pivotal: true
    },
    {
      id: 's15', act: 'a2', chapter: 'IV', chapterTitle: 'Voyage up Fox River',
      title: 'Men overboard on the rapids', date: 'All that day',
      place: 'Fox River rapids', placeShort: 'The rapids',
      summary: 'A hard pull. Wish-tay-yun\'s voice is the bugle of the party; when the boat wedges between two stones and will not budge, every rower goes over the side into the water and walks her up by hand. Juliette, who has scarcely witnessed severe bodily exertion before, is appalled to see her husband change into duck trousers and jump in with them — and then take the oar of a delicate boy soldier who bleeds at the nose on any unusual effort. Thirteen miles are gained in the day.',
      points: [
        'The recruit "Gridley" is a name assumed; he deserts twice and his remains are found the next spring, dead of cold or starvation, not many miles from the fort.',
        'Juliette records his end mid-sentence and calls it a sad interlude — the frontier\'s casual arithmetic of loss.'
      ],
      cast: ['juliette', 'john', 'doty', 'wishtayyun', 'gridley', 'kilgour', 'voyageurs'], offstage: [], pivotal: false
    },
    {
      id: 's16', act: 'a2', chapter: 'IV', chapterTitle: 'Voyage up Fox River',
      title: 'First encampment at the Grande Chûte', date: 'Sunset, and the next day',
      place: 'Grande Chûte', placeShort: 'Grande Chûte',
      summary: 'Juliette jumps ashore before the boat is pulled up and hurries downstream with the Judge to sketch the falls before the light goes: red caps and belts, two tents, smoke rising, the portage path up the wooded bank. It is her first encampment and she is enchanted by everything. Next morning the men spend hours dragging the boat up the Chûte and carrying the lading hundreds of rods along the bank, while she wanders after wild flowers and finds the soldiers\' fire, where a tall red-faced recruit named Krissman is making soup and offers her a tin cup of it.',
      points: [
        'The camp routine that will carry the whole book is established here: the bourgeois\'s shout of "How! how! how!" at daybreak, the kettles, the broches, the tent struck and the pack-horse loaded — tout démanché.',
        'Krissman was recruited only last summer, rode horse on the canal, and expects to be a bugler soon — chiefly for the extra pay.'
      ],
      cast: ['juliette', 'john', 'doty', 'krissman', 'kilgour', 'voyageurs'], offstage: [], pivotal: false
    },
    {
      id: 's17', act: 'a2', chapter: 'V', chapterTitle: 'Winnebago Lake — Miss Four-Legs',
      title: 'Four-Legs\' village, and the bargain in the fever', date: 'A rainy October day',
      place: 'Entrance to Winnebago Lake', placeShort: 'Winnebago Lake',
      summary: 'They pass Four-Legs\' village — a picturesque cluster of huts on a green glade, empty, its people gone to their wintering grounds — and there take leave of Wish-tay-yun at the border of his country. With him the sunshine departs; rain shuts them under the canvas all day across the lake. To beguile the time John tells how, lying at Prairie du Chien in the worst of an ague, he was talked at by a chief of the Four-Legs family until he agreed to anything, including the man\'s handsome daughter. Months later she arrived and threw a pack of furs at his feet, and it took a large present of blankets and guns to marry her to one of her own people instead.',
      points: [
        'The young gentleman took care never to make his next bargain while in a fit of the ague.',
        'The lady on the Mississippi is still called by his name in derision to this day.'
      ],
      cast: ['juliette', 'john', 'wishtayyun', 'voyageurs'], offstage: ['fourlegs', 'missfourlegs', 'wildcat'], pivotal: false
    },
    {
      id: 's18', act: 'a2', chapter: 'VI', chapterTitle: 'Breakfast at Betty More\'s',
      title: 'Breakfast in Judge Law\'s tent', date: 'Morning, Butte des Morts',
      place: 'Butte des Morts', placeShort: 'Butte des Morts',
      summary: 'A tall mitiff messenger brings an invitation to breakfast from Judge Law, camped a few miles above. The river fills with canoes paddled by women who press bowls of fresh cranberries on the new mother and scramble laughing for the crackers Juliette tosses them. In the tent, seated on the ground around an Indian mat, the Judge demonstrates that fastidious nicety has not been left behind in the wilderness: finding something on his tin plate not quite to his liking, he hands it over his shoulder to be wiped, and the waiter polishes it furiously with a black silk handkerchief pulled from his bosom.',
      points: [
        'A hunter given a quantity of ammunition returns within the hour with fifty ducks; from here on the party never wants for game.',
        'These are the first Winnebago Juliette meets — loudly and joyously greeting their father and their new mother.'
      ],
      cast: ['juliette', 'john', 'doty', 'law', 'porlier', 'voyageurs'], offstage: [], pivotal: false
    },
    {
      id: 's19', act: 'a2', chapter: 'VII', chapterTitle: 'Butte des Morts — Lake Puckaway',
      title: 'The Hillock of the Dead, and farewell to the Judge', date: 'After breakfast',
      place: 'Butte des Morts', placeShort: 'Butte des Morts',
      summary: 'The mound takes its gloomy name from a battle so bloody that the Foxes abandoned the river they had given their name to and went to live among the Sauks. Juliette learns the French habit of naming every tribe for a peculiarity — the Chippewas Sauteurs for their agility, the Menomonees Folles Avoines for their wild rice, the Winnebago les Puans for the polecat fur they wear on their legs in war — so that a stranger is puzzled to classify his own acquaintances. Then Judge Doty rides off overland to hold court at Mineral Point, leaving behind a valuable lesson in taking things as one finds them.',
      points: ['Seventy miles by land from here to the Portage; one hundred and thirty by water, so serpentine is the river.'],
      cast: ['juliette', 'john', 'doty', 'voyageurs'], offstage: [], pivotal: false
    },
    {
      id: 's20', act: 'a2', chapter: 'VII', chapterTitle: 'Butte des Morts — Lake Puckaway',
      title: 'The same wigwams, an hour later', date: 'Two days on the river',
      place: 'The upper Fox', placeShort: 'Upper Fox',
      summary: 'Sketching a pretty group of wigwams from the boat, Juliette notices the sun creeping from behind her to her left, then ahead, then to her right. She begins a second drawing of a scene surprisingly like the first — and the shouts of laughter from the bank explain it: four miles of rowing have advanced them the width of one river bank. They sleep in the boat at Lake Puckaway to escape the mosquitoes, pass the lovely Lac de Boeuf, and then leave scenery behind for seventy miles of monotony, the oars fouling in wild rice, the river too narrow for the men to sing.',
      points: [
        'A Winnebago tradition holds that the Fox is the trail of a vast serpent that crossed from the Mississippi to the Lakes, and the little lakes are where it turned in its sleep.',
        'From Gleason\'s at Lake Puckaway they could have crossed to the Portage overland in three hours, had they owned a carriage.'
      ],
      cast: ['juliette', 'john', 'voyageurs'], offstage: ['gleason'], pivotal: false
    },
    {
      id: 's21', act: 'a2', chapter: 'VII', chapterTitle: 'Butte des Morts — Lake Puckaway',
      title: 'The fort in sight for two hours', date: 'Late October 1830',
      place: 'Approaching the Portage', placeShort: 'The Portage',
      summary: 'The white walls of Fort Winnebago appear above the low prairie and Juliette cries that they will be there in half an hour. Instead the river turns its back on the fort, runs out into the prairie, approaches the Agency buildings — Paquette the interpreter\'s house, the Frenchmen\'s dwellings, the government blacksmith shop kept for mending the Indians\' guns and traps free of charge — turns again, and tacks backward and forward for most of two hours before reaching the little landing where the whole party stands waiting.',
      points: ['The zigzag has one advantage, as the next chapter observes: on the Fox River no traveller can ever take his friends by surprise.'],
      cast: ['juliette', 'john', 'voyageurs'], offstage: ['paquette'], pivotal: false
    },

    /* ---------------- Act 3 — The Winter Post ---------------- */
    {
      id: 's22', act: 'a3', chapter: 'VIII', chapterTitle: 'Fort Winnebago',
      title: 'Arrival at Fort Winnebago', date: 'Late October 1830',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Major and Mrs. Twiggs, the younger officers, and John\'s brother Robert — "Bob" to every tribe — give a welcome only those who have come to a remote home in the wilderness can measure. The Major insists they take vacant quarters inside the fort instead of the Agency: Mrs. Twiggs has been without a companion of her own sex for four months and will not hear of a separation. A dinner has been prepared, and the whole circle sits down a merry company. Juliette is shown two large rooms on each of three floors, a bedstead ample for Og King of Bashan, and a fantastically carved closet-cupboard christened "a Davis" after the young lieutenant who designed it.',
      points: [
        'The bachelors who planned the quarters forgot closets entirely; the shelves of the substitute are too close together to admit a gravy-boat.',
        'From the promontory the fort looks down on the Fox on one side and, across two miles of meadow, the portage road to the Wisconsin — where government oxen haul the Indians\' canoes across.'
      ],
      cast: ['juliette', 'john', 'robert', 'twiggs', 'mrstwiggs'], offstage: [], pivotal: true
    },
    {
      id: 's23', act: 'a3', chapter: 'VIII', chapterTitle: 'Fort Winnebago',
      title: 'The funeral of Four-Legs', date: 'The day before their arrival, and after',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'A great concourse has been gathering for the annuity payment, and with the traders came liquor. Four-Legs, the great chief of the nation, could not stand this full tide of prosperity: unchecked by the presence of his Father, he carried his indulgence to such excess that he died within a few days. He was buried on the highest point of the hill opposite the fort with his guns, tomahawk, pipes and tobacco, a vermilion-painted stake of hieroglyphics at his head and tamarack pickets around him. The Kinzies arrive one day too late for the ceremonies — in time only to furnish the white cotton for the flag over the grave and settle the sutler\'s bill, it being a duty expected of their Father to bury the dead suitably.',
      points: [
        'Drums, lamentation, whoops and the plaintive Indian love-flute go on all day and all night: "grief and whiskey had made their hearts tender."',
        'The chief of the nation is killed by the trade that the payment brings — the first plain accounting of the cost in these pages.'
      ],
      cast: ['juliette', 'john', 'twiggs'], offstage: ['fourlegs'], pivotal: true
    },
    {
      id: 's24', act: 'a3', chapter: 'VIII', chapterTitle: 'Fort Winnebago',
      title: 'The calico wrapper, and the widow', date: 'Early the following morning',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Juliette finds the next room full of squaws seated on the floor in attitudes of condolence around a little woman with blackened face and dishevelled hair, sobbing bitterly. Taking her wretched appearance for destitution, Juliette fetches a pretty calico wrapper and presses her to put it on at once — at which the other women burst out laughing. John explains: this is Madame Four-Legs, the widow, who has a comfortable wardrobe at home, and neglected dress and a blackened face are the etiquette of mourning.',
      points: [
        'Juliette\'s first attempt at kindness across the gap misfires entirely — and she records it against herself.',
        'The widow is no ornament to her husband\'s memory but a power in her own right: a Fox woman who speaks Chippewa, the court language of the tribes, and who counselled her husband on every occasion.'
      ],
      cast: ['juliette', 'john', 'mmefourlegs'], offstage: ['fourlegs'], pivotal: false
    },
    {
      id: 's25', act: 'a3', chapter: 'VIII', chapterTitle: 'Fort Winnebago',
      title: 'The chiefs call on their new mother', date: 'After breakfast',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'The principal chiefs put on their best clothing and paint to receive her: Naw-kaw the Walking Turtle, now principal chief; old Day-kau-ray, the most noble and dignified man of his own or any tribe; surly Black-Wolf with his loose black hair; Talk-English, who got his name by shouting the phrase at a stranger on the Lockport canal lock; Hoo-wau-ne-kah the Little Elk, picked out by Henry Clay as the ablest of the Washington deputation; jolly Wild-Cat; White Crow of Rock River with the black silk handkerchief over his lost eye; young Four-Legs the Dandy with his mirror and feather fan; and old Pawnee Blanc, who outdoes them all in finery. They seat themselves on the parlour floor with their long pipes, and Juliette thinks of her carpet. Then the interpreter\'s wife and all the Frenchwomen come, and the piano — unpacked and, thanks to Nunns and Clark, not a note out of tune — astonishes them: "Quelles inventions! Quelles merveilles!"',
      points: [
        'The whole leadership of the nation is introduced in a single scene; several of them return in Part 3, and White Crow becomes a friend of the whites in the Sauk war.',
        'One Frenchwoman spots Juliette\'s fingers reflected in the nameboard and triumphantly announces she has found the hidden machinery.'
      ],
      cast: ['juliette', 'john', 'nawkaw', 'daykauray', 'blackwolf', 'talkenglish', 'hoowaunekah', 'wildcat', 'whitecrow', 'youngfourlegs', 'pawneeblanc', 'paquette'], offstage: [], pivotal: true
    },
    {
      id: 's26', act: 'a3', chapter: 'IX', chapterTitle: 'Housekeeping',
      title: 'The boats, the mahogany, and Louisa', date: 'A week later',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Word that the furniture boats are in sight creates a sensation, and every off-duty officer and soldier goes down to the landing. Water pours out of the corners of the boxes; not a piece of mahogany has its veneer left; poor Hamilton Arndt is loud in his excuses. Rubbed down and set up beside the piano, the parlour is nevertheless pronounced magnificent. Failing to find a servant willing to come so far, Juliette accepts Major Twiggs\'s offer of Louisa, an uncommonly handsome young woman with a very demure face who calls herself fifteen and is certainly older.',
      points: [
        'Arndt\'s report of the piano at Green Bay: "There it stood on its four legs! Anybody might go up and touch it!"',
        'Juliette\'s first dinner in her own house is ambushed by six unexpected guests, including M. Rolette — and saved by a venison pasty of unusual proportions.'
      ],
      cast: ['juliette', 'john', 'mrstwiggs', 'twiggs', 'arndt', 'louisa', 'rolette', 'hempstead'], offstage: [], pivotal: false
    },
    {
      id: 's27', act: 'a3', chapter: 'X', chapterTitle: 'Indian Payment — Mrs. Washington',
      title: 'The payment: bundles of sticks and a last-day carouse', date: 'Autumn 1830',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Between four and five thousand Winnebago come in from Lake Winnebago, Green and Fox Lakes, the Barribault, Mud Lake, the Four Lakes, Kosh-ko-nong and Turtle Creek to receive fifteen thousand dollars. Each head of a lodge presents a bundle of sticks to be registered — so many men, so many women, so many children — and now and then two sticks are left over and the culprit vanishes amid the jeers of companions delighted by any roguery they had no share in. The chiefs, when the last band is paid, offer silver from the box to reimburse the young officers for their trouble, and are genuinely disturbed at the refusal. Whiskey finds its way into the lodges despite every prohibition, the women hide the guns and knives, and the last day of the payment is invariably one of general carousing.',
      points: [
        '"Where there is a demand there will always be a supply, let the legal prohibitions be what they may."',
        'Pawnee Blanc appears in a new blue coat with gold lace and a ribboned spear, receiving a visit of state — and is helped home from a ditch at the end of the day, coat muddied, hat battered, weeping.',
        'The one time Juliette ever sees the rule of equal sharing broken: Pawnee Blanc looks into the pitcher of raspberry negus, sets down the tumbler, and drinks from the pitcher with both hands.'
      ],
      cast: ['juliette', 'john', 'pawneeblanc', 'nawkaw', 'daykauray', 'rolette'], offstage: [], pivotal: true
    },
    {
      id: 's28', act: 'a3', chapter: 'X', chapterTitle: 'Indian Payment — Mrs. Washington',
      title: 'Mrs. Washington and the shell', date: 'During and after the payment',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Among the women is the wife of Yellow Thunder, known since the deputation to the President as the Washington woman, who greets Juliette with the air of one who has also seen something of the world and declines to exclaim at anything — until a tropical shell held to her ear defeats her entirely. Weeks after the payment Juliette misses her favourite conch, a small dark-veined one. Then Mrs. Yellow Thunder reappears, unfolds a chintz shawl and lays the shell on the table: she had taken it to her village to show the people who did not come to the payment, and had not asked because she saw her mother liked it and was afraid she would say no.',
      points: [
        'Her earlier stroke of genius in the East: having learned that white people pay "two shinnin" at a door, she collected it herself — from everyone coming in, and again from everyone trying to leave.',
        'She is admonished that it is far from the custom of white people to tax their friends and visitors in this manner.'
      ],
      cast: ['juliette', 'john', 'washingtonwoman'], offstage: ['yellowthunder'], pivotal: false
    },
    {
      id: 's29', act: 'a3', chapter: 'XI', chapterTitle: 'Louisa — Day-kau-ray on Education',
      title: 'Winter, and the news from Chicago', date: 'Late 1830',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'The payment over, the Indians disperse to their wintering grounds and the traders depart with most of the silver. Life settles into the bugle-calls — reveille, sick-call, guard-mounting, the Old English Roast Beef for dinner, Lochaber No More at retreat. Sunday is when Juliette most misses the East: there is no one in the garrison to hold a service, and Louisa cannot be kept from watching inspection. Then Letendre arrives from Chicago with word that Dr. Wolcott is hopelessly ill. John is gone within hours with Petaille Grignon, refusing to take his wife at that speed; days later a second messenger brings news of the death. The winter closes in behind him — water freezing in the parlours, brandy congealing in the sideboard at twenty-five below.',
      points: [
        'Green timber quarters shrink and warp; stuffing cracks with cotton batting and pasting paper strips over them is the work of many a leisure hour.',
        'Two gun-barrels are sawn off and set in the hearth to cure the smoking chimney — which Uncle Ephraim assures Louisa are to be filled with powder and fired off on Christmas Day.'
      ],
      cast: ['juliette', 'john', 'louisa', 'letendre', 'petaille', 'ephraim', 'newhall', 'mrstwiggs'], offstage: ['wolcott'], pivotal: true
    },
    {
      id: 's30', act: 'a3', chapter: 'XI', chapterTitle: 'Louisa — Day-kau-ray on Education',
      title: 'Christmas: the crullers and the white salt', date: 'Christmas and New Year, 1830–31',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'The holidays bring the Ho-Chunk back, having learned the observance from their French neighbours. Juliette lays in beads, ribbons and combs, and has crullers and doughnuts fried — most of which the soldier Hancock carries off from the kitchen. The matrons seat themselves in a circle and each, offered the dish, pours the entire contents into the corner of her blanket, until Juliette sits down to deliberate. The cakes are then equitably divided among the whole company — but nobody eats. They rub the grated white sugar between their fingers and mutter. At last one wets a finger and tastes: "Tah-nee-zhoo-rah!" Knowing only brown maple sugar, they had taken it for salt.',
      points: ['A comedy of two households misreading each other in both directions on the same afternoon — and everybody laughing at the end of it.'],
      cast: ['juliette', 'john', 'louisa', 'mmefourlegs'], offstage: [], pivotal: false
    },
    {
      id: 's31', act: 'a3', chapter: 'XI', chapterTitle: 'Louisa — Day-kau-ray on Education',
      title: 'Day-kau-ray answers the schoolmasters', date: 'The holiday season, 1830–31',
      place: 'Paquette\'s house, the Agency', placeShort: 'The Agency',
      summary: 'Colonel Richard M. Johnson of Kentucky writes asking the Agent to persuade the Winnebago not only to send their children to an Indian school in that state, but to set aside part of their annuity to sustain it. The chiefs are in the neighbourhood for the holidays and assemble at Paquette\'s. The advantages of civilisation and education are laid out paragraph by paragraph, each answered with a unanimous "Humph!" Then the oldest and most venerable of them rises. The Great Spirit made the white man and the Indian, and did not make them alike: to one he gave a heart for peace, towns, houses, books; to the other a love of the woods and a free life. "If he had made us with white skins, and characters like the white men, then we would send our children to this school. As he has not seen fit to do so, we believe he would be displeased with us, to try and make ourselves different from what he thought good. I have nothing more to say. This is what we think. If we change our minds, we will let you know."',
      points: [
        'The single most quoted passage of the book, and the moral centre of Part 1: the answer is neither hostile nor ignorant, and it is final.',
        'Juliette sets it down without argument, and only observes that the Indians hold the arts and sciences to be the Great Spirit\'s own instruction to the white man, which it would be unbecoming to acquire irregularly.'
      ],
      cast: ['john', 'daykauray', 'paquette', 'nawkaw', 'hoowaunekah'], offstage: ['juliette'], pivotal: true
    },
    {
      id: 's32', act: 'a3', chapter: 'XI', chapterTitle: 'Louisa — Day-kau-ray on Education',
      title: 'Captain Harney and the brandied mince pie', date: 'Winter 1831',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'Juliette sends a mince pie to each of the young officers\' quarters, on the theory that a mess without a lady may be deficient in such delicacies. At Captain Harney\'s the pork and beans are excellent and the pie is served — whereupon the Captain pushes his plate back with a jerk and roars at his servant David, who if he understands anything on earth understands a mince pie, for filling this one with brandy. "Please, sir," says David modestly, "I did not make the pie — it is one Mrs. Kinzie sent as a present."',
      points: ['The Captain conjures John Kinzie earnestly to say nothing to his wife — an injunction lost sight of the moment he gets home — and does not dare call again until he is sure she has forgotten it.'],
      cast: ['juliette', 'john', 'harney'], offstage: [], pivotal: false
    },

    /* ---------------- Act 4 — Overland ---------------- */
    {
      id: 's33', act: 'a4', chapter: 'XII', chapterTitle: 'Preparations for a journey',
      title: 'Sulky comes back blind; the tailor sits down', date: 'January – early March 1831',
      place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
      summary: 'January buries the country — five or six feet on the level in the lead diggings. Sulky the express, weeks overdue and given up for dead, appears at last nearly blind from travelling in the snow, having lain three weeks in an Indian lodge; his account kills the plan for a winter sleigh journey, which the commanding officer had in any case sworn to stop with the sentinels. Lizzie Twiggs is born before January is out and becomes the joint property of both households. Then February softens, and by early March the roads look possible on horseback. A riding habit is indispensable and does not exist: the regimental tailor, having found a man in Company D to take his turn at the spit, sits cross-legged in stocking feet on a mat by the parlour window for three days, admiring their joint performance — Juliette cutting out, since he has never made a lady\'s habit and she has never made anything.',
      points: [
        'Mrs. Pillon, tidy and active, has replaced the unmanageable Louisa and provisions the expedition: biscuits, ham, tongues, salt pork, coffee roasted and ground, sugar cracked, isinglass cut to the size of a coffee-pot, all in cotton bags inside skin porches.',
        'The direct route by Kosh-ko-nong is impossible — the villages are empty and the ice is gone — so the party must go far south to Ogie\'s Ferry to cross the Rock River: six days instead of a straight run.',
        'Two men only: Plante as guide, on his assurance that he knows every mile; and young Pierre Roy. Horses: Le Gris for Juliette, Tom for John, Jerry for Plante, Souris and Brunet for the packs.'
      ],
      cast: ['juliette', 'john', 'sulky', 'twiggs', 'mrstwiggs', 'lizzie', 'tailor', 'pillon', 'plante', 'roy', 'paquette'], offstage: ['louisa'], pivotal: true
    },
    {
      id: 's34', act: 'a4', chapter: 'XIII', chapterTitle: 'Departure from Fort Winnebago',
      title: 'March 8: the ducking at Duck Creek', date: '8 March 1831',
      place: 'Duck Creek', placeShort: 'Duck Creek',
      summary: 'Major Twiggs repeats his warnings at the ferry to no effect; Juliette is resolute. The young officers escort them four miles to Duck Creek behind an ox-cart carrying a canoe. Beyond the creek lies a marsh, and Juliette — declining to sit flat in the bottom of the canoe as instructed — perches on the little trunk to balance it, at which the two greyhounds bound in on top of her and dogs, furniture and lady go into the deepest of the water. She is hauled out laughing by the collar of her cloak, and carried over the marsh on her husband\'s shoulders. Pillon, attempting to ride Jerry across, is shot headfirst into the water and waddles back puffing while the horse sensibly joins his companions.',
      points: [
        'Juliette set out in a straw bonnet and kid gloves, having laughed at the suggestion of blanket socks and a woollen capuchon.',
        'At the first camp her riding habit, hung over the log by the fire, freezes stiff enough to stand upright — "a dress out of which a lady had vanished in some unaccountable manner."',
        'She refuses to stop and dry properly, partly on principle and partly so their friends at the fort shall have nothing to laugh at.'
      ],
      cast: ['juliette', 'john', 'twiggs', 'plante', 'roy', 'pillon'], offstage: [], pivotal: false
    },
    {
      id: 's35', act: 'a4', chapter: 'XIII', chapterTitle: 'Departure from Fort Winnebago',
      title: 'March 9: the Four Lakes, and fifty miles to Morrison\'s', date: '9 March 1831',
      place: 'The Four Lakes → Blue Mound', placeShort: 'Four Lakes',
      summary: 'A Winnebago encampment on the first of the Four Lakes greets their father vociferously and makes the usual announcement — "I have no bread" — which for once cannot be answered, the party\'s own supply being uncertain. The morning is beautiful: matted lodges, blue smoke, bushes powdered with new snow, the lake sparkling almost at their feet. Then rolling prairie, snow-filled hollows, ponies floundering, deer roused by the greyhounds, and the Blue Mound in mid-afternoon with seven more miles still to go. At Morrison\'s, Juliette falls into her husband\'s arms as he lifts her from the saddle — "This will never do; tomorrow we must turn our faces toward Fort Winnebago again." Mrs. Morrison and Miss Elizabeth Dodge lay her on a small bed, chafe her hands and bring warm wine and water.',
      points: [
        'Fifty miles in a day on her first horseback journey; she talks her husband out of turning back at the supper table.',
        'Mrs. Morrison passed her first eighteen months in the country without speaking to a white woman — and turns out to share half of Juliette\'s Oneida County friends.'
      ],
      cast: ['juliette', 'john', 'plante', 'roy', 'morrison', 'dodge'], offstage: [], pivotal: false
    },
    {
      id: 's36', act: 'a4', chapter: 'XIV', chapterTitle: 'William S. Hamilton — Kellogg\'s Grove',
      title: 'Lost on the rolling prairie', date: '10–11 March 1831',
      place: 'Between the Blue Mound and the diggings', placeShort: 'The prairie',
      summary: 'The directions are obscure and the country has no landmarks: one elevation exactly like another, and the trail a narrow path sunk in the sod, invisible at a few rods\' distance. Within a few miles it is plain that Plante is profoundly ignorant of the country, and John takes the lead himself. They ride the livelong day over a prospect broken only by oblong pits like gigantic graves where men have dug for lead, too anxious to be tempted even by the prairie-wolves watching from the rises. They camp on a stony side-hill; in the night a blizzard snaps the tent poles and brings the whole weight of canvas and snow down on them, and John takes his men into the wood to cut new ones while Juliette holds the tent up on her shoulders.',
      points: [
        'No compass, no trail, and an air so thick with driving sleet that they often cannot tell where the sun is.',
        'Juliette ties her husband\'s silk handkerchief over her veil against particles that cut like a razor, and suffers intensely anyway.'
      ],
      cast: ['juliette', 'john', 'plante', 'roy'], offstage: [], pivotal: true
    },
    {
      id: 's37', act: 'a4', chapter: 'XIV', chapterTitle: 'William S. Hamilton — Kellogg\'s Grove',
      title: '"Une clôture!" — Hamilton\'s diggings', date: '11 March 1831',
      place: 'Hamilton\'s diggings', placeShort: 'The diggings',
      summary: 'A shout from the head of the file — a fence! — and then the crowing of a cock, which never sounded so sweet. The cabins are Hamilton\'s. Their host hesitates to present himself, unwilling that anyone acquainted with his family in the East should see him in his present mode of life; then he comes in and is as agreeable and polite as the son of Alexander Hamilton naturally would be. A horn calls in a dozen miners in fringed deerskin with hunting-knives in their belts, the roughest-looking men Juliette ever beheld, who all address him as "Uncle Billy". One lingers to question them about Fort Winnebago with such bitterness against his former officers that she is sure he is a deserter — and that some of them had better not set foot in the diggings. That night the landlady stretches a cord between the two beds and hangs her petticoats on it for a partition.',
      points: [
        'Hamilton lends them books to pass the storm — the most interesting being the biography of his father. "Could this illustrious man have foreseen in what a scene this book was to be one day perused?"',
        'A miner takes leave of them wishing they may never have occasion to return: "I pity a body when I see them making such an awful mistake as to come out this way, for comfort never touched this Western country."'
      ],
      cast: ['juliette', 'john', 'hamilton', 'plante', 'roy'], offstage: [], pivotal: false
    },
    {
      id: 's38', act: 'a4', chapter: 'XIV', chapterTitle: 'William S. Hamilton — Kellogg\'s Grove',
      title: 'Thirty miles at a gallop to Kellogg\'s', date: '12 March 1831',
      place: 'Kellogg\'s Grove', placeShort: 'Kellogg\'s',
      summary: 'Hamilton offers to see them to his next neighbour, the trifling distance of twenty-five miles, and proves a most desperate rider — down ravines and through narrow passes at a gallop, Juliette leaving fragments of her veil on the branches and once nearly sharing the fate of Absalom. They reach Kellogg\'s at three, having certainly ridden thirty. Mrs. Kellogg, proud to entertain a gentleman for whose family she once did needle-work, feeds them well and installs Juliette in a rocking-chair by the fire. Mr. Kellogg decides to come with them to Chicago and takes two days\' provisions, refusing to burden his horse further; John quietly has Mrs. Kellogg bake an extra bag of biscuits.',
      points: ['"It will be seen that we had reason to rejoice in our own foresight."'],
      cast: ['juliette', 'john', 'hamilton', 'kellogg', 'mrskellogg', 'plante', 'roy'], offstage: [], pivotal: false
    },
    {
      id: 's39', act: 'a4', chapter: 'XV', chapterTitle: 'Rock River — Hours of Trouble',
      title: 'Ogie\'s Ferry, and the boy in the ashes', date: '13 March 1831',
      place: 'Dixon\'s, on the Rock River', placeShort: 'Ogie\'s Ferry',
      summary: 'They reach the dark rapid Rock River at sunset to find the ferry reduced to a skiff, the large boat having gone downstream with the ice the week before. Juliette crosses with the saddles while John swims two horses alongside — and little Brunet, refusing to be outdone, takes to the water on his own responsibility. At Dixon\'s there is a glowing fire and a good supper, and against the chimney-piece a boy in calico shirt, blanket and leggings, making marks in the ashes and never looking up. He is John Ogie, fretting after his mother; some say she is dead. Long afterwards Juliette learns the truth — that she had fled an abusive husband to her own people, and that years later the boy and his brother made their way to her on the Upper Missouri, whither the government had removed the tribe from the shores of Lake Michigan.',
      points: [
        'Mr. Dixon\'s directions are the hinge of the whole journey: keep a little to the north and strike the great Sauk trail; get too far south and the Winnebago Swamp will keep you. "As for the distance, it is nothing at all to speak of."',
        'It was a motherless look, and it went to her heart — one of the few places where Juliette follows a minor character out of her own story and into what became of him.'
      ],
      cast: ['juliette', 'john', 'dixon', 'johnogie', 'kellogg', 'plante', 'roy'], offstage: [], pivotal: true
    },
    {
      id: 's40', act: 'a4', chapter: 'XV', chapterTitle: 'Rock River — Hours of Trouble',
      title: 'The wrong trail, and the empty village', date: '14–15 March 1831',
      place: 'East of the Rock River', placeShort: 'The wrong trail',
      summary: 'Six miles out they strike a trail bearing northeast. John thinks it too faint and too northerly for a road used yearly by a whole nation; Plante is positive, remembering the very rising ground where he shot ducks for supper the year before; Mr. Kellogg sides alternately with each. Plante is the guide, so Plante is followed — until the great bend of the river with its rocky bluffs proves him wrong. "By your leave, I will now play pilot myself." A day of marsh where the ice cuts the horses\' ankles, then blinding snow with no sun to steer by, then a deeply indented trail running north and south, and an argument in which John is outvoted, rides north a few miles, and then simply turns: "You may go north if you please. I am convinced the other course is right, and I shall face about — follow who will." Rounding a point of woods they come on an Indian village and shout with joy. No answering shout, no dog, nothing. The bark walls are stripped bare; the people are at their wintering grounds.',
      points: [
        'The party is now lost, out of provisions, and living on the biscuits John insisted on at Kellogg\'s.',
        'The Frenchmen ride in silence — they would as soon cut off their right hand as show opposition to the bourgeois once he has decided.',
        'Breakfast on the last morning is coffee and three crackers, which the rest of the party insist Juliette pocket for her dinner. Mr. Kellogg produces a piece of tongue and a slice of fruit-cake he has been saving for the lady, "for he saw how matters was a-going."'
      ],
      cast: ['juliette', 'john', 'plante', 'roy', 'kellogg'], offstage: ['dixon'], pivotal: true
    },
    {
      id: 's41', act: 'a4', chapter: 'XV', chapterTitle: 'Rock River — Hours of Trouble',
      title: 'The dog, the two women, and the very small canoe', date: '16 March 1831',
      place: 'The Fox River, below Wau-ban-see\'s village', placeShort: 'Fox River ford',
      summary: 'A broad rapid river bars the way with wigwams on the far bank and no way down the ice-piled shore; the men shout and only echoes answer. Then Juliette\'s horse — mortally afraid of Indians — begins to prance, a little dog runs out of the bushes barking, and in a hollow they find two women crouching out of sight, digging Indian potatoes. Their canoe is very small: one passenger at a time, lying flat in the bottom, an old woman kneeling at her head with the paddle and a girl of fourteen at her feet. From them John learns that the village upstream is Wau-ban-see\'s, and therefore that this is the Fox and they are some fifty miles from Chicago. Ferried over first and left alone on the bank, Juliette sits on a fallen trunk in the snow, looks across the dark water, and for the first time on the journey cries — not from hunger, cold or fear, but from hope deferred. The little squaw stands watching her with a pitying face, and Juliette dries her eyes and is ready for fresh adventures by the time the last horse is across.',
      points: [
        'Asked how far Chicago is, the woman assures him it is close by. "That means it is not so far off as Canada. We must not be too sanguine."',
        'The entire party\'s survival turns on two women who were hiding from them.'
      ],
      cast: ['juliette', 'john', 'canoewomen', 'plante', 'roy', 'kellogg'], offstage: ['waubansee'], pivotal: true
    },
    {
      id: 's42', act: 'a4', chapter: 'XVI', chapterTitle: 'Relief',
      title: 'The lodge in the Big Woods', date: '16 March 1831',
      place: 'Piché\'s Grove', placeShort: 'Piché\'s Grove',
      summary: 'Juliette enters an Indian lodge for the first time: four sticks squared for a hearth, new mats, bags of dried food hanging from the poles, a kettle on an iron chain. The woman\'s first words are the familiar "I have no bread"; when Juliette makes her understand that she has had no breakfast herself, the woman instantly ladles out a bowl of Indian potatoes, which hunger makes delicious. Two little girls watch in astonishment as she reads her Prayer-Book — they have plainly never seen a book. The master of the lodge bounds in from shooting ducks, listens quietly to his wife, and tells them where they are: the Big Woods, the river behind them the Fox, the road plain from Piché\'s. He advises them to camp for the day, a storm being on the way, and goes straight back out to shoot their dinner.',
      points: [
        'Juliette cuts two yards of scarlet ribbon for each of the little girls, and their mother ties a piece to each knot of hair.',
        'Had they been one hour later at the ford, the river would have been impassable and there would have been nothing for it but to stay and starve.',
        'The hurricane brings down at least fifty full-grown trees within view of the tent; in the morning they can barely thread their way out of the wood.'
      ],
      cast: ['juliette', 'john', 'grovefamily', 'plante', 'roy', 'kellogg'], offstage: [], pivotal: true
    },
    {
      id: 's43', act: 'a4', chapter: 'XVI', chapterTitle: 'Relief',
      title: 'Piché\'s, the Du Page, and Mr. Dogherty\'s doctrine', date: '17 March 1831',
      place: 'Piché\'s → the Du Page', placeShort: 'The Du Page',
      summary: 'Their host guides them out past the bee-trees the grove is famous for and trots off well paid. Piché\'s cabin is full of Indians and travellers but the master is away and there is nothing but a fire; a man in Quaker costume offers to escort them to Chicago. Mr. Dogherty entertains Juliette across a wide freezing prairie with a thorough schedule of his religious opinions — he is a good deal of a perfectionist and evidently regards himself as a living illustration of the doctrine. Both forks of the Du Page have to be chopped open with an axe, and at Hawley\'s a huge ham comes down off the rafters, a dozen eggs into the pan and a johnny-cake against a board before the fire, while the good woman stares at appetites she cannot account for.',
      points: [
        '"St. John says, He that is born of God doth not commit sin. Now, if I am born of God, I do not commit sin." Juliette is too cold and too weary to argue the point.',
        'On the east fork the ice is running in large cakes and only Jerry\'s height keeps her out of it.'
      ],
      cast: ['juliette', 'john', 'dogherty', 'hawley', 'plante', 'roy', 'kellogg', 'grovefamily'], offstage: [], pivotal: false
    },
    {
      id: 's44', act: 'a4', chapter: 'XVI', chapterTitle: 'Relief',
      title: 'Lawton\'s, twelve miles out', date: 'Nightfall, 17 March 1831',
      place: 'The Aux Plaines', placeShort: 'Aux Plaines',
      summary: 'The Aux Plaines is frozen and the house is on the far side; shouting brings out Mr. Weeks, who cuts the ice and brings a canoe over as the light fails. Lawton\'s proves carpeted and warm, quite in civilised style. Mrs. Lawton complains bitterly of the loneliness of her condition and of having been brought out into the woods, which was a thing she had not expected when she came from the East; she does not mean to wait for things to improve unless her husband invites some of her young friends out to make it agreeable.',
      points: ['Nobody asks Mrs. Lawton what she had expected of a wild, unsettled country — a courtesy Juliette extends and quietly declines to endorse.'],
      cast: ['juliette', 'john', 'lawton', 'weeks', 'dogherty', 'kellogg', 'plante', 'roy'], offstage: [], pivotal: false
    },
    {
      id: 's45', act: 'a4', chapter: 'XVI', chapterTitle: 'Relief',
      title: 'Chicago le Désiré', date: '18 March 1831',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'Twelve miles of open plain, and on its farthest verge two tall trees that John planted with his own hand as a boy, now grown into landmarks. They keep them in view the whole way. At the little tavern at Wolf Point the old landlady marvels at the weather — two days ago the river was open, and now it is frozen hard enough to cross on horseback. John will not risk the horses, so they leave them and walk the last half mile, first over the ice and then down the northern bank. Genevieve spots them and flies into the house crying, "Oh! Madame Kinzie, who do you think has come? Monsieur John and Madame John, all the way from Fort Winnebago on foot!" A messenger is sent to the garrison for the rest of the family, and for that day at least Juliette is the wonder and admiration of the whole circle, for the dangers she has seen.',
      points: [
        'The journey planned for six days has taken ten, the last four of them lost and hungry.',
        'The season\'s destination is not a place but a household: the mother, the sisters, the brother — the family the whole book will eventually go back in time to explain.'
      ],
      cast: ['juliette', 'john', 'genevieve', 'eleanor', 'margaret', 'wentworth', 'dogherty', 'kellogg', 'plante', 'roy'], offstage: [], pivotal: true
    },

    /* ---------------- Act 5 — Chicago ---------------- */
    {
      id: 's46', act: 'a5', chapter: 'XVII', chapterTitle: 'Chicago in 1831',
      title: 'The whole town, named house by house', date: '1831',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'Fort Dearborn stands behind high pickets with bastions at alternate angles, its buildings put up in 1816 — with wooden pins instead of nails, they say, by a captain whose patriotic economy he expected the government to thank him for. Two companies garrison it, most senior officers on furlough, the command fallen to Lieutenant Hunter. On the north bank, facing the fort, is the Kinzie mansion under its Lombardy poplars and two great cottonwoods; further along, the Agency House, called Cobweb Castle from its long bachelor occupancy, with its comical additions tacked on wherever a vacant spot could be found. At the forks — the Point — stands Mark Beaubien\'s pretentious white two-storey house with bright blue shutters, the admiration of Wolf Point, and his canoe ferry. Robinson and Billy Caldwell keep cabins nearby; the Clybourns have named their place New Virginia; four miles up the South Branch is Lee\'s Place, or Hardscrabble, where stirring events of 1812 took place. Juliette enumerates every white inhabitant of Chicago, and there are few enough to name.',
      points: [
        'The river then turned south behind the fort and joined the lake half a mile below; the harbour cut of 1833 and the piers would change the shoreline within two years of this description.',
        'Written for readers who will find these particulars uninteresting — and for those who come later to make Chicago their home, and will want to know what it was.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'robert', 'dearbornofficers', 'markbeaubien', 'jbbeaubien', 'billycaldwell', 'robinson', 'clybourn', 'wentworth'], offstage: [], pivotal: true
    },
    {
      id: 's47', act: 'a5', chapter: 'XVII', chapterTitle: 'Chicago in 1831',
      title: 'How Chicago began', date: 'c. 1726 – 1804',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'The name is disputed — some derive it from the polecat, some from the wild onion — but all agree it came from an old chief drowned in the stream in a very remote time; a French letter of 1726 already spells it Chica-goux. As for the settlement: "the first white man who settled here was a negro," the Indians say with great simplicity. Jean Baptiste Point de Sable, a native of St. Domingo, came about 1796, made the first improvements, and left for Peoria — possibly disgusted at not being made a chief. Le Mai took over his place and traded until John Kinzie Sen. bought him out in 1804, the same year Major Whistler built the first fort. From that parent post the elder Kinzie ran a web of trading houses — Milwaukie, Rock River, the Illinois and Kankakee, the Kickapoo country — each with its superintendent, its engagés and its train of pack-horses, all feeding furs back to Chicago and on to Mackinac.',
      points: ['For nearly twenty years, the military excepted, John Kinzie Sen. was the only white inhabitant of Northern Illinois.'],
      cast: ['juliette'], offstage: ['pointdesable', 'lemai', 'kinziesen'], pivotal: false
    },
    {
      id: 's48', act: 'a5', chapter: 'XVII', chapterTitle: 'Chicago in 1831',
      title: 'The boy who ran away to Quebec', date: 'c. 1774 and after',
      place: 'New York · Quebec · Detroit', placeShort: 'Quebec',
      summary: 'At ten or eleven, John Kinzie was at school at Williamsburg on Long Island when the Saturday messenger found the place in commotion: Johnny Kinzie was missing. Weeks passed; he was given up and mourned as lost. He had crossed to New York, found a sloop bound up the North River, and been taken in hand by a passenger who paid his way the whole distance to Quebec and left him a stranger in the streets. He wandered from shop to shop until he liked the face of a silversmith, and asked if he wanted an apprentice — "What can you do?" "Anything you can teach me." He stayed three years before his parents found him. The old family Bible records the other loss: "George Forsyth was lost in the woods 6th August, 1775" — a small half-brother who followed the servant boy toward the common at dusk, and whose remains an Indian found the next year, identifiable by his auburn hair and his little boots.',
      points: ['The same mother twice lost a child into that particular silence — once for three years, once for ever.'],
      cast: ['juliette'], offstage: ['kinziesen', 'eleanor'], pivotal: false
    },
    {
      id: 's49', act: 'a5', chapter: 'XVII', chapterTitle: 'Chicago in 1831',
      title: 'The voyageurs — and a door left open to 1812', date: 'The close of Part 1',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'Juliette closes with a portrait of the race that carried her up the Fox: engaged at Montreal for three years on a quart of lyed corn and two ounces of tallow a day, cheerfully wintering on fresh fish and maple sugar when supplies fail, holding an agreement binding to the letter — the man who was hired to steer a boat and not to chop wood, and was left to steer it in the ice at twenty below until he changed his mind. There is an aristocracy among them: the first-year mangeur-de-lard is despised by any hivernant, who will not even drink with him. And they turn every bourgeois\'s name into a joke — Kinzie becomes Quinze-nez, fifteen noses; Mr. Shaw becomes Monsieur le Chat, until his old foreman greets him in the Champ de Mars before two officers and asks after Madame la Chatte and all the kittens. So the family lived, cut off from the world with no society but the military, in great contentment; and the Indians returned their friendship with an attachment of no ordinary strength — "as was manifested during the scenes of the year 1812."',
      points: [
        'The last line of Part 1 is a hinge: the narrative stops going forward and turns back nineteen years.',
        'Everything Part 2 needs is now in place — the post, the family, the tribes, and the friendship about to be tested.'
      ],
      cast: ['juliette', 'voyageurs'], offstage: ['john', 'kinziesen', 'eleanor'], pivotal: true
    }
  ]
};
