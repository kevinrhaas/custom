---
id: T-1028
title: EPIC — the 68 one-letter card pairs a fuzzy candidate test proposes and nobody has read a page for: 62 whose surname is a letter apart, 6 whose forename is
state: open
epic: META
requested_by: loop
seen: false
effort: L
legacy_id: null
parent: null
opened: 2026-09-11
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

EPIC — the 68 one-letter card pairs a fuzzy candidate test proposes and nobody has read a page for: 62 whose surname is a letter apart, 6 whose forename is.

**FOUND BY T-1002**, which ruled three pairs of this shape and then counted the class they
belong to. `tools/measure_card_fold.py` runs the candidate test behind
`data/residents/card_merge_rulings.json` again with a FUZZY KEY — edit distance 1 on the
surname, and on the forename where the surname folds — and prints what it newly proposes.
On the tree T-1002 shipped that is 68 pairs, and three more it had already ruled.

**WHY THIS IS AN EPIC AND NOT A TICKET.** The queue's own filing rule says so: "if
finishing it would take more than five tickets, it is an EPIC". Each of these 68 is a
RESEARCH QUESTION and not a string comparison. A fold is a card DELETION and the town's
resident count moves by it, so the rule that decides one — C10, written in T-1002 — asks
that the folded card's own page carry a fact BEYOND THE NAME which the survivor's record
holds out of a different document: a trade, a dwelling, a year of arrival, a civic office.
Answering that takes a page per pair, and some of these pairs will stand as two men.

**WHAT THE LIST IS NOT.** It is not 68 duplicates. It is a WORKLIST, exactly as the exact
candidate test's own clusters are — some of these are brothers, some a father and a son,
and some are one man. Read the list and it is obvious in both directions: `foot_john` /
`foote_john`, `lloyd_alexander` / `loyd_alexander`, `pearson_hiram` / `pearsons_hiram` and
`vanderbogart_henry` / `vanderbogert_henry` look like one man apiece; `hale_john` /
`vale_john`, `noble_mark` / `noble_mary` and `king_byram` / `king_hyram` look like two
people apiece, and `noble_mary` is a woman. NOTHING HERE MAY BE FOLDED TO TIDY A DUPLICATE
AWAY.

**AND THE CEILING OF THE TEST IS PART OF THE FINDING.** A further 22 pairs are an INITIAL
against an INITIAL — 'D Harmon' against 'M D Harmon', 'J Jones' against 'M Jones'. Every
initial is one letter from every other, so a fuzzy forename test that admits a
single-letter token proposes the whole alphabet and says nothing. They are counted and
never proposed, and no rule should ever be written that reaches them.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- THE OWNER PROMOTES THIS OUT OF `EPICS` BEFORE ANY OF IT IS WORKED. That is what the band
  is for, and the queue says so in its own words.
- Once promoted, one ticket per COHERENT GROUP of pairs, filed `--after` the ticket it
  serves, and each ruled in `data/residents/card_merge_rulings.json` under a named rule in
  that file's own shape — a merge, a `distinct`, or a `U1` that files the question. Never a
  fold on the resemblance alone.
- `tools/measure_card_fold.py` is the ledger: the number it prints falls by exactly the
  number of pairs a ticket folds, and the pairs a ticket rules DISTINCT stay in it, because
  the test is a proposal and a `distinct` ruling does not remove a card.
- `bash tools/check.sh` green on each, and the derived layer rebuilt with
  `node tools/rederive.mjs --run` in the same commit — a card merge moves the identity
  master, every domain crosswalk and spend, the town census, `docs/LIBERTIES.md` L220 and
  the resident audit workbook, and T-1002 learned that the hard way.

**THE LIST, as `tools/measure_card_fold.py --detail` prints it on the tree T-1002 shipped.**
It is reproduced here so the epic can be read without running anything, and the tool is the
authority if the two ever disagree.

