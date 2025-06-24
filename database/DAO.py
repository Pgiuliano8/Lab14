from database.DB_connect import DBConnect
from model.archi import Arco
from model.orders import Order


class DAO():

    @staticmethod
    def getStoresID():
        conn =DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select store_id
                    from stores
        """

        cursor.execute(query)

        for row in cursor:
            res.append(row["store_id"])

        conn.close()
        cursor.close()

        return res

    @staticmethod
    def getOrdersByStoreID(store_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select *
                        from orders
                        where store_id = %s
            """

        cursor.execute(query, (store_id,))

        for row in cursor:
            res.append(Order(**row))

        conn.close()
        cursor.close()

        return res

    @staticmethod
    def getEdges(store_id, days, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select o.order_id as o1, o2.order_id as o2, (oi.quantity + oi2.quantity) as peso
                    from orders o, orders o2, order_items oi, order_items oi2 
                    where o.store_id = o2.store_id and o2.store_id = %s and o.order_id < o2.order_id 
                    and abs(day(o.order_date)-day(o2.order_date)) < %s
                    and o.order_id = oi.order_id and o2.order_id = oi2.order_id 
                """

        cursor.execute(query, (store_id,days))

        for row in cursor:
            res.append(Arco(idMap[row['o1']], idMap[row['o2']], row['peso']))

        conn.close()
        cursor.close()

        return res


    if __name__=='__main__':
        print(getStoresID())
        print(getOrdersByStoreID(1))