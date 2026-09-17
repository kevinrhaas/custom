---
id: T-1155
title: The resident identity splitter discards square-bracket supplies, so E. K[in]zie becomes surname Zie and bracketed names can tie to the wrong identity
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-16
closed: null
pr: null
claimed_by: run 9/16/2026, 11:29:34 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35181828835
---

The resident identity splitter discards square-bracket supplies, so E. K[in]zie becomes surname Zie and bracketed names can tie to the wrong identity.

**Found while closing T-1115, 2026-09-16.** `split_name_or_reason()` removes a
square-bracket group and everything inside it before tokenising. That is correct for a
parenthetical directory annotation and wrong for an internal supplied reading:
`E. K[in]zie` becomes `E. K zie`, `Esth[e]r M. Bailey` becomes `Esth r M. Bailey`, and
`T[e]mple, John T.` becomes surname `tmple`. T-1115 now prevents any such appearance
from minting a new card, but the bad split remains in the identity master, its gazetteer
ties and every later adjudication that consumes those identities.

**Cost measured on T-1115's tree audit:** square brackets occur throughout the research
corpus, including valid internal supplies, uncertain letters and whole later-directory
annotations. Correcting the splitter re-derives the large resident identity artefacts and
can rekey many identities; it must not be smuggled into the bounded mint-guard repair.

**Acceptance:** distinguish square-bracket transcription supplies from parentheses used
for directory annotations; preserve supplied letters inside a name while retaining the
original `as_read`; prove `E. K[in]zie`, `Esth[e]r M. Bailey` and `T[e]mple, John T.` split
to `kinzie`, `bailey` and `temple`; re-derive the identity master, proposal and coverage;
enumerate every changed identity id and either migrate or explicitly refuse every
downstream tie/card affected; and add mutation fixtures that fail if bracket contents are
discarded again. This is parked research under filing rule (d), not a prerequisite for
T-1115's mint refusal.

## CLOSING RECORD — every identity id this repair moved

Re-derived from `origin/dev` with `consolidate_resident_evidence.py --build`.

- 270 identities kept exactly their appearances and were RE-KEYED by the repaired split.
- 84 further old ids no longer stand: their appearances moved onto another identity when the corrected surnames merged, or fell to a named refusal.
- 39 further new ids appear: a reading that had been folded onto a mangled key now stands on its own, or a corrected name met a card it belongs to.
- No reading was dropped: every appearance that left an identity is present in `identity_master.json`'s `refusals` under a rule (checked, 0 unaccounted).

### Re-keyed, same appearances

