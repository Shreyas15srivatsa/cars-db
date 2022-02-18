from enum import Enum
import entity as ent
from db import DB


class DBAction(Enum):
    SearchByCategory = 1
    SearchByKeyword = 2
    ReturnToHomeScreen = 3
    ExitProgram = 4


functionalities = {
    "1": ("Search by category", ent.ListingInfo, DBAction.SearchByCategory),
    "2": ("Search by keyword", ent.ListingInfo, DBAction.SearchByKeyword),
    "3": ("Return to Home Screen", ent.ListingInfo, DBAction.ReturnToHomeScreen),
    "4": ("Exit Program", None, DBAction.ExitProgram),
}


def isValidInput(key: str, value: str, e: ent.Entity) -> bool:
    val_type = e.search_parameters[key][1]
    try:
        val_type(value)
        return True
    except (ValueError, TypeError):
        print(f"ERROR: Input must be of type: {val_type.__name__}. Try again.")
        return False


def intakeParametersfromCLI(entity_cls: ent.Entity) -> ent.Entity:
    keys = [k for k in entity_cls.search_parameters.keys()]
    values = [v for v in entity_cls.search_parameters.values()]
    e = entity_cls()

    print("\nChoose categories to search by: (press Enter to skip a category)")
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
        elif not isValidInput(key, v, e):
            continue
        e.setAttribute(key, v)
        i += 1
        if val[0] == 1:
            range_val_seen = True
        else:
            range_val_seen = False
    return e


def intakeKeyword() -> str:
    return input(f"\nKeyword: ")


def confirmKeyword(keyword: str) -> bool:
    yesNo = input(f"Confirm Keyword: {keyword} ? [y/N]: ")
    return True if yesNo.lower() == "y" else False


def intakeSellerID(entity_cls: ent.Entity) -> str:
    while True:
        sp_id = input("\nSeller ID: ")
        if not isValidInput("sp_id", sp_id, entity_cls):
            continue
        else:
            return sp_id


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


def loop(db: DB) -> None:
    while True:
        prompt_msg = "\n".join([f"{k}: {v[0]}" for k, v in functionalities.items()])
        opt_num = input(f"\nChoose option to search by:\n{prompt_msg}\n\n")

        if opt_num not in functionalities.keys():
            print("ERROR: Invalid option. Try again.")
            continue

        functionality = functionalities[opt_num]
        entity = functionality[1]
        out_cols = ["listing_id", "model_name", "year", "trim_name", "price", "mileage"]

        if int(opt_num) == DBAction.SearchByCategory.value:
            e = intakeParametersfromCLI(entity)
            if not e.data:
                print("\nERROR: You must specify at least 1 parameter.")
                continue
            if confirm(e):
                # res = db.search_records(e.data, out_cols, entity.__name__)
                res = db.search_listing_by_category(e.data)
                printRecords(res)
                # print(res)
            else:
                print("\nSearch cancelled by user.")
                continue
        elif int(opt_num) == DBAction.SearchByKeyword.value:
            kw = intakeKeyword()
            if confirmKeyword(kw):
                # print(f"\n{sqlgen.search_records_using_keyword(kw, 'description', entity.__name__)}\n")
                res = db.search_records_using_keyword(
                    kw, "description", out_cols, entity.__name__
                )
                printRecords(res)
            else:
                print("\nSearch cancelled by user.")
                continue
        elif int(opt_num) == DBAction.ReturnToHomeScreen.value:
            print("\nReturning to Homescreen.\n")
            break
        else:
            db.cursor.close()
            db.cnx.close()
            raise SystemExit("\nProgram exited by user. Goodbye!")
