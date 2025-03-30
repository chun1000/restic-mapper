import policy_edit
from sql_func import ResticSql

if __name__ == "__main__":
    restic_sql = ResticSql()
    policy_edit.run_policy_edit(restic_sql)