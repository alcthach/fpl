/* 
FPL Initial Config
alext - alcthach@gmail.com 
2022-07-28
*/

-- NOTE: This config will likely need to be modified, rank data should be varchar
-- not int type


-- Bootstrap-static.events

CREATE TABLE IF NOT EXISTS events (
	id				varchar(3) NOT NULL,
	name				varchar(11) NOT NULL,
	deadline_time			timestamp NOT NULL,
	average_entry_score		int NOT NULL, 
	finished			bool NOT NULL,
	data_checked			bool NOT NULL, 
	highest_scoring_entry		varchar(128),           
 	deadline_time_epoch 		varchar(16) NOT NULL,
	deadline_time_game_offset	int NOT NULL,
	highest_score			int,
	is_previous			bool NOT NULL,
	is_current			bool NOT NULL, 
	is_next				bool NOT NULL,
	cup_leagues_created		bool NOT NULL, 	
	h2h_ko_matches_created		bool NOT NULL, 
	chip_plays			varchar(256) NOT NULL,
	most_selected			varchar(3),
	most_transferred_in		varchar(3),
	top_element			varchar(3),
	top_element_info		varchar(128),
	transfers_made			varchar(3),
	most_captained			varchar(3),
	most_vice_captained		varchar(3)
);


-- Bootstrap.game_settings

CREATE TABLE IF NOT EXISTS game_settings (
	league_join_private_max			int NOT NULL,
	league_join_public_max			int NOT NULL,
	league_max_size_public_classic		int NOT NULL,
	league_max_size_public_h2h		int NOT NULL,
	league_max_size_private_h2h		int NOT NULL,
	league_max_ko_rounds_private_h2h	int NOT NULL,
	league_prefix_public			varchar(8) NOT NULL,
	league_points_h2h_win			int NOT NULL,
	league_points_h2h_lose			int NOT NULL,
	league_points_h2h_draw			int NOT NULL,
	league_ko_first_instead_of_random	bool NOT NULL,
	cup_start_event_id			varchar(8),
	cup_stop_event_id			varchar(8),
	cup_qualifying_method			varchar(8),
	cup_type				varchar(8),
	squad_squadplay				int NOT NULL,
	squad_squadsize				int NOT NULL,
	squad_team_limit			int NOT NULL,
	squad_total_spend			int NOT NULL,
	ui_currency_multiplier			int NOT NULL,
	ui_use_special_shirts			bool NOT NULL,
	ui_special_shirt_exclusions		varchar(8),
	stats_form_days				int NOT NULL,
	sys_vice_captain_enabled		bool NOT NULL,
	transfers_cap				int NOT NULL,
	transfers_sell_on_fee			float NOT NULL,
	league_h2h_tiebreak_stats		varchar(128) NOT NULL,
	timezone				varchar(8)
);


-- Bootstrap.phases

CREATE TABLE IF NOT EXISTS phases (
	id		varchar(2) NOT NULL,
	name		varchar(16) NOT NULL,
	start_event	varchar(2) NOT NULL,
	stop_event	varchar(2) NOT NULL
);


-- Bootstrap-static.teams

CREATE TABLE IF NOT EXISTS teams (
	code			int NOT NULL,			
	draw			int NOT NULL,
	form			varchar(16),
	id			int NOT NULL,
	loss			int NOT NULL,
	name			varchar(16),
	played			int NOT NULL,
	points			int NOT NULL,
	position		int NOT NULL,
	short_name		varchar(3),
	strength		int NOT NULL,
	team_division		varchar(16),
	unavailable		varchar(16),
	win			int,
	strength_overall_home	int NOT NULL,
	strength_overall_away	int NOT NULL,
	strength_attack_home	int NOT NULL,
	strength_attack_away	int NOT NULL,
	strength_defence_home	int NOT NULL,
	strength_defence_away	int NOT NULL,
	pulse_id		int NOT NULL
);


-- Bootstrap.total_players

CREATE TABLE IF NOT EXISTS total_players (
	total_players	int NOT NULL
);


-- Bootstrap.elements

CREATE TABLE IF NOT EXISTS elements (
	chance_of_playing_next_round		varchar(8),
	chance_of_playing_this_round		varchar(8),
	code					varchar(16),
	cost_change_event			int,
	cost_change_event_fall			int,
	cost_change_start			int,
	cost_change_start_fall			int,
	dreamteam_count				int,
	element_type				varchar(1),
	ep_next					float NOT NULL,
	ep_this					float,
	event_points				float,
	first_name				varchar(64) NOT NULL,
	form					float,
	id					varchar(3) NOT NULL,
	in_dreamteam				bool NOT NULL,
	news					varchar(256),
	news_added				varchar(128), -- TODO tentative
	now_cost				int NOT NULL,
	photo					varchar(16),
	points_per_game				float,
	second_name				varchar(64),
	selected_by_percent			float,
	special					bool NOT NULL,
	squad_number				varchar(16),
	status					varchar(8),
	team					int NOT NULL,
	team_code				int NOT NULL,
	total_points				int,
	transfers_in				int,
	transfers_in_event			int,
	transfers_out				int,
	transfers_out_event			int,
	value_form				float,
	value_season				float,
	web_name				varchar(16) NOT NULL,
	minutes					int,
	goals_scored				int,
	assists					int,
	clean_sheets				int,
	goals_conceded				int,
	own_goals				int,
	penalties_saved				int,
	penalties_missed			int,
	yellow_cards				int,
	red_cards				int,
	saves					int,
	bonus					int,
	bps					int,
	influence				float,
	creativity				float,
	threat					float,
	ict_index				float,
	influence_rank				int,
	influence_rank_type			int,
	creativity_rank				int,
	creativity_rank_type			int,
	threat_rank				int,
	threat_rank_type			int,
	ict_index_rank				int,
	ict_index_rank_type			int,
	corners_and_indirect_freekicks_order	int,
	corners_and_indirect_freekicks_text	varchar(8),
	direct_freekicks_order			varchar(4),
	direct_freekicks_text			varchar(4),
	penalties_order				varchar(2),
	penalties_text				varchar(8)
);



-- Bootstrap.elements_stats

CREATE TABLE IF NOT EXISTS element_stats(
	label	varchar(32) NOT NULL,
	name	varchar(32) NOT NULL
);


-- Bootstrap-static.element_types

CREATE TABLE IF NOT EXISTS element_types (
	id			varchar(3) NOT NULL,
	plural_name		varchar(16), -- Might need to open this up later
	plural_name_short	varchar(3) NOT NULL,
	singular_name		varchar(16) NOT NULL, 
	singular_name_short	varchar(3) NOT NULL,
	squad_select		varchar(4) NOT NULL,
	squad_min_play		varchar(4) NOT NULL,
	squad_max_play		varchar(4) NOT NULL,
	ui_shirt_specific	bool NOT NULL,
	sub_positions_locked	varchar(8), -- Is a list, TODO deal with this later
	element_count		int NOT NULL
);

-- Snapshot pulls

CREATE TABLE IF NOT EXISTS transfers_half_hour_snapshot
	(
	id			varchar(3),
	transfers_in		int,
	transfers_in_events 	int,
	transfers_out		int,
	transfers_out_events    int,
	timestamp		timestamp
);

CREATE TABLE IF NOT EXISTS player_cost_daily_snapshot
	(
	id 		varchar(3),
	player_cost	int NOT NULL,
	timestamp	timestamp
);

CREATE TABLE IF NOT EXISTS selected_by_percent_daily_snapshot
	(
	id			varchar(3),
	selected_by_percent	float NOT NULL,
	timestamp		timestamp
);
