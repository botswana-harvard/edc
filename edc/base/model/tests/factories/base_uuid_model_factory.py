import factory

starting_seq_num = 0


class BaseUuidModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        abstract = True
