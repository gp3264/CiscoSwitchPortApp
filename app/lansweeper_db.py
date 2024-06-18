
#import pyodbc

class LansweeperLocalDB:
    def __init__(self, server, database, username, password):
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )

    # def get_connection(self):
    #     return pyodbc.connect(self.connection_string)
    #
    # def get_network_interfaces(self, asset_id):
    #     query = '''
    #     SELECT ni.*
    #     FROM tblAssets AS a
    #     INNER JOIN tblNetworkInterface AS ni ON a.AssetID = ni.AssetID
    #     WHERE a.AssetID = ?
    #     '''
    #     with self.get_connection() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(query, asset_id)
    #         columns = [column[0] for column in cursor.description]
    #         results = []
    #         for row in cursor.fetchall():
    #             results.append(dict(zip(columns, row)))
    #     return results
    #
    # def get_all_assets(self):
    #     query = "SELECT * FROM tblAssets"
    #     with self.get_connection() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(query)
    #         columns = [column[0] for column in cursor.description]
    #         results = []
    #         for row in cursor.fetchall():
    #             results.append(dict(zip(columns, row)))
    #     return results
