export const trip = {
  name: 'Zion + Bryce Canyon',
  subtitle: 'Chicago to canyon country',
  start: '2026-09-05',
  end: '2026-09-13',
  updated: '2026-08-30',
  days: 9,
  nights: 8,
  travelers: 'Chicago → Las Vegas → Zion → Bryce → St. George → Las Vegas',
  publicUrl: 'https://kevinrhaas.github.io/custom/zion-bryce/',
  timeZones: {
    lasVegas: 'PDT · UTC−7',
    utah: 'MDT · UTC−6'
  }
};

export const stays = [
  {
    id: 'waldorf',
    nights: 'Sept 5 · 1 night',
    name: 'Waldorf Astoria Las Vegas',
    place: 'Las Vegas, Nevada',
    note: 'Soft landing after the flight. Rental car pickup is planned before checking in.',
    map: 'https://www.google.com/maps/search/?api=1&query=Waldorf+Astoria+Las+Vegas'
  },
  {
    id: 'cliffrose',
    nights: 'Sept 6–10 · 4 nights',
    name: 'Cliffrose Springdale, Curio Collection',
    place: 'Springdale, Utah',
    note: 'About a half-mile from the Zion Canyon Visitor Center; walking avoids the morning parking scrum.',
    map: 'https://www.google.com/maps/search/?api=1&query=Cliffrose+Springdale+Curio+Collection'
  },
  {
    id: 'bryce-lodge',
    nights: 'Sept 10–12 · 2 nights',
    name: 'The Lodge at Bryce Canyon',
    place: 'Bryce Canyon National Park, Utah',
    note: 'Confirmed. The confirmation number is intentionally not published; save it in the private field below.',
    map: 'https://www.google.com/maps/search/?api=1&query=The+Lodge+at+Bryce+Canyon'
  },
  {
    id: 'advenire',
    nights: 'Sept 12–13 · 1 night',
    name: 'The Advenire, Autograph Collection',
    place: 'St. George, Utah',
    note: 'A short walk from the 7:00 PM Painted Pony reservation in Ancestor Square.',
    map: 'https://www.google.com/maps/search/?api=1&query=The+Advenire+St+George'
  }
];

