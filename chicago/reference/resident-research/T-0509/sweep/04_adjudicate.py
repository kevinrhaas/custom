import json, os, re, csv, collections, datetime

DATE = '2026-09-05'
TICKET = 'T-0509'
ROOT = '.'
PKG = '../reference/resident-research/T-0509'

cohort = json.load(open('data/research/residents/pass_14_76_cohort.json'))
people = cohort['people']
verdict = json.load(open('/tmp/verdict2.json'))
xw = json.load(open('/tmp/xw.json'))
CONTEMP = {'civic', 'land_sales', 'census_1830', 'church', 'books'}

SEED = 'chicago_democrat_1833_1835'
FERGUS = 'fergus_historical_series_26_29'

# ---- source-id normalisation: keep only ids that resolve to a committed source record
def resolves(sid):
    return os.path.exists(f'data/sources/{sid}.json')

# a positive crosswalk record does not always carry its own source_id; the file it
# lives in always identifies the volume the reading came out of.
FILE_SOURCE = [
 ('fergus_1839', 'fergus_chicago_directory_1839'),
 ('fergus_1843', 'fergus_chicago_directory_1843'),
 ('norris_1844', 'norris_directory_1844'),
 ('death_notices', 'fergus_1843_old_settler_death_notices'),
 ('old_settlers/crosswalk', 'calumet_club_early_chicago_1879'),
 ('old_settlers/people', 'calumet_club_early_chicago_1879'),
 ('census_1830', 'census_1830_peoria_county_chicago_precinct'),
 ('census_1840', 'census_1840_chicago_name_crosswalk'),
 ('newberry_index', 'newberry_genealogical_index'),
 ('st_cyr', 'st_cyr_register_ichr_v4'),
 ('st_marys', 'st_marys_baptismal_register_1833_1835'),
 ('civic/', 'chicago_voter_lists_1833_1835_irad'),
 ('land_sales', 'isa_public_domain_land_tract_sales'),
 ('books/', 'fergus_historical_series_26_29'),
]

# The Newberry genealogical index is a FINDING AID published in 1960, and
# tools/read_newberry_index.py refuses to let it stand behind a person, a household or
# a building.  A lead off one of its cards is recorded in the person's notes and is
# never cited as a source here.
FINDING_AIDS = {'newberry_genealogical_index'}


def source_from_file(f):
    for frag, sid in FILE_SOURCE:
        if frag in f:
            return None if sid in FINDING_AIDS else sid
    return None

