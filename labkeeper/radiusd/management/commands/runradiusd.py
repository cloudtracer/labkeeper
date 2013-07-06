from pyrad import dictionary, packet, server

from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.utils import timezone

from scheduler.models import Reservation
from labs.models import ConsoleServer

class RadiusServer(server.Server):

    # Here we're overriding Server's internal auth method because we need to handle NAS authentication dynamically
    def _HandleAuthPacket(self, pkt):

        # Sanity-checking
        if pkt.code != packet.AccessRequest:
            raise server.ServerPacketError("Received non-authentication packet on authentication port")

        print "Received an authentication request"
        print "Attributes: "
        for attr in pkt.keys():
            print "%s: %s" % (attr, pkt[attr])

        # Check that the request is coming from a valid ConsoleServer
        # This will need to be improved upon for IPv6 and DNS resolution support
        try:
            c = ConsoleServer.objects.get(ip4_address=pkt.source[0])
            pkt.secret = str(c.secret) # Convert from Unicode to plain string
        except ConsoleServer.DoesNotExist:
             raise server.ServerPacketError("Unrecognized console server ({0})".format(pkt.source[0]))

        # Craft a reply packet
        reply=self.CreateReplyPacket(pkt)

        # Attempt to find a Reservation matching the supplied credentials
        try:
            u = User.objects.get(username=pkt['User-Name'][0])
            r = Reservation.objects.get(user=u, password=pkt.PwDecrypt(pkt['User-Password'][0]), start_time__lte=timezone.now(), end_time__gt=timezone.now())
            print "Authenticated as {0} (reservation {1})".format(u.username, r.id)
            reply.code=packet.AccessAccept
            reply.AddAttribute('Session-Timeout', r.time_left.seconds)
            reply.AddAttribute('Termination-Action', 0)
            reply.AddAttribute('Reply-Message', "Welcome to {0}! Reservartion ID: {1}\nYour reservation ends in {2}.".format(r.pod, r.id, str(r.time_left).split('.')[0]))
        except User.DoesNotExist:
            print "Invalid username: {0}".format(pkt['User-Name'][0])
            reply.code=packet.AccessReject
        except Reservation.DoesNotExist:
            print "No reservation found"
            reply.code=packet.AccessReject

        # TODO: Check that port reported by ConsoleServer belongs to a device in Pod

        self.SendReplyPacket(pkt.fd, reply)

class Command(NoArgsCommand):
    help = 'Starts the RADIUS daemon'

    def handle_noargs(self, **options):
        srv=RadiusServer(dict=dictionary.Dictionary('/home/stretch/myradiusd/dictionary'))
        srv.BindToAddress('')
        srv.Run()
