from django.db import models

import typetable


@typetable.typetable
class Race(models.Model):

    BLACK = typetable.Value('Black/African American', 'Black')

    WHITE = typetable.Value('White', 'White')

    NATIVE_AMERICAN = typetable.Value('American Indian/Alaska Native', 'Amer. '
                                      'Indian')

    ASIAN = typetable.Value('Asian/Pacific Islander', 'Asian')

    HISPANIC = typetable.Value('Hispanic/Latin American', 'Hispanic')

    @typetable.to_object
    def make_value(self, name, abbreviation):
        return Race(name=name, abbreviation=abbreviation)

    name = models.CharField(max_length=25)

    abbreviation = models.CharField(max_length=10)


class Gender(typetable.SimpleTypeTable):

    MALE = "Male"

    FEMALE = "Female"

    OTHER = "Other"

    UNKNOWN = "Unknown"