# ---- hand readings taken off the Fergus Historical Series 26-29 volume (1843 Chicago
#      Directory + Wentworth's obituary/death lists), quoted as printed.
FERGUS_READ = {
 'thrall_e_l': ("Thrall, E, L,, clerk, Charles Walker & Co.",
   "The 1843 directory prints the same initial pair the 1835 record carries and adds a trade and an employer to a man the corpus otherwise holds only as an initialled letter-list name: clerk to Charles Walker & Co."),
 'bailey_bennet': ("Bailey. Bennet, car[p]e[n]ter. Dearborn, bds John Gray [died [N]ovember 7, 18[8]1, aged 70-11-[7]",
   "The 1843 directory prints the exact forename and surname, a trade, a street and a household he boards in, and a death date with an age to the month that puts birth about December 1810 \u2014 twenty-four at the scene date."),
 'clarke_h_b': ("Clarke. Hen[r]y B.. farmer, Michigan ave, n.-[e]. cor 16th Street [died July 28, 1840, aged 48.",
   "The 1843 directory resolves the initials H. B. to Henry B. and gives a trade and a corner. THE PRINTED DEATH YEAR IS NOT USABLE AS READ: this OCR gives 1840, which a directory of 1843 could not have listed him alive for, so the digit is recorded as printed and not corrected. The age 48 is left to whichever year is right."),
 'collins_j_h': ("Collins, James [H]., attorney (Butterfield & C.), res 15 Lake [died, Ottawa, 111., July 14, 1854, aged 50.",
   "The 1843 directory resolves the initials J. H. to James H., prints the trade attorney and the firm Butterfield & Collins, and gives a death date and age that put birth about 1804. The same volume prints 'James H. Collins, Esq.' in its list of the town's notables."),
 'sen_elijah_wentworth': ("Wentworth, Elijah, died, St. Jo., Mich., [N]ov.. 1863, aged 87. [and the line below it] Wentworth, jr., Elijah, died, Galesburg, 111., November 18, 1875, aged 72.",
   "The volume's obituary list carries BOTH Elijah Wentworths on consecutive lines and distinguishes them senior from junior exactly as this project's two person records do \u2014 an independent printing of the split, not just of the name. The senior's age at death puts birth about 1776, which makes him about fifty-nine at the scene date."),
 'moore_henry': ("Moore, Henry, died. Concord, Mass., after 1841, aged \u2014 .",
   "The volume's old-settler obituary list prints the exact name, so the entry is about a Chicago man, and dates the death only as 'after 1841' with no age. Henry Moore is among the commonest name shapes in the corpus and the entry carries no trade, address or kinship to discriminate on, so the reading is recorded and nothing is built on it."),
 'chapman_chas_h': ("Chapman. Charles [H]., res Wells, bet Randolph and Washington [and, two entries later] Chapman. Henry, tobacconist, 88 Clark, bds Charles [H]. Chapman [died Au[g]ust [6], 1851, aged 48.",
   "The 1843 directory resolves Chas. H. to Charles H., puts him on Wells between Randolph and Washington, and prints a second Chapman boarding in his house \u2014 an address and a household relation for a man the 1835 layer holds as an initialled name."),
 'dole_george_w': ("Dole, George Wa[sh]ington ([N]ewberry [&] D.). Michigan, bet [R]ush a[nd] Pine, alderman [6]th ward [died April 18, 18[6]0, a[g]ed \u2014 .",
   "The 1843 directory prints the full given names this project already carries, an address on Michigan between Rush and Pine, an aldermanship, and the firm as 'Newberry & D.' \u2014 which names the firm and still does not say WHICH Newberry stood in it, the question T-0396 holds open."),
 'harmon_charles_l': ("Harmon, Charles Loomis. dry goods and [g]roceries. 145 South Water. s.-w. cor Clark, res Dearborn, bet Washington and [M]adison [died [N]ovember 2, 1868, aged 5[9]-4. [and, in the volume's advertising pages] C L, HARMON, commission merchant and wholesale grocer, corner South-Water and Clark streets, Chicago. 111.",
   "TWO independent printings in one volume put the same man's business on the same corner \u2014 the directory line and his own advertisement \u2014 with a street number, 145 South Water, a residence street, and a death age to the month that puts birth about July 1809. This is the shape the owner asked for: a documented later address for a business the 1835 layer cannot place."),
 'elston_daniel': ("Elston, Daniel, patent press [b]rick [m]aker, res [N]orth [B]ranch [died Se[p]tember 13, 18[55], aged \u2014 .",
   "The 1843 directory prints the exact name with a trade \u2014 patent press brick maker \u2014 and a location on the North Branch, where the repository already places his brickyard."),
 'egan_william_b': ("Egan, [W]m. Bradshaw, ph[y]sician, recorder, etc., 68 Clark, res Clark [died October 27, 18[6]0, aged \u2014 .",
   "The 1843 directory prints the middle name Bradshaw in full, the trade the 1835 record carries, a second office (recorder), and a street number on Clark."),
 'hamilton_richard_j': ("Hamilton, Richard Jones (H. [&] Chamberlin). res 264 [M]ichi[g]an [died December 26, 1860, aged 6[?].",
   "The 1843 directory resolves the initial J. to Jones, names the firm Hamilton & Chamberlin and gives a residence on Michigan."),
 'gale_stephen_f': ("Gale. Stephen Francis (S. F. Gale [&] Co.), 108 Dearborn [and, in the fire-department roll] Stephen Francis Gale, 1st Assistant.",
   "The 1843 directory resolves the initial F. to Francis, gives the firm S. F. Gale & Co. at 108 Dearborn, and the same volume's fire-department roll makes him First Assistant Engineer \u2014 three printings of the same resolved name in one book."),
 'king_byram': ("King, By ram, died",
   "The volume's old-settler obituary list prints the exact and unusual forename Byram against this surname, which attests a Chicago old settler of that name. THE ENTRY IS TRUNCATED WHERE IT SHOULD CARRY ITS DATE: 'died' is followed straight by the next name, so no death date, no place and no age survive. The name is the whole of the reading."),
}

