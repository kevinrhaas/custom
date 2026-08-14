/* Wau-Bun — Part 2: The Early Frontier.
   Chapters XVIII–XXIII. The narrative stops going forward and turns back
   nineteen years, to the Fort Dearborn massacre of 15 August 1812 and its
   aftermath — and then back further still, to the Seneca captivity of
   1779–83 that made the woman at the centre of the Kinzie household.
   The 1831 frame (Juliette's two months at Chicago, where these stories were
   told to her) is part of the same chapters and is kept in its place here. */
var WAUBUN_PART2 = {
  id: 'part2',
  number: 2,
  title: 'The Early Frontier',
  range: '1779 – 1816 · told at Chicago, 1831',
  chapters: 'Chapters XVIII–XXIII',
  status: 'complete',
  blurb: 'The story jumps back to the world that created the Kinzies: the Great Lakes fur trade, Native nations, early settlers, and the beginnings of Chicago. Growing conflict culminates in the War of 1812 and the Fort Dearborn massacre, followed by captivity, survival, and the rebuilding of Fort Dearborn.',
  acts: [
    { id: 'b1', title: 'The Warning', sub: 'Fort Dearborn', note: 'April – 14 August 1812' },
    { id: 'b2', title: 'The Fifteenth of August', sub: 'The lake shore', note: '15 August 1812' },
    { id: 'b3', title: 'Prisoners of War', sub: 'St. Joseph → Detroit → Quebec', note: '1812 – 1816' },
    { id: 'b4', title: 'The Ship Under Full Sail', sub: 'The Seneca country', note: '1779 – 1783' },
    { id: 'b5', title: 'Leaving Chicago', sub: 'What Juliette saw there', note: 'Spring 1831' }
  ],
  scenes: [
    /* ---------------- Act 1 — The Warning ---------------- */
    {
      id: 'p2s1', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: '"The Indians! The Indians!"', date: 'Evening, 7 April 1812',
      place: 'The Kinzie house, Chicago', placeShort: 'Kinzie house',
      summary: 'The Kinzie children are dancing in front of the fire to their father\'s violin, the tea-table is laid, and they are waiting for their mother to come back from visiting a sick neighbour up the river. The door bangs open and she is in the room, white, barely able to get the words out: the Indians are at Lee\'s Place, killing and scalping. A man and a boy had come running down the far bank shouting the news to the Burns family before making for the fort. Within minutes the household is in two old pirogues moored by the house, paddling for the fort as hard as they can go.',
      points: [
        'Lee\'s Place — Hardscrabble — is a farm four miles up the south branch; the fort stands directly across the river from the Kinzie house, a few rods of sloping green turf on either side.',
        'This fort is not the one Juliette knew: two blockhouses on the south side, and on the north a sally-port running underground from the parade-ground to the river, to fetch water under siege or to get out.'
      ],
      cast: ['kinziesen', 'eleanor'], offstage: ['mrwhite', 'mrsburns'], pivotal: true
    },
    {
      id: 'p2s2', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'Seventy-five men, and a remark about corn-fields', date: 'Spring 1812',
      place: 'Fort Dearborn', placeShort: 'Fort Dearborn',
      summary: 'The garrison is Captain Heald commanding, Lieutenant Helm — John Kinzie\'s son-in-law — Ensign Ronan, and the surgeon Dr. Van Voorhees; about seventy-five men, few of them fit. Relations with the Potawatomi have been constant and friendly, even though their leading men still travel to Fort Malden every year for British presents, and even though Potawatomi and Winnebago fought at Tippecanoe the previous autumn. Everyone is comfortable. Then two Indians of the Calumet band, walking through the quarters, see Mrs. Heald and Mrs. Helm playing at battledore, and Nau-non-gee remarks to the interpreter that the white chiefs\' wives are amusing themselves very much — it will not be long before they are hoeing in our corn-fields.',
      points: [
        'It was taken at the time for an idle threat, or jealousy at the contrast between their women\'s lives and these. "Some months after, how bitterly was it remembered!"',
        'Juliette lists the warnings only in hindsight, which is the honest way to list them: nothing looked like a warning at the time.'
      ],
      cast: ['heald', 'mrsheald', 'helm', 'margaret', 'ronan', 'vanvoorhees', 'naunongee'], offstage: [], pivotal: false
    },
    {
      id: 'p2s3', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'The dog standing guard', date: '7–8 April 1812',
      place: 'Lee\'s Place', placeShort: 'Lee\'s Place',
      summary: 'Ten or twelve painted strangers had walked into the farmhouse that afternoon and sat down without ceremony. A Frenchman of the household said quietly that he did not like their look — by their dress and paint they were not Potawatomi. A discharged soldier told the boy to say nothing and do as he did, strolled down to the canoes, pointed at the cattle across the water as if to go and fodder them, and paddled over with the boy in the second canoe. They pulled hay, made a show of gathering the cattle, worked their way behind the haystacks and ran for the woods. A quarter of a mile on they heard two shots. Later that night a fishing party groping past the silent house finds a body in the enclosure, scalped and mutilated, with the dead man\'s dog still standing over him.',
      points: [
        'The commanding officer had fired a cannon to warn the fishing party in; the sound also decided the raiders — a party of Winnebago down from Rock River to take white scalps — to be satisfied with the one exploit and go home.',
        'In the morning Mr. White was found with two balls in him and eleven stabs in the breast. They were buried close by the fort.'
      ],
      cast: ['mrwhite'], offstage: ['heald'], pivotal: false
    },
    {
      id: 'p2s4', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'Ronan goes up the river for the Burns family', date: '7 April 1812',
      place: 'The Chicago River', placeShort: 'The river',
      summary: 'It occurs to the men who have just saved themselves that the Burns family is sitting exposed a mile upriver. The question is who will risk his own life to fetch them. Ensign Ronan volunteers, takes five or six soldiers up in a scow, and lifts the mother — with an infant scarcely a day old — bed and all into the boat, bringing the whole family down to the fort.',
      points: ['The first thing recorded of Ronan is that he went; the last thing recorded of him is how he died.'],
      cast: ['ronan', 'mrsburns'], offstage: [], pivotal: false
    },
    {
      id: 'p2s5', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'Barricaded, and the sheep let loose', date: 'April – July 1812',
      place: 'The Agency House', placeShort: 'Agency House',
      summary: 'The people living outside the pickets — discharged soldiers, half-breed families — fort up in the Agency House twenty rods west of the garrison: an old log building with a hall through the middle, its piazzas planked up, port-holes cut, sentinels posted at night. No one may leave the neighbourhood without a guard. One night a patrol walks into a party of Indians in the pasture; a thrown tomahawk misses the sergeant and sticks in a wagon, the blockhouse sentinel fires, and in the morning there is blood in the grass and a place where a body had lain. Another night, finding no horses in the stable, raiders stab every sheep and turn them loose, and the poor animals come flocking to the fort.',
      points: ['Then nothing at all for many weeks, which is its own kind of pressure.'],
      cast: [], offstage: ['kinziesen'], pivotal: false
    },
    {
      id: 'p2s6', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'Winnemeg brings the order — and better advice', date: '7 August 1812',
      place: 'Fort Dearborn', placeShort: 'Fort Dearborn',
      summary: 'Winnemeg, the Potawatomi called Catfish, rides in with dispatches from General Hull: war is declared with Great Britain, Hull is at Detroit with the Northwestern army, and Mackinac has fallen. Captain Heald\'s orders are to evacuate the fort if practicable and distribute all United States property among the neighbouring Indians. Winnemeg then asks Mr. Kinzie for a private word. He knows what the papers say. Stay, he argues — the garrison has ammunition and six months\' provisions, and a relief column can be sent. If you must go, go this instant, before the Potawatomi you must pass through learn what my errand was; a forced march might get you clear. Heald answers that he intends to evacuate, but cannot leave until he has assembled the Indians and divided the property fairly.',
      points: [
        'Winnemeg\'s fallback — march out and leave everything standing, and slip away while the goods are being divided — is seconded hard by Kinzie and refused.',
        'Both halves of the advice were sound, and neither was taken. Everything that follows runs through this conversation.'
      ],
      cast: ['winnemeg', 'heald', 'kinziesen'], offstage: [], pivotal: true
    },
    {
      id: 'p2s7', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'No council of war', date: '8–11 August 1812',
      place: 'Fort Dearborn', placeShort: 'Fort Dearborn',
      summary: 'The evacuation order is read on parade, and Captain Heald calls no council with his officers — explicable only by the bad feeling between him and Ensign Ronan. Getting no council, the officers go to him and argue: they will not be let through to Fort Wayne; the chiefs who once opposed attacking the fort did it out of regard for one family, the Kinzies, not from any love of Americans; the march must crawl to the pace of the women and children; half the command is superannuated or invalid. Since the order leaves it to his discretion, they advise staying and fortifying. Heald answers that no post is to be surrendered without a battle, that his force could not fight, that he would be censured for staying, and that he has full confidence in the Indians — from whom, like his own soldiers, the fall of Mackinac has been kept secret.',
      points: [
        'A soldier standing by forgets etiquette entirely: you have cattle enough for six months. No salt, says Heald. "Then jerk it, as the Indians do their venison."',
        'The Indians begin walking into the fort past the sentinels and into the officers\' quarters; one fires a rifle inside the commanding officer\'s parlour. The old chiefs move among the groups plainly agitated; the women rush about as though preparing for something.'
      ],
      cast: ['heald', 'ronan', 'helm', 'vanvoorhees', 'kinziesen'], offstage: [], pivotal: true
    },
    {
      id: 'p2s8', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'The council of the 12th, covered by the cannon', date: '12 August 1812',
      place: 'The esplanade', placeShort: 'Fort Dearborn',
      summary: 'The Indians are assembled from the neighbouring villages and a council is held. Captain Heald attends alone on the military side; he asked his officers and they refused. They have been told privately that the young chiefs mean to fall on the officers and kill them in council, and cannot make him believe it — so they wait only until he has walked out with Mr. Kinzie, then take the blockhouses overlooking the esplanade, open the port-holes and lay the cannon on the whole assembly. Heald promises the goods in the factory and the ammunition and provisions besides, and asks for an escort to Fort Wayne with a liberal reward on arrival. With many professions of friendship the Indians agree to everything.',
      points: ['It was probably the guns in the blockhouses, and not the professions of friendship, that brought everyone out of that council alive.'],
      cast: ['heald', 'kinziesen', 'ronan', 'helm'], offstage: [], pivotal: true
    },
    {
      id: 'p2s9', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'The powder in the well, the whiskey in the river', date: '13 August 1812',
      place: 'Fort Dearborn', placeShort: 'Fort Dearborn',
      summary: 'After the council Kinzie works on Heald again — since the Wabash troubles it has been American policy to keep out of these hands anything that could be used on the frontier; last autumn, hearing of Tippecanoe as far along as De Charme\'s, Kinzie turned straight back to Chicago to order his traders to sell no ammunition, and what they had was hidden. Heald is struck by the folly of arming the men he may have to fight and resolves to destroy everything but what his own troops need. The blankets, broadcloths, calicoes and paints are handed over as promised. That night the ammunition and liquor go into the sally-port well and out through the north gate into the river, barrel-heads knocked in — along with a large stock of alcohol of Kinzie\'s own. Every spare musket, the shot, the flints, the gunscrews, everything to do with a weapon, goes into the well.',
      points: [
        'The Indians crept as close as they were allowed and knew something was happening. The noise of the barrel-heads gave it away, and by morning the river tasted, as one man put it, of "strong grog."',
        'Twenty-five rounds are kept back, and one box of cartridges in the baggage wagons.'
      ],
      cast: ['heald', 'kinziesen'], offstage: [], pivotal: true
    },
    {
      id: 'p2s10', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'Captain Wells comes too late', date: '14 August 1812',
      place: 'Fort Dearborn', placeShort: 'Fort Dearborn',
      summary: 'Captain Wells arrives with fifteen friendly Miamis after a hard ride across country. He had heard at Fort Wayne of the order to evacuate, and knowing exactly what the Potawatomi intended, came to stop his relative Captain Heald from walking his command into it. He is too late: the ammunition is destroyed and the provisions are given away. There is nothing left to do but march in the morning. That afternoon a second council is held, and the Indians are openly furious about the powder and the liquor. Murmurs and threats everywhere. A few chiefs who share their people\'s hostility but keep a personal regard for this garrison and these families spend everything they have trying to hold the young men, and fail.',
      points: [
        'Wells had lived among the Indians since boyhood and understood exactly what he was riding into.',
        'From this afternoon on, nobody inside the fort is under any illusion about what the morning holds.'
      ],
      cast: ['wells', 'heald', 'kinziesen', 'miamichief'], offstage: [], pivotal: true
    },
    {
      id: 'p2s11', act: 'b1', chapter: 'XVIII', chapterTitle: 'Massacre at Chicago',
      title: 'Black Partridge gives back his medal', date: 'Evening, 14 August 1812',
      place: 'The commanding officer\'s quarters', placeShort: 'Fort Dearborn',
      summary: 'Black Partridge walks into Captain Heald\'s quarters and gives up the medal he wears. "Father, I come to deliver up to you the medal I wear. It was given me by the Americans, and I have long worn it in token of our mutual friendship. But our young men are resolved to imbrue their hands in the blood of the whites. I cannot restrain them, and I will not wear a token of peace while I am compelled to act as an enemy."',
      points: [
        'It is a warning and an act of honour at the same time, and it costs him nothing to withhold and everything to give.',
        'The garrison went on with its preparations, and there were men in it who kept trying to raise hopes of escape they did not hold themselves.'
      ],
      cast: ['blackpartridge', 'heald'], offstage: [], pivotal: true
    },

    /* ---------------- Act 2 — The Fifteenth of August ---------------- */
    {
      id: 'p2s12', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'The boat held at the river mouth', date: 'Early morning, 15 August 1812',
      place: 'The mouth of the Chicago River', placeShort: 'River mouth',
      summary: 'Mr. Kinzie has volunteered to march with the troops and has put his family in a boat with friendly Indians to be taken round the head of the lake to the St. Joseph. At first light a message comes from To-pee-nee-bee: the escort means mischief; do not go by land; the boat will be let through safely. Kinzie refuses — he believes his presence may hold the fury back, so warmly are most of them attached to him and his. The boat starts, and has barely reached the river mouth half a mile below the fort when a second messenger arrives to keep it exactly where it is. There is no mistaking why. In the boat sit Mrs. Kinzie and her four youngest, their nurse Josette, a clerk, two servants, the boatmen and two Indian protectors, while she watches her husband and her eldest child march away.',
      points: [
        'She was a woman of uncommon strength of character, and her heart died in her as she folded her arms around the little ones.',
        'To-pee-nee-bee is trying to save the family without being able to save anyone else, and the boat is being held out of the line of fire.'
      ],
      cast: ['eleanor', 'josette2', 'topeneebee', 'kinziesen', 'blackjim'], offstage: ['margaret'], pivotal: true
    },
    {
      id: 'p2s13', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'The band strikes up the Dead March', date: 'Nine o\'clock, 15 August 1812',
      place: 'The lake shore', placeShort: 'The beach',
      summary: 'The troops march out of the fort in order and in silence, and the band plays the Dead March. Captain Wells takes the lead with his Miamis, his face blackened before leaving the garrison in token of the fate he expects. They take the route along the beach. Where a range of sand-hills begins to run between the prairie and the water, the escort of about five hundred Potawatomi keeps the level of the prairie instead of staying on the beach with the Americans and the Miamis.',
      points: ['Everything that is about to happen is visible in that one movement — the escort quietly taking the high ground.'],
      cast: ['wells', 'heald', 'mrsheald', 'helm', 'margaret', 'ronan', 'vanvoorhees', 'kinziesen', 'holt', 'mrscorbin', 'hays', 'leclerc', 'miamichief'], offstage: [], pivotal: true
    },
    {
      id: 'p2s14', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'The volley from the sand-hills', date: '15 August 1812',
      place: 'The sand-hills', placeShort: 'Sand-hills',
      summary: 'A mile and a half out, Wells comes riding furiously back: they are about to attack us — form instantly and charge. The words are barely out when a volley comes down from the sand-hills. The troops form and charge up the bank; a veteran of seventy falls going up. The Miamis break at once, their chief riding at the Potawatomi to tell them they have deceived Americans and Miamis both. From here the story is Margaret Helm\'s own: the horses plunging as the balls whistle among them; the surgeon coming up wounded with his face working, asking whether their lives might be bought; her answer that they should use the moments they have left for something better; Ronan, mortally hit and nearly down, still fighting on one knee. "Look at that man. At least he dies like a soldier."',
      points: [
        'Van Voorhees is killed on the spot where she last saw him, and she is dragged past his body a minute later.',
        'A young man swings a tomahawk at her skull; she takes it on the shoulder, gets an arm round his neck and is going for his scalping-knife when an older man pulls her away.'
      ],
      cast: ['wells', 'margaret', 'vanvoorhees', 'ronan', 'miamichief', 'helm', 'heald'], offstage: [], pivotal: true
    },
    {
      id: 'p2s15', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'Held above the water', date: '15 August 1812',
      place: 'The lake', placeShort: 'The lake',
      summary: 'The older man carries her struggling into the lake and holds her under a firm hand — and she realises he is not drowning her, he is holding her head above water and keeping her out of the fight. Under the paint she recognises Black Partridge. When the firing dies he brings her out and up the sand-banks; it is a burning August morning and walking in soaked clothes is agony, and when she stops to shake the sand out of her shoes a woman takes them. On the prairie her father meets her with the news that her husband is alive and only slightly hurt. She is helped toward the Potawatomi camp on the river, half carried by Black Partridge and half by Pee-so-tum, who has a scalp swinging from his hand that she knows by its black ribbon to be Captain Wells\'s.',
      points: [
        'At the wigwam the wife of Wau-bee-nee-mah dips water, stirs maple sugar into it with her hand, and gives it to her to drink.',
        'When the wounded prisoners are brought in and an old woman goes at one of them with a stable-fork, Wau-bee-nee-mah stretches a mat between two poles so she does not have to watch. Five more of the wounded were tomahawked that night.'
      ],
      cast: ['margaret', 'blackpartridge', 'peesotum', 'waubeeneemah', 'kinziesen'], offstage: ['wells', 'helm'], pivotal: true
    },
    {
      id: 'p2s16', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'The baggage wagon, and the end of Captain Wells', date: '15 August 1812',
      place: 'The sand-hills', placeShort: 'Sand-hills',
      summary: 'The Americans charge the ravine between the sand-banks and the prairie; after hard fighting twenty-eight are left, and that remnant breaks through and gains rising ground near the Oak Woods. Lieutenant Helm sends out Peresh Leclerc, a half-breed boy in Kinzie\'s service who has fought all morning on their side, to propose terms: the lives of the survivors to be spared and ransom permitted. But while that was happening, a young man climbed into the wagon holding the twelve children of the white families and killed all of them. Wells, fighting nearby, sees it. "Is that their game, butchering the women and children? Then I will kill, too!" — and turns his horse for the Indian camp where their own women and children are.',
      points: [
        'He rides flat along his horse\'s neck, loading and firing, turning on his pursuers, until their shots kill the horse and cripple him.',
        'Winnemeg and Wau-ban-see reach him and are helping him along when Pee-so-tum stabs him in the back.',
        'Sergeant Hays, shot through the body, runs Nau-non-gee through with his bayonet as the chief comes to tomahawk him — a man from whom Nau-non-gee had received many kindnesses.'
      ],
      cast: ['wells', 'helm', 'leclerc', 'winnemeg', 'waubansee', 'peesotum', 'hays', 'naunongee'], offstage: [], pivotal: true
    },
    {
      id: 'p2s17', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'Two women who would not be taken', date: '15 August 1812',
      place: 'The field', placeShort: 'The field',
      summary: 'Mrs. Corbin had said from the first that she would never fall into their hands, believing captivity held worse than death. When a party comes to take her prisoner she fights them, refuses every sign that she will be safe and well treated, and lets herself be cut to pieces rather than go. Sergeant Holt, shot through the neck early on, hands his sword up to his wife on horseback and tells her to defend herself. The Indians want the horse and not the woman, so they come at her with gun-butts only, and she hacks and hews at the barrels as they are thrust at her, first one side then the other, breaks clear, and gallops out into the prairie. They chase her laughing and shouting to each other, "The brave woman! Don\'t hurt her!"',
      points: [
        'She is finally pulled off the horse from behind, a large and powerful woman taken by main force, and with their guns ruined and several of them cut they seem to regard her with nothing but admiration.',
        'She was carried to a trader on the Illinois River, treated with every kindness, and restored to her friends.'
      ],
      cast: ['mrscorbin', 'holt'], offstage: [], pivotal: false
    },
    {
      id: 'p2s18', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'A mule and ten bottles of whiskey', date: '15 August 1812',
      place: 'The boat, and the Kinzie house', placeShort: 'The boat',
      summary: 'From the boat they see the smoke, then the blaze, then hear the first discharge. Nothing is clear until an Indian comes toward them from the battleground leading a horse with a wounded lady on it. "That is Mrs. Heald," cries Mrs. Kinzie — "that Indian will kill her. Run, Chandonnai, take the mule and offer it to him." He is already lifting her bonnet off to take the scalp. Chandonnai offers the mule and ten bottles of whiskey at his village; the man asks whether he gets the whiskey even though she is badly wounded and will die anyway, is told yes, and the bargain is made. He puts her bonnet on his own head. She is brought aboard moaning, shot through both arms.',
      points: [
        'Her horse was a fine spirited animal, and they had aimed to disable the rider without spoiling the mount.',
        'A young Indian comes to the boat with a pistol resting on the gunwale; she is hidden under a buffalo robe and told to make no sound, and Black Jim takes up an axe and signs what will happen if he fires.',
        'At the house an old chief with some skill in surgery is asked to take the ball out of her arm. "No, father. I cannot do it — it makes me sick here," touching his heart. Kinzie does it himself with his penknife.'
      ],
      cast: ['mrsheald', 'chandonnai', 'eleanor', 'blackjim', 'kinziesen'], offstage: ['heald'], pivotal: true
    },
    {
      id: 'p2s19', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'Under the feather bed', date: '16 August 1812',
      place: 'Ouilmette\'s house', placeShort: 'Ouilmette\'s',
      summary: 'The fort is fired the next morning and the plunder divided — shawls, ribbons and feathers fluttering everywhere. Black Partridge, Wau-ban-see and Kee-po-tah post themselves in the porch of the Kinzie house as sentries. Then a party comes in from the Wabash, the most implacable of all the Potawatomi, who had hurried to share in this and arrived at the Aux Plaines to learn the battle was over and the scalps taken. They blacken their faces and come on. Black Partridge, watching from the piazza, fears above all for Mrs. Helm, newly arrived at the post and unknown to the remoter bands. She is dressed as a Frenchwoman of the country and walked to Ouilmette\'s — where the searchers come first, so she is pushed face to the wall on the bedstead and a great feather bed heaved over her, with Mrs. Bisson sitting on the edge of it sewing.',
      points: [
        'August heat, terror and near-suffocation get the better of her and she begs to be given up: "I can but die." Mrs. Bisson tells her that her death would be the destruction of them all — Black Partridge has sworn that if one drop of that family\'s blood is spilled he will take the lives of everyone concerned, even his nearest friends, and once that starts it will not stop while a white person or half-breed remains in the country.',
        'The searchers glide about the room inspecting everything without appearing to search, and go. Mrs. Bisson never stops sorting her patchwork.'
      ],
      cast: ['margaret', 'blackpartridge', 'waubansee', 'keepotah', 'ouilmette', 'mrsbisson', 'neescotneemeg'], offstage: [], pivotal: true
    },
    {
      id: 'p2s20', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: '"I am a Sau-ga-nash!"', date: '16 August 1812',
      place: 'The Kinzie house', placeShort: 'Kinzie house',
      summary: 'The Wabash party goes on to the Kinzie house, walks into the parlour where the family sit with their protectors, and sits down on the floor in silence. Black Partridge reads their faces and dares not remonstrate; he only says low to Wau-ban-see that they have tried to save their friends and nothing will save them now. Then a friendly whoop from the opposite bank. Black Partridge springs down to the canoes: "Who are you?" — "A man. Who are you?" — "A man like yourself. But tell me who you are." — "I am a Sau-ga-nash!" — "Then make all speed to the house. Your friend is in danger, and you alone can save him."',
      points: [
        'Billy Caldwell walks into that room without a trace of agitation, unslings his accoutrements, stands his rifle behind the door, and greets the men who came to kill: he had heard there were enemies here and is glad to find only friends. Why the blackened faces — are they mourning their dead? Or fasting? If fasting, ask our friend here, who never yet refused an Indian what he needed.',
        'Taken completely by surprise, they are too ashamed to admit what they came for, and say instead that they came to beg some white cotton to wrap their dead in. They are given it, with other presents, and leave peaceably.'
      ],
      cast: ['billycaldwell', 'blackpartridge', 'waubansee', 'kinziesen', 'eleanor', 'neescotneemeg'], offstage: [], pivotal: true
    },
    {
      id: 'p2s21', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'The sergeant who became a Frenchman', date: '16–17 August 1812',
      place: 'Ouilmette\'s house', placeShort: 'Ouilmette\'s',
      summary: 'Quartermaster-sergeant Griffith had been sent out as the column formed to recover the surgeon\'s strayed baggage horses — the packs held the medicines and part of his apparatus — and so was not in the ranks. Failing to find them and alarmed at what he saw among the Indians, he was taken by To-pee-nee-bee, who stripped him of his arms, paddled him across the river and told him to hide in the woods. The next afternoon he creeps into Ouilmette\'s garden, waits behind the currant bushes, and climbs in a back window just as the Wabash party leaves for the Kinzie house. The family strip off his uniform and put him in deerskin with belt, moccasins and pipe; his dark complexion and black whiskers help; everyone is ordered to address him only in French, which he does not speak a word of.',
      points: ['He passed as a Weem-tee-gosh, undetected by his enemies, all the way to safety.'],
      cast: ['griffith', 'topeneebee', 'ouilmette'], offstage: [], pivotal: false
    },
    {
      id: 'p2s22', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'Where they all went', date: 'August 1812 – winter 1813',
      place: 'St. Joseph · Detroit · Fort George', placeShort: 'After the battle',
      summary: 'Three days after the battle the family is put in a boat under a half-breed interpreter and taken to St. Joseph, where they live under To-pee-nee-bee\'s band until November and are then escorted to Detroit by Chandonnai and Kee-po-tah and handed over as prisoners of war to Colonel McKee. Kinzie is kept behind to salvage what he can of his property, wearing the dress and paint of the tribe so as not to be killed by men still thirsting for it. The Healds go across the lake, he with two wounds and she with seven, and are eventually paddled three hundred miles up the Michigan coast by Robinson and his wife and delivered to the British at Mackinac. Helm is carried to a village on the Au Sable and freed at Peoria through Thomas Forsyth. He and his wife are then arrested at Detroit and sent on horseback through Canada in the dead of winter to Fort George — where a delicate woman of seventeen is left sitting in her saddle outside the gate for over an hour before anyone offers fire, food or a roof.',
      points: [
        'Colonel Sheaffe, absent at the time, comes to her the moment he hears of it, apologises, and treats them both with the greatest kindness until they are exchanged.',
        'The soldiers and their families are scattered among villages on the Illinois, the Wabash, Rock River and at Milwaukie until spring, when most are carried to Detroit and ransomed.',
        'Captain Heald\'s own captor released him to go with his wounded wife — and got such trouble from his band for it that he set out to take him back, which is why the Healds were moved to Mackinac.'
      ],
      cast: ['eleanor', 'kinziesen', 'margaret', 'helm', 'heald', 'mrsheald', 'topeneebee', 'keepotah', 'chandonnai', 'robinson', 'sheaffe', 'mckee', 'forsyth'], offstage: [], pivotal: false
    },
    {
      id: 'p2s23', act: 'b2', chapter: 'XIX', chapterTitle: 'Narrative of the massacre, continued',
      title: 'A young raccoon', date: 'Winter 1812–13',
      place: 'Black Partridge\'s village, and Chicago', placeShort: 'Au Sable',
      summary: 'Mrs. Lee and her infant are claimed by Black Partridge and carried to his village on the Au Sable — the rest of that family having been killed. He had been fond of her twelve-year-old daughter, who was tied to her saddle for the march because she could not ride, was badly wounded at the first fire, and was thrown and left hanging as the horse bolted. Black Partridge caught the horse, got her loose, saw that she could not live and was in agony, and finished it himself with his tomahawk. He said afterwards it was the hardest thing he ever did, and that he did it because he could not bear to see her suffer. In the winter the baby falls ill, and he wraps it with the greatest care and carries it to the French trader now living in the Kinzie mansion. "What have you there?" — "A young raccoon, which I have brought you as a present," and he opens the pack.',
      points: [
        'He had asked Mrs. Lee to marry him and, when she refused, left it at that and treated her with complete respect — while remaining in no hurry to release her.',
        'M. Du Pin, doubting the resolution would hold, opened a negotiation for her ransom on the spot. In time Mrs. Lee became Madame Du Pin, and they lived happily together for many years.',
        'Nau-non-gee, dying of Sergeant Hays\'s bayonet, called his young men together and charged them to take no prisoner\'s life for his sake, since he had deserved his fate from a man whose kindness he had ill requited.'
      ],
      cast: ['blackpartridge', 'mrslee', 'dupin'], offstage: ['naunongee', 'hays'], pivotal: false
    },

    /* ---------------- Act 3 — Prisoners of War ---------------- */
    {
      id: 'p2s24', act: 'b3', chapter: 'XX', chapterTitle: 'Captivity of J. Kinzie, Sen.',
      title: 'Detroit that winter', date: 'Winter 1812–13',
      place: 'Detroit', placeShort: 'Detroit',
      summary: 'By the terms of Hull\'s surrender — the day after the massacre at Chicago — the inhabitants were left undisturbed, so the family take up quarters in the old mansion at Jefferson Avenue and Wayne Street. Almost daily they are made to watch what is done to American prisoners brought in: men who can barely drag their bleeding feet over frozen ground compelled to dance for their captors\' amusement, sometimes in front of the Government House, with British officers watching from the windows. Every article the citizens can spare is bartered to ransom them. Private houses become hospitals; the women of Detroit trade their own clothing from their doorways as the wretched are carried past for sale.',
      points: [
        'One large room of the Kinzie house is given over to the sufferers. Few survived. Two brothers from Kentucky, both badly wounded and worse used since, made an impression nobody in that house forgot — each of them worrying about the other.',
        'The last bargain was Black Jim\'s: an old white horse, the only thing of value left, traded to redeem a Black servant of Colonel Allen.'
      ],
      cast: ['eleanor', 'blackjim', 'mckee', 'margaret'], offstage: ['kinziesen'], pivotal: false
    },
    {
      id: 'p2s25', act: 'b3', chapter: 'XX', chapterTitle: 'Captivity of J. Kinzie, Sen.',
      title: 'Arrested three times', date: 'January – autumn 1813',
      place: 'Detroit and Sandwich', placeShort: 'Detroit',
      summary: 'Kinzie rejoins his family in January. Soon Proctor suspects him of corresponding with General Harrison at Fort Meigs. A British lieutenant invites him across the river on business; he goes unsuspecting and is put under guard in the house of his former partner. When he does not come home, Mrs. Kinzie tells the chiefs, who go straight to headquarters, demand their friend, and bring him back. A second time dragoons carry him off and are crossing the river with him when a party of friendly Indians appears — "Where is the Shaw-nee-aw-kee?" — and they seize canoes, cross to Sandwich and make Proctor give him up again. The third time he goes to Fort Malden in irons.',
      points: ['Nothing has ever explained Proctor\'s conduct toward a man taken from his family while living quietly under parole and protected by the terms of the surrender.'],
      cast: ['kinziesen', 'eleanor', 'proctor'], offstage: ['harrison'], pivotal: false
    },
    {
      id: 'p2s26', act: 'b3', chapter: 'XX', chapterTitle: 'Captivity of J. Kinzie, Sen.',
      title: 'Guns on Lake Erie', date: '10 September 1813',
      place: 'Fort Malden', placeShort: 'Fort Malden',
      summary: 'His confinement eases enough that he is allowed to walk on the riverbank under guard. On the 10th of September prisoner and guard alike are stopped by gunfire on Lake Erie, not far below. It must be Barclay firing into some Yankee. The firing goes on. His hour expires and nobody notices. Told at last that he must go back in, he begs another half hour — let me stay till we learn how the battle has gone. Then a sloop comes round the point under press of sail with two gunboats after her. "She is running — she bears the British colors — yes, yes, they are lowering — she is striking her flag! Now I will go back to prison contented. I know how the battle has gone."',
      points: ['The sloop was the Little Belt, the last of the squadron taken by Perry — "We have met the enemy, and they are ours."'],
      cast: ['kinziesen'], offstage: [], pivotal: true
    },
    {
      id: 'p2s27', act: 'b3', chapter: 'XX', chapterTitle: 'Captivity of J. Kinzie, Sen.',
      title: 'Tied to the saddle, and let go', date: 'Autumn 1813 – 1814',
      place: 'Quebec', placeShort: 'Quebec',
      summary: 'With the frontier no longer safe for prisoners, he is put on a horse under a guard ordered to shoot him through the head if he speaks to anyone on the road, tied to the saddle to prevent escape, and started for Quebec. The saddle had not been properly girthed and turned under him, and with his limbs fastened he could not right himself; he was made to ride in that position until he was nearly exhausted before anyone had the humanity to let him loose. At Quebec he is put aboard a small vessel for England, which is chased by an American frigate into Halifax; a second attempt springs a leak and puts back. Then, as inexplicably as the arrest, he and Mr. Macomb of Detroit are released and allowed to go home, the war not yet over. Meanwhile Harrison lands at Detroit on 29 September and the whole town goes out to meet him, Mrs. Kinzie leading her children by the hand.',
      points: ['The general walks her home and stays under her roof — and is introduced there to Kee-po-tah, whom he had last met at the council at Vincennes.'],
      cast: ['kinziesen', 'harrison', 'eleanor', 'keepotah'], offstage: ['proctor'], pivotal: false
    },
    {
      id: 'p2s28', act: 'b3', chapter: 'XX', chapterTitle: 'Captivity of J. Kinzie, Sen.',
      title: 'The fort rebuilt, and the quiet years', date: '1816 – 1830',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'The fort is rebuilt in 1816 — the same year the Potawatomi cede the tract Chicago stands on, though they remain its peaceful occupants for twenty years more, until 1836. An Indian Agency is established under Charles Jewett and then, from 1820, under Dr. Alexander Wolcott, who holds it until his death in 1830. The troops are withdrawn in 1823 and restored in 1828 after the Winnebago war, in which Red Bird was taken and died at Prairie du Chien of confinement and chagrin before trial — the Potawatomi being kept out of it largely by Billy Caldwell, Robinson and Shaw-bee-nay, who rode among the Rock River bands to talk them quiet. The handful of citizens live very well and very quietly, with more corn, butter and vegetables than they can eat and no market to sell them in — they persuade arriving captains to accept some as a present, which helps get rid of the surplus.',
      points: [
        'A traveller once asked for a night\'s lodging at the Kinzie house, called for a boot-jack after tea, ordered his breakfast, stayed out a storm, and then asked for his bill. "My house is not a tavern, sir." The family had known from the first and spent the whole visit looking forward to the moment.',
        'Chicago was laid out into lots in 1830, at ten to sixty dollars each.',
        'John Kinzie Sen., who had always predicted what this place would become, died on 6 January 1828, aged sixty-five, without seeing a word of it come true.'
      ],
      cast: ['kinziesen', 'billycaldwell', 'robinson', 'shawbeenay', 'redbird', 'wolcott'], offstage: [], pivotal: true
    },

    /* ---------------- Act 4 — The Ship Under Full Sail ---------------- */
    {
      id: 'p2s29', act: 'b4', chapter: 'XXI', chapterTitle: 'A sermon',
      title: 'The stories begin', date: 'Spring 1831',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'Chicago in the spring of 1831 is not the cheerful place it had been: Dr. Wolcott, Lieutenant Furman and a promising young son of Mr. Beaubien all dead within a few weeks of each other, and weather worse than anyone could remember — the sun out for a whole day only twice in two months. Robert Kinzie, Medard Beaubien and Billy Caldwell go off to hunt the Calumet and are so long gone that everyone gives them up for frozen; they come back alive because Robert and Caldwell each thought to carry two blankets instead of one. Riding is the only recreation: a bridle path under arching boughs along what is now Rush Street, or south across the prairie past Dr. Harmon building his sod fence. During her two months there, Juliette\'s mother-in-law tells her the story of her own captivity among the Senecas.',
      points: [
        'Juliette sets that story down, she says, exactly as she had it from her lips and from her sister\'s — the little Maggie of the tale — and only puts it in the form of a story.',
        'So Part 2\'s deepest layer arrives the way everything else in this book does: as talk, in a house, in bad weather.'
      ],
      cast: ['juliette', 'eleanor', 'robert', 'medard', 'billycaldwell', 'harmon2'], offstage: ['wolcott', 'john'], pivotal: true
    },
    {
      id: 'p2s30', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: 'The quail that answered itself', date: 'An autumn afternoon, 1779',
      place: 'Plum River, Pennsylvania', placeShort: 'Plum River',
      summary: 'Two of the Lytle children — a girl of nine and her brother, two years younger — are playing in a hollow behind the house among felled trees and cut logs. A few hours earlier they thought they saw a stranger crouching behind one of the trunks and ran in, and their mother told them they were always alarming everyone unnecessarily and sent them back out to learn courage. Now, sitting on a log, they hear a quail call, and a second answer it. Listen. Do you hear that? And then a rustling in the branches — something red, like a fawn lifting its head — and they are seized from behind and pinned in arms they cannot break, hurried away in silence on pain of death.',
      points: [
        'The whole of western Pennsylvania beyond the Susquehanna lived like this: the Delawares friendly, the Iroquois allied to Britain, and every isolated farm a day away from being emptied.',
        'One of the party, a man of mild face, spreads them a bed of grass at the halt, gives them dried meat and parched corn, and makes signs that nothing more will be done to them.'
      ],
      cast: ['eleanor', 'thomaslytle'], offstage: ['lytleparents'], pivotal: true
    },
    {
      id: 'p2s31', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: 'The mother\'s silence', date: 'Autumn 1779',
      place: 'The trail north', placeShort: 'The trail',
      summary: 'A second party comes in bringing the children\'s mother and her youngest, an infant of three months. The father and the serving men had gone to a raising miles off and the house had been left undefended. By the paint she judges them Senecas, and she is right — a war party that came down for the Delawares, failed, and took white settlers instead. On the march an older man offers to relieve her of the baby she has been carrying in her arms, and, pleased at the kindness, she gives it to him. He falls behind, finds a spot convenient for the purpose, takes the child by the feet and swings its head against a tree, and rejoins the party empty-handed. She looks at him, looks wildly round the group, and understands. She does not scream. She knows the lives of the others depend on her firmness in that hour, and she pulls them closer and walks on without a word or a question.',
      points: [
        'She reads in the face of the man commanding the party something more merciful than she had let herself hope for — and notices how gently he treats her eldest girl.',
        'On those two slender things she builds every hope of ransom she has.'
      ],
      cast: ['eleanor', 'thomaslytle', 'lytleparents', 'bigwhiteman'], offstage: [], pivotal: true
    },
    {
      id: 'p2s32', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: '"Then, Maggie, I must kill you"', date: 'Autumn 1779',
      place: 'The Lytle farm', placeShort: 'The farm',
      summary: 'The two younger children were in the garden when the Indians came into the yard. The boy, six years old, helped his four-year-old sister over the fence into a field grown over with blackberry and raspberry, and they hid in it. When it seemed quiet they tried to force their way across to the far side, but Maggie had pulled off her shoes and stockings at play and the briers cut her feet until she could hardly keep from crying out. Her brother gave her his stockings, and tried his shoes on her, but they slipped off. At last she said she could go no further. "Then, Maggie, I must kill you, for I can\'t let you be killed by the Indians." — "Oh, no, Thomas! Don\'t, pray don\'t kill me! I don\'t think the Indians will find us." He argued a long time and even looked for a stick big enough, and she promised she would not complain or falter if he would help her out of the field.',
      points: [
        'That a six-year-old\'s idea of mercy was to kill his sister first says everything about the stories those children had grown up on.',
        'They hid until sunset, followed the cows home to Granny Myers\'s, found the house empty, failed to get milk, and slept under an old bedstead behind it — mistaking their own father\'s search party in the night for the whoops of Indians.'
      ],
      cast: ['maggie'], offstage: ['lytleparents'], pivotal: false
    },
    {
      id: 'p2s33', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: '"I bring you a child to supply the place of my brother"', date: 'Autumn 1779',
      place: 'The Seneca village, head-waters of the Alleghany', placeShort: 'Seneca village',
      summary: 'After many days\' painful march the party reaches the village near what is now Olean Point. The chief who led them — the Big White Man — takes his prisoners straight to the principal lodge, where his mother lives, the widow of the band\'s head chief, whom they call the Old Queen. He presents the little girl to her: "My mother, I bring you a child to supply the place of my brother, who was killed by the Lenape six moons ago. She shall dwell in my lodge, and be to me a sister. Take the white woman and her children and treat them kindly — our father will give us many horses and guns to buy them back again." The Old Queen does exactly as she is told, and every comfort her way of life allows is given them.',
      points: [
        'The "father" he means is Colonel Johnson, the British Indian Agent at Fort Niagara — the ransom is assumed from the first, for everyone except the girl.',
        'It is to the generally mild disposition of this tribe, and to the character of this chief, that the prisoners owe their lives at all.'
      ],
      cast: ['bigwhiteman', 'oldqueen', 'eleanor', 'thomaslytle', 'lytleparents'], offstage: ['coljohnson'], pivotal: true
    },
    {
      id: 'p2s34', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: 'Ransomed, all but one', date: '1779–80',
      place: 'The Seneca village', placeShort: 'Seneca village',
      summary: 'The father comes home at dark to an empty house and spends the night rousing the valley; the servant girl is found, having hidden under a brewing-tub; an old settler far up the valley remembers seeing strange Indians pass at sunset with a white woman carrying an infant in her arms rather than on her back. At Fort Pitt the commandant furnishes soldiers, and after long and careful searching the party reaches the Big White Man\'s village. A treaty is made and the mother and the younger child are ransomed easily. For Eleanor there is no price. "No — she is my sister. I took her to supply the place of my brother who was killed by the enemy. She is dear to me, and I will not part with her." The father has to go home with the ones he has recovered and leave his daughter behind.',
      points: [
        'Colonel Johnson, warmly enlisted, goes in person to the village as soon as spring opens the country and offers splendid presents of guns and horses. The chief is immovable.',
        'Year by year the hope of recovering her grows fainter.'
      ],
      cast: ['lytleparents', 'bigwhiteman', 'eleanor', 'coljohnson'], offstage: ['maggie', 'thomaslytle'], pivotal: false
    },
    {
      id: 'p2s35', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: 'The Ship under full sail', date: '1780–83',
      place: 'The Seneca village', placeShort: 'Seneca village',
      summary: 'She winds herself closer and closer round her Indian brother\'s heart. Nothing exceeds the consideration and affection shown her by him and by the Old Queen: the family\'s whole stock of brooches and wampum goes on decorating her, the principal seat and the best food are always hers, and no effort is spared to make her forget her own people. Having watched her parents and her little brother go and having refused every comfort for a long time — preferring death to separation from everything she loved — time does what it does, and she grows contented and happy. For her energy and drive, qualities she kept to the last day of her life, they give her a name: The Ship under full sail.',
      points: ['Juliette is writing about her own mother-in-law, the matriarch of the Chicago household — and the reader of Part 1 has already met the name.'],
      cast: ['eleanor', 'bigwhiteman', 'oldqueen'], offstage: [], pivotal: true
    },
    {
      id: 'p2s36', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: 'The bowl of May-apple', date: 'c. 1781',
      place: 'The Seneca village', placeShort: 'Seneca village',
      summary: 'The one shadow is the chief\'s wife, who from the day of the adoption conceived a hatred she was careful to hide from her husband. Childless, with nothing else to occupy her, she nurses the grievance until she has a chance. While the Big White Man is away, the girl falls ill with fever and ague, and the wife — to lull suspicion — is tireless in her attentions. One afternoon, with the Old Queen out, she comes in with a bowl and stoops to the mat: "Drink, my sister; I have brought you that which will drive this fever far from you." Lifting her head to answer, the child sees a pair of eyes at a crevice in the lodge wall, fixed on her with a peculiar significance, and says faintly: set it down, my sister — when this fit has passed, I will drink your medicine.',
      points: [
        'The eyes belonged to a young playfellow who had watched the woman all morning gathering the most deadly roots and herbs and knew who they were for.',
        'The bowl is carried to the Old Queen\'s lodge and found to be chiefly a decoction of May-apple root, the deadliest poison the Seneca know.',
        'The chief, returning, does not take the summary vengeance custom allowed him. He banishes her from his lodge for good and sets her to hoe corn at the far end of the common field — where she still swung her hoe at the girl when she came too near.'
      ],
      cast: ['chiefswife', 'eleanor', 'oldqueen', 'bigwhiteman'], offstage: [], pivotal: true
    },
    {
      id: 'p2s37', act: 'b4', chapter: 'XXII', chapterTitle: 'The captives',
      title: 'The Feast of the Green Corn, and the boat at Niagara', date: '1783',
      place: 'Fort Niagara', placeShort: 'Fort Niagara',
      summary: 'Four years on, she loves the chief and his mother, speaks their language and keeps their customs, and has all but forgotten her own — everything except her mother. Then peace comes in 1783 and with it a general pacification, and the Lytles move their family to Fort Niagara. Colonel Johnson goes once more to the village, arriving during the Feast of the Green Corn, when everything is suspended for festivity and everyone is in gala dress — the adopted child in blue broadcloth bordered with ribbons, a black silk sack with three rows of silver brooches, strings of white and purple wampum, scarlet leggings and quilled moccasins. Warmed by the festival, the chief listens to what her parents have given up merely to be near her, and agrees to bring her to the Grand Council at Niagara — on condition that no one ask him to give her up.',
      points: [
        'She had promised she would never leave him without his permission, and he relied on her word absolutely.',
        'At the crossing he tells his young men to stand and hold the horses; told they will be ferried over and cared for, he says no — let them wait. He holds her hand until the boat touches the far bank and she springs into her mother\'s arms.',
        '"She shall go. The mother must have her child again. I will go back alone." One silent gesture of farewell, and he takes the boat back and rides into the forest.'
      ],
      cast: ['bigwhiteman', 'eleanor', 'lytleparents', 'coljohnson'], offstage: ['oldqueen'], pivotal: true
    },

    /* ---------------- Act 5 — Leaving Chicago ---------------- */
    {
      id: 'p2s38', act: 'b5', chapter: 'XXIII', chapterTitle: 'Second-sight — Hickory Creek',
      title: 'The saddle on his shoulders', date: 'Late spring, c. 1790s',
      place: 'Grosse Pointe, above Detroit', placeShort: 'Grosse Pointe',
      summary: 'At fourteen she married Colonel McKillip, a British officer, who was shot dead by one of his own sentries near the Miami Rapids in 1794 — Margaret Helm is the daughter of that marriage. Living as a widow with her parents at Grosse Pointe, she is sitting at work by an open window one forenoon when something crosses the light. It is her brother Thomas, who had taken leave that morning to visit a young lady on the river Trench. He has no horse and is carrying his saddle on his shoulders. She calls out to ask what has happened; he makes no answer, only looks earnestly into her face as he moves slowly along the walk toward the stables. She waits, then goes to look. No Thomas, no horse, no saddle, and no one about the place has seen him.',
      points: [
        'The next morning a messenger comes from the river Trench: he and his horse have been found drowned below the ford, the stream swollen with rain. He had stripped and made his clothes into a bundle strapped to his shoulders to swim it, and the current shifted the bundle and held his head under.',
        'From the time he was seen passing a house near the stream, he must have died at the very moment his sister saw him pass her window.',
        '"I am not superstitious. I have never believed in ghosts or witches, but nothing can ever persuade me that this was not a warning sent from God."'
      ],
      cast: ['eleanor', 'thomaslytle', 'juliette'], offstage: ['mckillip', 'margaret'], pivotal: true
    },
    {
      id: 'p2s39', act: 'b5', chapter: 'XXIII', chapterTitle: 'Second-sight — Hickory Creek',
      title: 'The ball at Hickory Creek', date: 'Spring 1831',
      place: 'Hickory Creek', placeShort: 'Hickory Creek',
      summary: 'The settlers at Hickory Creek honour the Chicago beaux with a ball. Mr. Dole declines and Lieutenant Foster is on duty, but does better than accepting — he lends his beautiful horse to Medard Beaubien, who rides down with Robert Kinzie and Gholson Kercheval, all three well mounted and in their best, meaning to eclipse the local swains. They are received politely, dined, and shown into the dancing hall, where all the beauty of the precinct is assembled in bombazet gowns and large white handkerchiefs scented with oil of cinnamon. The city gentlemen grow more gallant, the girls more delighted, the country boys more silently murderous; in vain do they pigeon-wing and double-shuffle at "hoe corn and dig potatoes" — they are fairly danced off their own floor.',
      points: [
        'At daylight nobody is on hand to bring the horses. "Poor fellows — they couldn\'t stand it. They\'ve gone home to bed."',
        'In the stable stand three animals that are, on inspection, the original bodies with their manes hacked to a scrubby ridge and their tails cut to bare stumps.',
        'Gholson sat down on a log and cried; Medard was philosophical, the horse being Lieutenant Foster\'s; Robert looked round for someone to knock down and found nobody. They had to cross the prairie home in full view of a settlement that always turned out to greet an arrival.'
      ],
      cast: ['robert', 'medard', 'gholson', 'foster', 'juliette'], offstage: [], pivotal: false
    },
    {
      id: 'p2s40', act: 'b5', chapter: 'XXIII', chapterTitle: 'Second-sight — Hickory Creek',
      title: 'The Napoleon sails without them', date: 'Spring 1831',
      place: 'Chicago', placeShort: 'Chicago',
      summary: 'The order has come to evacuate Fort Dearborn and move the troops to Fort Howard at Green Bay, and the family circle breaks up: the mother, Mrs. Helm and her little son to return with the Kinzies to Fort Winnebago, the rest to go with the command. The schooner Napoleon comes from Detroit. With no harbour, she anchors outside the bar and everything must be rowed out through the river mouth, so everyone lives packed up for days. At last the final article is aboard and only the passengers remain on shore — at which point Captain Hinckley, who has been in a fever about the weather for hours, hoists sail and stands out into the open lake with all their possessions.',
      points: [
        'Mrs. Engle ate her breakfast off a shingle with her husband\'s jack-knife and passed both down to Lieutenant Foster when she had finished.',
        'Mrs. Portier — their kind Victoire — supplied the dishes, knives and forks the mess-basket could not.',
        'Two days later the Napoleon was back at anchor beyond the bar, and by afternoon they had taken leave of their friends, who sailed away from Chicago.'
      ],
      cast: ['juliette', 'john', 'eleanor', 'margaret', 'foster', 'victoire', 'hinckley', 'robert'], offstage: ['petaille'], pivotal: true
    }
  ]
};