export const activityPlans = {
  scout: {
    id: 'scout',
    title: 'Scout Lookout via West Rim',
    short: 'Scout Lookout',
    strap: 'Coolest clear morning · strenuous climbing',
    stats: ['4.2 mi round trip', '≈1,000–1,200 ft gain', '≈3 hours', 'No permit to Scout Lookout'],
    schedule: [
      { time: '6:25 AM', title: 'Walk to the Visitor Center', detail: 'Bring breakfast, water and layers. The first canyon shuttle leaves at 7:00 AM during these dates.' },
      { time: '7:00 AM', title: 'Board the first canyon shuttle', detail: 'Ride to stop 6, The Grotto. Expect a busy Labor Day week and leave room for one full shuttle.' },
      { time: '7:35–10:45 AM', title: 'Climb the West Rim Trail', detail: 'Walter’s Wiggles are steep. Scout Lookout has exposed edges and long drop-offs; turn around sooner if heat or footing is uncomfortable.' },
      { time: '11:00 AM', title: 'Recover at Zion Lodge', detail: 'Ride or walk one stop to the lodge lawn for shade, lunch and a slow reset.' },
      { time: '2:00 PM onward', title: 'Pool, nap or Springdale', detail: 'Keep the afternoon deliberately light. This is not the day to stack another exposed hike.' }
    ],
    alerts: [
      { tone: 'amber', title: 'The original mileage was low', text: 'NPS lists the Scout Lookout outing at about 4.2 miles round trip and strenuous—not 3.6 miles.' },
      { tone: 'blue', title: 'Permit line', text: 'No permit is needed to stop at Scout Lookout. Continuing onto the Angels Landing chain section requires an Angels Landing permit.' }
    ],
    links: [
      ['NPS West Rim trail details', 'https://www.nps.gov/zion/planyourvisit/zion-national-park-trail-information.htm'],
      ['Angels Landing permit rules', 'https://www.nps.gov/zion/planyourvisit/angels-landing-hiking-permits.htm']
    ]
  },
  narrows: {
    id: 'narrows',
    title: 'The Narrows · bottom-up',
    short: 'The Narrows',
    strap: 'Driest forecast · river conditions decide',
    stats: ['Out-and-back', 'Riverside Walk adds 2.2 mi', 'Turn around anytime', 'No permit to Big Spring'],
    schedule: [
      { time: 'Night before', title: 'Collect river gear', detail: 'Pick up closed-toe canyon shoes, neoprene socks and a sturdy pole if renting. Set out warm layers and a dry bag.' },
      { time: '6:20 AM', title: 'Walk to the Visitor Center', detail: 'Carry a real breakfast, water and everything you need; there are no bathrooms beyond the Temple of Sinawava.' },
      { time: '7:00–7:45 AM', title: 'First shuttle to Temple of Sinawava', detail: 'It takes roughly 45 minutes from the Visitor Center to the final stop.' },
      { time: '7:45–8:25 AM', title: 'Riverside Walk approach', detail: 'The paved trail ends where river hiking begins. Reassess the sky, water and group comfort before entering.' },
      { time: '8:25–11:30 AM', title: 'Hike upstream, then turn around', detail: 'Wall Street is roughly 3 miles upstream. There is no prize for forcing a mileage goal—save equal time and energy for the return.' },
      { time: '1:00 PM onward', title: 'Warm up in Springdale', detail: 'Dry clothes, lunch, shops and galleries. Keep the rest of the day unstructured.' }
    ],
    alerts: [
      { tone: 'red', title: 'Forecast is not clearance', text: 'Do not enter with rain in the watershed or a flash-flood warning. Zion closes the Narrows above 150 CFS. Check NPS and river flow the same morning.' },
      { tone: 'amber', title: 'River health advisory', text: 'Avoid submerging your head and never drink river water, even after filtering, because harmful cyanobacteria may be present.' }
    ],
    links: [
      ['NPS Narrows guide', 'https://www.nps.gov/zion/planyourvisit/thenarrows.htm'],
      ['Zion current conditions', 'https://www.nps.gov/zion/planyourvisit/conditions.htm'],
      ['Virgin River live gauge', 'https://waterdata.usgs.gov/monitoring-location/09405500/#parameterCode=00060&period=P7D&showMedian=false'],
      ['NWS flash-flood potential', 'https://www.weather.gov/slc/flashflood']
    ]
  },
  flex: {
    id: 'flex',
    title: 'Zion canyon flex day',
    short: 'Zion flex',
    strap: 'E-bikes + pools · sunset option',
    stats: ['Low-pressure day', 'Class 1 e-bikes only', 'Lower Pool: 1.2 mi RT', 'Watchman: 3.3 mi RT'],
    schedule: [
      { time: '8:00 AM', title: 'Choose the shape of the day', detail: 'Best all-around version: reserve Class 1 e-bikes, ride the Scenic Drive and stop for Lower Emerald Pool.' },
      { time: '9:00 AM–1:00 PM', title: 'Pedal the canyon', detail: 'Ride single-file, stop for shuttles and expect to ride both directions—e-bikes are not carried on shuttle racks.' },
      { time: '1:00–4:30 PM', title: 'Lunch + genuine downtime', detail: 'Pool, spa, galleries or a no-agenda afternoon. Keep legs fresh for Bryce.' },
      { time: '5:35 PM', title: 'Optional Watchman Trail', detail: 'A moderate, exposed 3.3-mile outing with limited shade—not an easy stroll. Carry headlamps if timing it near sunset.' },
      { time: 'Sunset', title: 'Or choose Pa’rus instead', detail: 'The accessible Pa’rus Trail is the calmer sunset call. Use the pedestrian bridge view; do not stop on the road bridge at Canyon Junction.' }
    ],
    alerts: [
      { tone: 'blue', title: 'Long-hike alternative', text: 'Observation Point via East Mesa is an all-day replacement, not an add-on. Allow roughly 8 miles and arrange the East Zion trailhead shuttle if selected.' },
      { tone: 'amber', title: 'Kolob Terrace is not nearby', text: 'Lava Point is about 1 hour 20 minutes each way from Zion’s South Entrance. Save it for a dedicated scenic-drive version of this day.' }
    ],
    links: [
      ['NPS bicycling rules', 'https://www.nps.gov/zion/planyourvisit/bicycling-in-zion.htm'],
      ['Emerald Pools trail details', 'https://www.nps.gov/zion/planyourvisit/zion-national-park-trail-information.htm'],
      ['East Mesa trailhead shuttle', 'https://eastzionadventures.com/hiking-tours/observation-point-shuttle/']
    ]
  }
};

