

class ModelMixin:
    def to_dict(self):
        att_dict = {}
        for field in self._meta.get_fields():
            att_dict[field.attname] = getattr(self, field.attname, None)
        return att_dict
