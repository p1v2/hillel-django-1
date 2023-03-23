class CheapMixin:
    def cheap(self):
        return self.filter(price__lt=100)