export const days = [
  {
    day: 1,
    date: '2026-09-05',
    dateLabel: 'Sat · Sept 5',
    route: 'Chicago → Las Vegas',
    title: 'Land softly in Las Vegas',
    eyebrow: 'Arrival day',
    stay: 'Waldorf Astoria Las Vegas',
    summary: 'Pick up the car, eat close to the hotel and protect tomorrow’s early start.',
    chips: ['AA1497', 'Arrive 2:25 PM PDT', '1 night'],
    schedule: [
      { time: '2:25 PM PDT', title: 'Arrive at LAS', detail: 'AA1497 from Chicago. Follow the airport rental-car signs and allow time for the off-terminal shuttle.' },
      { time: '3:30–4:30 PM', title: 'Rental car + hotel', detail: 'Photograph the vehicle, confirm the spare/tire kit and make sure the fuel policy matches the booking.' },
      { time: '5:30 PM', title: 'Easy dinner nearby', detail: 'Stay close to the Waldorf/CityCenter. The objective is food, hydration and an early night—not a Vegas evening.' },
      { time: '8:30 PM', title: 'Reset for mountain time', detail: 'Put tomorrow’s park layers and water in the car. Utah is one hour ahead.' }
    ],
    alerts: [
      { tone: 'blue', title: 'Clock change tomorrow', text: 'Las Vegas is on Pacific time; Zion is on Mountain time. The drive east costs one hour on the clock.' }
    ],
    links: [
      ['AA flight status', 'https://www.aa.com/travelInformation/flights/status'],
      ['LAS rental-car center', 'https://www.harryreidairport.com/Transportation/RentalCars']
    ]
  },
  {
    day: 2,
    date: '2026-09-06',
    dateLabel: 'Sun · Sept 6',
    route: 'Las Vegas → Springdale',
    title: 'Red-rock warm-up',
    eyebrow: 'Drive day · lose 1 hour',
    stay: 'Cliffrose Springdale · night 1 of 4',
    summary: 'Choose the direct line or a heat-aware Valley of Fire scenic detour, then walk Pa’rus at golden hour.',
    chips: ['Direct ≈2 hr 45', 'Optional Valley of Fire', 'Sunset 7:55 PM MDT'],
    schedule: [
      { time: '7:30 AM PDT', title: 'Leave Las Vegas', detail: 'Fuel up and decide on the Valley of Fire fork before reaching I-15/US-93.' },
      { time: '8:30–11:00 AM PDT', title: 'Optional: Valley of Fire scenic pass', detail: 'Sunday access should avoid the 2026 weekday west-entrance construction closure. Keep this to open roadside stops; many signature trails are closed May 15–Sept 30 for dangerous heat.' },
      { time: '12:30–2:00 PM MDT', title: 'Lunch + arrive Springdale', detail: 'The exact arrival depends on the detour. Check in when available and leave the car parked at Cliffrose.' },
      { time: '5:45 PM MDT', title: 'Pa’rus Trail', detail: 'Walk from the Visitor Center side and use the pedestrian bridge for the Watchman view. The full trail is about 3.5 miles round trip, but sunset can be a shorter out-and-back.' },
      { time: '7:55 PM MDT', title: 'Sunset, then dinner', detail: 'Carry a small light for the walk back. Do not stop on the Canyon Junction road bridge.' }
    ],
    alerts: [
      { tone: 'amber', title: 'Valley of Fire summer closures', text: 'Fire Wave, Seven Wonders, White Domes, Pink Canyon and several other trails are closed on this date. Treat the park as a scenic drive and check the alert again that morning.' },
      { tone: 'blue', title: 'Fee math', text: 'Zion and Bryce are $35 per vehicle each. The $80 America the Beautiful annual pass is only $10 more than buying both separately.' }
    ],
    links: [
      ['Direct route', 'https://www.google.com/maps/dir/Waldorf+Astoria+Las+Vegas/Cliffrose+Springdale+Curio+Collection'],
      ['Valley of Fire alerts', 'https://parks.nv.gov/parks/valley-of-fire'],
      ['Zion shuttle schedule', 'https://www.nps.gov/zion/planyourvisit/zion-canyon-shuttle-system.htm'],
      ['NPS Pa’rus Trail', 'https://www.nps.gov/zion/planyourvisit/zion-national-park-trail-information.htm']
    ]
  },
  { day: 3, date: '2026-09-07', dateLabel: 'Mon · Sept 7', route: 'Zion National Park', flexible: true, eyebrow: 'Flexible Zion day · Labor Day', stay: 'Cliffrose Springdale · night 2 of 4' },
  { day: 4, date: '2026-09-08', dateLabel: 'Tue · Sept 8', route: 'Zion National Park', flexible: true, eyebrow: 'Flexible Zion day', stay: 'Cliffrose Springdale · night 3 of 4' },
  { day: 5, date: '2026-09-09', dateLabel: 'Wed · Sept 9', route: 'Zion National Park', flexible: true, eyebrow: 'Flexible Zion day', stay: 'Cliffrose Springdale · night 4 of 4' },
  {
    day: 6,
    date: '2026-09-10',
    dateLabel: 'Thu · Sept 10',
    route: 'Springdale → Bryce Canyon',
    title: 'The east-side scenic line',
    eyebrow: 'Drive day · build in stops',
    stay: 'The Lodge at Bryce Canyon · night 1 of 2',
    summary: 'Drive UT-9 early, hike Canyon Overlook before parking disappears, then fold Red Canyon into the natural route to Bryce.',
    chips: ['≈2 hr drive only', 'Canyon Overlook 1 mi', 'Sunset 7:43 PM'],
    schedule: [
      { time: '7:00 AM', title: 'Check out and take UT-9 east', detail: 'Climb the switchbacks and pass through the Zion–Mt. Carmel Tunnel. Oversize-vehicle controls can create short holds.' },
      { time: '7:30–8:45 AM', title: 'Canyon Overlook', detail: 'One mile round trip with exposed edges. Parking just east of the tunnel is extremely limited, so skip cleanly if both legal lots are full.' },
      { time: '9:10 AM', title: 'Checkerboard Mesa pullout', detail: 'A short geology stop, not a hike. Continue east before the tour-bus wave builds.' },
      { time: '10:20 AM', title: 'Belly of the Dragon', detail: 'A short, rough drainage tunnel near Mount Carmel Junction. Do not enter if storms are possible; this is a culvert, not a maintained park trail.' },
      { time: '11:30 AM', title: 'Lunch around Orderville', detail: 'Refuel people and car before UT-12. Keep an hour in reserve for unplanned overlooks.' },
      { time: '1:30 PM', title: 'Red Canyon arches', detail: 'The two red-rock tunnels span UT-12 directly on today’s route. This fixes the original plan, which placed them on tomorrow’s southbound drive.' },
      { time: '3:00–4:00 PM', title: 'Check in at Bryce', detail: 'Settle at the Lodge, walk the rim and identify the path to Sunrise Point for the dark pre-dawn start.' },
      { time: '6:55 PM', title: 'Sunrise Point → Sunset Point', detail: 'The paved Rim Trail is about a half-mile one way. Be at Sunset Point before the 7:43 PM sunset.' }
    ],
    alerts: [
      { tone: 'red', title: 'Never stop in the tunnel', text: 'Use signed pullouts only. Canyon Overlook parking is small; an illegal roadside stop is not worth forcing the hike.' },
      { tone: 'blue', title: 'New moon tonight', text: 'The new moon arrives this evening, setting up exceptionally dark skies at Bryce on both nights.' }
    ],
    links: [
      ['Full drive with stops', 'https://www.google.com/maps/dir/Cliffrose+Springdale+Curio+Collection/Canyon+Overlook+Trail,+Utah/Checkerboard+Mesa,+Utah/Belly+of+the+Dragon,+Orderville,+UT/Red+Canyon+Arch,+Utah/The+Lodge+at+Bryce+Canyon'],
      ['NPS Canyon Overlook', 'https://www.nps.gov/thingstodo/canyon-overlook-trail.htm'],
      ['UT-9 tunnel rules', 'https://www.nps.gov/zion/planyourvisit/the-zion-mount-carmel-tunnel.htm']
    ]
  },
  {
    day: 7,
    date: '2026-09-11',
    dateLabel: 'Fri · Sept 11',
    route: 'Bryce Canyon National Park',
    title: 'Hoodoos from first light to starlight',
    eyebrow: 'Sunrise + signature loop',
    stay: 'The Lodge at Bryce Canyon · night 2 of 2',
    summary: 'Walk to sunrise—the shuttle is not running yet—then hike the classic loop clockwise and drive to Rainbow Point.',
    chips: ['Sunrise 7:07 AM', 'Loop 2.9 mi', 'Dark by ≈9:11 PM'],
    schedule: [
      { time: '6:25 AM', title: 'Walk from the Lodge', detail: 'Carry warm layers and a headlamp. The Bryce shuttle starts at 8:00 AM, so it cannot take you to a 7:07 AM sunrise.' },
      { time: '6:45–7:25 AM', title: 'Sunrise Point', detail: 'Arrive before first light, stay behind railings and expect chilly high-elevation air well below Zion’s midday temperatures.' },
      { time: '7:30 AM', title: 'Breakfast + water refill', detail: 'Return to the Lodge or eat a packed breakfast before the loop.' },
      { time: '8:30–11:30 AM', title: 'Queen’s Garden / Navajo Loop', detail: 'Go clockwise: descend Queen’s Garden from Sunrise Point, connect to Navajo, ascend Wall Street if open (Two Bridges if not), then walk the rim back. 2.9 miles, 625 feet, moderate.' },
      { time: '12:00 PM', title: 'Lunch and a quiet hour', detail: 'Altitude is about 8,000 feet at the amphitheater. Hydrate and avoid turning the afternoon into a mileage contest.' },
      { time: '2:00–5:00 PM', title: 'Scenic drive to Rainbow Point', detail: 'Drive the 18-mile park road to the end first, then stop at overlooks on the return when the pullouts are on your side.' },
      { time: '8:45 PM', title: 'Dark-sky reset', detail: 'Astronomical darkness arrives around 9:11 PM. Check the Visitor Center for a ranger astronomy program and let your eyes adapt for 20 minutes.' }
    ],
    alerts: [
      { tone: 'amber', title: 'Wall Street can close', text: 'Rockfall or weather can close the Wall Street side of Navajo Loop. Two Bridges preserves the same loop structure when Wall Street is unavailable.' },
      { tone: 'blue', title: 'Rare moon timing', text: 'The moon is under 1% illuminated and sets around sunset—about as good as a Bryce stargazing night gets.' }
    ],
    links: [
      ['NPS Queen’s Garden/Navajo loop', 'https://www.nps.gov/thingstodo/queens-garden-navajo-combination-loop.htm'],
      ['Bryce shuttle details', 'https://www.nps.gov/brca/planyourvisit/shuttle.htm'],
      ['Bryce current conditions', 'https://www.nps.gov/brca/planyourvisit/conditions.htm'],
      ['NPS astronomy programs', 'https://www.nps.gov/brca/planyourvisit/astronomyprograms.htm']
    ]
  },
  {
    day: 8,
    date: '2026-09-12',
    dateLabel: 'Sat · Sept 12',
    route: 'Bryce → Kanab → St. George',
    title: 'Sand, slickrock and a hard dinner deadline',
    eyebrow: 'Scenic return · stay disciplined',
    stay: 'The Advenire, St. George · 1 night',
    summary: 'A curated route makes Kanab, Coral Pink and a short Snow Canyon visit fit before the 7:00 PM Painted Pony reservation.',
    chips: ['≈4 hr driving', 'Dinner 7:00 PM', 'Stay on MDT'],
    schedule: [
      { time: '7:45 AM', title: 'Leave Bryce', detail: 'Red Canyon is already handled on Day 6, avoiding a northbound detour today.' },
      { time: '9:15–10:00 AM', title: 'Kanab pause', detail: 'Coffee, a short main-street walk and fuel. Keep the stop under an hour if Coral Pink remains in the plan.' },
      { time: '10:30 AM–12:00 PM', title: 'Coral Pink Sand Dunes', detail: 'Walk the edge of the dunes, not the whole field. Sand is tiring and exposed; save dry shoes in the car.' },
      { time: '1:45–4:20 PM', title: 'Snow Canyon scenic pass', detail: 'Prioritize Jenny’s Canyon (0.5 mile, easy), the Petrified Dunes overlook and signed lava-flow viewpoints. Skip Johnson Canyon, seasonally closed through Sept 14.' },
      { time: '5:00 PM', title: 'Check in at The Advenire', detail: 'Shower, change and leave buffer for parking or the short walk to Ancestor Square.' },
      { time: '6:40 PM', title: 'Arrive at Painted Pony', detail: 'Reservation is at 7:00 PM. The restaurant lists free parking behind Ancestor Square plus street parking.' }
    ],
    alerts: [
      { tone: 'red', title: 'Scout Cave does not fit', text: 'The official Scout Cave route is about 6 miles and moderate. It would put the dinner reservation at risk; Jenny’s Canyon is the right short stop.' },
      { tone: 'blue', title: 'Want more Snow Canyon?', text: 'Skip Coral Pink and use the extra time for Lava Flow (2.6 miles) or more overlooks. Do not try to do every listed stop.' }
    ],
    links: [
      ['Curated drive', 'https://www.google.com/maps/dir/The+Lodge+at+Bryce+Canyon/Kanab,+UT/Coral+Pink+Sand+Dunes+State+Park/Snow+Canyon+State+Park/The+Advenire,+Autograph+Collection'],
      ['Coral Pink Sand Dunes', 'https://stateparks.utah.gov/parks/coral-pink/'],
      ['Snow Canyon trail map', 'https://stateparks.utah.gov/parks/snow-canyon/discover/'],
      ['Painted Pony details', 'https://painted-pony.com/']
    ]
  },
  {
    day: 9,
    date: '2026-09-13',
    dateLabel: 'Sun · Sept 13',
    route: 'St. George → Las Vegas → Chicago',
    title: 'Cash in the time-zone hour',
    eyebrow: 'Flight day · gain 1 hour',
    stay: 'Home',
    summary: 'Leave St. George at 10:30 AM Mountain time and reach the rental center around 11:30 AM Pacific time.',
    chips: ['Flight 3:48 PM PDT', 'Drive ≈2 hr', 'Flight number to confirm'],
    schedule: [
      { time: '8:30 AM MDT', title: 'Breakfast + final pack', detail: 'Refill fuel if needed, check the room and separate flight layers from checked luggage.' },
      { time: '10:30 AM MDT', title: 'Leave St. George', detail: 'The westbound clock change means a roughly two-hour drive lands around 11:30 AM Pacific time.' },
      { time: '11:30 AM PDT', title: 'Rental return at LAS', detail: 'This leaves more than four hours before the scheduled flight for fuel, shuttle, bags and security.' },
      { time: '3:48 PM PDT', title: 'Fly Las Vegas → Chicago', detail: 'The source itinerary appears to contain a mistyped American flight number. Confirm it in the airline booking before departure.' }
    ],
    alerts: [
      { tone: 'amber', title: 'One unresolved item', text: 'The return flight number needs confirmation. The app preserves the 3:48 PM departure time without inventing a corrected flight.' }
    ],
    links: [
      ['Drive to LAS Rental Car Center', 'https://www.google.com/maps/dir/The+Advenire,+Autograph+Collection/Harry+Reid+International+Airport+Rent-A-Car+Center'],
      ['AA flight status', 'https://www.aa.com/travelInformation/flights/status']
    ]
  }
];

