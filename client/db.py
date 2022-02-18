import mysql.connector
import getpass


class DB:
    def __init__(self) -> None:
        # passwd = getpass.getpass("Password for MySQL: ")
        # username = getpass.getuser()  # not portable
        # username = input("Database user (root if local): ")  # not portable
        # personal_db = f"db356_{username}"
        username = input("MySQL user: ")
        passwd = getpass.getpass("Database password: ")
        host = input("host: ")
        personal_db = input("Select database: ")

        config = {
            "user": username,
            "password": passwd,
            "host": host,
            "database": personal_db,
            "raise_on_warnings": True,
        }

        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()
        self.make_id = None

    def db_read(self, query: str) -> list:
        res = []
        self.cursor.execute(query)
        out = self.cursor.fetchall()
        for line in out:
            res.append(line)
        return res

    def db_update(self, query: str) -> None:
        pass

    def db_delete(self, query: str) -> None:
        self.cursor.execute(query)
        self.cnx.commit()
        print(f"{self.cursor.rowcount} record(s) deleted")

    def db_close(self) -> None:
        self.cursor.close()
        self.cnx.close()

    def search_records(self, record: dict, select_columns: list, table: str) -> list:
        """
        Simple select query with no jois.
        """
        # TODO: Ensure keys() and values() are ordered sets
        columns = ", ".join(select_columns)
        where_clause = " AND ".join([f"{k} = '{v}'" for k, v in record.items()])
        sql = f"SELECT {columns} FROM {table} WHERE {where_clause};"
        self.cursor.execute(sql)
        out = self.cursor.fetchall()
        res = [columns]
        for line in out:
            res.append(line)
        return res

    def search_records_using_keyword(
        self, keyword: str, search_column: str, select_columns: list, table: str
    ) -> list:
        columns = ", ".join(select_columns)
        sql = f"SELECT {columns} FROM {table} WHERE {search_column} LIKE '%{keyword}%';"
        self.cursor.execute(sql)
        out = self.cursor.fetchall()
        res = [columns]
        for line in out:
            res.append(line)
        return res

    def search_listing_by_category(self, record: dict) -> list:
        select_cols = [
            "make_name",
            "model_name",
            "year",
            "trim_name",
            "sp_name",
            "price",
            "mileage",
            "seller_rating",
        ]
        cols = ",".join(select_cols)
        where_clause = " AND ".join(
            [
                f"""{k} = UPPER("{v}")"""
                for k, v in record.items()
                if (
                    not k.startswith("min_")
                    and not k.startswith("max_")
                    and not k.startswith("threshold_")
                )
            ]
        )
        # loop over the range items
        range_records = {
            k: v
            for k, v in record.items()
            if k.startswith("min_") or k.startswith("max_")
        }
        ranged_where_clause = ""
        ranged_keys = [k for k in range_records.keys()]
        ranged_vals = [v for v in range_records.values()]
        for i, k in enumerate(ranged_keys):
            if k.startswith("min_"):
                attr = k[4:]  # get rid of "min_"
                if where_clause:
                    ranged_where_clause += (
                        f"AND {attr} BETWEEN {ranged_vals[i]} AND {ranged_vals[i+1]} "
                    )
                else:
                    ranged_where_clause += (
                        f"{attr} BETWEEN {ranged_vals[i]} AND {ranged_vals[i+1]} "
                    )

        gt_clause = " AND ".join(
            [
                f"""{k} >= UPPER("{v}")"""
                for k, v in record.items()
                if k.startswith("threshold_")
            ]
        )
        gt_clause = gt_clause.replace("threshold_", "")

        if gt_clause:
            where_clause = (
                where_clause + " " + ranged_where_clause + " " + "AND " + gt_clause
            )
        else:
            where_clause = where_clause + " " + ranged_where_clause

        sql = f"""
        SELECT {cols} 
        FROM ListingInfo INNER JOIN MakeInfo USING (make_id)
        INNER JOIN SellerInfo USING (sp_id)
        WHERE {where_clause}
        ;
        """
        self.cursor.execute(sql)
        out = self.cursor.fetchall()
        res = [cols.replace("sp_name", "sp_name as seller_name")]
        for line in out:
            res.append(line)
        return res

    def create_listing(self, record: dict) -> None:
        # TODO: Ensure keys() and values() are ordered sets
        # record like {k<str>: v<tuple<any, type>>}

        # replace make_name with make_id
        record.pop("make_name")
        record["make_id"] = (self.make_id, int)
        columns = "(" + ",".join(record.keys()) + ")"

        value_str = ""
        vals = record.values()
        value_str += "("

        for i, v in enumerate(vals):
            if v[1] == int:
                value_str += str(v[0])
            else:
                value_str += f"'{v[0]}'"

            if i < len(vals) - 1:
                value_str += ","
        value_str += ")"

        sql = f"INSERT INTO ListingInfo {columns} VALUES {value_str};"
        self.make_id = None
        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            print("\nInserted record successfully.\n")
        except Exception:
            print("\nFailed to insert record\n")

    def searchListingsBySpId(self, sp_id: str) -> list:
        select_cols = [
            "listing_id",
            "make_name",
            "model_name",
            "year",
            "trim_name",
            "price",
            "mileage",
        ]
        cols = ",".join(select_cols)
        sql = f"""
        SELECT {cols} 
        FROM ListingInfo INNER JOIN MakeInfo USING (make_id)
        WHERE sp_id = "{sp_id}";
        """
        self.cursor.execute(sql)
        out = self.cursor.fetchall()
        res = [cols]
        for line in out:
            res.append(line)
        return res

    def updateListingByListingId(self, listing_id: str, record: dict):
        if record.get("make_name"):
            val = record.pop("make_name")
            first_query = f"SELECT make_id FROM MakeInfo WHERE make_name = '{val}';"
            self.cursor.execute(first_query)
            res = self.cursor.fetchall()
            record["make_id"] = int(res[0][0])

        set_clause = " , ".join([f"""{k} = UPPER("{v}")""" for k, v in record.items()])

        if not set_clause:
            print("Nothing to update!")
            return

        set_clause = "SET " + set_clause

        sql = f"UPDATE ListingInfo {set_clause} WHERE listing_id = {listing_id};"
        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            print("\nUpdated record successfully.\n")
        except Exception:
            print("\nFailed to update record\n")

    def runPredefinedReadQuery(self, cols: list, query: str) -> list:
        columns = ",".join(cols)
        self.cursor.execute(query)
        out = self.cursor.fetchall()
        res = [columns]
        for line in out:
            res.append(line)
        return res

    def updateSeller(self, sp_id: str, record: dict):
        set_clause = " , ".join([f"""{k} = UPPER("{v}")""" for k, v in record.items()])

        if not set_clause:
            print("Nothing to update!")
            return

        set_clause = "SET " + set_clause

        sql = f"UPDATE SellerInfo {set_clause} WHERE sp_id = {sp_id};"
        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            print("\nUpdated record successfully.\n")
        except Exception:
            print("\nFailed to update record\n")

    def showSeller(self, sp_id:str) -> list:
        cols = [	
            "sp_id", 
            "sp_name",
            "seller_rating",
            "dealer_zip",
            "longitude",
            "latitude," 
            "city",
            "franchise_dealer"
        ]
        columns = ",".join(cols)
        query = f"SELECT * FROM SellerInfo WHERE sp_id = {sp_id};"
        self.cursor.execute(query)
        out = self.cursor.fetchall()
        res = [columns]
        for line in out:
            res.append(line)
        return res
    
    def removeListing(self, listing_id: str):
        sql = f"DELETE FROM ListingInfo WHERE listing_id = {listing_id};"
        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            print("\nDeleted record successfully.\n")
        except Exception:
            print("\nFailed to delete record\n")