```
id_adams_strat_en -> id_adams_stratten
id_ade_afarvin_r -> id_wade_afarvin_r
id_adkin_j -> id_adkins_j
id_adolp_micha_l -> id_michael_adolph
id_ahams_mortimer -> id_wahams_mortimer
id_ail_h_p -> id_tail_h_p
id_alden_ebene_er -> id_alden_ebenezer
id_alker_gerge_c -> id_walker_gerge_c
id_alle_robert_v -> id_allen_robert_v
id_alson_robert_a -> id_walson_robert_a
id_ansiyke_james -> id_tansiyke_james
id_anwet_addy -> id_vanwert_addy
id_ard_ashel_p -> id_ward_ashel_p
id_ard_sam_l -> id_ward_samuel
id_arnold_mar_a_s -> id_arnold_maria_s
id_arrer_henry -> id_warrer_henry
id_arsons_bolton -> id_parsons_bolton
id_arsons_jerry -> id_parsons_jerry
id_avery_j_y_h -> id_avery_joy_h
id_ayer_edmund -> id_sayer_edmund
id_bailey_esth_r_m -> id_bailey_esther_m
id_ball_jame -> id_ball_james
id_barry_ch_s_l -> id_barry_charles_l
id_baxter_sa_l -> id_baxter_samuel
id_beaubien_mark -> id_beaubien_mark_b
id_berry_w -> id_berry_william
id_bett_ira -> id_betts_ira_h
id_bonner_ra -> id_bonner_ira
id_born_cyrus_schil -> id_schillborn_cyrus
id_brigg_stephen_r -> id_briggs_stephen_r
id_buckle_thom_s -> id_buckle_thomas
id_cad_no_mars_w -> id_cady_john_marsh_w
id_camp_jo_n -> id_camp_john
id_carrier_law_on -> id_carrier_lawson
id_carty_j_m -> id_mccarty_j
id_cha_l -> id_chas_l
id_chapman_george -> id_chapman_george_l
id_christie_n_w -> id_bchristie_n_w
id_chs_l_drag_a -> id_dragua_chs_l
id_clar_leander -> id_clark_leander
id_cloutier_bapti -> id_cloutier_baptis
id_clure_isaa_w_m -> id_mcclure_isaac_w
id_cook_jame_s -> id_cook_james_s
id_cook_robert -> id_cook_robert_g
id_cook_sam_l -> id_cook_samuel
id_coury_pier_e -> id_coury_pierre
id_covington_w_c -> id_covington_william_c
id_cry_jacob -> id_cryee_jacob
id_dean_phill_p -> id_dean_phillip
id_dellike_george -> id_delliker_george
id_derby_ate_r -> id_derby_water_r
id_doublass_a -> id_doublass_andrew
id_eake_cole -> id_weake_cole
id_eek_samuel_h -> id_week_samuel_h
id_eigs_david -> id_meigs_david
id_eland_robert_lo -> id_loveland_robert
id_eldon_jonthan -> id_weldon_jonthan
id_eli_stratt_n -> id_stratton_eli
id_ellis_ohn -> id_ellis_john
id_ells_e_ra -> id_wells_ezra
id_end_c_c_town -> id_townsend_c_c
id_er_alby_f_w -> id_fowler_alby
id_er_alvah_fow -> id_fowler_alvah
id_er_jacob_sip -> id_sipler_jacob
id_er_jo_n_wal -> id_walter_john
id_er_william_chand -> id_chandler_william
id_escott_james -> id_wescott_james
id_essege_daniel_barclay -> id_kessege_daniel_barclay
id_est_georgo -> id_west_georgo
id_est_wil_iam -> id_west_william
id_esteott_james_r_e -> id_westeott_james_r_e
id_esthalai_o -> id_desthalais_o
id_et_john_haz -> id_hazlet_john
id_ett_robert_bur -> id_burnett_robert
id_eur_john -> id_weur_john
id_ever_jane_mirs -> id_wever_jane_mirs
id_ewin_g_w -> id_ewing_g_w
id_ey_b_rnihart_la -> id_blauey_barnihart
id_ey_d_mose -> id_moseley_d
id_ey_james_w_bend -> id_bendley_james_w
id_ey_robert_ogil -> id_ogilvey_robert
id_eyborn_william_c -> id_cleyborn_william
id_faber_g_o_c -> id_faber_george_c
id_foodruli_h_e_mies -> id_wfoodruli_h_e_mies
id_freeman_k_y -> id_freeman_hinkley
id_gilbert_sam_j_w -> id_gilbert_samuel_j_w
id_gley_w_s -> id_higley_w_s
id_gur_acob -> id_gur_jacob
id_han_m_s -> id_hancock_m_s
id_harbour_samu_l -> id_harbour_samuel
id_heim_soph_a_wei -> id_weilheim_sophia
id_her_handler_fi -> id_fisher_chandler
id_hipple_illard -> id_whipple_millard
id_hiting_betsey -> id_whiting_betsey
id_hitney_joshus -> id_whitney_joshus
id_hoare_mad_sara_l -> id_hoare_sara_l
id_holderman_rank -> id_holderman_frank
id_holmer_yr_nius -> id_holmer_cyrenius
id_huguni_john_c -> id_hugunin_john_c
id_hunter_osice -> id_hunter_rosice
id_huntley_yman -> id_huntley_lyman
id_iard_r_e -> id_wiard_r_e
id_ichardson_a_m -> id_richardson_a_m
id_ierel_john -> id_witherel_john
id_ifford_calvin_c -> id_clifford_calvin
id_il_m_ta_f -> id_taff_william
id_ilams_julia_ann -> id_williams_julia_ann
id_ilcocks_john_s -> id_wilcocks_john_s
id_ill_rob_rt -> id_hill_robert
id_illard_elish_w_s -> id_willard_elish_w_s
id_ilmot_jes_o -> id_wilmot_jesso
id_ilson_harry_f -> id_wilson_harry_f
id_ilson_sally_mies -> id_wilson_sally_mies
id_in_francis_car -> id_carlin_francis
id_in_hardin_m_ir -> id_irvin_hardin_m
id_in_samuel_cha -> id_chapin_samuel
id_ingraam_aniel -> id_ingraham_daniel
id_ingroll_austin -> id_ingersoll_austin
id_interfer_jacob_m -> id_mcinterfer_jacob
id_inters_henry -> id_winters_henry
id_intyfer_jacob_m -> id_mcintyfer_jacob
id_is_robert_f_har -> id_harris_robert_f
id_isaac_h -> id_harmon_isaac
id_ite_adonijah -> id_white_adonijah
id_itherby_luke_b -> id_witherby_luke_b
id_ity_richard -> id_witty_richard
id_iur_samuel -> id_wilbur_samuel
id_jacobs_benjamin -> id_jacobs_benjn
id_jacubus_homas -> id_jacubus_thomas
id_james_d_myr_s -> id_myres_james_d
id_james_lorenz_d -> id_james_lorenzo_d
id_jeerson_rob_rt_h -> id_jefferson_robert_h
id_jesteorple_bernard -> id_jesteoryaple_bernard
id_johnson_wi_am_c -> id_johnson_william_c
id_jorgan_lames -> id_mjorgan_lames
id_joseph_grayh_m -> id_grayham_joseph
id_jun_moore -> id_junr_moore
id_kay_julius_ma -> id_malkay_julius
id_ke_bamuel_h -> id_walker_bamuel_h
id_kiger_ja_es -> id_kiger_james
id_kilern_d_w -> id_kilbearn_d_w
id_kin_john -> id_king_john_h
id_kinge_edward -> id_kingsley_edward
id_kzey_william -> id_kinzey_william
id_ladd_os -> id_ladd_thomas
id_land_rebec_a_cle -> id_cleveland_rebecca
id_lane_joh -> id_lane_john
id_laning_d_c -> id_lansing_d_c
id_ld_david_c_butterfi -> id_butterfield_david_c
id_ler_ethan_bu -> id_butler_ethan
id_lew_read -> id_lewis_read
id_lewis_rich -> id_lewis_richard
id_lilie_john -> id_lillie_john
id_lingley_bikannh -> id_tlingley_bikannh
id_lowry_ugh -> id_lowry_hugh
id_lutty_richard -> id_wlutty_richard
id_ly_doct_e_s -> id_kimberly_doct_e_s
id_lyman_cale -> id_lyman_caleb
id_mannin_charles -> id_manning_charles
id_marghall_phili -> id_marghall_philip
id_marn_robert_b -> id_martin_robert_b
id_mcall_ale_ander -> id_mccall_alexander
id_mcclintock_thoma -> id_mcclintock_thomas
id_mccomb_rebecca -> id_mccomber_rebecca
id_mccra_edward -> id_mccrary_edward
id_mcewen_cy_b -> id_mcewen_lucy_b
id_mdonald_j_mes -> id_mdonald_james
id_mfadder_ja_es_s -> id_mfadder_james_s
id_mke_ja_es -> id_mkee_james
id_mled_charles_s -> id_mleod_charles_s
id_mls_ben_amin -> id_mills_benjamin
id_morrison_enry -> id_morrison_henry
id_ms_gil_s_willi -> id_williams_giles
id_nathan_hutchin_s -> id_hutchings_nathan
id_nbridge_w_h_bra -> id_brainbridge_w_h
id_nd_oliver_raym -> id_raymond_oliver
id_newhall_saac -> id_newhall_isaac
id_nn_ge_m -> id_munn_george
id_nock_cha_les -> id_nock_charles
id_notton_ly -> id_notton_lyman
id_nter_edward_f_h -> id_hunter_edward_f
id_ol_joho -> id_tool_joho
id_olcott_el_en_a -> id_wolcott_ellen_a
id_olf_john -> id_wolf_john
id_on_benjamin_thomp -> id_thompson_benjamin
id_ontague_rodney -> id_montague_rodney
id_oodbury_jeddediah -> id_woodbury_jeddediah
id_ooding_anson -> id_wooding_anson
id_ooiward_george -> id_wooiward_george
id_oolley_jediah -> id_woolley_jediah
id_ore_philip_whitte -> id_whittemore_philip
id_orode_peter_r -> id_torode_peter_r
id_ortbingham_william -> id_wortbingham_william
id_os_l_m_ll_n -> id_mullin_joseph_l
id_ostrander_r_bec_a -> id_ostrander_rebecca
id_ottaway_w -> id_ottaway_william
id_parelee_henry -> id_parmelee_henry
id_parker_nry -> id_parker_henry
id_parson_timothy_e -> id_parsons_timothy_e
id_patch_phen_w -> id_patch_stephen_w
id_peck_nath -> id_peck_nathaniel
id_pennington_sa_c_t -> id_pennington_isaac_t
id_pennington_saa_p -> id_pennington_isaac_p
id_penrose_ja_es_w -> id_penrose_james_w
id_plummer_eno -> id_plummer_enos
id_pok_seth -> id_peok_seth
id_pox_ab_e -> id_pox_abner
id_prank_a_e -> id_prank_andrew
id_prescot_elij_s -> id_prescot_elijah_s
id_prntice_gilbert_w -> id_prentice_gilbert_w
id_prout_granville_t -> id_sprout_granville_t
id_ps_emily_a -> id_capps_emily
id_pullen_udwell -> id_pullen_ludwell
id_purcell_odric_r -> id_purcell_rodrick_r
id_puston_hi_or_joh -> id_puston_hiram_or_john
id_qu_ohn_ba -> id_barquee_john
id_reed_jo_n -> id_reed_john
id_rel_jobn -> id_russel_jobn
id_rhine_mary -> id_rhines_mary
id_right_horace -> id_wright_horace
id_rin_j_lius_pe -> id_perrin_julius
id_rlatt_william_j_m -> id_marlatt_william_j
id_rnolds_nazro -> id_reynolds_nazro
id_roberts_charles -> id_roberts_charles_h
id_roby_s -> id_roby_j_s
id_rossiter_nichol_s -> id_rossiter_nicholls
id_rowe_st -> id_rowe_stephen
id_saac_stua_t -> id_stuart_isaac
id_sam_c -> id_saml_c
id_savage_malanc_ton -> id_savage_malanchton
id_sewall_ki_h_b -> id_sewall_kiah_b
id_siker_josish -> id_wsiker_josish
id_sith_allira -> id_smith_allira
id_skinner_willia_h -> id_skinner_william_h
id_slato_walt_n -> id_slato_walton
id_smons_thomas -> id_simmons_thomas
id_son_dean_fer -> id_fergson_dean
id_stapleton_w -> id_stapleton_william
id_stephens_noah_or_al_puller -> id_stephens_noah_or_almon_puller
id_stephens_obt -> id_stephens_robert
id_stewart_sa_uel -> id_stewart_samuel
id_stowel_walter -> id_stowell_walter
id_swartwout_enry -> id_swartwout_henry
id_swartwout_j_o -> id_swartwout_john
id_sweet_alon_on -> id_sweet_alonson
id_switzer_jo_n -> id_switzer_john
id_talcott_thom -> id_talcott_thomas_b
id_tcal_thom_s -> id_metcalf_thomas
id_thomas_ett_y -> id_ettey_thomas
id_thomas_hartec_l -> id_hartecll_thomas
id_thomas_sh_r -> id_shird_thomas
id_thomes_r_or_ja -> id_thomes_robert_or_james
id_town_ijah_s -> id_town_elijah_s
id_troutman_jo_n -> id_troutman_john
id_turner_harmo -> id_turner_harmon
id_ur_e_ra_wood -> id_ury_e_ra_wood
id_urd_barnard -> id_wurd_barnard
id_vhler_bernard -> id_vohler_bernard
id_walter_el_hu -> id_walter_elihu
id_whittely_w_c -> id_whittely_william_c
id_wiht_orrin -> id_wright_orrin
id_wilcox_sam_el -> id_wilcox_samuel
id_willis_joh_j -> id_willis_john_j
id_wilson_asahe_b -> id_wilson_asahel_b
id_witherll_erdi_nd -> id_witherell_ferdinand
id_wlson_walter -> id_wilson_walter
id_wm_prendergu_t -> id_prendergust_william
id_woodruff_al_d -> id_woodruff_alean_d
id_wr_hirom -> id_wwr_hirom
id_wtkins_theophilus_or_robert -> id_watkins_theophilus_or_robert
```

