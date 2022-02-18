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

def printRecords(records: list) -> None:
    print("\nResult:\n")
    for i, r in enumerate(records):
        print(i, r)
        if i == 0:
            print("------------------------------------------------------------")
    print(f"\nShowing all {len(records)-1} records.\n")

def confirm(listing_id:str):
    yesNo = input(f"\nConfirm deletion of listing {listing_id}? [y/N]: ")
    return True if yesNo.lower() == "y" else False


def loop(db: DB):

    while True:
        print("\nEnter the seller id for the lisiting you wish to remove.")
        sp_id = input("sp_id: ")

        # ask for inputs for required creation paramters
        entity = ent.ListingInfo
        if not isValidInput(db, "sp_id", sp_id, entity()):
            continue

        res = db.searchListingsBySpId(sp_id=sp_id)
        printRecords(res)

        print("\nEnter the listing_id of the listing to be removed.\n")

        listing_id = ""
        while True:
            listing_id = input("listing_id: ")
            if not isValidListingIdForSpId(db, sp_id, listing_id):
                continue
            break

        if confirm(listing_id):
            # dispatch deletion query
            db.removeListing(listing_id)
        else:
            print("\nOperation cancelled by user.")

        break