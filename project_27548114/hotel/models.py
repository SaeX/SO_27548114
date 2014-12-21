from django.db import models


class AvailableRoomManager(models.Manager):

    def available_with_Q(self, indate, outdate):
        qs = super(AvailableRoomManager, self).get_queryset()

        if indate and outdate:
            qs = qs.exclude(models.Q(reservation__date_out__gt=indate, reservation__date_in__lt=outdate, reservation__live=True)
                            | models.Q(reservation__date_out__isnull=True, reservation__date_in__isnull=False, reservation__date_in__lt=outdate, reservation__live=True))

        elif indate and not outdate:
            qs = qs.exclude((models.Q(reservation__date_out__gt=indate, reservation__date_in__isnull=False, reservation__live=True)
                            | models.Q(reservation__date_out__isnull=True, reservation__date_in__isnull=False, reservation__live=True)))
            print "Query of available_with_Q: ", qs.query

        return qs

    def available_with_chained_excludes(self, indate, outdate):
        qs = super(AvailableRoomManager, self).get_queryset()

        if indate and outdate:
            qs = qs.exclude(reservation__date_out__gt=indate, reservation__date_in__lt=outdate, reservation__live=True) \
                   .exclude(reservation__date_out__isnull=True, reservation__date_in__isnull=False, reservation__date_in__lt=outdate, reservation__live=True)

        elif indate and not outdate:
            qs = qs.exclude(reservation__date_out__gt=indate, reservation__date_in__isnull=False, reservation__live=True) \
                   .exclude(reservation__date_out__isnull=True, reservation__date_in__isnull=False, reservation__live=True)
            print "Query of available_with_chained_excludes: ", qs.query

        return qs

    def available(self, indate, outdate):
        qs = super(AvailableRoomManager, self).get_queryset()

        ress = Reservation.objects.filter(live=True)
        qs = qs.filter(reservation__in=ress)
        print "QS after reservations filter: ", qs

        if indate and outdate:
            print "Both indate and outdate are provided..."
            qs = qs.exclude(models.Q(reservation__date_out__gt=indate, reservation__date_in__lt=outdate)
                            | models.Q(reservation__date_out__isnull=True, reservation__date_in__isnull=False, reservation__date_in__lt=outdate))

        elif indate and not outdate:
            print "Only indate is provided..."
            qs = qs.exclude((models.Q(reservation__date_out__gt=indate, reservation__date_in__isnull=False)
                            | models.Q(reservation__date_out__isnull=True, reservation__date_in__isnull=False)))

        return qs


class Room(models.Model):
    name = models.CharField(max_length=30, unique=True)

    objects = models.Manager()
    available_rooms = AvailableRoomManager()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    date_in = models.DateField()
    date_out = models.DateField(blank=True, null=True)
    room = models.ForeignKey(Room)
    active = models.NullBooleanField()
    live = models.NullBooleanField()

    def __str__(self):
        return "res#%s in %s" % (self.id, self.room)
