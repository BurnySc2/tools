from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Stats(BaseModel):
    rating: int | None = None
    games_played: int | None = Field(..., alias="gamesPlayed")
    rank: int | None = None


class Partition(Enum):
    GLOBAL = "GLOBAL"


class Account(BaseModel):
    battle_tag: str = Field(..., alias="battleTag")
    id: int
    partition: Partition
    hidden: None


class Region(Enum):
    EU = "EU"
    KR = "KR"
    US = "US"


class Character(BaseModel):
    realm: int
    name: str
    id: int
    account_id: int = Field(..., alias="accountId")
    region: Region
    battlenet_id: int = Field(..., alias="battlenetId")


class Clan(BaseModel):
    tag: str
    id: int
    region: Region
    name: str | None
    members: int | None
    active_members: int | None = Field(..., alias="activeMembers")
    avg_rating: int | None = Field(..., alias="avgRating")
    avg_league_type: int | None = Field(..., alias="avgLeagueType")
    games: int | None


class Members(BaseModel):
    character: Character
    account: Account
    zerg_games_played: int = Field(0, alias="zergGamesPlayed")
    terran_games_played: int = Field(0, alias="terranGamesPlayed")
    clan: Clan | None = None
    protoss_games_played: int = Field(0, alias="protossGamesPlayed")
    random_games_played: int = Field(0, alias="randomGamesPlayed")


class PlayerData(BaseModel):
    league_max: int = Field(..., alias="leagueMax")
    rating_max: int = Field(..., alias="ratingMax")
    total_games_played: int = Field(..., alias="totalGamesPlayed")
    previous_stats: Stats = Field(..., alias="previousStats")
    current_stats: Stats = Field(..., alias="currentStats")
    members: Members
