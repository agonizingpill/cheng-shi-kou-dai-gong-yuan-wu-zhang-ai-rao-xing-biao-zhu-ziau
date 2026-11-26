import json
from sqlalchemy import func, select

from core.db import transaction
from domain.demo import FIXTURES

def seed():
    sizes = {}
    with transaction() as conn:
        for table, rows in FIXTURES:
            for row in rows:
                if 'code' in row:
                    present = conn.scalar(select(table.c.code).where(table.c.code == row['code']))
                else:
                    present = conn.scalar(select(table.c.entrance).where(
                        table.c.trial == row['trial'], table.c.entrance == row['entrance']))
                if present is None:
                    conn.execute(table.insert().values(**row))
            sizes[table.name] = conn.scalar(select(func.count()).select_from(table))
    return sizes

if __name__ == '__main__':
    print(json.dumps(seed(), ensure_ascii=False, sort_keys=True))
