
class BackupRule:

    def __init__(self, name, path, query="", exclusion=False, forced=True):
        self.name = name
        self.path = path
        self.query = query
        self.exclusion = exclusion
        self.forced = forced

    @classmethod
    def create_rule_from_str(cls, rule_str):
        if rule_str.find("No existing rules") >=0:
            return None
        lines = rule_str.split('\n')

        name = lines[2]
        path = lines[3]

        if lines[4].upper() == 'NO QUERY':
            query=''
        else:
            query=lines[4]

        if lines[5].upper() == 'INCLUSION':
            inclusion = False
        else:
            inclusion = True

        if lines[6].upper() == 'NOT FORCED':
            forced = False
        else:
            forced = True

        return BackupRule(name,path,query,exclusion=inclusion,forced=forced)


