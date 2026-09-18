from player_class import player
import json
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class Player(BaseModel):
#     id: int = Field(gt=0)
#     username: str = Field(min_length=1)
#     score: int = Field(ge=0)

class PlayerCreate(BaseModel):
    username: str = Field(min_length=1)
    score: int = Field(ge=0)

class Score(BaseModel):
    score: int = Field(gt=0)

class PlayerEdit(BaseModel):
    username: str = Field(min_length=1)
    score: int = Field(ge=0)

class PlayerDelete(BaseModel):
    id: int = Field(ge=0)

menu = {}
players = json.load(open("players.json", "r"))["players"]

menu["1"] = "Add Player"
menu["2"] = "Delete Player"
menu["3"] = "Customize Player"
menu["4"] = "Find Player"
menu["5"] = "Show Leaderboard"
menu["6"] = "Exit"


@app.get("/players")
def get_players():
    with open("players.json", "r") as file:
        data = json.load(file)

        return data["players"]


@app.get("/players/{id}")
def get_player(id: str):
    with open("players.json", "r") as file:
        data = json.load(file)

    for player in data["players"]:
        if player["id"] == int(id):
            return player

    raise HTTPException(status_code=404, detail="Player not found")


@app.get("/leaderboard")
def get_leaderboard():
    with open("players.json", "r") as file:
        data = json.load(file)

    sorted_players = sorted(
        data["players"], key=lambda p: int(p["score"]), reverse=True
    )

    return sorted_players

@app.post("/players/add")
def post_player(added_player: PlayerCreate):
    player_id = 1

    for player in players:
        if player["id"] >= player_id:
            player_id = player["id"] + 1

    new_player = {
        "id": player_id,
        "username": added_player.username,
        "score": added_player.score
    }

    with open("players.json", "r+") as file:
        data = json.load(file)
        data["players"].append(new_player)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    players.append(new_player)

    return new_player

@app.patch("/players/edit/{id}")
def edit_player(id: int, edited_player: PlayerEdit):
    for player in players:
        if player["id"] == id:
            player["username"] = edited_player.username
            player["score"] = edited_player.score

            with open("players.json", "w") as file:
                json.dump({"players": players}, file, indent=4)

            return player

    raise HTTPException(status_code=404, detail="Player not found")

@app.patch("/players/{id}/score")
def add_score(id: int, score_data: Score):
    for player in players:
        if player["id"] == id:
            player["score"] += score_data.score

            with open("players.json", "w") as file:
                json.dump({"players": players}, file, indent=4)

            return player

    raise HTTPException(status_code=404, detail="Player not found")

@app.delete("/players/delete")
def delete_player(id: int):
    for player in players:
        if player['id'] == id:
            players.remove(player)

            with open("players.json", "w") as file:
                json.dump({"players": players}, file, indent=4)

            return f"Player with id {id} deleted"
        
    return f"No player with id {id} found"

def add_player():
    while True:
        player_id = 1

        for player in players:
            if player["id"] >= player_id:
                player_id = player["id"] + 1

        print(player_id)

        username = input("Enter player username: ")
        score = int(input("Enter player score: "))

        new_player = {"id": player_id, "username": username, "score": score}

        with open("players.json", "r+") as file:
            data = json.load(file)
            data["players"].append(new_player)

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

        players.append(new_player)

        print(
            f"Player {new_player['username']} "
            f"added with id {new_player['id']} "
            f"and score {new_player['score']}"
        )

        again = input("Do you want to add another player? (y/n): ").strip().lower()

        if again != "y":
            break


def delete_player():
    id = int(input("Enter player id to delete: "))

    for player in players:
        if player["id"] == id:
            players.remove(player)

            with open("players.json", "w") as file:
                json.dump({"players": players}, file, indent=4)

            print(f"Player with id {id} deleted")
            return

    print(f"No player with id {id} found")


def customize_player():
    id = int(input("Enter player id to customize: "))

    for player in players:
        if player["id"] == id:
            player["username"] = input("Enter new player username: ")
            player["score"] = int(input("Enter new player score: "))

            with open("players.json", "w") as file:
                json.dump({"players": players}, file, indent=4)

            print(
                f"Player with id {id} customized to "
                f"username {player['username']} "
                f"and score {player['score']}"
            )
            return

    print(f"No player with id {id} found")


def find_player():
    id = int(input("Enter player id to find: "))
    for player in players:
        if player["id"] == id:
            print(id)
            selected_player = player
    if selected_player is None:
        print(f"No player with id {id} found")
    else:
        print(
            f"Player {selected_player['username']} has id {selected_player['id']} and score {selected_player['score']}"
        )


def show_leaderboard():
    players.sort(key=lambda p: int(p["score"]), reverse=True)

    print("Leaderboard:")

    for i, player in enumerate(players, start=1):
        print(f"{i}. {player['username']} - {player['score']}")


if __name__ == "__main__":
    while True:
        options = sorted(menu.keys())

        for entry in options:
            print(entry, menu[entry])
        selection = input("Please select: ")
        if selection == "1":
            add_player()
        elif selection == "2":
            delete_player()
        elif selection == "3":
            customize_player()
        elif selection == "4":
            find_player()
        elif selection == "5":
            show_leaderboard()
        elif selection == "6":
            break
        else:
            print("Unknown option selected")