### Old ids that no longer stand

```
id_ad_el_s_jon_s
id_ain_l_c_chamber
id_albe_clark_b
id_allen_e
id_allen_eben_zer
id_anderson_sam
id_borland_a_drew_w
id_case_ohn
id_crain_arvey
id_donald_john_g_m
id_dunlap_jo_n
id_ean_ja
id_el_wil_m
id_ellmaker_john
id_er_eb
id_ewton_daniel
id_field_p
id_fleet_john_va
id_ght_d_n_l
id_gooding_ja_per_a
id_heeler_william_r
id_holmes_cyrenius
id_hopkin_nathan
id_hy_elias
id_hyde_eli_s
id_iams_john_c
id_iles_david
id_illard_a
id_in_david_cur
id_intry_m
id_jones_char_es
id_joseph_ada_s
id_king_byra
id_king_j
id_laughton_a_h
id_ld_f
id_ler_albert_fo
id_lmes_yrenius_c_h
id_lo_richard
id_man_hol
id_martin_h_a
id_martin_henry_on
id_mcdonald_john
id_mh_freeman
id_miller_sa_uel
id_mils_andrew
id_miner_fobes
id_moreland_t_h
id_nsing_jacob_l
id_ork_james_houston
id_oss_joseph
id_peet_l_wis
id_peet_wi
id_rey_mcca
id_rk_nathaniel_c_cl
id_rod_m
id_sammon_no
id_sanderson_ames_cap
id_sanford_johns_n
id_sctt_leonard_h
id_sen_le_ett
id_sewel_john
id_sewell_joh
id_sherman_ho_r
id_sith_r_g
id_sith_thomas
id_smith_ben_amin
id_smith_f_r
id_smith_m
id_spence_me
id_talor_charles
id_taylor_james
id_taylor_w_l
id_thomas_h_t
id_titterington_charl
id_tmple_john_t
id_tylor_ja_es_r
id_vanfet_john
id_weed_sal
id_welch_william
id_wheeler_william
id_wm_band_e
id_woolle_jeddiah
id_work_charles
```

### New ids

```
id_allen_ebenezer
id_beaubien_m_b
id_botsford_k
id_brown_samuel
id_brown_samuel_j
id_clark_nathaniel_c
id_field_p_r
id_hoer_sherman
id_holmes_c_e
id_holmes_cyrenius_c
id_hugunin_s
id_hyde_elias
id_johnson_william
id_jones_adiel_s
id_king_john
id_lockridge_w_s
id_martin_hylon
id_mcdonald_john_g
id_miner_f_t
id_miner_fobes_h
id_moreland_thomas_h
id_peck_d
id_peck_dudly
id_peet_lewis
id_poke_edmund
id_scott_leonard_h
id_sewell_john
id_shee_g
id_sherman_h
id_smith_freeman
id_snow_j
id_sweet_a
id_taylor_james_r
id_walter_e
id_welch_william_s
id_wheeler_william_r
id_willis_h_r
id_wilson_w_s
id_worthington_m
```
