// The survey. Each question is a scenario that measures one or two of the
// axes in data.js (AXES). `set` places the voter on an axis, -2..+2, with the
// same sign convention the candidates are scored on; `[v, w]` is a value at
// partial weight. Each question has two or three variants (one is picked at
// random per session) and the option order is shuffled, so no two runs read
// quite alike. The engine in app.js picks the next question by how many
// still-undecided races it could move, and stops as soon as more questions
// would not change the ballot.

export const QUESTIONS = [
  {
    id: 'econ', emoji: '🏛️', topic: 'Springfield’s wallet', axes: ['econ'],
    variants: [
      { title: 'Illinois has a budget hole and the CTA is staring at a fiscal cliff. You get one move.',
        scenario: 'The legislature hands you the pen for a day. Whatever you pick, somebody pays for it.' },
      { title: 'A genie offers Illinois one fiscal wish.',
        scenario: 'It’s a practical genie, so every wish comes with a bill. Which one would you actually make?' },
      { title: 'Twelve friends, one long table on Randolph Street, and the check just landed.',
        scenario: 'Nothing about taxes here. Just tell us what you’d honestly do.',
        labels: { a: 'Whoever earns the most covers more. That’s what friends are for.', b: 'Split it evenly and round up the tip.',
          c: 'Everyone pays for what they ordered.', d: 'Everyone pays for what they ordered, and I skip the shared appetizers I didn’t ask for.' } },
      { title: 'Your aunt in Naperville says Illinois taxes are why she’s moving to Tennessee.',
        scenario: 'Your cousin says the state should tax the rich and fix the trains. Thanksgiving is getting loud. Whose side are you on?' },
    ],
    options: [
      { id: 'a', label: 'Tax the top earners and fund schools, transit and property-tax relief.',
        short: 'tax the top earners to fund public services', set: { econ: -2 } },
      { id: 'b', label: 'A balanced mix: a little new revenue, a little trimming, no big swings.',
        short: 'a balanced budget mix', set: { econ: -0.5 } },
      { id: 'c', label: 'Cut spending and fix pensions before anyone pays a dollar more.',
        short: 'cut spending before raising taxes', set: { econ: 1.2 } },
      { id: 'd', label: 'Lower taxes and shrink government. People are leaving the state.',
        short: 'lower taxes and smaller government', set: { econ: 2 } },
    ],
  },
  {
    id: 'safety', emoji: '🚨', topic: 'Public safety', axes: ['safety'],
    variants: [
      { title: 'Three carjackings on your block this month. The block-club group chat wants answers.',
        scenario: 'Your neighbors are angry and scared. What do you want from the people on your ballot?' },
      { title: 'A judge just let someone charged with a gun crime go home to await trial.',
        scenario: 'Since 2023, Illinois has had no cash bail; judges decide who stays locked up, case by case. What’s your reaction?' },
    ],
    options: [
      { id: 'a', label: 'Prevention first: violence interrupters, mental-health responders, youth jobs. Arrests alone don’t fix it.',
        short: 'prevention and alternatives to policing', set: { safety: -2 } },
      { id: 'b', label: 'Both: more detectives to actually solve cases, plus prevention programs. Keep the bail reform.',
        short: 'solve more cases and keep the reforms', set: { safety: -0.5 } },
      { id: 'c', label: 'More officers on patrol, and judges who keep repeat offenders locked up.',
        short: 'more police and tougher detention', set: { safety: 1.3 } },
      { id: 'd', label: 'Roll back the SAFE-T Act, bring back cash bail, prosecute to the max.',
        short: 'roll back the SAFE-T Act', set: { safety: 2 } },
    ],
  },
  {
    id: 'federal', emoji: '🛂', topic: 'Chicago vs. Washington', axes: ['federal'],
    variants: [
      { title: 'Unmarked federal SUVs are making immigration arrests outside a school drop-off in your neighborhood.',
        scenario: 'It’s what happened across Chicago during 2025’s Operation Midway Blitz. What should your city, county and state do?' },
      { title: 'Your neighbor has worked here undocumented for twenty years. She asks you if Chicago will protect her.',
        scenario: 'Federal immigration agents are back in town. What do you want your local officials to say to her, and to Washington?' },
    ],
    options: [
      { id: 'a', label: 'Sue, block and send Washington the bill. Not one ounce of local help.',
        short: 'fight federal immigration raids in court and on the ground', set: { federal: -2 } },
      { id: 'b', label: 'Keep the sanctuary rules and keep schools and courthouses off-limits, without picking new fights.',
        short: 'keep the sanctuary protections, lower the temperature', set: { federal: -0.8 } },
      { id: 'c', label: 'Leave law-abiding people alone, but hand over people charged with serious crimes.',
        short: 'cooperate with ICE on serious criminals', set: { federal: 1 } },
      { id: 'd', label: 'Immigration law is federal law. Cooperate fully and end the sanctuary rules.',
        short: 'cooperate fully with ICE', set: { federal: 2 } },
    ],
  },
  {
    id: 'social', emoji: '⚖️', topic: 'Rights & guns', axes: ['social'],
    variants: [
      { title: 'The courts keep handing big rights questions back to the states. What should Illinois be?',
        scenario: 'Abortion, LGBTQ protections, the 2023 assault-weapons ban: Springfield sets the rules now.' },
      { title: 'A national group is rating every state, from “haven” to “restrictive.”',
        scenario: 'On abortion, LGBTQ rights and guns, where do you want Illinois to land?' },
    ],
    options: [
      { id: 'a', label: 'A haven: abortion access and LGBTQ rights protected in law, and keep the assault-weapons ban.',
        short: 'Illinois as a haven for abortion and LGBTQ rights, with strict gun laws', set: { social: -2 } },
      { id: 'b', label: 'Mostly protect those rights, with room for compromise at the edges.',
        short: 'mostly protect those rights, with compromise', set: { social: -0.7 } },
      { id: 'c', label: 'Limit late-term abortion, add parental notice, loosen the gun ban for law-abiding owners.',
        short: 'more abortion limits, more gun rights', set: { social: 1.3 } },
      { id: 'd', label: 'Restrict abortion, put parents first, and repeal the gun ban.',
        short: 'socially conservative laws and repealing the gun ban', set: { social: 2 } },
    ],
  },
  {
    id: 'change', emoji: '🔧', topic: 'Experience vs. a shake-up', axes: ['change'],
    variants: [
      { title: 'Cook County government, as an apartment building.',
        scenario: 'The longtime manager knows every pipe in the place, but she’s cozy with the landlord. A tenant is running to replace her.' },
      { title: 'Your favorite corner tavern just got a new owner.',
        scenario: 'Mind-reader question: it isn’t about politics, and it is. What do you hope she does?',
        labels: { a: 'Touch nothing. The Old Style sign and the jukebox stay.', b: 'Fix the bathroom and the books, but keep its soul.',
          c: 'New menu, new beer list. Give it a second act.', d: 'Gut it and start over. It was tired.' } },
      { title: 'You’re hiring someone for a job where one mistake costs millions.',
        scenario: 'One applicant has done it for twenty years under the old bosses. The other is an outsider with big ideas and no track record.' },
    ],
    options: [
      { id: 'a', label: 'Keep the experienced hand. Knowing how things work is the job.',
        short: 'experience and continuity', set: { change: -2 } },
      { id: 'b', label: 'Keep them, but demand an audit and real transparency.',
        short: 'experience with accountability', set: { change: -0.7 } },
      { id: 'c', label: 'Give the newcomer a shot. Fresh eyes find the leaks.',
        short: 'giving newcomers a shot', set: { change: 1 } },
      { id: 'd', label: 'Clean house. The system itself is the problem.',
        short: 'a clean sweep of the old system', set: { change: 2 } },
    ],
  },
  {
    id: 'taxfair', emoji: '🏠', topic: 'Your property tax bill', axes: ['taxfair'],
    variants: [
      { title: 'Your property tax bill just jumped 20%. A Loop office tower’s bill dropped after its lawyers appealed.',
        scenario: 'Cook County’s Assessor sets values, the Board of Review hears appeals, and the Treasurer sends the bill. What should change?' },
      { title: 'Two bungalow owners and a Gold Coast hotel walk into the Board of Review.',
        scenario: 'Everyone thinks they’re overtaxed. Who should the system be built to listen to?' },
    ],
    options: [
      { id: 'a', label: 'Assess big commercial property at full value and rein in the appeal lawyers.',
        short: 'make big commercial property pay its full share', set: { taxfair: -2 } },
      { id: 'b', label: 'Just make the assessments accurate and predictable. Stop the whiplash.',
        short: 'accurate, predictable assessments', set: { taxfair: -0.3 } },
      { id: 'c', label: 'Assessments are wrong too often. Make appeals easier and fix the errors.',
        short: 'easier appeals and fixing assessment errors', set: { taxfair: 1.2 } },
      { id: 'd', label: 'Businesses are being taxed out of Cook County. Ease up so they stay and hire.',
        short: 'tax relief for businesses so they stay', set: { taxfair: 2 } },
    ],
  },
  {
    id: 'green', emoji: '🌊', topic: 'Water & flooding', axes: ['green'],
    variants: [
      { title: 'A 100-year storm floods basements in your ward for the third time in five years.',
        scenario: 'The Metropolitan Water Reclamation District has money for one big push. Where does it go?' },
      { title: 'The Chicago River is cleaner than it has been in a century. Now what?',
        scenario: 'The water district has to choose between going big on climate-ready projects and keeping its tax levy flat.' },
    ],
    options: [
      { id: 'a', label: 'Go green at scale: rain gardens, permeable alleys, buying out flood-prone land. Build for the climate we’ll have.',
        short: 'large-scale green infrastructure and climate action', set: { green: 2 } },
      { id: 'b', label: 'A mix: finish the Deep Tunnel reservoirs, and add green infrastructure where it pays off.',
        short: 'a mix of tunnels and green infrastructure', set: { green: 0.7 } },
      { id: 'c', label: 'Stick to the core job: pipes, tunnels and treatment, at the lowest cost.',
        short: 'the core job, at the lowest cost', set: { green: -1 } },
      { id: 'd', label: 'Hold the line on the tax levy. Homeowners can’t absorb more.',
        short: 'holding the line on the tax levy', set: { green: -2, econ: [1, 0.4] } },
    ],
  },
  {
    id: 'union', emoji: '🍎', topic: 'Chicago Public Schools', axes: ['union'],
    variants: [
      { title: 'CPS closed a $732 million budget gap partly by counting on state money that hasn’t been approved. Chicago is electing a school board president for the first time.',
        scenario: 'The Chicago Teachers Union says borrow and push Springfield for more money. Critics say stop the borrowing, cut central office, and consolidate half-empty schools.' },
      { title: 'You sit on your neighborhood school’s Local School Council, and the budget just got cut 8%.',
        scenario: 'Downtown says there’s no more money unless the district borrows. What do you want the new school board to do?' },
    ],
    options: [
      { id: 'a', label: 'Fund the schools: borrow if needed, fight for state money, and back the teachers.',
        short: 'fully funding schools and backing the teachers union', set: { union: -2, econ: [-1, 0.3] } },
      { id: 'b', label: 'Protect classrooms, but no more high-interest borrowing. Find a deal with the union.',
        short: 'protect classrooms without new borrowing', set: { union: -0.4 } },
      { id: 'c', label: 'An independent board: audit everything, right-size the buildings, hold the line on spending.',
        short: 'an independent board that holds the line on spending', set: { union: 1.3 } },
      { id: 'd', label: 'More school choice, more accountability, less union influence on the board.',
        short: 'school choice and less union influence', set: { union: 2, econ: [1, 0.3] } },
    ],
  },
  {
    id: 'judges', emoji: '👩‍⚖️', topic: 'The judges', axes: [], kind: 'judges',
    variants: [
      { title: 'Flip the ballot over: sixty-some judges, each one a Yes or a No.',
        scenario: 'A judge keeps the job with 60% Yes, and nearly every judge does. The bar associations screen every one of them. What’s your strategy?' },
      { title: 'The judges’ side of the ballot: dozens of names you’ve never heard of.',
        scenario: 'Each needs 60% Yes to stay on the bench. Lawyers’ groups rate them all, and occasionally one gets flagged. What do you do?' },
    ],
    options: [
      { id: 'bar', label: 'Follow the big bar associations: No where the Chicago Bar Association, the Council of Lawyers or the state bar says “not recommended,” Yes on the rest.',
        short: 'follow the big bar associations', policy: 'bar' },
      { id: 'strict', label: 'Stricter: also No on any judge a smaller bar group voted against, or with a documented controversy.',
        short: 'a strict line on any red flag', policy: 'strict' },
      { id: 'all', label: 'Yes on all of them. Judges shouldn’t face political pressure.',
        short: 'retain every judge', policy: 'all' },
      { id: 'skip', label: 'Leave the judges blank. I’ll only vote where I know something.',
        short: 'leave the judges blank', policy: 'skip' },
    ],
  },
  {
    id: 'label', emoji: '🏷️', topic: 'The tiebreaker', axes: [], kind: 'party',
    variants: [
      { title: 'A race you know nothing about. All you can see is each candidate’s party label.',
        scenario: 'No ads, no endorsements, just a little “Democratic” or “Republican” or “Libertarian” under each name. You…' },
      { title: 'It’s 6:52 p.m., polls close at 7, and you’re stuck on a race you’ve never heard of.',
        scenario: 'The line behind you is getting restless. All you’ve got is each candidate’s party label. You…' },
    ],
    options: [
      { id: 'd', label: 'Pick the Democrat.', short: 'lean Democratic in races you know little about', party: { D: 1, R: -0.6, T: -0.3 } },
      { id: 'r', label: 'Pick the Republican.', short: 'lean Republican in races you know little about', party: { R: 1, D: -0.6, T: -0.1 } },
      { id: 't', label: 'Pick the third party or independent, if there is one. Two parties aren’t enough.',
        short: 'lean toward third parties and independents', party: { T: 1, D: -0.3, R: -0.3 }, set: { change: [1, 0.3] } },
      { id: 'n', label: 'Ignore the labels and go with experience and endorsements.',
        short: 'ignore party labels', party: {}, set: { change: [-1, 0.3] } },
    ],
  },
];

// Lightning round: direct Yes/No on the public questions the axes above
// leave undecided. Only asked when the scenarios didn't settle the measure.
export const LIGHTNING_PROMPT = 'Lightning round: one tap each. These are the public questions your answers didn’t settle.';
