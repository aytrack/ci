
class Version(object):
    """
    version interface
    """
    def __init__(self, v):
        # format "vx.x.x" or "x.x.x"
        v = v.lstrip("v")
        self.strs = v.split(".")
        if len(self.strs) != 3:
            raise Exception(self.strs)

    def less(self, v2):
        """
        :param v2:
        :return: true or false
        """
        for i in range(3):
            if int(self.strs[i]) < int(v2.strs[i]):
                return True
            if int(self.strs[i]) > int(v2.strs[i]):
                return False
        return True

    def branch(self):
        # return release branch
        return "{}.{}".format(self.strs[0], self.strs[1])

    def is_branch(self):
        # whether it is branch name or not
        return self.strs[2] == "0"

    def is_adjacent(self, v2):
        # whether the two versions are adjacent or not
        if self.strs[0] == v2.strs[0] and self.strs[1] == v2.strs[1] and abs(int(self.strs[2]) - int(v2.strs[2])) == 1:
            return True
        return False

    def is_branch_adjacent(self, v2):
        # whether the two branches are adjacent or not
        if self.strs[0] == v2.strs[0] and abs(int(self.strs[1]) - int(v2.strs[1])) == 1:
            return True
        if self.strs[1] == "0" and v2.strs[1] == "0" and abs(int(self.strs[0]) - int(v2.strs[0])) == 1:
            return True
        return False
