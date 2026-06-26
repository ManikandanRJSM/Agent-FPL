from pydantic import BaseModel

class ManagerModel(BaseModel):
    manager_id : int
    transfer_balance : float

class PlayerModel(BaseModel):
    assists: int
    bonus: int
    can_select: bool
    can_transact: bool
    chance_of_playing_next_round: int | None
    chance_of_playing_this_round: int | None
    clean_sheets: int
    clean_sheets_per_90: float
    clearances_blocks_interceptions: int
    cost_change_event: int
    cost_change_event_fall: int
    cost_change_start: int
    cost_change_start_fall: int
    defensive_contribution: int
    defensive_contribution_per_90: float
    event_points: int
    expected_assists: str
    expected_assists_per_90: float
    expected_goal_involvements: str
    expected_goal_involvements_per_90: float
    expected_goals: str
    expected_goals_conceded: str
    expected_goals_conceded_per_90: float
    expected_goals_per_90: float
    first_name: str
    form: str
    goals_conceded: int
    goals_conceded_per_90: float
    goals_scored: int
    id: int
    in_dreamteam: bool
    minutes: int
    now_cost: int
    now_cost_rank: int
    own_goals: int
    penalties_missed: int
    penalties_saved: int
    points_per_game: str
    price_change_percent: str
    recoveries: int
    red_cards: int
    saves: int
    saves_per_90: float
    second_name: str
    selected_by_percent: str
    selected_rank: int
    starts: int
    starts_per_90: float
    status: str
    tackles: int
    threat: str
    total_points: int
    transfers_in: int
    transfers_in_event: int
    transfers_out: int
    transfers_out_event: int
    value_form: str
    value_season: str
    yellow_cards: int
    is_captain: bool
    is_vice_captain: bool
    purchase_price: int
    code: int
    name: str
    short_name: str