export const trailMatrix = [
  { name: 'Pa’rus Trail', place: 'Zion', distance: '3.5 mi RT', gain: 'Minimal', level: 'Easy / accessible', best: 'Sunset warm-up', caveat: 'Use the pedestrian bridge, not the road bridge.' },
  { name: 'Scout Lookout', place: 'Zion', distance: '4.2 mi RT', gain: '≈1,000–1,200 ft', level: 'Strenuous', best: 'Cool clear morning', caveat: 'Exposed edges; no permit unless continuing to Angels Landing.' },
  { name: 'The Narrows', place: 'Zion', distance: 'Variable', gain: 'River travel', level: 'Variable / strenuous', best: 'Driest safe day', caveat: 'Flash-flood and flow conditions are decisive.' },
  { name: 'Lower Emerald Pool', place: 'Zion', distance: '1.2 mi RT', gain: '≈130 ft', level: 'Easy', best: 'Flex-day stop', caveat: 'No swimming; wet rock can be slick.' },
  { name: 'Watchman Trail', place: 'Zion', distance: '3.3 mi RT', gain: '≈480 ft', level: 'Moderate', best: 'Late afternoon', caveat: 'Limited shade; headlamp if returning after sunset.' },
  { name: 'Canyon Overlook', place: 'Zion east side', distance: '1 mi RT', gain: '163 ft', level: 'Moderate', best: 'Early drive day', caveat: 'Exposed edges and extremely limited parking.' },
  { name: 'Queen’s Garden + Navajo', place: 'Bryce', distance: '2.9 mi loop', gain: '625 ft', level: 'Moderate', best: 'After sunrise', caveat: 'Clockwise; Wall Street may close.' },
  { name: 'Jenny’s Canyon', place: 'Snow Canyon', distance: '0.5 mi RT', gain: 'Minimal', level: 'Easy', best: 'Quick afternoon stop', caveat: 'A better fit than the 6-mile Scout Cave route.' }
];