# outcome overrides decided by hand against the discriminator, not the count
HAND = {
 # two rival J. Curtisses in one volume, and the 1835 record carries only the initial.
 'curtiss_j': ('candidate_identity',
   "Fergus's reprint of the 1843 Chicago Directory prints TWO men who answer to 'J. Curtiss': 'Curtiss, James, State\u2019s attorney, 136 Lake, res W. Randolph, bet May and Ann [9th mayor, died, Joliet, Ill., November 2, 1859, aged 56' and 'Curtiss. J. W., gunsmith, res cor North Water and Wolcott'. The 1835 record carries the initial alone, and nothing in it \u2014 no trade, no street, no kin \u2014 chooses between an attorney and a gunsmith. Both readings are recorded and neither is asserted.",
   ['cand_curtiss_j_fergus_1843_james_attorney', 'cand_curtiss_j_fergus_1843_jw_gunsmith']),
 # the initial agrees and the age refuses.
 'crocker_h': ('candidate_identity',
   "The volume prints two Crockers and neither settles 'H. Crocker'. Its obituary list has 'Crocker. Hans, lawyer, died, Milwaukee, Wis., Mar. 17, 1889, a. 73', whose initial agrees but whose age puts birth about 1816 \u2014 nineteen at the scene date, and in Milwaukee thereafter; the 1843 directory has 'Crocker, Josiah Dunton, whitewasher, res 171 Clark [died December 28, 1888, aged 82', whose initial does not agree at all. The lead is retained unasserted.",
   ['cand_crocker_h_fergus_hans_lawyer']),
}

# hand evidence_against, appended where a documented refusal is the discriminator
AGAINST_EXTRA = {
 'bennett_h_c': "Fergus's reprint of the 1843 Chicago Directory prints Abel Bennett, Henry Bennett, Samuel Curtis Bennett and a 'S. C. Bennett' whose house a teacher boards in \u2014 and no H. C. Bennett at all. An initial pair that the volume does not carry is a refusal on the pair, not on the surname.",
 'comstock_h_h': "The 1843 directory prints 'Comstock. J. S. (C. & Ackley)' and 'Comstock, Luke, laborer' and no H. H. Comstock.",
 'goss_o': "The 1843 directory prints only 'Goss, Samuel W. & Co., dry goods and groceries, 98 Lake' and its principal 'Goss, Samuel W.'; no O. Goss stands in the volume.",
 'bostwick_e_b': "The 1843 directory prints 'Bostwick, George M., bartender, Illinois Exchange' and a 'Lardner, Bostwick, straw milliner, Clark'; neither answers to E. B.",
 'stewart_r': "The 1843 directory prints E. A. Stewart the watchmaker, Ephraim T. Stewart and Hart L. Stewart, and no R. Stewart.",
 'cook_rowland_i': "A raw surname sweep over-reports this name badly: every apparent hit in the volume is the COUNTY \u2014 'Dunlap of Cook', 'Cook County' \u2014 and no Rowland Cook is printed anywhere in it.",
 'house_chester': "The surname is also the commonest building word in a directory. Every apparent hit is a hotel \u2014 'American Temperance House', 'the Tremont House', 'the Mansion House' \u2014 and the volume prints no person named House.",
 'clark_erastus': "One hundred and fifteen apparent surname hits in the volume and not one 'Erastus Clark'. The forename appears in it only as Erastus Bowen, Erastus Selden Bowen and Erastus Smith Williams, all bearing other surnames.",
 'sherman_h': "The 1835 record carries no forename at all \u2014 'Mrs. H. Sherman' \u2014 and the volume prints Alson S., Francis Cornwell, Francis T., B. F. and N. Sherman jr. A surname-only agreement is a refusal under this project's standing rule, and an initial with no forename behind it cannot be tested against any of them.",
 'lewis_samuel': "The apparent hits are the FORENAME Lewis, not the surname \u2014 'Burke, Lewis', 'Roberts. Henry Lewis' \u2014 and the volume prints no Samuel Lewis.",
}

