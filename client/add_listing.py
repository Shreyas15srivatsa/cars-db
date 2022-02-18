from enum import Enum
import entity as ent
from db import DB


class DBAction(Enum):
    SearchByCategory = 1
    SearchByKeyword = 2
    ReturnToHomeScreen = 4
    ExitProgram = 5


functionalities = {
    "1": ("Search by category", ent.ListingInfo, DBAction.SearchByCategory),
    "2": ("Search by keyword", ent.ListingInfo, DBAction.SearchByKeyword),
    "3": ("Return to Home Screen", ent.ListingInfo, DBAction.ReturnToHomeScreen),
    "4": ("Exit Program", None, DBAction.ExitProgram),
}


def isValidInput(db: DB, key: str, value: str, e: ent.Entity) -> bool:
    if key.lower() == "vin":
        return isValidVIN(db, value)

    if key.lower() == "make_name":
        return isValidMakeName(db, value)

    val_type = e.creation_parameters[key][1]
    try:
        val_type(value)
        return True
    except (ValueError, TypeError):
        print(f"ERROR: Input must be of type: {val_type.__name__}. Try again.")
        return False


def intakeRequiredParametersfromCLI(db: DB, entity_cls: ent.Entity) -> ent.Entity:
    keys = [k for k, v in entity_cls.creation_parameters.items() if v[0]]
    vals = [v for v in entity_cls.creation_parameters.values() if v[0]]
    e = entity_cls()

    print("Input REQUIRED parameters:")
    i = 0
    while i < len(keys):
        k = keys[i]
        val = vals[i]
        v = input(f"Value for {k}: ")
        if not v:
            print("ERROR: Required parameter cannot be empty. Try again.")
            continue
        if not isValidInput(db, k, v, e):
            continue
        e.setAttribute(k, (v, val[1]))
        i += 1
    return e


# def intakeOptionalParametersfromCLI(db: DB, e: ent.Entity) -> ent.Entity:
#     keys = [k for k, v in e.creation_parameters.items() if not v[0]]
#     vals = [v for v in e.creation_parameters.values() if not v[0]]

#     print(
#         "Input OPTIONAL parameters: (Press ENTER to continue, OR press q + ENTER to skip)"
#     )
#     if input() == "q":
#         return e

#     i = 0
#     while i < len(keys):
#         k = keys[i]
#         val = vals[i]
#         v = input(f"Value for {k}: ")
#         if not isValidInput(db, k, v, e):
#             continue
#         e.setAttribute(k, (v, val[1]))
#         i += 1
#     return e

def intakeOptionalParametersfromCLI(db: DB, e: ent.Entity) -> ent.Entity:
    keys = [k for k, v in e.creation_parameters.items() if not v[0]]
    vals = [v for v in e.creation_parameters.values() if not v[0]]

    print(
        "\nInput optional parameters: (press Enter to continue or press (q + Enter) to skip this menu entirely.)"
    )
    print("NOTE: Press Enter to skip attributes.")
    if input() == "q":
        return e

    i = 0
    while i < len(keys):
        key = keys[i]
        val = vals[i]
        v = input(f"{key}: ")
        if not v:
            i += 1
            continue
        elif not isValidInput(db, key, v, e):
            continue
        e.setAttribute(key, (v, val[1]))
        i += 1
    return e




def isValidVIN(db: DB, vin: str) -> bool:
    if not (len(vin) == 17):
        print("ERROR: vin must be 17 characters in length. Try again")
        return False

    validation_query = f"""SELECT COUNT(*) FROM ListingInfo WHERE vin=UPPER("{vin}")"""
    db.cursor.execute(validation_query)

    res = db.cursor.fetchall()
    if not int(res[0][0]):
        return True
    else:
        print("ERROR: A listing exists with the same vin. Try again")
        return False


def isValidMakeName(db: DB, make_name: str) -> bool:
    sql = f"""SELECT make_id FROM MakeInfo WHERE make_name = '{make_name}';"""
    db.cursor.execute(sql)
    res = db.cursor.fetchall()
    if len(res) > 0:
        db.make_id = int(res[0][0])
        return True
    else:
        print("ERROR: Manufacturer doesn't exist. Try again")
        return False

def confirm(entity_obj: ent.Entity) -> bool:
    yesNo = input(f"\n{toString(entity_obj)}\nConfirm? [y/N]: ")
    return True if yesNo.lower() == "y" else False

def toString(entity_obj: ent.Entity) -> str:
    res = "++++++++++++++++++++++++++++++++++++++++++++\n"
    for k, v in entity_obj.data.items():
        res += f"{k}: {v[0]}\n"
    res += "++++++++++++++++++++++++++++++++++++++++++++\n"
    return res

def loop(db: DB) -> None:

    # ask for inputs for required creation paramters
    entity = ent.ListingInfo
    e = intakeRequiredParametersfromCLI(db, entity)
    e = intakeOptionalParametersfromCLI(db, e)
    if confirm(e):
        db.create_listing(e.data)
    else:
        print("\nOperation cancelled by user.")