export const checklist = [
  { id: 'flight-return', category: 'Confirm', label: 'Verify the return AA flight number', note: 'The source itinerary’s number appears mistyped; departure is listed as 3:48 PM.' },
  { id: 'flight-app', category: 'Confirm', label: 'Load both flights in the American app', note: 'Save boarding passes when available.' },
  { id: 'rental', category: 'Confirm', label: 'Confirm rental pickup, fuel policy and return location', note: 'Return is the LAS off-terminal Rental Car Center.' },
  { id: 'hotels', category: 'Confirm', label: 'Save all hotel confirmations offline', note: 'Use the private notes tab rather than publishing numbers.' },
  { id: 'painted-pony', category: 'Confirm', label: 'Reconfirm Painted Pony · Sept 12 at 7:00 PM', note: 'Aim to arrive by 6:40 PM.' },
  { id: 'pass', category: 'Reserve', label: 'Choose park fees or an America the Beautiful pass', note: 'Two $35 vehicle entries total $70; the annual pass is $80.' },
  { id: 'narrows-gear', category: 'Reserve', label: 'Reserve Narrows shoes, socks and poles', note: 'Choose flexible pickup because Sept 7–9 may swap.' },
  { id: 'ebike', category: 'Reserve', label: 'Reserve Class 1 e-bikes if using the flex-day plan', note: 'Confirm cancellation terms before locking the date.' },
  { id: 'east-mesa', category: 'Reserve', label: 'Book East Mesa shuttle only if choosing Observation Point', note: 'This is an alternate full-day plan, not an add-on.' },
  { id: 'offline-maps', category: 'Download', label: 'Download NPS app maps for Zion and Bryce', note: 'Also save the route in Google Maps for offline use.' },
  { id: 'conditions', category: 'Download', label: 'Bookmark Zion and Bryce current-conditions pages', note: 'Check again the night before and morning of each hike.' },
  { id: 'headlamps', category: 'Pack', label: 'Headlamps for Bryce sunrise, stars and sunset returns', note: 'Pack spare batteries.' },
  { id: 'water', category: 'Pack', label: '2–3 liters per person plus electrolytes', note: 'Carry more for exposed or river days.' },
  { id: 'layers', category: 'Pack', label: '40°F-to-95°F layering system', note: 'Bryce dawn can feel wintry while Zion afternoons are hot.' },
  { id: 'sun', category: 'Pack', label: 'Sun hat, sunscreen and sunglasses', note: 'Most routes have limited midday shade.' },
  { id: 'shoes', category: 'Pack', label: 'Dry hiking shoes plus Narrows footwear', note: 'Keep one pair dry for Bryce and dinner.' },
  { id: 'drybag', category: 'Pack', label: 'Dry bag or waterproof phone pouch', note: 'Useful in the Narrows; never rely on a pocket.' },
  { id: 'first-aid', category: 'Pack', label: 'Blister kit and basic first aid', note: 'Include any personal medications in carry-on luggage.' },
  { id: 'snacks', category: 'Pack', label: 'Trail breakfasts and salty snacks', note: 'First-shuttle mornings start before many kitchens.' }
];