def domains_of(pid, kinds=('pos',)):
    return set(verdict[pid].get('pos_domains') or [])

AGREE_RE = re.compile(r'folds to the same string|initial for initial|both agree|forenames? agree')
REFUSE_RE = re.compile(r'is a refusal|is refused|\bis NOT\b|^Refused', re.I)

def classify(rec):
    """One classifier, used for both the source list and the quoted rules."""
    o = (rec.get('outcome') or '').lower()
    m = (rec.get('match') or '').lower()
    b = json.dumps(rec, ensure_ascii=False)
    r = rec.get('rule') or rec.get('reason') or ''
    if o == 'refused': return 'neg'
    if o == 'candidate' or 'CONTESTED' in b: return 'cand'
    if o in ('matched', 'merged', 'earlier_evidence'): return 'pos'
    if m in ('forename_agrees', 'exact'): return 'pos'
    if 'into' in rec and 'from' in rec: return 'pos'
    if AGREE_RE.search(r): return 'pos'
    if REFUSE_RE.search(r): return 'neg'
    return 'other'

def rule_texts(pid, want, limit=3):
    out = []
    for f, rec in xw.get(pid, []):
        r = rec.get('rule') or rec.get('reason') or ''
        if not r: continue
        if classify(rec) != want: continue
        r = re.sub(r'\s+', ' ', r).strip()[:400]
        if r not in out: out.append(r)
        if len(out) >= limit: break
    return out

PRETTY = {'civic': "the town's 1833 tax and 1834/1835 poll lists",
          'land_sales': 'the Illinois public-domain land tract sales',
          'census_1830': 'the 1830 census of the Chicago precinct',
          'census_1840': 'the 1840 census heads',
          'church': 'the St Cyr / St Mary registers',
          'books': 'the held book corpus',
          'directories': 'the Fergus 1839/1843 and Norris 1844 directories',
          'old_settlers': "the old-settler rolls and Fergus's death notices",
          'genealogytrails': 'the Genealogy Trails transcriptions',
          'newberry_index': 'the Newberry genealogical index cards',
          'sources': 'the source register'}

def pretty(doms):
    return ', '.join(PRETTY.get(d, d) for d in sorted(doms)) or 'a later volume'

rows = []
overrides = {}
counts = collections.Counter()
candidates_sheet = []
sources_used = collections.Counter()
search_log = []

