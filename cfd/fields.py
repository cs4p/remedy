from multiselectfield import MultiSelectField as DefaultMultiSelectField

class MultiSelectField(DefaultMultiSelectField):
    '''
    This is a patch for the MultiSelectField to make it 
    serializable in Django 2.0+
    https://github.com/goinnn/django-multiselectfield/issues/74    
    '''
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)