```
1374 person card(s), 1373 with a parseable name
21 pair(s) the exact candidate test already joins — already ruled, and subtracted below
62 cohort A   the surname one letter apart, forenames compatible
6 cohort B   the surname exact, the forename one letter apart
22 degenerate  an initial against an initial — counted, never proposed

COHORT A — the surname one letter apart  (62)
   allan_richard_b                  Richard B. Allan               | allin_richard                    Richard Allin
   anight_clark                     Clark Anight                   | knight_clark                     Clark Knight
   babeu_joseph                     Joseph Babeu                   | babeue_joseph                    Joseph Babeue
   barre_john_s                     John S. Barre                  | barry_john_s                     John S. Barry
   beech_reuben                     Reuben Beech                   | bench_reuben                     Reuben Bench
   blanchard_f_gantry               F Gantry Blanchard             | blanshard_f_g                    F G Blanshard
   bread_a_o_t                      A O T Bread                    | breed_a_o_t                      A O T Breed
   burk_james                       James Burk                     | burke_james                      James Burke
   camp_g_t                         G T Camp                       | canp_george_s                    George S. Canp
   cary_john_marshall               John Marshall Cary             | cory_john_l                      John L Cory
   chark_john_a                     John A. Chark                  | clark_john_a                     John A Clark
   chark_john_a                     John A. Chark                  | clark_john_k                     John K Clark
   collins_j_h                      J. H. Collins                  | rollins_john                     John Rollins
   curtin_l_g                       L. G. Curtin                   | curtis_liman                     Liman Curtis
   curtis_jacob_s                   Jacob S Curtis                 | curtiss_j                        J. Curtiss
   curtis_liman                     Liman Curtis                   | curtiss_l_g                      L G Curtiss
   david_john                       John David                     | davis_john                       John Davis
   dell_frank                       Frank Dell                     | dill_frank                       Frank Dill
   eldredge_john_w                  John W Eldredge                | eldridge_john_w                  John W Eldridge
   falker_j_b                       J. B. Falker                   | walker_james                     James Walker
   falker_j_b                       J. B. Falker                   | walker_jeremiah                  Jeremiah Walker
   foot_john                        John Foot                      | foote_john                       John Foote
   foot_s                           S. Foot                        | foote_star                       Star Foote
   forsyth_william                  William Forsyth                | forsythe_william                 William Forsythe
   fraser_wm_h                      Wm. H. Fraser                  | frazer_wm_h                      Wm. H. Frazer
   gabbs_james_i1                   James [?] Gabbs                | gibbs_james_h                    James H. Gibbs
   green_j                          J Green                        | greene_john                      Major John Greene
   hale_john                        John Hale                      | vale_john                        John Vale
   hands_george_e                   George E Hands                 | handy_major                      Major Handy
   harman_isaac                     Isaac Harman                   | harmon_isaac_d                   Isaac Dewey Harmon
   hoit_thomas                      Thomas Hoit                    | hoyt_thomas                      Thomas Hoyt
   hussey_robert                    Robert Hussey                  | hussy_robert                     Robert Hussy
   inf_joiner_north_02              J. W. Reed                     | reid_j_chester                   J. Chester Reid
   kimbal_wm                        Wm. Kimbal                     | kimball_walter                   W. Kimball
   kingston_paul                    Paul Kingston                  | kingstone_paul                   Paul Kingstone
   lewie_wm                         Wm. Lewie                      | lewin_w_y                        W. Y. Lewin
   lloyd_alexander                  Alexander Lloyd                | loyd_alexander                   Alexander Loyd
   ludb_john                        John Ludb                      | ludby_john                       John Ludby
   mcgregor_ashor                   Ashor Mcgregor                 | mgregor_a                        A Mgregor
   murray_alonzo                    Alonzo Murray                  | murry_alonzo                     Alonzo Murry
   paine_william                    William Paine                  | payne_william                    William Payne
   pearson_hiram                    Hiram Pearson                  | pearsons_hiram                   Hiram Pearsons
   pruyne_peter                     Peter Pruyne                   | pryne_peter                      Peter Pryne
   rose_niles                       Niles Rose                     | ross_niles                       Niles Ross
   salisbury_stephen_m              Stephen M. Salisbury           | salsbury_stephen_m               Stephen M Salsbury
   scarrett_isaac                   Isaac Scarrett                 | scarritt_isaac                   Isaac Scarritt
   shearman_h_c                     H. C. Shearman                 | sherman_h                        Mrs. H. Sherman
   sheldon_james                    James Sheldon                  | wheldon_james                    James Wheldon
   smow_george_w                    George W Smow                  | snow_george_w                    George W. Snow
   square_geo                       Geo. Square                    | squire_george                    George Squire
   stoel_c_ii                       C. II. Stoel                   | stoer_clement                    Clement Stoer
   teal_william                     William Teal                   | teall_wm                         Wm. Teall
   temple_john_t                    Dr John Taylor Temple          | tmple_john_t                     John T Tmple
   temple_mrs_john_t                Mrs Temple                     | tmple_john_t                     John T Tmple
   thrall_e_l                       E. L. Thrall                   | trall_e_l                        E L Trall
   vanderbogart_henry               Henry Vanderbogart             | vanderbogert_henry               Henry Vanderbogert
   vandine_john                     John Vandine                   | vandino_john                     John Vandino
   wesencraft_charles               Charles Wesencraft             | wessencraft_charles              Charles Wessencraft
   wight_j_ambrose                  J Ambrose Wight                | wright_j                         J Wright
   wight_j_ambrose                  J Ambrose Wight                | wright_john                      John Wright
   wight_j_ambrose                  J Ambrose Wight                | wright_john_s                    John S. Wright
   wilson_john                      John Wilson                    | wilton_john_l                    John L Wilton

COHORT B — the forename one letter apart  (6)
   king_byra                        Byra King                      | king_byram                       Byram King
   king_byram                       Byram King                     | king_hyram                       Hyram King
   morrison_ordemus                 Ordemus Morrison               | morrison_orsemus                 Orsemus Morrison
   noble_mark                       Esq. Mark Noble                | noble_mary                       Mary Noble
   rider_eli_a                      Eli A Rider                    | rider_elia                       Elia Rider
   wooley_jeddiah                   Jeddiah Wooley                 | wooley_jedidiah                  Jedidiah Wooley

DEGENERATE — an initial is one letter from every other initial, and this is not a proposal  (22)
   bennett_c_h                      C H Bennett                    | bennett_h_c                      H. C. Bennett
   blanchard_f_gantry               F Gantry Blanchard             | blanchard_w_g                    W. G. Blanchard
   blanshard_f_g                    F G Blanshard                  | blanshard_g                      G. Blanshard
   clarke_h_b                       H. B. Clarke                   | clarke_w_b                       W B Clarke
   curtiss_j                        J. Curtiss                     | curtiss_l_g                      L G Curtiss
   dewey_d_s                        D S Dewey                      | dewey_s                          S Dewey
   field_a_b                        A B Field                      | field_j_e                        J. E. Field
   harmon_d                         D Harmon                       | harmon_m_d                       M D Harmon
   hugunin_leonard_c                Leonard, C. Hugunin            | leonard_n                        N Leonard
   inf_joiner_north_02              J. W. Reed                     | reed_s_w                         S W Reed
   jones_d_e                        D E Jones                      | jones_m                          M Jones
   keeney_g_w                       G. W. Keeney                   | keeney_w                         W Keeney
   montgomery_l_w                   L. W. Montgomery               | montgomery_w                     W Montgomery
   owen_j_v                         J V Owen                       | owen_v                           V Owen
   palmer_j_k                       J K Palmer                     | palmer_n_h                       N. H. Palmer
   sanford_a_r                      A R Sanford                    | sanford_n_g                      N G Sanford
   smith_d_a                        D A Smith                      | smith_e_kirby                    E Kirby Smith
   smith_d_a                        D A Smith                      | smith_l_w                        L W Smith
   smith_e_kirby                    E Kirby Smith                  | smith_l_w                        L W Smith
   thompson_lieut_j_l               Lieut J L Thompson             | thompson_o_i                     O I Thompson
   townsend_a                       A Townsend                     | townsend_c_e                     C. E. Townsend
   trowbridge_g_g                   G G Trowbridge                 | trowbridge_s_g                   S G Trowbridge
```
