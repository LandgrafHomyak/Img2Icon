class Resources(dict):
    def open(self, name, path, cls):
        if name in self:
            return
        self[name] = cls(path)


resources = Resources()
