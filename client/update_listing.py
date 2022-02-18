from enum import Enum
import entity as ent
from db import DB


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


def isValidListingIdForSpId(db: DB, sp_id: str, listing_id: str) -> bool:
    validation_query = f"""select count(*) from ListingInfo WHERE sp_id = "{sp_id}" AND listing_id = "{listing_id}";"""
    db.cursor.execute(validation_query)

    res = db.cursor.fetchall()
    if int(res[0][0]):
        return True
    else:
        print("ERROR: listing_id does not exist for given sp_id. Try again")
        return False


def intakeOptionalParametersfromCLI(db: DB, e: ent.Entity) -> ent.Entity:
    keys = [k for k in e.update_parameters.keys()]
    values = [v for v in e.update_parameters.values()]

    print(
        "\nChoose attributes to update by: (press Enter to continue or press (q + Enter) to skip this menu entirely.)"
    )
    print("Press Enter to skip attributes.")
    if input() == "q":
        return e

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


def printRecords(records: list) -> None:
    print("\nResult:\n")
    for i, r in enumerate(records):
        print(i, r)
        if i == 0:
            print("------------------------------------------------------------")
    print(f"\nShowing all {len(records)-1} records.\n")


def confirm(entity_obj: ent.Entity) -> bool:
    yesNo = input(f"\n{entity_obj.toString()}\nConfirm? [y/N]: ")
    return True if yesNo.lower() == "y" else False


def loop(db: DB):

    while True:
        print("\nEnter the seller id for the lisiting you wish to update.")
        sp_id = input("sp_id: ")

        # ask for inputs for required creation paramters
        entity = ent.ListingInfo
        if not isValidInput(db, "sp_id", sp_id, entity()):
            continue

        res = db.searchListingsBySpId(sp_id=sp_id)
        printRecords(res)

        print("\nEnter the listing_id of the listing to update.\n")

        listing_id = ""
        while True:
            listing_id = input("listing_id: ")
            if not isValidListingIdForSpId(db, sp_id, listing_id):
                continue
            break

        e = intakeOptionalParametersfromCLI(db, entity())

        if confirm(e):
            # dispatch update query
            db.updateListingByListingId(listing_id, e.data)
        else:
            print("\nUpdate cancelled by user.")

        break
