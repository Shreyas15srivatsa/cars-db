# from _typeshed import Self
from enum import Enum
# import datetime
import search_listings
import add_listing
import update_listing
import remove_listing
import seller
import stats
import entity as ent
from db import DB

database = DB()

# TODO_NEW:
class DBAction(Enum):
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4
    STATS = 5
    SELLER = 6
    EXIT = 7

# Update this if you want to add more functionalities
# <option number> : (<Prompt message>, <Entity>, <Type of action>)
# TODO_NEW:
functionalities = {
    "1": ("Create a new listing for a car", ent.ListingInfo, DBAction.CREATE),
    "2": ("Search for car listings", ent.ListingInfo, DBAction.READ),
    "3": ("Modify an existing listing for a car", ent.ListingInfo, DBAction.UPDATE),
    "4": ("Delete an existing listing for a car", ent.ListingInfo, DBAction.DELETE),
    "5": ("View Stats", None, DBAction.STATS),
    "6": ("Seller Info", ent.SellerInfo, DBAction.SELLER),
    "7": ("Exit Program", None, DBAction.EXIT),
}

def isValidInput(key: str, value: str, e: ent.Entity) -> bool:
    val_type = e.parameters[key][1]
    try:
        val_type(value)
        return True
    except (ValueError, TypeError):
        print(f"ERROR: Input must be of type: {val_type.__name__}. Try again.")
        return False


def intakeRequiredParametersfromCLI(entity_cls: ent.Entity) -> ent.Entity:
    keys = [k for k, v in entity_cls.parameters.items() if v[0]]
    e = entity_cls()

    print("Input REQUIRED parameters:")
    i = 0
    while i < len(keys):
        k = keys[i]
        v = input(f"Value for {k}: ")
        if not v:
            print("ERROR: Required parameter cannot be empty. Try again.")
            continue
        if not isValidInput(k, v, e):
            continue
        e.setAttribute(k, v)
        i += 1
    return e


def intakeOptionalParametersfromCLI(e: ent.Entity) -> ent.Entity:
    keys = [k for k, v in e.parameters.items() if not v[0]]

    print("Input OPTIONAL parameters: (Press ENTER to continue, OR press q + ENTER to skip)")
    if input() == "q":
        return e

    i = 0
    while i < len(keys):
        k = keys[i]
        v = input(f"Value for {k}: ")
        if not isValidInput(k, v, e):
            continue
        e.setAttribute(k, v)
        i += 1
    return e

class CliState():
    pass

while True:

    prompt_msg = "\n".join([f"{k}: {v[0]}" for k, v in functionalities.items()])
    opt_num = input(f"\nSelect the number corresponding to your choice:\n{prompt_msg}\n\n")

    if opt_num not in functionalities.keys():
        print("ERROR: Invalid option. Try again.")
        continue

    functionality = functionalities[opt_num]
    entity = functionality[1]

    # branch off UI based on option selected
    if int(opt_num) == DBAction.READ.value:
        search_listings.loop(database)
    elif int(opt_num) == DBAction.CREATE.value:
        add_listing.loop(database)
    elif int(opt_num) == DBAction.UPDATE.value:
        update_listing.loop(database)
    elif int(opt_num) == DBAction.DELETE.value:
        remove_listing.loop(database)
    elif int(opt_num) == DBAction.STATS.value:
        stats.loop(database)
    elif int(opt_num) == DBAction.SELLER.value:
        seller.loop(database)
    else:  # exit
        database.cursor.close()
        database.cnx.close()
        raise SystemExit("\nProgram exited by user. Goodbye!")
