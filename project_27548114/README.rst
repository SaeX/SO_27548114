See http://stackoverflow.com/questions/27548114/

    >>> import django
    >>> django.setup
    <function setup at 0x02633AB0>
    >>> django.setup()
    >>> from hotel.models import *
    >>> room1 = Room.objects.get_or_create(name="R001")[0]
    >>> room2 = Room.objects.get_or_create(name="R002")[0]
    >>> res1 = Reservation.objects.get_or_create(date_in="2014-12-01", date_out=None, room=room1, live=False)[0]
    >>> res2 = Reservation.objects.get_or_create(date_in="2014-12-01", date_out="2014-12-15", room=room1, live=True)[0]
    >>> Room.available_rooms.available_with_Q("2014-12-16", "")
    Query of available_with_Q:  SELECT "hotel_room"."id", "hotel_room"."name" FROM "hotel_room" WHERE NOT ((("hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_out" > 2014-12-16) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL)) OR ("hotel_room"."id" IN (SELECT U0."id" AS "id" FROM "hotel_room" U0 LEFT OUTER JOIN "hotel_reservation" U1 ON ( U0."id" = U1."room_id" ) WHERE (U1."date_out" IS NULL AND U0."id" = ("hotel_room"."id"))) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL))))
    [<Room: R002>]
    >>> Room.available_rooms.available_with_chained_excludes("2014-12-16", "")
    Query of available_with_chained_excludes:  SELECT "hotel_room"."id", "hotel_room"."name" FROM "hotel_room" WHERE (NOT ("hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_out" > 2014-12-16) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL)) AND NOT ("hotel_room"."id" IN (SELECT U0."id" AS "id" FROM "hotel_room" U0 LEFT OUTER JOIN "hotel_reservation" U1 ON ( U0."id" = U1."room_id" ) WHERE U1."date_out" IS NULL) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL)))
    [<Room: R002>]
    >>> res1.live
    False
    >>> res2.live
    True
    >>>
    >>> res1.room = room2
    >>> Room.available_rooms.available_with_Q("2014-12-16", "")
    Query of available_with_Q:  SELECT "hotel_room"."id", "hotel_room"."name" FROM "hotel_room" WHERE NOT ((("hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_out" > 2014-12-16) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL)) OR ("hotel_room"."id" IN (SELECT U0."id" AS "id" FROM "hotel_room" U0 LEFT OUTER JOIN "hotel_reservation" U1 ON ( U0."id" = U1."room_id" ) WHERE (U1."date_out" IS NULL AND U0."id" = ("hotel_room"."id"))) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL))))
    [<Room: R002>]
    >>> res1.save()
    >>> Room.available_rooms.available_with_Q("2014-12-16", "")
    Query of available_with_Q:  SELECT "hotel_room"."id", "hotel_room"."name" FROM "hotel_room" WHERE NOT ((("hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_out" > 2014-12-16) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL)) OR ("hotel_room"."id" IN (SELECT U0."id" AS "id" FROM "hotel_room" U0 LEFT OUTER JOIN "hotel_reservation" U1 ON ( U0."id" = U1."room_id" ) WHERE (U1."date_out" IS NULL AND U0."id" = ("hotel_room"."id"))) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."live" = True) AND "hotel_room"."id" IN (SELECT U1."room_id" AS "room_id" FROM "hotel_reservation" U1 WHERE U1."date_in" IS NOT NULL))))
    [<Room: R001>, <Room: R002>]
