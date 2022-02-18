from enum import Enum
import entity as ent
from db import DB

class DBAction(Enum):
    UpdateInfo = 1
    ViewInfo = 2
    ReturnToHomeScreen = 3
    ExitProgram = 4


functionalities = {
    "1": ("Update Seller Info", ent.SellerInfo, DBAction.UpdateInfo),
    "2": ("View Seller Info", ent.SellerInfo, DBAction.ViewInfo),
    "3": ("Return to Home Screen", None, DBAction.ReturnToHomeScreen),
    "4": ("Exit Program", None, DBAction.ExitProgram),
}

def isValidInput(db: DB, key: str, value: str, e: ent.Entity) -> bool:
    if key.lower() == "sp_id":
        return isValidSpId(db, value)

    val_type = e.update_parameters[key][1]
    try:
        val_type(value)
        return True
    except (ValueError, TypeError):
        print(f"ERROR: Input must be of type: {val_type.__name__}. Try again.")
        return False


def isValidSpId(db: DB, value: str) -> bool:

    validation_query = (
        f"""SELECT COUNT(*) FROM SellerInfo WHERE sp_id=UPPER("{value}")"""
    )
    db.cursor.execute(validation_query)

    res = db.cursor.fetchall()
    if int(res[0][0]):
        return True
    else:
        print("ERROR: Seller ID does not exist. Try again")
        return False

def intakeParametersfromCLI(db: DB, e: ent.Entity) -> ent.Entity:
    keys = [k for k in e.update_parameters.keys()]
    values = [v for v in e.update_parameters.values()]

    print(
        "\nChoose what to change: (press Enter to continue)"
    )
    print("NOTE: Press Enter to skip attributes.")

    i = 0
    range_val_seen = False
    while i < len(keys):
        key = keys[i]
        val = values[i]
        v = input(f"{key}: ")
        if not v:
            if range_val_seen:
                print("ERROR: Must choose end of range\n")
                continue
            i += 1
            continue
        elif not isValidInput(db, key, v, e):
            continue
        e.setAttribute(key, v)
        i += 1
        if val[0] == 1:
            range_val_seen = True
        else:
            range_val_seen = False
    return e


def confirm(entity_obj: ent.Entity) -> bool:
    yesNo = input(f"\n{entity_obj.toString()}\nConfirm? [y/N]: ")
    return True if yesNo.lower() == "y" else False

def printRecords(records: list) -> None:
    print("\nResult:\n")
    for i, r in enumerate(records):
        print(i, r)
        if i == 0:
            print("------------------------------------------------------------")
    print(f"\nShowing all {len(records)-1} records.\n")

def loop(db: DB):

    while True:
        print("\nEnter the seller id: ")
        sp_id = input("sp_id: ")

        # ask for inputs for required creation paramters
        entity = ent.SellerInfo
        if not isValidInput(db, "sp_id", sp_id, entity()):
            continue

        while True:
            prompt_msg = "\n".join([f"{k}: {v[0]}" for k, v in functionalities.items()])
            opt_num = input(f"\nSelect the number corresponding to your choice:\n{prompt_msg}\n\n")

            if opt_num not in functionalities.keys():
                print("ERROR: Invalid option. Try again.")
                continue

            if int(opt_num) == DBAction.UpdateInfo.value:
                e = intakeParametersfromCLI(db, entity())
                if confirm(e):
                    db.updateSeller(sp_id, e.data)
                else:
                     print("\nUpdate cancelled by user.")
            elif int(opt_num) == DBAction.ViewInfo.value:
                res = db.showSeller(sp_id=sp_id)
                printRecords(res)
            elif int(opt_num) == DBAction.ReturnToHomeScreen.value:
                print("\nReturning to Homescreen.\n")
                break
            else:  # ExitProgram
                db.cursor.close()
                db.cnx.close()
                raise SystemExit("\nProgram exited by user. Goodbye!")
        break

