from fastapi import APIRouter, Path, HTTPException, status, Body

from gamestore.models import Game, CreateGame

router = APIRouter(
    tags=['game']
)

gow = Game(
    id=1,
    title='God of War',
    platform='PS4',
    price=19.99,
    release_year=2018
)

db = {
    gow.id: gow
}

@router.post(
    path='/game',
    response_model=Game
)
def create_game(game: CreateGame = Body()):
    game = Game(
        **game.model_dump(),
        id=max(db.keys()) + 1
    )
    db[game.id] = game
    return game


@router.get(
    path='/game/{game_id}',
    response_model=Game
)
def read_game(game_id: int = Path()):
    g = db.get(game_id)
    if g is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Game with id {game_id} does not exist'
        )
    return g


