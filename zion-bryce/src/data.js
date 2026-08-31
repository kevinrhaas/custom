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
    carry: [
      { id: 'water-3l', label: '3 liters of water per person' },
      { id: 'breakfast-lunch', label: 'Packed breakfast, salty snacks and lunch' },
      { id: 'sun-kit', label: 'Sun hoodie or shirt, hat, sunscreen and sunglasses' },
      { id: 'trail-shoes', label: 'Dry hiking shoes with dependable traction' },
      { id: 'poles', label: 'Trekking poles, if helpful on the descent' },
      { id: 'phone-power', label: 'Phone, offline map and small power bank' }
    ],
    tips: [
      { title: 'Use the restroom at The Grotto', text: 'There are no facilities on the climb. Refill water and go before leaving the shuttle stop.' },
      { title: 'Set a turnaround time', text: 'Aim to leave Scout Lookout by about 10:15 AM so the exposed descent is finished before peak heat.' },
      { title: 'Protect the knees', text: 'Short steps and poles help on the steep return through Walter’s Wiggles; descending often feels harder than climbing.' }
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
    carry: [
      { id: 'river-kit', label: 'Canyon shoes, neoprene socks and wooden river pole' },
      { id: 'drybag', label: 'Dry bag or waterproof phone pouch' },
      { id: 'warm-layer', label: 'Quick-dry layers plus a light warm layer' },
      { id: 'water-2l', label: 'At least 2 liters of drinking water per person' },
      { id: 'food', label: 'Breakfast, trail food and salty snacks' },
      { id: 'car-change', label: 'Complete dry change and towel left at the hotel' }
    ],
    tips: [
      { title: 'Check the whole watershed', text: 'A blue sky over Springdale is not enough—storms upstream can reach the Narrows later.' },
      { title: 'The pole matters', text: 'Plant it before each step and maintain three points of contact. Ordinary trekking poles are less stable between submerged rocks.' },
      { title: 'Turn around early', text: 'Make 11:00 AM the default turnaround even if Wall Street is close. The return takes longer when the river gets crowded.' }
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
    carry: [
      { id: 'water-2l', label: '2 liters of water per person' },
      { id: 'bike-sun', label: 'Sun protection and a light long-sleeve layer' },
      { id: 'bike-glasses', label: 'Sunglasses or clear eye protection for riding' },
      { id: 'trail-shoes', label: 'Walking shoes for Emerald Pools or Watchman' },
      { id: 'headlamp', label: 'Headlamp if Watchman remains an option' },
      { id: 'swimsuit', label: 'Swimsuit and a separate dry outfit for downtime' }
    ],
    tips: [
      { title: 'Confirm the bike class', text: 'Only Class 1 pedal-assist e-bikes are allowed. Test brakes, battery level and saddle height before leaving town.' },
      { title: 'Yield completely to shuttles', text: 'Pull over, stop and place one foot down. Ride single-file and expect to pedal both directions.' },
      { title: 'Choose one sunset', text: 'Watchman is a real moderate hike; Pa’rus is the recovery-day choice. Do not force both.' }
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

export const brycePlanOptions = {
  arrival: {
    label: 'Arrival evening · Sept 10',
    help: 'Choose based on arrival time and energy. Sunset is 7:43 PM.',
    options: {
      rim: {
        short: 'Rim walk to sunset',
        description: 'Walk the paved half-mile from Sunrise Point to Sunset Point.',
        entry: { time: '6:55 PM', title: 'Sunrise Point → Sunset Point', detail: 'The paved Rim Trail is about a half-mile one way. Be at Sunset Point before the 7:43 PM sunset.' }
      },
      direct: {
        short: 'Sunset Point only',
        description: 'Protect a late arrival or tired legs with one excellent overlook.',
        entry: { time: '7:05 PM', title: 'Go directly to Sunset Point', detail: 'Use the shortest version of the evening: settle in, carry a warm layer and reach the overlook before the 7:43 PM sunset.' }
      }
    }
  },
  afternoon: {
    label: 'Full-day afternoon · Sept 11',
    help: 'The morning sunrise and classic loop stay fixed; choose how much driving follows.',
    options: {
      rainbow: {
        short: 'Rainbow Point drive',
        description: 'Cover the full 18-mile park road and work back through overlooks.',
        entry: { time: '2:00–5:00 PM', title: 'Scenic drive to Rainbow Point', detail: 'Drive the 18-mile park road to the end first, then stop at overlooks on the return when the pullouts are on your side.' }
      },
      rim: {
        short: 'Lodge reset + rim overlooks',
        description: 'Trade driving for recovery and short amphitheater viewpoints.',
        entry: { time: '2:30–5:00 PM', title: 'Lodge reset + amphitheater overlooks', detail: 'Rest at the Lodge, then choose one or two rim stops such as Inspiration Point or Bryce Point. Keep this version deliberately low-mileage.' }
      }
    }
  },
  night: {
    label: 'Night plan · Sept 11',
    help: 'Dark skies are exceptional, but clouds and fatigue get the final vote.',
    options: {
      stars: {
        short: 'Dark-sky session',
        description: 'Use the new moon for stargazing after astronomical darkness.',
        entry: { time: '8:45 PM', title: 'Dark-sky reset', detail: 'Astronomical darkness arrives around 9:11 PM. Check the Visitor Center for a ranger astronomy program and let your eyes adapt for 20 minutes.' }
      },
      rest: {
        short: 'Early night',
        description: 'Bank recovery if clouds, cold or altitude make stars a poor trade.',
        entry: { time: '8:30 PM', title: 'Early night at the Lodge', detail: 'Skip the late outing, organize tomorrow’s southbound drive and get a full night at altitude.' }
      }
    }
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
    chips: ['AA1497', 'ORD 10:30 AM CDT', 'LAS 12:25 PM PDT'],
    schedule: [
      { time: '10:30 AM CDT', title: 'Fly Chicago → Las Vegas', detail: 'AA1497 nonstop from ORD. Scheduled arrival is 12:25 PM Pacific time.' },
      { time: '12:25 PM PDT', title: 'Arrive at LAS', detail: 'Follow the airport rental-car signs and allow time for the off-terminal Rental Car Center shuttle.' },
      { time: '1:30–2:30 PM', title: 'Rental car + hotel', detail: 'Photograph the vehicle, confirm the spare/tire kit and make sure the fuel policy matches the booking.' },
      { time: '5:00 PM', title: 'Easy dinner nearby', detail: 'Stay close to the Waldorf/CityCenter. The objective is food, hydration and an early night—not a Vegas evening.' },
      { time: '8:30 PM', title: 'Reset for mountain time', detail: 'Put tomorrow’s park layers and water in the car. Utah is one hour ahead.' }
    ],
    carry: [
      { id: 'id-wallet', label: 'Photo ID, wallet and airline details' },
      { id: 'rental', label: 'Rental confirmation and driver’s license' },
      { id: 'charger', label: 'Phone charger and power bank in carry-on' },
      { id: 'meds', label: 'Medication and one essential outfit in carry-on' },
      { id: 'light-layer', label: 'Light layer for the flight and hotel' }
    ],
    tips: [
      { title: 'Photograph the rental', text: 'Capture every side, wheels, fuel gauge and odometer before leaving the garage.' },
      { title: 'Keep valuables invisible', text: 'Move luggage directly to the hotel; do not leave visible bags in the vehicle during dinner.' },
      { title: 'Buy tomorrow’s basics', text: 'If energy allows, pick up a cooler, gallon of car water and breakfast supplies before the early start.' }
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
    carry: [
      { id: 'park-pass', label: 'Park pass or card for entrance fees' },
      { id: 'car-water', label: 'Extra gallon of water in the car' },
      { id: 'cooler-food', label: 'Cooler, lunch and road snacks' },
      { id: 'sun-kit', label: 'Hat, sunscreen, sunglasses and light long sleeves' },
      { id: 'walk-shoes', label: 'Walking shoes for Pa’rus Trail' },
      { id: 'headlamp', label: 'Small headlamp for the walk after sunset' }
    ],
    tips: [
      { title: 'Make the detour decision early', text: 'Valley of Fire adds hours, not minutes. Skip it if the temperature is extreme or the flight day left everyone tired.' },
      { title: 'Change the car clock in Utah', text: 'Phones update automatically; the dashboard may not. Utah is one hour ahead of Las Vegas.' },
      { title: 'Leave the car at Cliffrose', text: 'Walk the roughly half-mile to the Visitor Center instead of joining the parking queue.' }
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
    carry: [
      { id: 'daypack', label: 'Small daypack kept accessible between stops' },
      { id: 'water-food', label: '2 liters of water, lunch and road snacks' },
      { id: 'trail-shoes', label: 'Hiking shoes for Canyon Overlook' },
      { id: 'layers', label: 'Warm Bryce layer moved out of packed luggage' },
      { id: 'headlamp', label: 'Headlamp for the post-sunset walk' },
      { id: 'paper-route', label: 'Offline route and hotel address' }
    ],
    tips: [
      { title: 'Never circle for Canyon Overlook', text: 'Check both legal lots once. If full, continue—the schedule has plenty of scenery without it.' },
      { title: 'Treat Belly as a culvert', text: 'Skip it with any storm potential and expect rough footing, mud or standing water.' },
      { title: 'Expect a temperature drop', text: 'Bryce sits thousands of feet above Springdale. Put the warm layer in the cabin, not under the luggage.' }
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
    carry: [
      { id: 'warm-kit', label: 'Warm jacket, beanie and thin gloves' },
      { id: 'red-headlamp', label: 'Headlamp with a true red-light mode' },
      { id: 'water-3l', label: '2–3 liters of water plus electrolytes' },
      { id: 'trail-food', label: 'Breakfast, lunch and salty snacks' },
      { id: 'trail-shoes', label: 'Hiking shoes with good downhill traction' },
      { id: 'poles', label: 'Trekking poles for the Navajo ascent' },
      { id: 'stars', label: 'Binoculars and stargazing app downloaded offline' }
    ],
    tips: [
      { title: 'Walk, do not wait for a bus', text: 'The shuttle starts after sunrise. Follow the rim path from the Lodge with a headlamp.' },
      { title: 'Pause at altitude', text: 'The rim is near 8,000 feet and Rainbow Point exceeds 9,000. Hydrate and keep the first climb deliberately slow.' },
      { title: 'Preserve night vision', text: 'Use red light only after dark, dim phone screens and allow about 20 minutes for your eyes to adapt.' }
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
    carry: [
      { id: 'car-water', label: 'Extra water and electrolytes in the car' },
      { id: 'sand-shoes', label: 'Closed shoes for sand plus clean socks' },
      { id: 'towel-bag', label: 'Small towel and bag for sandy clothing' },
      { id: 'sun-kit', label: 'Hat, sunscreen and sunglasses' },
      { id: 'dinner-clothes', label: 'Dinner clothes kept separate and clean' },
      { id: 'reservation', label: 'Painted Pony reservation saved offline' }
    ],
    tips: [
      { title: 'Use the noon gate', text: 'If leaving Coral Pink after 12:15 PM, shorten Snow Canyon immediately rather than borrowing time from dinner.' },
      { title: 'Use the 2:30 gate', text: 'Arriving at Snow Canyon after 2:30 means Jenny’s Canyon only; after 3:30, skip the hike.' },
      { title: 'Change before the restaurant', text: 'Sand travels. Bag dusty shoes and clothes before checking in so dinner gear stays clean.' }
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
    summary: 'Leave St. George at 7:45 AM Mountain time, return the car around 9:00 AM Pacific time and protect the 12:56 PM departure.',
    chips: ['AA1497', 'LAS 12:56 PM PDT', 'ORD 7:19 PM CDT'],
    schedule: [
      { time: '6:30 AM MDT', title: 'Breakfast + final pack', detail: 'Check the room, load the car and keep flight layers outside checked luggage.' },
      { time: '7:45 AM MDT', title: 'Leave St. George', detail: 'After gaining an hour at the Nevada line, a roughly two-hour drive reaches Las Vegas around 8:45 AM Pacific time. Keep 15 minutes for fuel.' },
      { time: '9:00 AM PDT', title: 'Rental return at LAS', detail: 'Target the off-terminal Rental Car Center about four hours before departure, leaving comfortable time for the shuttle, checked bags and security.' },
      { time: '12:56 PM PDT', title: 'AA1497 · Las Vegas → Chicago', detail: 'Nonstop to ORD, scheduled to arrive at 7:19 PM Central time.' },
      { time: '7:19 PM CDT', title: 'Arrive at ORD', detail: 'Collect bags and head home.' }
    ],
    carry: [
      { id: 'id-wallet', label: 'Photo ID, wallet and confirmed flight details' },
      { id: 'rental-receipt', label: 'Rental agreement and fuel receipt' },
      { id: 'flight-layer', label: 'Flight layer kept outside checked luggage' },
      { id: 'charger', label: 'Phone charger and power bank' },
      { id: 'snacks', label: 'Water bottle emptied for security and travel snacks' }
    ],
    tips: [
      { title: 'Use 7:45 as the hard departure', text: 'Do not let breakfast or repacking consume the highway buffer; the flight now leaves before 1:00 PM.' },
      { title: 'Keep the clock math visible', text: '7:45 AM Mountain becomes roughly 8:45 AM Pacific after the two-hour drive.' },
      { title: 'Photograph the final dashboard', text: 'Capture fuel and mileage at return, then keep the rental receipt until the final charge settles.' }
    ],
    alerts: [
      { tone: 'blue', title: 'Confirmed return', text: 'AA1497 departs LAS at 12:56 PM PDT and arrives ORD at 7:19 PM CDT. The public guide intentionally omits the booking confirmation code.' }
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
  { id: 'flight-return', category: 'Confirm', label: 'Save return flight AA1497 offline', note: 'LAS 12:56 PM PDT → ORD 7:19 PM CDT on Sept 13.' },
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
  { id: 'offline-stays', category: 'Download', label: 'Screenshot hotels, rental and Painted Pony details', note: 'Do not depend on cell service to retrieve confirmations.' },

  { id: 'photo-id', category: 'Documents', label: 'Photo ID and driver’s license', note: 'Keep both in the flight-day personal item.' },
  { id: 'insurance-card', category: 'Documents', label: 'Health-insurance card and emergency contacts', note: 'Store a paper copy separately from the phone.' },
  { id: 'park-pass-paper', category: 'Documents', label: 'Park pass or payment card', note: 'Keep it accessible in the vehicle, not packed in luggage.' },
  { id: 'itinerary-paper', category: 'Documents', label: 'One-page paper itinerary and hotel addresses', note: 'Useful when navigation or phone service fails.' },

  { id: 'daypack', category: 'Trail', label: 'Comfortable 15–25 liter daypack', note: 'Large enough for water, food and layers without overpacking.' },
  { id: 'headlamps', category: 'Trail', label: 'Headlamps with spare batteries', note: 'At least one should have a true red-light mode for Bryce.' },
  { id: 'water', category: 'Trail', label: '2–3 liter water capacity per person', note: 'Carry more for exposed days and keep reserve water in the car.' },
  { id: 'poles', category: 'Trail', label: 'Collapsible trekking poles', note: 'Helpful on Scout Lookout and the Bryce switchbacks; not a substitute for a Narrows pole.' },
  { id: 'binoculars', category: 'Trail', label: 'Compact binoculars for Bryce dark skies', note: 'More travel-friendly than a telescope under the near-new moon.' },
  { id: 'sit-pad', category: 'Trail', label: 'Small sit pad or packable towel', note: 'Useful on the Lodge lawn, wet river gear and sunrise overlooks.' },

  { id: 'layers', category: 'Clothing', label: '40°F-to-95°F layering system', note: 'Bryce dawn can feel wintry while Zion afternoons are hot.' },
  { id: 'shoes', category: 'Clothing', label: 'Broken-in dry hiking shoes', note: 'Keep these separate from Narrows footwear.' },
  { id: 'socks', category: 'Clothing', label: 'Hiking socks plus two spare pairs', note: 'Carry a dry pair in the daypack on river and sand days.' },
  { id: 'sun-shirt', category: 'Clothing', label: 'Sun hoodie or light long-sleeve shirt', note: 'Better all-day coverage than repeatedly applying sunscreen.' },
  { id: 'warm-jacket', category: 'Clothing', label: 'Packable fleece or light down jacket', note: 'Keep it accessible during the drive to Bryce.' },
  { id: 'rain-shell', category: 'Clothing', label: 'Light rain shell', note: 'For wind and brief rain—not permission to hike during flood risk.' },
  { id: 'cold-accessories', category: 'Clothing', label: 'Thin gloves and beanie', note: 'Small weight, large payoff at Bryce sunrise.' },
  { id: 'swimsuit', category: 'Clothing', label: 'Swimsuit and casual recovery clothes', note: 'Useful for the Cliffrose pool and post-hike downtime.' },
  { id: 'dinner-outfit', category: 'Clothing', label: 'Clean Painted Pony outfit and shoes', note: 'Pack separately from sand and hiking gear.' },

  { id: 'drybag', category: 'Narrows', label: 'Dry bag or waterproof phone pouch', note: 'Never rely on a pocket or ordinary backpack zipper.' },
  { id: 'quick-dry', category: 'Narrows', label: 'Quick-dry shorts or pants and synthetic layers', note: 'Avoid cotton in the river.' },
  { id: 'river-change', category: 'Narrows', label: 'Complete dry change and towel', note: 'Leave it ready at Cliffrose for the return.' },

  { id: 'sun', category: 'Health', label: 'Sun hat, sunscreen, sunglasses and lip balm', note: 'Most routes have limited midday shade.' },
  { id: 'first-aid', category: 'Health', label: 'Blister kit and basic first aid', note: 'Include tape, bandages, pain relief and antiseptic.' },
  { id: 'medications', category: 'Health', label: 'Prescription medication plus one spare day', note: 'Keep it in carry-on luggage, never the checked bag.' },
  { id: 'electrolytes', category: 'Health', label: 'Electrolyte packets', note: 'Heat, altitude and dry air make plain water insufficient for some hikers.' },
  { id: 'sanitizer', category: 'Health', label: 'Hand sanitizer, tissues and small toilet kit', note: 'Facilities are limited on long trail and scenic-drive stretches.' },
  { id: 'bug-spray', category: 'Health', label: 'Small insect repellent', note: 'Mostly for dusk near the river and Springdale rather than exposed trails.' },

  { id: 'car-water', category: 'Car', label: 'One extra gallon of water', note: 'Emergency reserve; refill as it is used.' },
  { id: 'cooler', category: 'Car', label: 'Small soft cooler and reusable ice packs', note: 'Keeps early breakfasts, lunches and drinks available.' },
  { id: 'car-charger', category: 'Car', label: '12V/USB car charger and spare cable', note: 'Navigation days can drain a phone quickly.' },
  { id: 'trash-bags', category: 'Car', label: 'Trash bags and zip bags for wet or sandy gear', note: 'Keep dinner clothes and dry shoes isolated.' },
  { id: 'rental-kit', category: 'Car', label: 'Rental inspection photos and roadside number', note: 'Confirm the tire-inflation kit or spare before leaving Las Vegas.' },

  { id: 'power-bank', category: 'Electronics', label: 'Charged power bank', note: 'Keep it in the daypack, not the vehicle.' },
  { id: 'cables', category: 'Electronics', label: 'Phone, watch and camera charging cables', note: 'Add a compact multi-port wall charger.' },
  { id: 'camera', category: 'Electronics', label: 'Camera or phone tripod and lens cloth', note: 'A small stable support is useful for Bryce night photos.' },
  { id: 'star-app', category: 'Electronics', label: 'Stargazing app with offline data', note: 'Sky Guide or Stellarium works well without cell service.' },

  { id: 'snacks', category: 'Food', label: 'Trail breakfasts and salty snacks', note: 'First-shuttle mornings begin before many kitchens.' },
  { id: 'lunches', category: 'Food', label: 'Packable lunch supplies', note: 'Plan at least Scout, Narrows and the Bryce loop lunches in advance.' },
  { id: 'road-food', category: 'Food', label: 'Shelf-stable road snacks', note: 'Keep a separate reserve for Days 6, 8 and 9.' },
  { id: 'bottles', category: 'Food', label: 'Reusable bottles or hydration reservoirs', note: 'Label them so each person’s capacity is obvious.' }
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
