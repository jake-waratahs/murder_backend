# CSESoc Murder Backend

This is the API server and database for CSESoc murder. It's a flask application that just returns JSON data to the frontend.

Murder is a game where each player is assigned a target, and a codeword. A player has to find their target IRL and get their codeword. Once the player has their target's codeword, they move on to their target's target, and so forth, until one player remains.

The aim of the game is to meet new people and make friends. It's not violent. We're lovers not fighters.

## Database Schema
The database schema is as follows:

### `games`

|  **Name**  | **Type** | **Relation** |
|------------|----------|--------------|
|`id`        |Integer   |              |
|`start_date`|Time      |              |
|`end_date`  |Time      |              |
|`winner`    |Integer   |Players ID    |

### `players`

|  **Name** | **Type** | **Relation** |
|-----------|----------|--------------|
|`id`       |Integer   |              |
|`zid`      |String    |UNSW zID      |
|`full_name`|String    |              |
|`admin`    |Boolean   |              |

### `players_games`

|  **Name** | **Type** | **Relation** |
|-----------|----------|--------------|
|`player_id`|Integer   |Players ID    |
|`game_id`  |Integer   |Games ID      |
|`alive`    |Boolean   |              |
|`target`   |Integer   |Players ID    |
|`codeword` |String    |              |

### `kills`
|  **Name** | **Type** | **Relation** |
|-----------|----------|--------------|
|`game_id`  |Integer   |Games ID      |
|`killer_id`|Integer   |Players ID    |
|`killed_id`|Integer   |Players ID    |
|`time`     |Time      |              |

## API Spec

\_healthcheck
\me
\kill
\kills
\game
\play
\register
\login

## Developing

## Deploying
