# The final dataset tree, file by file

## What is missing or to confirm

- Still to write: the final README (what the wizard needs to run, that the 90 manual crops from 42 patents come from the PDF links of PatSeer in the pdf_link column, the SBERT wording, the one-line triage description).
- Dependencies in the column 'Depends on' are to be checked against the code that built each table (list in VERIFICAR_ANTES_DE_PUBLICAR.md).
- The data dictionary has a description for only a few columns.
- 05_images is not in this draft: it is added when the release archives are built.
- Code (wizard, gold standard scripts, 11A19_triage.py, table build) goes to the GitHub repository, not to the dataset. Their paths still point to this machine and are fixed when the repository is prepared.
- The Zenodo record has the files README.md, eVTOL_dataset.zip (everything except images) and eVTOL_dataset_images.zip (05_images).

## `eVTOL_dataset/`

The public dataset. One folder per step of the work, numbered in order.

### `01_query/`

The patent query and its PatSeer export.

#### `README.md` (321 B)

The files of this folder, what they are and what one row means.

#### `patseer_1639_2026-06-08.xlsx` (14.6 MB)

The PatSeer export of that query, as it came.

**One row per:** patent family

**Depends on:** query_thesis.txt

Sheet “Sheet1”, 102 columns: `Record Number`, `Title`, `Abstract`, `Description of Drawings`, `CPC`, `PDF Link`, `Record Type`, `Publication/Issue Date`, `Filing/Application Date`, `Estimated Expiry Date`, `EFAM Earliest Priority Date`, `EFAM Earliest Publication Date`, `Priority Details`, `Priority Dates (All)`, `Application No.`, `Priority Country Code`, `Priority Year`, `Register Legal Status`, `Register Legal Status Date`, `Summary of Invention`, `Designated States`, `Active in Designated States`, `Field of search`, `Industry`, `Tech Domain`, `Tech Sub Domain`, `Description`, `Claims`, `Number Of Claims`, `No. of Independent Claims`, `Independent Claims`, `First Claim`, `Advantages of Invention`, `No. of Assignees`, `Assignee`, `Assignee Original`, `Assignee Country`, `Current Assignee`, `Current Owner`, `Inventors`

#### `query_thesis.txt` (1.0 KB)

The PatSeer query, in one line, as PatSeer accepts it. It returns the 1 639 patent families.

### `02_gold_standard/`

The gold standard, in the order the work was done (21 to 29).

#### `21_census_candidates.csv` (201.3 KB)

Who could enter the census of mature eVTOL programmes, and why each one entered or not. Long table: list says which list a row comes from.

**One row per:** candidate and list

**Depends on:** 06_external (directory and AAM index), 04_aircraft/45_designs.csv

419 rows · 9 columns