export const weatherPlaces = [
  { id: 'springdale', name: 'Springdale / Zion', latitude: 37.1889, longitude: -112.9986, dates: ['2026-09-06', '2026-09-07', '2026-09-08', '2026-09-09', '2026-09-10'] },
  { id: 'bryce', name: 'Bryce Canyon', latitude: 37.6283, longitude: -112.1677, dates: ['2026-09-10', '2026-09-11', '2026-09-12'] },
  { id: 'stgeorge', name: 'St. George', latitude: 37.0965, longitude: -113.5684, dates: ['2026-09-12', '2026-09-13'] }
];

export const sources = [
  { group: 'Zion · official', label: '2026 Zion Canyon shuttle schedule', url: 'https://www.nps.gov/zion/learn/news/2026-zion-national-park-shuttle-bus-service.htm' },
  { group: 'Zion · official', label: 'Current conditions and closures', url: 'https://www.nps.gov/zion/planyourvisit/conditions.htm' },
  { group: 'Zion · official', label: 'The Narrows', url: 'https://www.nps.gov/zion/planyourvisit/thenarrows.htm' },
  { group: 'Zion · official', label: 'Trail information', url: 'https://www.nps.gov/zion/planyourvisit/zion-national-park-trail-information.htm' },
  { group: 'Zion · official', label: 'Bicycling and e-bike rules', url: 'https://www.nps.gov/zion/planyourvisit/bicycling-in-zion.htm' },
  { group: 'Zion · official', label: 'Angels Landing permits', url: 'https://www.nps.gov/zion/planyourvisit/angels-landing-hiking-permits.htm' },
  { group: 'Zion · live data', label: 'Virgin River streamflow gauge', url: 'https://waterdata.usgs.gov/monitoring-location/09405500/#parameterCode=00060&period=P7D&showMedian=false' },
  { group: 'Zion · live data', label: 'NWS flash-flood potential', url: 'https://www.weather.gov/slc/flashflood' },
  { group: 'Bryce · official', label: '2026 Bryce shuttle', url: 'https://www.nps.gov/brca/planyourvisit/shuttle.htm' },
  { group: 'Bryce · official', label: 'Queen’s Garden/Navajo combination', url: 'https://www.nps.gov/thingstodo/queens-garden-navajo-combination-loop.htm' },
  { group: 'Bryce · official', label: 'Scenic drive', url: 'https://www.nps.gov/brca/planyourvisit/scenicdrive.htm' },
  { group: 'Bryce · official', label: 'Astronomy programs', url: 'https://www.nps.gov/brca/planyourvisit/astronomyprograms.htm' },
  { group: 'State parks', label: 'Valley of Fire alerts and closures', url: 'https://parks.nv.gov/parks/valley-of-fire' },
  { group: 'State parks', label: 'Coral Pink Sand Dunes', url: 'https://stateparks.utah.gov/parks/coral-pink/' },
  { group: 'State parks', label: 'Snow Canyon trail information', url: 'https://stateparks.utah.gov/parks/snow-canyon/discover/' },
  { group: 'Roads', label: 'Utah traffic and road conditions', url: 'https://www.udottraffic.utah.gov/' },
  { group: 'Weather', label: 'Open-Meteo forecast API', url: 'https://open-meteo.com/' },
  { group: 'Dining', label: 'Painted Pony', url: 'https://painted-pony.com/' }
];