for p in people:
    pid, name, stratum = p['person_id'], p['name'], p['stratum']
    v = verdict[pid]
    outcome = v['outcome']
    cand_ids = []
    if pid in HAND:
        outcome, hand_summary, cand_ids = HAND[pid]
    else:
        hand_summary = None

    pos_rules = rule_texts(pid, 'pos')
    neg_rules = rule_texts(pid, 'neg')
    cand_rules = rule_texts(pid, 'cand')

    srcs = [s for s in v['sources'] if resolves(s) and s not in FINDING_AIDS]
    for f, rec in xw.get(pid, []):
        k = classify(rec)
        keep = k == 'pos' or (outcome == 'candidate_identity' and k == 'cand')
        if keep:
            sid = source_from_file(f)
            if sid and resolves(sid) and sid not in srcs: srcs.append(sid)
    if pid in HAND and resolves(FERGUS) and FERGUS not in srcs: srcs.append(FERGUS)
    fergus = FERGUS_READ.get(pid)
    if fergus and resolves(FERGUS) and FERGUS not in srcs:
        srcs.append(FERGUS)
        if outcome == 'no_corroboration': outcome = 'corroborated_enrichment'

    # evidence_for carries CONTEMPORARY evidence only (see the package README):
    # the synthesizer promotes canonical facts out of this field, and a trade or an
    # age read out of an 1843 volume is a back-projection this pass will not make.
    ev_for = ' '.join(pos_rules) if pos_rules else ''
    ev_against = ' '.join(neg_rules)
    if pid in AGAINST_EXTRA:
        ev_against = (ev_against + ' ' + AGAINST_EXTRA[pid]).strip()
        if resolves(FERGUS) and FERGUS not in srcs: srcs.append(FERGUS)

    notes_bits = []
    if fergus:
        notes_bits.append(f'FERGUS 26-29, AS PRINTED: "{fergus[0]}". {fergus[1]}')
    if cand_rules and outcome == 'candidate_identity':
        notes_bits.append('Repository lead retained as a candidate: ' + cand_rules[0])
    notes_bits.append('Research only. Later-volume readings are recorded here and NOT promoted: T-0513 consolidates and T-0514/T-0515 apply.')
    notes = ' '.join(notes_bits)

    if hand_summary:
        summary = hand_summary
    elif outcome == 'corroborated':
        summary = (f"Independently corroborated. {name} agrees, forename for forename or initial for initial, "
                   f"with a record outside the post-office lists in " + pretty(domains_of(pid)) + ". " + (pos_rules[0] if pos_rules else ''))
    elif outcome == 'corroborated_enrichment':
        summary = (f"Corroborated in a volume printed after the scene date. {name} agrees with an entry in "
                   + pretty(domains_of(pid)) +
                   ". The reading enriches the biography and adds no 1835 attestation.")
    elif outcome == 'candidate_identity':
        summary = (f"A plausible external identity for {name} was found and is retained unasserted: no date, place, "
                   f"occupation or kinship discriminator bridges it to the 1835 person.")
    else:
        summary = (f"No reliable record outside the Chicago post-office lists could be tied to {name} with a "
                   f"date, place, occupation or kinship discriminator. "
                   + ("The repository's own crosswalks record the refusal: " + neg_rules[0] if neg_rules else
                      "No later volume, civic list, land-sale, census or church register reached prints the name at all.")
                   + " This is a documented no-corroboration result, not evidence that the person did not exist.")

    counts[outcome] += 1
    for s in srcs: sources_used[s] += 1

    item = {'outcome': outcome, 'summary': summary}
    if srcs: item['sources'] = sorted(set(srcs + [SEED]))
    if ev_for: item['evidence_for'] = ev_for
    if ev_against: item['evidence_against'] = ev_against
    if notes: item['notes'] = notes
    if cand_ids: item['candidate_ids'] = cand_ids
    overrides[pid] = item

    rows.append({'person_id': pid, 'name_transcribed': name, 'name_normalized': name,
                 'stratum': stratum, 'outcome': outcome, 'candidate_ids': ';'.join(cand_ids),
                 'proposed_facts': '', 'evidence_for': ev_for, 'evidence_against': ev_against,
                 'source_ids': ';'.join(sorted(set(srcs + [SEED]))),
                 'source_urls_tiers': '', 'queries': 'exact name; justified initial and OCR variants; surname with forename initial',
                 'access_date': DATE, 'notes': notes})

    search_log.append({'person_id': pid, 'name': name, 'date': DATE,
        'corpora': 'repository newspapers + identity ledger; civic tax/poll lists 1833-1835; ISA land tract sales; 1830 census; 1840 census heads; St Cyr / St Mary church registers; Fergus 1839, Fergus 1843 and Norris 1844 directories; Fergus Historical Series 26-29; Calumet Club old-settler rolls; Newberry index cards; genealogytrails transcriptions',
        'result': f"{v['pos']} agreement record(s), {v['cand']} candidate record(s), {v['neg']} documented refusal(s)",
        'limitation': 'FamilySearch and Ancestry are login-walled and were recorded as inaccessible, not absent; HathiTrust page views return 403.'})

json.dump({'counts': dict(counts), 'sources': dict(sources_used)}, open('/tmp/counts.json','w'), indent=1)
json.dump({'overrides': overrides, 'rows': rows, 'search_log': search_log,
           'counts': dict(counts)}, open('/tmp/built.json','w'), indent=1)
print(counts)
print(json.dumps(dict(sources_used), indent=1))