| column | example | filled |
|---|---|---|
| `list` | census | 100 % |
| `company` | Pivotal | 100 % |
| `aircraft` | BlackFly V2 | 96 % |
| `category` | Hoverbike/PFD | 83 % |
| `first_flight_year` | 2014.0 | 76 % |
| `trl` | 7 | 42 % |
| `outcome` | no patent found (new query: 0 families) | 19 % |
| `reason` | academic or private actor | 17 % |
| `details` | {"criterion": "VFS TRL 7", "trl7_sentence": "The | 100 % |

#### `22_searches_described.md` (6.9 KB)

The ten PatSeer searches (companies, programmes, multicopters), each with a description and its query.

**Depends on:** file 21

#### `23_search_query.txt` (5.5 KB)

The ten queries joined with OR.

**Depends on:** file 22

#### `24_search_patseer_export.xlsx` (21.3 MB)

The PatSeer export of all ten searches, as it came, without repeated families.

**One row per:** patent family

**Depends on:** file 23

Sheet “Sheet1”, 84 columns: `Record Number`, `Record Type`, `Publication/Issue Date`, `Filing/Application Date`, `Estimated Expiry Date`, `EFAM Earliest Priority Date`, `EFAM Earliest Publication Date`, `Priority Details`, `Priority Dates (All)`, `Application No.`, `Priority Country Code`, `Priority Year`, `Register Legal Status`, `Register Legal Status Date`, `Summary of Invention`, `Designated States`, `Active in Designated States`, `Field of search`, `Industry`, `Tech Domain`, `Tech Sub Domain`, `Title`, `Abstract`, `Description`, `Description of Drawings`, `Claims`, `Number Of Claims`, `No. of Independent Claims`, `Independent Claims`, `First Claim`, `Advantages of Invention`, `No. of Assignees`, `Assignee`, `Assignee Original`, `Assignee Country`, `Current Assignee`, `Current Owner`, `Inventors`, `No. of Inventors`, `IPC Original (ICO)`

#### `25_search_hits_per_aircraft.csv` (1.6 KB)

How many families each search returned for each census aircraft.

**One row per:** aircraft and search

**Depends on:** files 21, 24

35 rows · 4 columns

| column | example | filled |
|---|---|---|
| **Identificação** | | |
| `company` | Pivotal | 100 % |
| **Domínio, ground truth e tags** | | |
| `search` | census | 100 % |
| `aircraft` | BlackFly V2 | 100 % |
| `n_families` | 0 | 100 % |

#### `26_search_triage.xlsx` (2.1 MB)

Automatic triage of the exported families using keywords and PatentSBERTa only: whether the family is in the dataset, which keyword groups it matches, a keyword verdict, SBERT estimates and a review priority. The coder_ columns are left for a reading. Sheets: triage, regexes, codebook.

**One row per:** patent family

**Depends on:** file 24, 01_query export, files 27, 29 (to mark families already decided)

Sheet “triage”, 67 columns: `Record Number`, `Simple Family ID`, `Title`, `Assignee`, `Priority Year`, `Publication/Issue Date`, `CPC`, `PDF Link`, `Simple Family Members`, `Abstract`, `in_dataset`, `author_decision_recorded`, `kw_electric_field`, `kw_electric_evidence`, `kw_electric_n`, `kw_vtol_field`, `kw_vtol_evidence`, `kw_vtol_n`, `kw_passenger_field`, `kw_passenger_evidence`, `kw_passenger_n`, `kw_multicopter_field`, `kw_multicopter_evidence`, `kw_multicopter_n`, `kw_uav_field`, `kw_uav_evidence`, `kw_uav_n`, `kw_helicopter_field`, `kw_helicopter_evidence`, `kw_helicopter_n`, `kw_wing_field`, `kw_wing_evidence`, `kw_wing_n`, `kw_component_field`, `kw_component_evidence`, `kw_component_n`, `kw_electric`, `kw_vtol`, `kw_passenger`, `kw_multicopter`

Sheet “regexes”, 2 columns: `flag`, `regex`

Sheet “codebook”, 2 columns: `column`, `meaning`

#### `27_author_answers.csv` (13.4 KB)

The author's answers on the review pages, in order of step (column step).

**One row per:** answer

**Depends on:** files 21, 24

231 rows · 6 columns

| column | example | filled |
|---|---|---|
| `step` | pool | 100 % |
| `item` | SHy4 | 100 % |
| `company` | Joby Aviation | 68 % |
| `answer` | family | 92 % |
| `families` | US2021125515A1 | 7 % |
| `note` | The only Volocopter family of the pool in the wi | 12 % |

#### `28_query_misses.xlsx` (9.8 KB)

Which clause of the query leaves out each family: winged programmes that were missed, and multicopter families. Rule based.

**One row per:** patent family

**Depends on:** 01_query/query_thesis.txt, file 24

Sheet “winged_missed”, 18 columns: `aircraft`, `family`, `record_in_export`, `title`, `text_chars`, `1 CPC B64C29`, `2 architecture words (W5)`, `3 electric (CPC B64D27/30-34 or words)`, `4 no excluded CPC`, `5 no combustion or fuel-cell words (TA)`, `6 no UAV, unmanned, drone (TA)`, `7 no excluded title words`, `fails`, `UAV hit`, `title hit`, `excluded CPC`, `fuel hit`, `CPC`

Sheet “multicopters”, 17 columns: `Record Number`, `coder_vfs_design`, `coder_in_627`, `Title`, `A1 CPC B64C29`, `B1 scope (27/08 no 29, or U10/1 + crew)`, `B2 multicopter words (TACD)`, `B3 crew words (TA)`, `4 architecture words (TACD)`, `5 electric (CPC or TACD)`, `6 year 2005-2026`, `N1 not excluded CPC`, `N2 not combustion (TA)`, `N3 not UAV without crew (TA)`, `N4 not helicopter words (TA)`, `N5 not component title`, `branch B`

#### `29_gold_standard.csv` (16.0 KB)

The gold standard: every census aircraft, its programme and the result (captured, outside the query with a patent, without a patent).

**One row per:** census aircraft

**Depends on:** files 21, 25, 27

69 rows · 16 columns

| column | example | filled |
|---|---|---|
| `entered_by` | census (index or TRL 7) | 100 % |
| `criterion` | VFS TRL 7 | 100 % |
| `company` | Pivotal | 100 % |
| `aircraft` | BlackFly V2 | 100 % |
| `category` | Hoverbike/PFD | 100 % |
| `first_flight_year` | 2014 | 100 % |
| `aircraft_outcome` | outside, patent found | 100 % |
| `design_ids` | CN111301676A_ad1 | 42 % |
| `family` | US2014097290A1 | 17 % |
| `url` | https://evtol.news/opener-blackfly-v2 | 100 % |
| `programme` | pivotal / Hoverbike/PFD | 100 % |
| `programme_size` | 1 | 100 % |
| `programme_outcome` | outside, patent found | 100 % |
| `decided_by` | BlackFly V2 | 100 % |
| `mixed` | yes | 13 % |
| `tier` | TRL 7 or higher | 100 % |

#### `README.md` (1.8 KB)

The files of this folder, what they are and what one row means.

### `03_patents/`

The 1 639 patent families: what the text says and the author's labels. This folder holds what the wizard (the HTML tool used to label) takes in and what it produces. Files 30 and 31 are machine output, not labels, and nothing in them was reviewed or checked. File 32 is the labels. - **File 30** holds the suggestions the wizard shows when a batch is loaded: SigLIP on the figures, SBERT on the text and fields taken from the PatSeer record, each with a confidence and a flag that says whether it needs review. They were only an aid to label faster. - **File 31** is a different thing: what a script read in the text of each patent about the aircraft (name, powertrain, take-off, UAV), which is what tells whether the patent describes an electric aircraft inside the domain. - **File 32 is the real file of the dataset.** It holds every label the author gave, in the long format of the wizard (one row per field). The easiest way to see these labels is to open file 32 in the wizard HTML (wizard/11H_master_wizard.html in the GitHub repository), which shows each patent with its figures and labels. The wizard has two file inputs, the batch to review (file 30) and an optional earlier export to resume from (file 32). Files 33, 41, 42 and 43 hold the same labels as tables, so they can be read without opening the wizard. They add no labels of their own. In file 32 the sections META and T1 are patent level (they give file 33), T2 is figure level (file 41) and G1, M1, M2, M3 are aircraft level (file 42). The tables have one row per patent, figure or aircraft, the rejected patents are left out of file 42, and some columns are calculated (duplicate of, number of figures, final electric). Why file 33 is needed: it is the only table with one row for each of the 1 639 patent families. File 42 lists only the 1 108 patents that have an approved aircraft, so the 531 patents without one, and the reason, appear as a table only in file 33.

#### `30_wizard_input_suggestions.xlsx` (3.8 MB)

The suggestions the wizard loads with a batch, in the long format (patent, section, sub-dimension, field, definition, options, value, confidence, source, image path, needs review). The Source column says where each suggestion comes from (siglip, sbert, ensemble, patseer, among others). They are not reviewed and not checked.

**One row per:** suggested field of a patent, figure or aircraft

**Depends on:** 01_query export, 05_images

Sheet “Review”, 11 columns: `Patent_ID`, `Section`, `Sub_Dimension`, `Field`, `Definition`, `Options`, `Value`, `Confidence`, `Source`, `Image_Path`, `Needs_Review`

#### `31_patent_text_extraction.csv` (2.6 MB)

What a script read in the text of each patent (name, powertrain, take-off, UAV, with the quoted sentence and a confidence). The author's final value sits next to it in the _human and _final columns.

**One row per:** patent family

**Depends on:** 01_query export

1 639 rows · 165 columns

| column | example | filled |
|---|---|---|
| `patent_id` | US2020223542A1 | 100 % |
| `batch` | Batch_01 | 100 % |
| `company_canonical` | AMSL Innovations | 100 % |
| `assignee_raw` | AMSL INNOVATIONS PL (AU) | 100 % |
| `prototype_label` | Unclassified | 100 % |
| `title` | WING TILT ACTUATION SYSTEM FOR ELECTRIC VERTICAL | 100 % |
| `pdf_link` | https://api.patseer.com/data/pdf/IBa9A%24%24%24o | 99 % |
| `wizard_approved` | True | 100 % |
| `wizard_disapprove_reason` | No Aircraft Image | 32 % |
| `wizard_aircraft_name` | AMSL INNOVATIONS | 63 % |
| `wizard_duplicate_type` | 1 | 27 % |
| `wizard_duplicate_of` | US2020223542A1 | 27 % |
| `wizard_arch_count` | 1 | 100 % |
| `wizard_variant_types` | TP / TP | 4 % |
| `wizard_edge_tags` | UAVSimilar | 4 % |
| `duplicate_root` | US2020223542A1 | 25 % |
| `duplicate_root_note` | you answered this duplicate yourself — kept | 25 % |
| `duplicate_root_aircraft` | 4 | 2 % |
| `duplicate_root_variant` | b | 1 % |
| `duplicate_ambiguous` | False | 25 % |
| `aircraft_group` | Amsl Innovations | 100 % |
| `aircraft_group_source` | wizard | 100 % |
| `aircraft_group_note` | D3 of US2022306289A1 (Honda Motor 2) — different | 1 % |
| `aircraft_group_variants` | AERHART LLC 2a; AERHART LLC 2b | 4 % |
| `aircraft_name_variant_proposals` | CityAirbus; Vahana | 1 % |
| `aircraft_name` | Vertiia | 23 % |
| `aircraft_name_source` | gazetteer | 23 % |
| `aircraft_name_confidence` | 0.95 | 23 % |
| `aircraft_name_in_text` | No | 23 % |
| `aircraft_name_section` | Summary of invention | 2 % |
| `aircraft_name_quote` | The high-speed remote advantage of Fixed Wing Ai | 2 % |
| `aircraft_name_alternatives` | CityAirbus; Vahana | 15 % |
| `aircraft_name_human` | Vertiia | 28 % |
| `aircraft_name_human_variants` | AIrbus Defence 3a; AIrbus Defence 3b; AIrbus Def | 1 % |
| `name_uncertain` |  | 0 % |
| `aircraft_name_final` | Vertiia | 100 % |
| `aircraft_name_final_variants` | AERHART LLC 2a; AERHART LLC 2b | 5 % |
| `is_electric` | Yes | 100 % |
| `is_electric_source` | keyword | 100 % |
| `powertrain` | BatteryElectric | 100 % |
| `powertrain_source` | keyword | 100 % |
| `powertrain_confidence` | 0.8 | 100 % |
| `powertrain_section` | Summary of invention | 100 % |
| `powertrain_quote` | In particular, the present invention relates to  | 81 % |
| `powertrain_other` | Piston | 22 % |
| `powertrain_other_quote` | Claims: The aircraft according to claim 37 , whe | 22 % |
| `is_electric_human` | Yes | 11 % |
| `is_electric_human_variants` | No; No; No; No; No | 1 % |
| `electric_uncertain` | TRUE | 0 % |
| `is_electric_final` | Yes | 100 % |
| `is_electric_final_variants` | Yes; Yes | 5 % |
| `electric_similar_human` | ElectricSimilar | 2 % |
| `electric_similar_human_variants` |  | 0 % |
| `electric_similar_final` | ElectricSimilar | 5 % |
| `electric_similar_final_variants` | ;  | 5 % |
| `takeoff_mode` | VTOL | 96 % |
| `takeoff_source` | keyword | 96 % |
| `takeoff_confidence` | 0.8 | 96 % |
| `takeoff_section` | Title | 96 % |
| `takeoff_quote` | WING TILT ACTUATION SYSTEM FOR ELECTRIC VERTICAL | 96 % |
| `takeoff_human` | VTOL | 8 % |
| `takeoff_human_variants` | VTOL; VTOL; VTOL; VTOL; VTOL | 1 % |
| `takeoff_uncertain` |  | 0 % |
| `takeoff_final` | VTOL | 98 % |
| `takeoff_final_variants` | VTOL; VTOL | 5 % |
| `uav_hint` | UAV | 12 % |
| `uav_source` | keyword | 12 % |
| `uav_confidence` | 0.8 | 12 % |
| `uav_section` | Description of drawings | 12 % |
| `uav_quote` | 1 is an illustration of a prior-art, four-propel | 12 % |
| `uav_human` | No | 5 % |
| `uav_human_variants` | UAVSimilar; UAVSimilar | 1 % |
| `uav_uncertain` |  | 0 % |
| `uav_final` | No | 10 % |
| `uav_final_variants` | UAVSimilar; UAVSimilar | 5 % |
| `review_queue` |  | 0 % |
| `name_review` | False | 100 % |
| `electric_review` | False | 100 % |
| `takeoff_review` | False | 100 % |
| `uav_review` | False | 100 % |
| `needs_review` | True | 100 % |
| `review_reason` | proposed real name not found in patent text; pro | 90 % |
| `review_status` | done | 18 % |
| `reviewed_by` | Vasco Lopes | 14 % |
| `reviewed_at` | 2026-09-09 | 18 % |
| `notes` |  | 0 % |
| `pub_office` | US | 100 % |
| `assignee_country` | AU | 97 % |
| `assignee_country_source` | assignee_string | 97 % |
| `region` | Asia-Pacific | 100 % |
| `app_year` | 2018 | 100 % |
| `pub_year` | 2020 | 100 % |
| `industry_primary` | General_Unspecified | 100 % |
| `industry_source` | sbert | 100 % |
| `industry_confidence` | 0.3 | 100 % |
| `pax` | 2 | 1 % |
| `mtow_kg` | 3170.61 | 0 % |
| `payload_kg` |  | 0 % |
| `cruise_speed_kmh` | 648.2 | 0 % |
| `max_speed_kmh` |  | 0 % |
| `range_km` | 2000 | 0 % |
| `endurance_min` |  | 0 % |
| `spec_source` | regex | 1 % |
| `spec_confidence` | 0.4 | 1 % |
| `blades_primary` | 2 | 1 % |
| `blades_all` | 2 (Lift); 4 | 1 % |
| `blades_min` | 2 | 1 % |
| `blades_max` | 4 | 1 % |
| `blades_distinct` | 0 | 100 % |
| `blade_count_source` | regex | 1 % |
| `blade_count_confidence` | 0.65 | 1 % |
| `scope` | Architectural Subsystem Enabler | 100 % |
| `scope_source` | sbert | 100 % |
| `scope_confidence` | 0.6524 | 100 % |
| `innovation_field` | Mechanical/Kinematic | 100 % |
| `innovation_field_source` | sbert | 100 % |
| `innovation_field_confidence` | 0.6432 | 100 % |
| `architecture_primary` | CVT | 100 % |
| `architecture_primary_label` | Combined (fixed lift + tilting cruise) | 100 % |
| `architecture_all` | Combined (fixed lift + tilting cruise); Tilt-Win | 100 % |
| `architecture_count` | 2 | 100 % |
| `architecture_pure` | False | 100 % |
| `architecture_source` | sbert | 100 % |
| `architecture_confidence` | 0.6715 | 100 % |
| `specificity` | ArchitectureGeneric | 100 % |
| `specificity_confidence` | 0.69 | 100 % |
| `specificity_score` | 0 | 100 % |
| `specificity_reason` | subsystem-enabler scope (-2); 10/20 figures show | 100 % |
| `aircraft_link` | CompanyAttributed | 23 % |
| `generic_language_density` | 2.116 | 100 % |
| `generic_language_level` | medium | 100 % |
| `figures_total` | 20 | 100 % |
| `figures_whole_aircraft` | 10 | 100 % |
| `figures_subsystem` | 7 | 100 % |
| `figures_detail` | 1 | 100 % |
| `figures_diagram` | 2 | 100 % |
| `figures_other` | 0 | 100 % |
| `whole_aircraft_share` | 0.5 | 76 % |
| `legal_stage` | Granted | 100 % |
| `legal_stage_source` | legal_status | 100 % |
| `legal_stage_confidence` | 0.95 | 100 % |
| `kind_code` | A1 | 99 % |
| `legal_status_raw` | ACTIVE - GRANTED | 100 % |
| `right_active` | True | 100 % |
| `forward_citations` | 28 | 100 % |
| `backward_citations` | 28 | 100 % |
| `forward_citations_per_year` | 4.667 | 100 % |
| `forward_citations_in_corpus` | 4 | 100 % |
| `backward_citations_in_corpus` | 11 | 100 % |
| `self_citations_in_corpus` | 0 | 100 % |
| `in_corpus_forward_share` | 0.143 | 76 % |
| `years_since_publication` | 6 | 100 % |
| `grant_lag_years` |  | 0 % |
| `priority_year` | 2017 | 100 % |
| `record_type` | Application | 100 % |
| `snapshot_date` | 2026-06-08 | 100 % |
| `family_id` | 65809451 | 100 % |
| `family_size` | 92 | 100 % |
| `claim_count` | 21 | 100 % |
| `figure_count` |  | 0 % |
| `forward_citation_percentile` | 0.7761 | 100 % |
| `impact_tier` | Medium | 100 % |
| `maturity_tier` | Established | 100 % |
| `llm_reasoning` |  | 0 % |
| `powertrain_review` | engine_generator | 6 % |

#### `32_master_labels.xlsx` (5.8 MB)

Every label of the dataset in the long format the wizard reads and saves: patent, section, sub-dimension, field, value, source and image path. The Source column says whether a value was typed by the author (human) or taken from the PatSeer record (patseer). It is the source of files 33, 41, 42 and 43.

**One row per:** field of a patent, figure or aircraft

**Depends on:** file 30, file 31, 05_images

Sheet “Review”, 7 columns: `Patent_ID`, `Section`, `Sub_Dimension`, `Field`, `Value`, `Source`, `Image_Path`

#### `33_patents.csv` (237.2 KB)

The patent-level labels of file 32 as a table: the author's verdict (approved, reason, duplicate of what, aircraft name) and the final decisions on electric, take-off and UAV.

**One row per:** patent family

**Depends on:** file 31, file 32

1 639 rows · 26 columns

| column | example | filled |
|---|---|---|
| `patent_id` | US2021331794A1 | 100 % |
| `company` | Aerhart | 100 % |
| `aircraft_name` | US2021331794A1_ad1 | 100 % |
| `is_approved` | True | 100 % |
| `reason` | Similar: UAV | 47 % |
| `is_representative` | True | 100 % |
| `similar_tag` | UAVSimilar | 14 % |
| `edgeTags` | UAVSimilar | 9 % |
| `topType` | TP | 42 % |
| `n_approved` | 1 | 100 % |
| `same_aircraft_as` | US2021331794A1_ad1 | 26 % |
| `ad` | 1 | 100 % |
| `batch` | Batch_01 | 100 % |
| `assignee` | AERHART LLC (US) | 68 % |
| `pub_year` | 2021 | 68 % |
| `dup_type` | 2 | 28 % |
| `dup_type_name` | D2 | 28 % |
| `dup_of` | US2021331794A1 | 28 % |
| `dup_root` | US2021331794A1 | 28 % |
| `dup_of_missing` | False | 100 % |
| `uav_final` | No | 10 % |
| `uav_uncertain` |  | 0 % |
| `is_electric_final` | Yes | 68 % |
| `powertrain_review` | engine_generator | 6 % |
| `takeoff_final` | VTOL | 68 % |
| `takeoff_uncertain` |  | 0 % |

#### `README.md` (3.3 KB)

The files of this folder, what they are and what one row means.

### `04_aircraft/`

The aircraft, figures, designs and their technology readiness levels (TRL). Files 41 and 42 are the labels of file 32 as tables (figure level and aircraft level). File 43 gives the architecture class of each aircraft from the figure and from the text. File 44 adds the technology readiness levels (TRL) and is built from the evtol.news directory in folder 06. File 45 is the list of the 621 designs of the analysis: the labels of file 32 (through file 42) plus the TRL of file 44. The suggestions the wizard showed are in 03_patents, file 30.

#### `41_figures.csv` (1.5 MB)

The figure-level labels of file 32 (T2) as a table: state, view, parts, aircraft. The image files are linked in index.csv.

**One row per:** assessed figure

**Depends on:** file 32, 05_images

5 815 rows · 50 columns

| column | example | filled |
|---|---|---|
| `aircraft_id` | AT503689A1_ad1 | 100 % |
| `patent_id` | AT503689A1 | 100 % |
| `ad` | 1 | 100 % |
| `batch` | Batch_02 | 100 % |
| `company` | Individual Inventor | 100 % |
| `fig_key` | 2 | 98 % |
| `block` | Image: AT503689A1_fig_01_crop_0_F2.png | 100 % |
| `image_file` | AT503689A1_fig_01_crop_0_F2.png | 100 % |
| `status` | approved | 100 % |
| `arch` | 1 | 33 % |
| `is_main` | False | 33 % |
| `per` | Side | 33 % |
| `acSty` | Line Drawing | 33 % |
| `acCol` | B/W (Monochrome) | 33 % |
| `bgSty` | Solid Fill | 33 % |
| `bgCol` | White | 33 % |
| `parts` | Whole Vehicle Layout | 33 % |
| `qualityFlag` | clean | 33 % |
| `acState` | Hover | 33 % |
| `stateNote` | not invariant | 0 % |
| `hasLegends` | False | 33 % |
| `dupOf` | USD1017462S FIG. 2 | 2 % |
| `comment` | parts: flow deflector | 0 % |
| `fig_tags` | Image label is not correspponding | 0 % |
| `rotation_deg` | 0 | 33 % |
| **Pré-etiquetas** | | |
| `ml_per` | Rear-Isometric | 12 % |
| `ml_per_conf` | 0.151 | 12 % |
| `ml_acSty` | Render | 12 % |
| `ml_acSty_conf` | 0.156 | 12 % |
| `ml_acCol` | Grayscale | 12 % |
| `ml_acCol_conf` | 0.134 | 12 % |
| `ml_bgSty` | Solid Fill | 12 % |
| `ml_bgSty_conf` | 0.135 | 12 % |
| `ml_bgCol` | White | 12 % |
| `ml_bgCol_conf` | 0.13 | 12 % |
| `ml_acState` | Transition | 12 % |
| `ml_acState_conf` | 0.139 | 12 % |
| `ml_parts` | Rotor/Propeller Blade | 4 % |
| `ml_parts_conf` |  | 0 % |
| `ml_tiltedInView` | Rotors | 1 % |
| `ml_match_status` | disk_only | 87 % |
| `ml_dupOfPatent` | CA2874341A1 | 21 % |
| `ml_dupOfFig` | 5 | 21 % |
| `ml_per_agrees` | True | 4 % |
| `ml_acSty_agrees` | False | 4 % |
| `ml_acCol_agrees` | False | 4 % |
| `ml_bgSty_agrees` | True | 4 % |
| `ml_bgCol_agrees` | True | 4 % |
| `ml_acState_agrees` | False | 4 % |
| `is_primary` | True | 100 % |

#### `42_aircraft.csv` (1.3 MB)

The aircraft-level labels of file 32 (G1, M1, M2, M3) as a table, with the domain answers. Approved patents only.

**One row per:** aircraft (patent variant)

**Depends on:** file 32, file 41

1 219 rows · 405 columns

| column | example | filled |
|---|---|---|
| **Identificação** | | |
| `aircraft_id` | US2021331794A1_ad1 | 100 % |
| `patent_id` | US2021331794A1 | 100 % |
| `ad` | 1 | 100 % |
| `n_variants` | 1 | 100 % |
| `batch` | Batch_01 | 100 % |
| `company` | Aerhart | 100 % |
| `aircraft_name` | US2021331794A1_ad1 | 100 % |
| `name_is_real` | False | 100 % |
| `variant` | 1 | 100 % |
| `variant_id` | US2021331794A1 | 100 % |
| `is_approved` | True | 100 % |
| `reason` |  | 0 % |
| `reason_source` |  | 0 % |
| `sub_reason` |  | 0 % |
| `reason_human` |  | 0 % |
| `reason_sbert` |  | 0 % |
| `reason_note` |  | 0 % |
| `is_duplicate` | False | 100 % |
| `dup_type` | 2 | 38 % |
| `dup_type_name` | D2 | 38 % |
| `dup_of` | US2021331794A1 | 38 % |
| `dup_root` | US2021331794A1 | 38 % |
| `is_primary` | True | 100 % |
| `same_aircraft_as` | US2021331794A1_ad1 | 35 % |
| `points_to_ad` | 1 | 35 % |
| `labels_inherited_from` | US2021331794A1 | 35 % |
| `dup_of_missing` | False | 100 % |
| `n_figures` | 13 | 100 % |
| `n_approved` | 1 | 100 % |
| `n_approved_this_variant` | 1 | 100 % |
| `n_fig_placeholders` | 3 | 100 % |
| `main_figure` | 05_images/crops/Batch_01/US2021331794A1_78221758 | 100 % |
| `img_not_reflect` | False | 100 % |
| `overrides` | M2 | 1 % |
| `propulsor_units` | 4 | 63 % |
| `propulsor_units_note` | HB: the codebook excludes hoverbikes and PFVs fr | 3 % |
| `wing_thrust_carrier` | wing | 58 % |
| `wing_borne_units` | 4 | 54 % |
| `wing_borne_units_note` | wingless | 12 % |
| `wing_boom_candidate` | False | 58 % |
| `boom_thrust_state` | none | 65 % |
| **T1 · triagem da patente** | | |
| `assignee` | AERHART LLC (US) | 100 % |
| `title` | Aeronautical Apparatus | 100 % |
| `app_year` | 2021 | 100 % |
| `pub_year` | 2021 | 100 % |
| `pdf_link` | https://api.patseer.com/data/pdf/IBa9A%24%24%24o | 98 % |
| **T1 · escapes** | | |
| `t1_humanUncertain` | False | 98 % |
| `t1_uncertainNote` | Some fields may be unanswered cause there is onl | 0 % |
| `t1_quickOverride` | False | 98 % |
| `t1_quickNote` | Aircraft supported by other UAVs... Not to be us | 0 % |
| **G1 · arquitetura** | | |
| `topType` | TP | 65 % |
| `edgeTags` | UAVSimilar | 14 % |
| `g1_humanUncertain` | False | 65 % |
| `g1_uncertainNote` | not a common  multicopter | 5 % |
| `g1_quickOverride` | False | 65 % |
| `g1_quickNote` | Convertiplane | 0 % |
| **M1 · morfologia estrutural** | | |
| `fusShape` | Circular | 63 % |
| `fusShapeOtherNote` | unknow, but seems like a large sqared fuselage t | 1 % |
| `fusKin` | Fixed | 63 % |
| `gearArch` | Wheeled Gear | 63 % |
| `latSym` | True | 65 % |
| `dinoUnderstanding` | Hard | 65 % |
| `boomsPresent` | False | 65 % |
| `boom1_count` | 1 | 30 % |
| `boom1_attach` | Fuselage | 29 % |
| `boom1_attachOth` | connected to the structural booms | 0 % |
| `boom1_wingRel` | Bridge | 19 % |
| `boom1_wingRelOth` | at the tipp of the wing, paralell to it | 1 % |
| `boom1_wingIdx` | Multi | 6 % |
| `boom1_span` | MidSpan | 19 % |
| `boom1_long` | Fore | 11 % |
| `boom1_longOth` | in the  middle of the fuselage | 0 % |
| `boom1_orient` | Long | 30 % |
| `boom1_orientOth` | CONNECTED TO THE BOTTOM OF THE FUSELAGE IN A SQU | 1 % |
| `boom1_sym` | True | 30 % |
| `boom1_circSym` | False | 30 % |
| `boom1_hasProps` | True | 29 % |
| `boom1_tilts` | True | 28 % |
| `boom1_retracts` | False | 17 % |
| `boom1_onFixedPart` | True | 0 % |
| `boom2_count` | 1 | 15 % |
| `boom2_attach` | Fuselage | 15 % |
| `boom2_attachOth` | connnects fuselage ot the booms that have propel | 0 % |
| `boom2_wingRel` | Aft | 11 % |
| `boom2_wingIdx` | W1 | 2 % |
| `boom2_span` | MidSpan | 11 % |
| `boom2_long` | Aft | 5 % |
| `boom2_orient` | Long | 15 % |
| `boom2_orientOth` | circular, holded by the 3 booms of group one | 0 % |
| `boom2_sym` | True | 15 % |
| `boom2_circSym` | False | 15 % |
| `boom2_hasProps` | True | 15 % |
| `boom2_tilts` | True | 14 % |
| `boom2_retracts` | False | 9 % |
| `boom2_onFixedPart` | True | 0 % |
| `boom3_count` | 1 | 4 % |
| `boom3_attach` | Fuselage | 4 % |
| `boom3_attachOth` | to the boom group 2 | 0 % |
| `boom3_wingRel` | Fore | 3 % |
| `boom3_wingIdx` | W2 | 1 % |
| `boom3_span` | MidSpan | 3 % |
| `boom3_long` | Mid | 1 % |
| `boom3_orient` | Lat | 4 % |
| `boom3_sym` | True | 4 % |
| `boom3_circSym` | False | 4 % |
| `boom3_hasProps` | True | 4 % |
| `boom3_tilts` | True | 4 % |
| `boom3_retracts` | False | 2 % |
| `boom4_count` | 1 | 1 % |
| `boom4_attach` | Wings | 1 % |
| `boom4_attachOth` | to the longitudinal booms | 0 % |
| `boom4_wingRel` | Aft | 1 % |
| `boom4_wingIdx` | W2 | 0 % |
| `boom4_span` | MidSpan | 1 % |
| `boom4_long` | Aft | 0 % |
| `boom4_orient` | Long | 1 % |
| `boom4_sym` | True | 1 % |
| `boom4_circSym` | False | 1 % |
| `boom4_hasProps` | True | 1 % |
| `boom4_tilts` | False | 1 % |
| `boom4_retracts` | False | 1 % |
| `boom5_count` | 1 | 0 % |
| `boom5_attach` | Wings | 0 % |
| `boom5_wingRel` | Straddle | 0 % |
| `boom5_wingIdx` | W1 | 0 % |
| `boom5_span` | Outboard | 0 % |
| `boom5_orient` | Long | 0 % |
| `boom5_sym` | True | 0 % |
| `boom5_circSym` | False | 0 % |
| `boom5_hasProps` | True | 0 % |
| `boom5_tilts` | True | 0 % |
| `boom5_retracts` | False | 0 % |
| `boom6_count` | 1 | 0 % |
| `boom6_attach` | Wings | 0 % |
| `boom6_wingRel` | Aft | 0 % |
| `boom6_wingIdx` | W1 | 0 % |
| `boom6_span` | MidSpan | 0 % |
| `boom6_orient` | Long | 0 % |
| `boom6_sym` | True | 0 % |
| `boom6_circSym` | False | 0 % |
| `boom6_hasProps` | True | 0 % |
| `boom6_tilts` | False | 0 % |
| `boom6_retracts` | False | 0 % |
| `wingNotes` | Wings in X form | 2 % |
| `boomNotes` | booms in x form mounted on top of the cabin | 2 % |
| `fusNotes` | 2 fuselages | 1 % |
| `empNotes` | on both wingtip booms | 4 % |
| `gearNotes` | retractable | 0 % |
| `m1_humanUncertain` | False | 65 % |
| `m1_uncertainNote` | wingtip rotates witht the propeller | 0 % |
| `m1_quickOverride` | False | 65 % |
| **M2 · morfologia aerodinâmica** | | |
| `wingConf` | W | 57 % |
| `wingConfOtherNote` | wings in x shape | 4 % |
| `wCount` | 2 | 65 % |
| `empType` | VertFin | 63 % |
| `empTypeOtherNote` | INVERTED CONVENTIONAL | 1 % |
| `empTilts` | False | 65 % |
| `wing1_role` | Main | 60 % |
| `wing1_tilt` | Fixed | 55 % |
| `wing1_posV` | High | 55 % |
| `wing1_posL` | Fwd | 55 % |
| `wing1_plan` | Str | 57 % |
| `wing1_plan_otherNote` | Complex | 2 % |
| `wing1_tipJoin` | False | 31 % |
| `wing2_role` | Tandem | 19 % |
| `wing2_role_otherNote` | on top of the main aircraft, much bigger than th | 0 % |
| `wing2_tilt` | Fixed | 19 % |
| `wing2_posV` | High | 19 % |
| `wing2_posL` | Aft | 19 % |
| `wing2_plan` | Str | 19 % |
| `wing2_plan_otherNote` | Complex | 1 % |
| `wing2_tipJoin` | False | 11 % |
| `wing3_role` | Aft | 2 % |
| `wing3_tilt` | Fixed | 2 % |
| `wing3_posV` | High | 2 % |
| `wing3_posL` | Aft | 2 % |
| `wing3_plan` | Str | 2 % |
| `wing3_plan_otherNote` | it serves as rotor for hover | 0 % |
| `wing3_tipJoin` | True | 1 % |
| `m2_humanUncertain` | False | 65 % |
| `m2_uncertainNote` | aft wing can seem bigger, either way the front w | 1 % |
| `m2_quickOverride` | False | 65 % |
| `m2_quickNote` | stoped rotor wing | 0 % |
| **M3 · morfologia propulsiva** | | |
| `fuselage_count` | 0 | 65 % |
| `fuselage_sym` | False | 65 % |
| `fuselage_ntypes` | 1 | 65 % |
| `fuselage_zone` | Aft | 18 % |
| `fuselage_quickOverride` | False | 65 % |
| `fuselage_quickCount` | 2 | 0 % |
| `fuselage_notes` | non-visible on the image, may abnother duplicate | 1 % |
| `fuselage_chord` | Back | 18 % |
| `fuselage_orient` | Horizontal | 18 % |
| `fuselage_bmech` | Open | 18 % |
| `fuselage_rmech` | Fixed | 18 % |
| `fuselage_propKin` | Fixed | 18 % |
| `fuselage_ctrlOnly` | False | 6 % |
| `fuselage_t1_count` | 1 | 6 % |
| `fuselage_t1_chord` | Front | 6 % |
| `fuselage_t1_orient` | Vertical | 6 % |
| `fuselage_t1_bmech` | Open | 6 % |
| `fuselage_t1_rmech` | Fixed | 6 % |
| `fuselage_t1_propKin` | Fixed | 6 % |
| `fuselage_t1_ctrlOnly` | False | 4 % |
| `fuselage_t1_zone` | FusFront | 6 % |
| `fuselage_t2_count` | 1 | 6 % |
| `fuselage_t2_chord` | Front | 6 % |
| `fuselage_t2_orient` | Vertical | 6 % |
| `fuselage_t2_bmech` | Open | 6 % |
| `fuselage_t2_rmech` | Fixed | 6 % |
| `fuselage_t2_propKin` | Fixed | 6 % |
| `fuselage_t2_ctrlOnly` | False | 4 % |
| `fuselage_t2_zone` | FusRear | 6 % |
| `fuselage_t3_count` | 3 | 0 % |
| `fuselage_t3_chord` | Front | 0 % |
| `fuselage_t3_orient` | Horizontal | 0 % |
| `fuselage_t3_bmech` | Ducted | 0 % |
| `fuselage_t3_rmech` | Fixed | 0 % |
| `fuselage_t3_propKin` | Fixed | 0 % |
| `fuselage_t3_ctrlOnly` | False | 0 % |
| `fuselage_t3_zone` | Aft | 0 % |
| `wing1_count` | 2 | 55 % |
| `wing1_sym` | True | 55 % |
| `wing1_ntypes` | 1 | 55 % |
| `wing1_zoneChord` | LE | 30 % |
| `wing1_zoneSpan` | Wingtip | 30 % |
| `wing1_quickOverride` | False | 55 % |
| `wing1_quickCount` | 2 | 0 % |
| `wing1_notes` | 2 propellers stacked vertically (one over  and t | 1 % |
| `wing1_chord` | Front | 30 % |
| `wing1_orient` | Mixed | 30 % |
| `wing1_bmech` | Open | 30 % |
| `wing1_rmech` | Fixed | 30 % |
| `wing1_propKin` | Tilt | 30 % |
| `wing1_propKinOth` | the propeller inside the "nacelle" roatets to go | 0 % |
| `wing1_ctrlOnly` | False | 11 % |
| `wing1_t1_count` | 8 | 3 % |
| `wing1_t1_chord` | Front | 3 % |
| `wing1_t1_orient` | Horizontal | 3 % |
| `wing1_t1_bmech` | Open | 3 % |
| `wing1_t1_rmech` | Fixed | 3 % |
| `wing1_t1_propKin` | Fixed | 3 % |
| `wing1_t1_propKinOth` | THIS SECTIO OF THE WING TILTS  | 0 % |
| `wing1_t1_ctrlOnly` | False | 1 % |
| `wing1_t1_zoneChord` | LE | 3 % |
| `wing1_t1_zoneSpan` | FullSpan | 3 % |
| `wing1_t2_count` | 8 | 3 % |
| `wing1_t2_chord` | Front | 3 % |
| `wing1_t2_orient` | Vertical | 3 % |
| `wing1_t2_bmech` | Open | 3 % |
| `wing1_t2_rmech` | Fixed | 3 % |
| `wing1_t2_propKin` | Fixed | 3 % |
| `wing1_t2_ctrlOnly` | False | 1 % |
| `wing1_t2_zoneChord` | Above | 3 % |
| `wing1_t2_zoneSpan` | FullSpan | 3 % |
| `wing1_t3_count` | 2 | 0 % |
| `wing1_t3_chord` | Front | 0 % |
| `wing1_t3_orient` | Horizontal | 0 % |
| `wing1_t3_bmech` | Ducted | 0 % |
| `wing1_t3_rmech` | Fixed | 0 % |
| `wing1_t3_propKin` | Tilt | 0 % |
| `wing1_t3_ctrlOnly` | False | 0 % |
| `wing1_t3_zoneChord` | TE | 0 % |
| `wing1_t3_zoneSpan` | MidSpan | 0 % |
| `wing2_count` | 2 | 19 % |
| `wing2_sym` | True | 19 % |
| `wing2_ntypes` | 1 | 19 % |
| `wing2_zoneChord` | LE | 10 % |
| `wing2_zoneSpan` | Wingtip | 10 % |
| `wing2_quickOverride` | False | 19 % |
| `wing2_quickCount` | 1 | 0 % |
| `wing2_notes` | Each "propulsor unit", and there are 4, has 4 pr | 0 % |
| `wing2_chord` | Front | 10 % |
| `wing2_orient` | Mixed | 10 % |
| `wing2_bmech` | Open | 10 % |
| `wing2_rmech` | Fixed | 10 % |
| `wing2_propKin` | Tilt | 10 % |
| `wing2_propKinOth` | the propeller inside the "nacelle" roatets to go | 0 % |
| `wing2_ctrlOnly` | False | 4 % |
| `wing2_t1_count` | 2 | 0 % |
| `wing2_t1_chord` | Front | 0 % |
| `wing2_t1_orient` | Mixed | 0 % |
| `wing2_t1_bmech` | Open | 0 % |
| `wing2_t1_rmech` | Fixed | 0 % |
| `wing2_t1_propKin` | Fixed | 0 % |
| `wing2_t1_ctrlOnly` | False | 0 % |
| `wing2_t1_zoneChord` | LE | 0 % |
| `wing2_t1_zoneSpan` | Inboard | 0 % |
| `wing2_t2_count` | 2 | 0 % |
| `wing2_t2_chord` | Front | 0 % |
| `wing2_t2_orient` | Mixed | 0 % |
| `wing2_t2_bmech` | Open | 0 % |
| `wing2_t2_rmech` | Fixed | 0 % |
| `wing2_t2_propKin` | Fixed | 0 % |
| `wing2_t2_ctrlOnly` | False | 0 % |
| `wing2_t2_zoneChord` | LE | 0 % |
| `wing2_t2_zoneSpan` | Wingtip | 0 % |
| `wing3_count` | 0 | 2 % |
| `wing3_sym` | True | 2 % |
| `wing3_ntypes` | 1 | 2 % |
| `wing3_zoneChord` | LE | 1 % |
| `wing3_zoneSpan` | Wingtip | 1 % |
| `wing3_quickOverride` | False | 2 % |
| `wing3_quickCount` | 1 | 0 % |
| `wing3_notes` | it is its own propeller that stops in cruise mod | 0 % |
| `wing3_chord` | Front | 1 % |
| `wing3_orient` | Mixed | 1 % |
| `wing3_bmech` | Open | 1 % |
| `wing3_rmech` | Fixed | 1 % |
| `wing3_propKin` | Tilt | 1 % |
| `wing3_ctrlOnly` | False | 0 % |
| `emp_count` | 0 | 45 % |
| `emp_sym` | False | 45 % |
| `emp_ntypes` | 1 | 45 % |
| `emp_zone` | Tip | 10 % |
| `emp_quickOverride` | False | 45 % |
| `emp_notes` | diectional stabilizer propeller | 1 % |
| `emp_chord` | Back | 10 % |
| `emp_orient` | Horizontal | 10 % |
| `emp_bmech` | Ducted | 10 % |
| `emp_rmech` | Fixed | 10 % |
| `emp_propKin` | Fixed | 10 % |
| `emp_ctrlOnly` | True | 4 % |
| `emp_t1_count` | 2 | 0 % |
| `emp_t1_chord` | Front | 0 % |
| `emp_t1_orient` | Vertical | 0 % |
| `emp_t1_bmech` | Ducted | 0 % |
| `emp_t1_rmech` | Fixed | 0 % |
| `emp_t1_propKin` | Fixed | 0 % |
| `emp_t1_zone` | StackH | 0 % |
| `emp_t2_count` | 1 | 0 % |
| `emp_t2_chord` | Back | 0 % |
| `emp_t2_orient` | Horizontal | 0 % |
| `emp_t2_bmech` | Open | 0 % |
| `emp_t2_rmech` | Fixed | 0 % |
| `emp_t2_propKin` | Fixed | 0 % |
| `emp_t2_zone` | Tip | 0 % |
| `boom_count` | 0 | 65 % |
| `boom_sym` | True | 65 % |
| `boom_ntypes` | 1 | 65 % |
| `boom_quickOverride` | False | 65 % |
| `boom_quickCount` | 10 | 0 % |
| `boom_notes` | squared shape, one in eahc corner, having both t | 1 % |
| `boom_chord` | Front | 12 % |
| `boom_orient` | Mixed | 12 % |
| `boom_bmech` | Open | 12 % |
| `boom_rmech` | Fixed | 12 % |
| `boom_propKin` | Fixed | 12 % |
| `boom_ctrlOnly` | False | 5 % |
| `boom_t1_count` | 2 | 15 % |
| `boom_t1_chord` | Front | 15 % |
| `boom_t1_orient` | Mixed | 15 % |
| `boom_t1_bmech` | Open | 15 % |
| `boom_t1_rmech` | Fixed | 15 % |
| `boom_t1_propKin` | Fixed | 15 % |
| `boom_t1_ctrlOnly` | False | 6 % |
| `boom_t2_count` | 2 | 15 % |
| `boom_t2_chord` | Front | 15 % |
| `boom_t2_orient` | Mixed | 15 % |
| `boom_t2_bmech` | Open | 15 % |
| `boom_t2_rmech` | Fixed | 15 % |
| `boom_t2_propKin` | Fixed | 15 % |
| `boom_t2_ctrlOnly` | False | 6 % |
| `boom_t3_count` | 2 | 4 % |
| `boom_t3_chord` | Front | 4 % |
| `boom_t3_orient` | Mixed | 4 % |
| `boom_t3_bmech` | Open | 4 % |
| `boom_t3_rmech` | Fixed | 4 % |
| `boom_t3_propKin` | Fixed | 4 % |
| `boom_t3_ctrlOnly` | False | 2 % |
| `boom_t4_count` | 2 | 2 % |
| `boom_t4_chord` | Front | 2 % |
| `boom_t4_orient` | Vertical | 2 % |
| `boom_t4_bmech` | Ducted | 2 % |
| `boom_t4_rmech` | Fixed | 2 % |
| `boom_t4_propKin` | Fixed | 2 % |
| `boom_t4_ctrlOnly` | False | 1 % |
| `boom_t5_count` | 2 | 0 % |
| `boom_t5_chord` | Front | 0 % |
| `boom_t5_orient` | Mixed | 0 % |
| `boom_t5_bmech` | Open | 0 % |
| `boom_t5_rmech` | Fixed | 0 % |
| `boom_t5_propKin` | Fixed | 0 % |
| `boom_t5_ctrlOnly` | False | 0 % |
| `boom_t6_count` | 2 | 0 % |
| `boom_t6_chord` | Front | 0 % |
| `boom_t6_orient` | Vertical | 0 % |
| `boom_t6_bmech` | Open | 0 % |
| `boom_t6_rmech` | Fixed | 0 % |
| `boom_t6_propKin` | Fixed | 0 % |
| `boom_t6_ctrlOnly` | False | 0 % |
| `m3_humanUncertain` | False | 65 % |
| `m3_uncertainNote` | tehre is no image showing the rotors turned, but | 0 % |
| **Domínio, ground truth e tags** | | |
| `uav_final` | No | 16 % |
| `uav_uncertain` |  | 0 % |
| `is_electric_final` | Yes | 100 % |
| `electric_uncertain` | True | 0 % |
| `electric_similar_final` | ElectricSimilar | 8 % |
| `powertrain_review` | engine_generator | 10 % |
| `takeoff_final` | VTOL | 100 % |
| `takeoff_uncertain` |  | 0 % |
| `identity_from` | US2021331794A1 | 100 % |
| `arch_gt` | TP | 65 % |
| `arch_gt_provenance` | confirmed | 65 % |
| `arch_gt_visible` | yes | 65 % |
| `is_design` | True | 100 % |

#### `43_architecture_image_and_text.csv` (64.0 KB)

The architecture class of each primary aircraft in two readings: architecture_from_image (what the author labelled from the main figure in the wizard) and architecture_from_text (what the patent text states, checked by the author). visible_in_figures says whether that architecture can be seen in the figures, and note marks the uncertain cases. The analysis uses these classes as the reference to evaluate the image models.

**One row per:** primary aircraft

**Depends on:** file 42, file 31, 05_images

797 rows · 8 columns

| column | example | filled |
|---|---|---|
| `aircraft_id` | US2021331794A1_ad1 | 100 % |
| `patent_id` | US2021331794A1 | 100 % |
| `company` | Aerhart | 100 % |
| `aircraft_name` | US2021331794A1_ad1 | 100 % |
| `architecture_from_image` | TP | 100 % |
| `architecture_from_text` | TP | 100 % |
| `visible_in_figures` | yes | 100 % |
| `note` | image label marked uncertain in the wizard | 8 % |

#### `44_trl.csv` (199.0 KB)

The technology readiness level (TRL) of each aircraft with everything behind it. trl is the final value: the script reading of the evtol.news directory page (directory_page, directory_sentence, script_trl), replaced by author_trl where the author reviewed it (trl_source says which). The evidence_* columns hold a second TRL from web sources for the programmes with public evidence, with its basis, a confidence (high, medium, default), the quoted sentence and the source. The programme_status and company_status columns say whether the programme and the company are active or ended, with the date and the source. The scale of the levels is in codebook/trl_scale.csv.

**One row per:** aircraft

**Depends on:** file 42, **06_external/61_evtol_news_directory** (pages and patent links) and the web pages cited in the source columns

798 rows · 29 columns

| column | example | filled |
|---|---|---|
| `aircraft_id` | US2021331794A1_ad1 | 100 % |
| `patent_id` | US2021331794A1 | 100 % |
| `aircraft_name` | US2021331794A1_ad1 | 100 % |
| `company` | Aerhart | 100 % |
| `directory_page` | airbus-helicopters | 10 % |
| `directory_sentence` | The vehicle is designed to fly autonomously. | 10 % |
| `script_trl` | 2 | 100 % |
| `author_trl` | 6 | 6 % |
| `trl` | 2 | 100 % |
| `trl_source` | script | 100 % |
| `evidence_trl` | 2 | 100 % |
| `evidence_basis` | patent only | 100 % |
| `evidence_confidence` | default | 100 % |
| `evidence_quote` | (no public evidence of hardware found; not linke | 100 % |
| `evidence_source` | evtol.news/airbus-helicopters / evtol.news/airbu | 13 % |
| `programme_trl` | 2 | 100 % |
| `arch_match` | yes | 13 % |
| `public_arch` | Vectored thrust (S4, tilt rotor) | 1 % |
| `evidence_note` | no untethered forward or wingborne flight stated | 8 % |
| `programme_status` | paused | 13 % |
| `status_since` | 2025-01 | 13 % |
| `status_confidence` | high | 13 % |
| `status_evidence` | Airbus to 'pause' CityAirbus NextGen development | 13 % |
| `status_source` | evtol.news/airbus-helicopters-cityairbus-nextgen | 13 % |
| `status_note` | the flight test campaign continued through March | 4 % |
| `company_status` | paused | 4 % |
| `company_status_since` | 2025-09 | 4 % |
| `company_status_evidence` | Hyundai Pausing Work on Supernal Air Taxi Progra | 4 % |
| `company_status_source` | https://www.flyingmag.com/hyundai-supernal-elect | 4 % |

#### `45_designs.csv` (58.6 KB)

The 621 analysed designs. Which aircraft are designs, and their architecture and company, come from the labels in file 32 (through file 42, column is_design). The final TRL and its source come from file 44. Priority year and firm are added from the patent records.

**One row per:** design

**Depends on:** file 32 (through file 42), file 44, 01_query export

621 rows · 9 columns

| column | example | filled |
|---|---|---|
| `aircraft_id` | US2021331794A1_ad1 | 100 % |
| `patent_id` | US2021331794A1 | 100 % |
| `aircraft_name` | US2021331794A1_ad1 | 100 % |
| `company` | Aerhart | 100 % |
| `firm` | Aerhart | 71 % |
| `architecture` | TP | 100 % |
| `priority_year` | 2018 | 100 % |
| `final_trl` | 2 | 100 % |
| `trl_source` | script | 100 % |

#### `README.md` (2.6 KB)

The files of this folder, what they are and what one row means.

### `06_external/`

Outside sources: the evtol.news directory, the AAM Reality Index and context series. Sources from outside the patent corpus. Each folder is a few tables, one idea per file.

#### `06_external/61_evtol_news_directory/`



##### `directory_accuracy.csv` (1009 B)

How often the script rules agree with the author on those reviewed pages, with the 95 % interval.

**One row per:** rule and check

**Depends on:** directory_rule_vs_author.csv

9 rows · 7 columns

| column | example | filled |
|---|---|---|
| `input` | Domain flag: deleting pages as out of domain | 100 % |
| `method` | script rules | 100 % |
| `agree` | 61 | 100 % |
| `of_n` | 68 | 100 % |
| `share_pct` | 89.7 | 100 % |
| `interval_95_pct` | 82.1-94.3 | 100 % |
| `what_it_measures` | share of excluded pages that really are out | 100 % |

##### `directory_aircraft.csv` (1.3 MB)

The evtol.news directory, one row per aircraft page: the page data (title, company, status, specifications), the domain flags (domain_*, with domain_in_domain the decision), the development year (year_script, the author's year_author where reviewed, year_final) and the TRL sentences the scripts found (trl_script, trl7).

**One row per:** directory page

**Depends on:** the public pages of evtol.news

1 229 rows · 49 columns

| column | example | filled |
|---|---|---|
| **Identificação** | | |
| `company` | 3D Molier | 99 % |
| **T1 · triagem da patente** | | |
| `title` | 3D Molier Cargo Quadrocopter Drone (concept desi | 100 % |
| **Domínio, ground truth e tags** | | |
| `slug_key` | 3d-molier-cargo-quadrocopter-drone-concept-desig | 100 % |
| `slug` | 3d-molier-cargo-quadrocopter-drone-concept-desig | 100 % |
| `url` | https://evtol.news/3d-molier-cargo-quadrocopter- | 100 % |
| `list_name` | 3D Molier Cargo Quadrocopter Drone | 100 % |
| `list_status` | concept design | 63 % |
| `evtol_class` | WM | 100 % |
| `list_pos` | 0 | 100 % |
| `model` | Cargo Quadrocopter Drone | 99 % |
| `status` | concept design | 63 % |
| `location` | Panama, Republic of Panama | 98 % |
| `website` | www.3dsmolier.com | 92 % |
| `spec_aircraft_type` | Hybrid-electric or electric heavy-lift VTOL inte | 90 % |
| `spec_piloting` | Autonomous or remote | 83 % |
| `spec_capacity` | Intermodal cargo containers | 70 % |
| `spec_cruise_speed` | 124 mph (200 km/h, 110 kt) | 62 % |
| `spec_range` | +200 km (+125 miles) | 45 % |
| `spec_flight_time` | Unknown | 29 % |
| `spec_propellers` | 8 propellers | 81 % |
| `spec_electric_motors` | 8 electric motors | 83 % |
| `spec_power_source` | Hybrid-electric or batteries | 83 % |
| `spec_fuselage` | Carbon fiber composite | 77 % |
| `spec_wings` | 1 high long main wing | 39 % |
| `spec_windows` | The entire nose of the aircraft is clear allowin | 45 % |
| `spec_landing_gear` | Lands on the bottom of its fuselage | 89 % |
| `spec_safety_features` | Distributed Electric Propulsion (DEP), provides  | 82 % |
| `spec_tail` | 1 horizontal stabilizer | 32 % |
| `n_images` | 5 | 100 % |
| `page_status` | ok | 100 % |
| `n_classes` | 1 | 100 % |
| `evtol_class_main` | WM | 100 % |
| `gofly` | False | 100 % |
| `domain_class5` | WM | 100 % |
| `domain_status` | concept design | 66 % |
| `domain_status_group` | concept design | 100 % |
| `domain_not_combustion` | True | 100 % |
| `domain_crewed` | False | 100 % |
| `domain_in_domain` | False | 100 % |
| `domain_patented` | False | 100 % |
| `year_script` | 2018 | 89 % |
| `year_sentence` | Video: 4Front Robotics , Your Alberta (Governmen | 89 % |
| `year_author` | 2024 | 7 % |
| `year_final` | 2018 | 89 % |
| `year_source` | script | 100 % |
| `trl_script` | 2 | 100 % |
| `trl_script_sentence` | The Navig8 designation is a family of UAV’s whic | 85 % |
| `trl7` | 0 | 100 % |
| `trl7_sentence` | Aerofugia announced on June 12, 2024 that the AE | 2 % |

##### `directory_pages.jsonl` (7.1 MB)

The text of every directory page as collected.

**One row per:** directory page

**Depends on:** the public pages of evtol.news

##### `directory_patent_links.csv` (20.1 KB)

Which aircraft of the dataset correspond to which directory pages, and how the match was made (match).

**One row per:** aircraft of the dataset

**Depends on:** file 42, directory_aircraft.csv

108 rows · 13 columns

| column | example | filled |
|---|---|---|
| `aircraft_id` | US2018244367A1_ad1 | 100 % |
| `patent_id` | US2018244367A1 | 100 % |
| `aircraft_name` | CityAirbus | 100 % |
| `family` | CityAirbus | 100 % |
| `company` | Airbus | 100 % |
| `topType` | MR | 100 % |
| `match` | name+company | 100 % |
| `n_pages` | 4 | 100 % |
| `slug_keys` | airbus-helicopters/airbus-helicopters-cityairbus | 92 % |
| `page_titles` | Airbus Helicopters CityAirbus (technology demons | 92 % |
| `page_classes` | WM/WM/WM/WM | 92 % |
| `use` | yes | 100 % |
| `note` | not in the directory index | 8 % |

##### `directory_rule_vs_author.csv` (22.8 KB)

The pages the author reviewed to check the script rules: for the domain flag and for the development year, the script answer, the author answer and whether they agree.

**One row per:** reviewed page and question

**Depends on:** directory_aircraft.csv

247 rows · 8 columns

| column | example | filled |
|---|---|---|
| `question` | domain | 100 % |
| `slug_key` | a3-by-airbus | 100 % |
| `sample` | patent-linked, excluded | 100 % |
| `script_value` | out | 99 % |
| `author_value` | in | 100 % |
| `agree` | False | 99 % |
| `within_1_year` | True | 33 % |
| `sentence` | Video: Vertical Flight Society (VFS) 3rd Annual  | 32 % |

##### `directory_year_sentences.csv` (4.1 MB)

Every sentence of the pages that contains a year, split from the pages by a script. The development year rule reads them.

**One row per:** sentence

**Depends on:** directory_pages.jsonl

14 148 rows · 7 columns

| column | example | filled |
|---|---|---|
| `evidence_id` | E0001.01 | 100 % |
| `page_id` | P0001 | 100 % |
| `slug_key` | 3d-molier-cargo-quadrocopter-drone-concept-desig | 100 % |
| `is_resource` | False | 100 % |
| `years` | 2005 | 100 % |
| `sentence` | The 3D Molier company was founded in 2005 by And | 100 % |
| `link` | https://evtol.news/3d-molier-cargo-quadrocopter- | 100 % |

#### `06_external/62_aam_index/`



##### `aam_index_company_map.csv` (2.2 KB)

Which dataset company each index company is (company_canonical), the match the script proposed (script_match), the author's choice (author) and a flag for companies outside the domain.

**One row per:** company of the index

**Depends on:** the published index, companies in file 33

43 rows · 6 columns

| column | example | filled |
|---|---|---|
| `oem` | Ehang | 100 % |
| `script_match` | Volocopter | 42 % |
| `author` | Guangzhou Ehang Intelligent Technology | 60 % |
| `company_canonical` | Guangzhou Ehang Intelligent Technology | 60 % |
| `note` | not in the patent corpus | 30 % |
| `domain_flag` | out: not VTOL (EL-9, blown-lift STOL) | 9 % |

##### `aam_index_current.csv` (3.0 KB)

The AAM Reality Index as published in May 2026: score, trend, funding, use case, vehicle, first flight and entry into service.

**One row per:** company of the index

**Depends on:** the published index

24 rows · 13 columns

| column | example | filled |
|---|---|---|
| `oem` | Ehang (NASDAQ: EH) | 100 % |
| `trend` | ↔︎ | 100 % |
| `ari` | 8.45 | 100 % |
| `funding_musd` | 262.0 | 100 % |
| `use_case` | Tourism,EMS,Firefighting,Air Taxi | 100 % |
| `vehicle_type` | Multicopter/ Lift + Cruise | 100 % |
| `propulsion` | Electric | 100 % |
| `operation` | Autonomous | 100 % |
| `vehicles` | EH216-S/F / VT-35 | 100 % |
| `first_flight` | 2018 / 2025 | 100 % |
| `eis` | 2025 / - | 100 % |
| `cert_regulator` | CAAC | 100 % |
| `country` | China | 100 % |

##### `aam_index_history.csv` (4.9 KB)

The score of each company at each published edition, from December 2020.

**One row per:** company of the index

**Depends on:** the published index

43 rows · 35 columns

| column | example | filled |
|---|---|---|
| `oem` | EHANG | 100 % |
| `December 2020` | 7.9 | 33 % |
| `February 2021` | 7.9 | 37 % |
| `May 2021` | 7.4 | 37 % |
| `June 2021` | 7.4 | 42 % |
| `July 2021` | 7.4 | 47 % |
| `August 2021` | 7.4 | 47 % |
| `October 2021` | 7.4 | 49 % |
| `December 2021` | 7.2 | 56 % |
| `February 2022` | 7.4 | 56 % |
| `March 2022` | 7.4 | 56 % |
| `April 2022` | 7.4 | 58 % |
| `June 2022` | 7.4 | 56 % |
| `August 2022` | 7.4 | 58 % |
| `October 2022` | 7.4 | 60 % |
| `December 2022` | 8.1 | 63 % |
| `February 2023` | 8.1 | 63 % |
| `April 2023` | 8.1 | 65 % |
| `June 2023` | 8.1 | 65 % |
| `August 2023` | 8.1 | 65 % |
| `November 2023` | 8.0 | 65 % |
| `December 2023` | 8.0 | 65 % |
| `March 2024` | 8.0 | 65 % |
| `April 2024` | 8.5 | 63 % |
| `June 2024` | 8.5 | 65 % |
| `August 2024` | 8.5 | 65 % |
| `October 2024` | 8.5 | 65 % |
| `December 2024` | 8.5 | 63 % |
| `February 2025` | 8.5 | 60 % |
| `April 2025` | 8.5 | 60 % |
| `June 2025` | 8.5 | 60 % |
| `October 2025` | 8.5 | 58 % |
| `December 2025` | 8.5 | 56 % |
| `February 2026` | 8.5 | 58 % |
| `May 2026` | 8.45 | 56 % |

#### `63_context_series/` (7 files, 11.4 KB)

Context series, one file each: `aviation_patent_baselines.csv` and `aviation_b64_by_priority_year.csv` (aviation patent families by year, for scale), `grant_status_by_priority_year.csv` and `grant_lag_summary.csv` (how many families are granted, pending or dead, and the time to grant), `funding_by_period.csv` and `market_forecasts.csv` (investment and forecasts of the sector), `sector_events.csv` (dated events). PatSeer series count families by earliest priority year, WIPO series by applicant origin and first filing year, so they are context and not to be added together. Use windows ending in 2023 at the latest, because 2024 to 2026 are incomplete. Depends on: PatSeer exports, WIPO statistics and public sources, as cited in each file.

#### `README.md` (3.1 KB)

The files of this folder, what they are and what one row means.

### `07_results/`

Results of the paper that are not plain tables of the dataset.

#### `07_results/71_label_reliability/`



##### `reliability_replicas.csv` (1.4 MB)

The value of every result in each of the 1 000 replicas, with the number of codes and designs changed in that replica.

**One row per:** replica

**Depends on:** file 42

1 000 rows · 225 columns

| column | example | filled |
|---|---|---|
| `replica` | 0 | 100 % |
| `codes changed` | 3335 | 100 % |
| `designs changed` | 596 | 100 % |
| `redraws` | 528 | 100 % |
| `designs redrawn` | 264 | 100 % |
| `designs kept after 20 redraws` | 0 | 100 % |
| `seconds` | 123.1 | 100 % |
| `designs analysed` | 619 | 100 % |
| `1 | top share | number of wings (winged designs)` | 0.59 | 100 % |
| `1 | varies (under 80 %) | number of wings (winged designs)` | True | 100 % |
| `1 | top share | tail type` | 0.26 | 100 % |
| `1 | varies (under 80 %) | tail type` | True | 100 % |
| `1 | top share | fuselage motion hover to cruise` | 0.73 | 100 % |
| `1 | varies (under 80 %) | fuselage motion hover to cruise` | True | 100 % |
| `1 | top share | wing configuration` | 0.72 | 100 % |
| `1 | varies (under 80 %) | wing configuration` | True | 100 % |
| `1 | top share | landing-gear type` | 0.58 | 100 % |
| `1 | varies (under 80 %) | landing-gear type` | True | 100 % |
| `1 | top share | left-right symmetry` | 0.8 | 100 % |
| `1 | varies (under 80 %) | left-right symmetry` | False | 100 % |
| `1 | top share | fuselage shape` | 0.57 | 100 % |
| `1 | varies (under 80 %) | fuselage shape` | True | 100 % |
| `1 | top share | booms present` | 0.54 | 100 % |
| `1 | varies (under 80 %) | booms present` | True | 100 % |
| `1 | top share | propulsor units per aircraft (band)` | 0.26 | 100 % |
| `1 | varies (under 80 %) | propulsor units per aircraft (band)` | True | 100 % |
| `1 | top share | places carrying propulsor units per aircraft` | 0.47 | 100 % |
| `1 | varies (under 80 %) | places carrying propulsor units per aircraft` | True | 100 % |
| `1 | top share | propulsor enclosure (any ducted)` | 0.53 | 100 % |
| `1 | varies (under 80 %) | propulsor enclosure (any ducted)` | True | 100 % |
| `1 | dimensions that vary (count)` | 10 | 100 % |
| `1 | dimensions read (count)` | 11 | 100 % |
| `1 | dimensions that vary, landing gear left out (count)` | 9 | 100 % |
| `1 | dimensions read, landing gear left out (count)` | 10 | 100 % |
| `1 | wing configuration fixed at 80 % (winged architectures)` | 0 | 100 % |
| `1 | wing configuration, winged architectures read` | 6 | 100 % |
| `2 | configurations | A` | 12 | 100 % |
| `2 | effective number 1D | A` | 8.1 | 100 % |
| `2 | effective number 2D | A` | 6.3 | 100 % |
| `2 | largest share | A` | 0.234 | 100 % |
| `2 | configurations | A·W·T` | 54 | 100 % |
| `2 | effective number 1D | A·W·T` | 24.3 | 100 % |
| `2 | effective number 2D | A·W·T` | 15.9 | 100 % |
| `2 | largest share | A·W·T` | 0.134 | 100 % |
| `2 | configurations | A·U` | 48 | 100 % |
| `2 | effective number 1D | A·U` | 31.5 | 100 % |
| `2 | effective number 2D | A·U` | 24.2 | 100 % |
| `2 | largest share | A·U` | 0.096 | 100 % |
| `3 | all designs | 1 share | A` | False | 100 % |
| `3 | all designs | 1 share | A·W·T` | False | 100 % |
| `3 | all designs | 1 share | A·U` | False | 100 % |
| `4 | all designs | 1 share | F` | False | 100 % |
| `3 | all designs | 2 balance | A` | False | 100 % |
| `3 | all designs | 2 balance | A·W·T` | False | 100 % |
| `3 | all designs | 2 balance | A·U` | False | 100 % |
| `4 | all designs | 2 balance | F` | True | 100 % |
| `3 | all designs | 3 disparity | A` | False | 100 % |
| `3 | all designs | 3 disparity | A·W·T` | False | 100 % |
| `3 | all designs | 3 disparity | A·U` | False | 100 % |
| `4 | all designs | 3 disparity | F` | False | 100 % |
| `3 | all designs | all three | A` | False | 100 % |
| `3 | all designs | all three | A·W·T` | False | 100 % |
| `3 | all designs | all three | A·U` | False | 100 % |
| `4 | all designs | all three | F` | False | 100 % |
| `3 | actively protected | 1 share | A` | False | 100 % |
| `3 | actively protected | 1 share | A·W·T` | False | 100 % |
| `3 | actively protected | 1 share | A·U` | False | 100 % |
| `4 | actively protected | 1 share | F` | False | 100 % |
| `3 | actively protected | 2 balance | A` | True | 100 % |
| `3 | actively protected | 2 balance | A·W·T` | False | 100 % |
| `3 | actively protected | 2 balance | A·U` | True | 100 % |
| `4 | actively protected | 2 balance | F` | True | 100 % |
| `3 | actively protected | 3 disparity | A` | False | 100 % |
| `3 | actively protected | 3 disparity | A·W·T` | False | 100 % |
| `3 | actively protected | 3 disparity | A·U` | False | 100 % |
| `4 | actively protected | 3 disparity | F` | False | 100 % |
| `3 | actively protected | all three | A` | False | 100 % |
| `3 | actively protected | all three | A·W·T` | False | 100 % |
| `3 | actively protected | all three | A·U` | False | 100 % |
| `4 | actively protected | all three | F` | False | 100 % |
| `3 | all designs | largest share | A` | 0.33299999999999996 | 100 % |
| `3 | all designs | 2D 2020-23 | A` | 5.19 | 100 % |
| `3 | all designs | 2D band low 2020-23 | A` | 5.18 | 100 % |
| `3 | all designs | dQ 2020-23 | A` | -0.0052 | 100 % |
| `3 | all designs | dQ band low 2020-23 | A` | -0.0187 | 100 % |
| `3 | all designs | largest share | A·W·T` | 0.265 | 100 % |
| `3 | all designs | 2D 2020-23 | A·W·T` | 11.42 | 100 % |
| `3 | all designs | 2D band low 2020-23 | A·W·T` | 10.8 | 100 % |
| `3 | all designs | dQ 2020-23 | A·W·T` | -0.0043 | 100 % |
| `3 | all designs | dQ band low 2020-23 | A·W·T` | -0.016 | 100 % |
| `3 | all designs | largest share | A·U` | 0.2 | 100 % |
| `3 | all designs | 2D 2020-23 | A·U` | 15.17 | 100 % |
| `3 | all designs | 2D band low 2020-23 | A·U` | 14.6 | 100 % |
| `3 | all designs | dQ 2020-23 | A·U` | -0.0043 | 100 % |
| `3 | all designs | dQ band low 2020-23 | A·U` | -0.0156 | 100 % |
| `4 | all designs | F share 2020` | 0.46399999999999997 | 100 % |
| `4 | all designs | F above 50 % in 2020` | False | 100 % |
| `4 | all designs | F share 2021` | 0.444 | 100 % |
| `4 | all designs | F above 50 % in 2021` | False | 100 % |
| `4 | all designs | largest share | F` | 0.46399999999999997 | 100 % |
| `4 | all designs | 2D 2020-23 | F` | 4.01 | 100 % |
| `4 | all designs | 2D band low 2020-23 | F` | 4.2 | 100 % |
| `4 | all designs | dQ 2020-23 | F` | -0.0052 | 100 % |
| `4 | all designs | dQ band low 2020-23 | F` | -0.0187 | 100 % |
| `3 | actively protected | largest share | A` | 0.373 | 100 % |
| `3 | actively protected | 2D 2020-23 | A` | 4.89 | 100 % |
| `3 | actively protected | 2D band low 2020-23 | A` | 4.96 | 100 % |
| `3 | actively protected | dQ 2020-23 | A` | -0.0128 | 100 % |
| `3 | actively protected | dQ band low 2020-23 | A` | -0.0191 | 100 % |
| `3 | actively protected | largest share | A·W·T` | 0.237 | 100 % |
| `3 | actively protected | 2D 2020-23 | A·W·T` | 10.86 | 100 % |
| `3 | actively protected | 2D band low 2020-23 | A·W·T` | 10.86 | 100 % |
| `3 | actively protected | dQ 2020-23 | A·W·T` | -0.0126 | 100 % |
| `3 | actively protected | dQ band low 2020-23 | A·W·T` | -0.0186 | 100 % |
| `3 | actively protected | largest share | A·U` | 0.185 | 100 % |
| `3 | actively protected | 2D 2020-23 | A·U` | 14.26 | 100 % |
| `3 | actively protected | 2D band low 2020-23 | A·U` | 14.47 | 100 % |
| `3 | actively protected | dQ 2020-23 | A·U` | -0.0126 | 100 % |
| `3 | actively protected | dQ band low 2020-23 | A·U` | -0.0171 | 100 % |
| `4 | actively protected | F share 2020` | 0.5 | 100 % |
| `4 | actively protected | F above 50 % in 2020` | False | 100 % |
| `4 | actively protected | F share 2021` | 0.491 | 100 % |
| `4 | actively protected | F above 50 % in 2021` | False | 100 % |
| `4 | actively protected | largest share | F` | 0.5 | 100 % |
| `4 | actively protected | 2D 2020-23 | F` | 3.77 | 100 % |
| `4 | actively protected | 2D band low 2020-23 | F` | 3.92 | 100 % |
| `4 | actively protected | dQ 2020-23 | F` | -0.0128 | 100 % |
| `4 | actively protected | dQ band low 2020-23 | F` | -0.0191 | 100 % |
| `8 | F share 2020-23 | North America` | 0.3896 | 100 % |
| `8 | F share 2020-23 | Europe` | 0.5079 | 100 % |
| `8 | F share 2020-23 | Asia-Pacific` | 0.4239 | 100 % |
| `8 | region x F 2020-23, p | all assignees` | 0.358 | 100 % |
| `8 | region x F 2020-23, p (Holm) | all assignees` | 1.0 | 100 % |
| `8 | regions differ 2020-23 (p < 0.05) | all assignees` | False | 100 % |
| `8 | region x F 2020-23, p | without the largest assignee` | 0.5146 | 100 % |
| `8 | region x F 2020-23, p (Holm) | without the largest assignee` | 1.0 | 100 % |
| `8 | regions differ 2020-23 (p < 0.05) | without the largest assignee` | False | 100 % |
| `8 | largest assignee left out` | Bell / Textron | 100 % |
| `5 | rho | SLC` | 0.414 | 100 % |
| `5 | p (Holm) | SLC` | 0.6662747812900587 | 100 % |
| `5 | rises (rho > 0, Holm p < 0.05) | SLC` | False | 100 % |
| `5 | falls (rho < 0, Holm p < 0.05) | SLC` | False | 100 % |
| `5 | rho 2016-23 | SLC` | 0.443 | 100 % |
| `5 | p 2016-23 (Holm) | SLC` | 1.0 | 100 % |
| `5 | rho | TP` | -0.78 | 100 % |
| `5 | p (Holm) | TP` | 0.002582961866219367 | 100 % |
| `5 | rises (rho > 0, Holm p < 0.05) | TP` | False | 100 % |
| `5 | falls (rho < 0, Holm p < 0.05) | TP` | True | 100 % |
| `5 | rho 2016-23 | TP` | -0.595 | 100 % |
| `5 | p 2016-23 (Holm) | TP` | 0.8367086429715481 | 100 % |
| `5 | rho | CVT` | 0.256 | 100 % |
| `5 | p (Holm) | CVT` | 1.0 | 100 % |
| `5 | rises (rho > 0, Holm p < 0.05) | CVT` | False | 100 % |
| `5 | falls (rho < 0, Holm p < 0.05) | CVT` | False | 100 % |
| `5 | rho 2016-23 | CVT` | 0.548 | 100 % |
| `5 | p 2016-23 (Holm) | CVT` | 0.9601538552333795 | 100 % |
| `5 | rho | TW` | -0.203 | 100 % |
| `5 | p (Holm) | TW` | 1.0 | 100 % |
| `5 | rises (rho > 0, Holm p < 0.05) | TW` | False | 100 % |
| `5 | falls (rho < 0, Holm p < 0.05) | TW` | False | 100 % |
| `5 | rho 2016-23 | TW` | -0.405 | 100 % |
| `5 | p 2016-23 (Holm) | TW` | 1.0 | 100 % |
| `5 | rho | MR` | 0.173 | 100 % |
| `5 | p (Holm) | MR` | 1.0 | 100 % |
| `5 | rises (rho > 0, Holm p < 0.05) | MR` | False | 100 % |
| `5 | falls (rho < 0, Holm p < 0.05) | MR` | False | 100 % |
| `5 | rho 2016-23 | MR` | -0.333 | 100 % |
| `5 | p 2016-23 (Holm) | MR` | 1.0 | 100 % |
| `5 | rho | TF` | 0.04 | 92 % |
| `5 | p (Holm) | TF` | 1.0 | 92 % |
| `5 | rises (rho > 0, Holm p < 0.05) | TF` | False | 92 % |
| `5 | falls (rho < 0, Holm p < 0.05) | TF` | False | 92 % |
| `5 | rho 2016-23 | TF` | -0.19 | 92 % |
| `5 | p 2016-23 (Holm) | TF` | 1.0 | 92 % |
| `5 | rho | PTC` | 0.477 | 78 % |
| `5 | p (Holm) | PTC` | 0.4335694040133097 | 78 % |
| `5 | rises (rho > 0, Holm p < 0.05) | PTC` | False | 78 % |
| `5 | falls (rho < 0, Holm p < 0.05) | PTC` | False | 78 % |
| `5 | rho 2016-23 | PTC` | 0.228 | 78 % |
| `5 | p 2016-23 (Holm) | PTC` | 1.0 | 78 % |
| `5 | architectures tested` | SLC,TP,CVT,TW,MR,TF,HB | 100 % |
| `6 | rho | propulsors on booms in CVT` | 0.21 | 100 % |
| `6 | p (Holm) | propulsors on booms in CVT` | 0.1177560480068088 | 100 % |
| `6 | significant (Holm p < 0.05) | propulsors on booms in CVT` | False | 100 % |
| `6 | sign | propulsors on booms in CVT` | 1 | 100 % |
| `6 | rho | ducted in CVT` | 0.02 | 100 % |
| `6 | p (Holm) | ducted in CVT` | 1.0 | 100 % |
| `6 | significant (Holm p < 0.05) | ducted in CVT` | False | 100 % |
| `6 | sign | ducted in CVT` | 1 | 100 % |
| `6 | rho | propulsors in TP` | 0.34 | 100 % |
| `6 | p (Holm) | propulsors in TP` | 0.00020309942825399202 | 100 % |
| `6 | significant (Holm p < 0.05) | propulsors in TP` | True | 100 % |
| `6 | sign | propulsors in TP` | 1 | 100 % |
| `6 | rho | propulsors in CVT` | 0.27 | 100 % |
| `6 | p (Holm) | propulsors in CVT` | 0.015963949372216645 | 100 % |
| `6 | significant (Holm p < 0.05) | propulsors in CVT` | True | 100 % |
| `6 | sign | propulsors in CVT` | 1 | 100 % |
| `7 | p | 2016-19` | 0.030917587267269835 | 100 % |
| `7 | p without the largest assignee | 2016-19` | 0.3004906687410112 | 100 % |
| `7 | differ (p < 0.05) | 2016-19` | True | 100 % |
| `7 | differ without the largest (p < 0.05) | 2016-19` | False | 100 % |
| `7 | largest returning assignee | 2016-19` | Bell / Textron | 100 % |
| `7 | p | 2020-23` | 0.016108528379850585 | 100 % |
| `7 | p without the largest assignee | 2020-23` | 0.053850561916975445 | 100 % |
| `7 | differ (p < 0.05) | 2020-23` | True | 100 % |
| `7 | differ without the largest (p < 0.05) | 2020-23` | False | 100 % |
| `7 | largest returning assignee | 2020-23` | Bell / Textron | 100 % |
| `5 | falls (rho < 0, Holm p < 0.05) | DS` | False | 0 % |
| `5 | falls (rho < 0, Holm p < 0.05) | HB` | False | 100 % |
| `5 | falls (rho < 0, Holm p < 0.05) | PFV` | False | 26 % |
| `5 | p (Holm) | DS` | 0.047955864351176485 | 0 % |
| `5 | p (Holm) | HB` | 1.0 | 100 % |
| `5 | p (Holm) | PFV` | 0.4436248290616862 | 26 % |
| `5 | p 2016-23 (Holm) | DS` | 1.0 | 0 % |
| `5 | p 2016-23 (Holm) | HB` | 0.9601538552333795 | 100 % |
| `5 | p 2016-23 (Holm) | PFV` | 1.0 | 26 % |
| `5 | rho 2016-23 | DS` | 0.024 | 0 % |
| `5 | rho 2016-23 | HB` | -0.524 | 100 % |
| `5 | rho 2016-23 | PFV` | 0.167 | 26 % |
| `5 | rho | DS` | 0.654 | 0 % |
| `5 | rho | HB` | 0.145 | 100 % |
| `5 | rho | PFV` | 0.474 | 26 % |
| `5 | rises (rho > 0, Holm p < 0.05) | DS` | True | 0 % |
| `5 | rises (rho > 0, Holm p < 0.05) | HB` | False | 100 % |
| `5 | rises (rho > 0, Holm p < 0.05) | PFV` | False | 26 % |

##### `reliability_summary.csv` (23.5 KB)

For each result of the analysis: its original value and how it behaves when a share of the coded values is replaced by random errors (1 000 replicas): median, 5th and 95th percentile, share of replicas where it changes or holds, with Wilson 95 % intervals.

**One row per:** result of the analysis

**Depends on:** files 41, 42, 45

200 rows · 17 columns

| column | example | filled |
|---|---|---|
| `result` | 0 | 100 % |
| `key` | designs analysed | 100 % |
| `original value` | 619 | 100 % |
| `replicas` | 1000 | 100 % |
| `replicas where it is computed` | 1000 | 100 % |
| `kind` | number | 100 % |
| `median` | 619.0 | 62 % |
| `5th percentile` | 619.0 | 62 % |
| `95th percentile` | 619.0 | 62 % |
| `share of replicas where it changes` | 0.0 | 38 % |
| `share of replicas where it holds` | 1.0 | 36 % |
| `holds, Wilson 95 % low` | 0.9961732414543059 | 36 % |
| `holds, Wilson 95 % high` | 1.0 | 36 % |
| `share of replicas with the original verdict` | 1.0 | 36 % |
| `original verdict, Wilson 95 % low` | 0.9961732414543059 | 36 % |
| `original verdict, Wilson 95 % high` | 1.0 | 36 % |
| `share of replicas with the original value` | 1.0 | 2 % |

#### `72_weight_sensitivity/` (11 files, 2.6 MB)

Sensitivity of the dominant-design test to the weights of its third condition: the 1 000 weight draws (`weight_draws_1000.csv`), test 1 (`test1_*`, with its figure) and test 2 (`test2_*`). Each summary table states the number of designs used. Depends on: files 42 and 45.

#### `README.md` (952 B)

The files of this folder, what they are and what one row means.

### `README.md` (13.6 KB)

The dataset overview: one table per folder with what each file is, what one row means and what it depends on.

### `codebook/`

The dictionary of columns.

#### `README.md` (498 B)

The files of this folder, what they are and what one row means.

#### `data_dictionary.csv` (87.2 KB)

Every column of the main tables (files 02, 03, 04 and index.csv): the file it belongs to, the wizard section, the type, the values found (for categories), how many rows are filled and, when written, a description.

**One row per:** column of a file

**Depends on:** all tables above

809 rows · 7 columns

| column | example | filled |
|---|---|---|
| `file` | 02_gold_standard/21_census_candidates.csv | 100 % |
| `column` | list | 100 % |
| `section` | derived | 55 % |
| `kind` | category | 100 % |
| `options` | aam_index / aam_index_left_out / aam_index_map / | 63 % |
| `non_empty` | 419 | 100 % |
| `description` | user ruling 2026-09-30 (review_decisions/POWERTR | 1 % |

#### `trl_scale.csv` (3.2 KB)

The nine technology readiness levels with their definitions and the rule used to place an eVTOL on each.

**One row per:** level

9 rows · 4 columns

| column | example | filled |
|---|---|---|
| `trl` | 1 | 100 % |
| `nasa_definition` | Basic principles observed and reported. | 100 % |
| `nasa_hardware_description` | Scientific knowledge generated underpinning hard | 100 % |
| `evtol_evidence_rule` | Not used: a patented aircraft is already past ba | 100 % |

### `index.csv` (5.0 MB)

Links only: patent, aircraft, figure and the image files (raw page, crop, approved image), plus the filter steps that led to each crop. The figure labels are in 04_aircraft/41_figures.csv.

**One row per:** cropped figure (or page, when there was no crop)

**Depends on:** 05_images, 03_patents, 04_aircraft

16 816 rows · 20 columns

| column | example | filled |
|---|---|---|
| `patent_id` | AT503689A1 | 100 % |
| `aircraft_id` | AT503689A1_ad1 | 35 % |
| `fig_key` | 2 | 34 % |
| `source` | epo_ops_download | 100 % |
| `record_dir` | AT503689A1_38777771 | 99 % |
| `raw_file` | AT503689A1_fig_01.png | 99 % |
| `raw_path` | 05_images/raw_pages/AT503689A1_38777771/AT503689 | 99 % |
| `fig_number` | 2 | 52 % |
| `siglip_pred` | drawing | 99 % |
| `siglip_score_drawing` | 0.5229 | 99 % |
| `siglip_score_table` | 0.4771 | 99 % |
| `keep_siglip` | True | 99 % |
| `crop_file` | AT503689A1_fig_01_crop_0_F2.png | 73 % |
| `crop_path` | 05_images/crops/Batch_02/AT503689A1_38777771/AT5 | 73 % |
| `crop_label` | 2 | 56 % |
| `crop_method` | doclayout_easyocr | 73 % |
| `crop_match_status` | unmatched | 73 % |
| `crop_quality` | merged | 26 % |
| `duplicate_group` | 3 | 0 % |
| `approved_path` | 05_images/approved/AT503689A1_ad1/AT503689A1_fig | 11 % |
