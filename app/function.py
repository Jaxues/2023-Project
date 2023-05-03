from datetime import timedelta
from cryptography import fernet
def testfunction():
    print('Hello world')

from datetime import timedelta
from sqlalchemy import func

def consecutive(session, table_name):
    result = session.query(table_name.date_column)\
                    .order_by(table_name.date_column)\
                    .all()
    if len(result) > 1:
        for i in range(len(result) - 1):
            if (result[i + 1][0] - result[i][0]) != timedelta(days=1):
                return False
        return True
    elif len(result) == 1:
        return True
    else:
        return False

def encrypt():
