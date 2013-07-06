from pyrad import dictionary, packet, server

from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.utils import timezone

from scheduler.models import Reservation
from labs.models import ConsoleServer, ConsoleServerPort

class RadiusServer(server.Server):

    # Here we're overriding Server's internal auth method because we need to handle NAS authentication dynamically
    def _HandleAuthPacket(self, pkt):

        # Sanity-checking
        if pkt.code != packet.AccessRequest:
            raise server.ServerPacketError("Received non-authentication packet on authentication port")

        print "Authentication request received from {0}:".format(pkt.source[0])
        for attr in pkt.keys():
            print "  {0:20} {1}".format(attr, pkt[attr])

        # Check that the request is coming from a valid ConsoleServer
        # This will need to be improved upon for IPv6 and DNS resolution support
        try:
            c = ConsoleServer.objects.get(ip4_address=pkt.source[0])
            pkt.secret = str(c.secret) # Convert from Unicode to plain string
        except ConsoleServer.DoesNotExist:
             raise server.ServerPacketError("Unrecognized console server ({0})".format(pkt.source[0]))

        # Initialize a reply packet
        reply = self.CreateReplyPacket(pkt)
        reply.code = packet.AccessReject

        # Attempt to find a Reservation matching the supplied credentials
        try:
            u = User.objects.get(username=pkt['User-Name'][0])
            r = Reservation.objects.get(user=u, password=pkt.PwDecrypt(pkt['User-Password'][0]), start_time__lte=timezone.now(), end_time__gt=timezone.now())
        except (User.DoesNotExist, Reservation.DoesNotExist):
            print "No reservation found for user '{0}'".format(pkt['User-Name'][0])
            reply.AddAttribute('Reply-Message', 'No reservation found')
            self.SendReplyPacket(pkt.fd, reply)
            return

        # Validate ConsoleServerPort number
        try:
            d = c.ports.get(number=pkt['NAS-Port'][0]).device
        except ConsoleServerPort.DoesNotExist:
            print "Invalid console server port ({0})".format(pkt['NAS-Port'][0])
            reply.AddAttribute('Reply-Message', "This console server port ({0}) is not recognized".format(pkt['NAS-Port'][0]))
            self.SendReplyPacket(pkt.fd, reply)
            return

        # Validate that this Device belongs to the reserved Pod
        if not d in r.pod.devices.all():
            print "Device {0} not in reserved pod {1}".format(d, r.pod)
            reply.AddAttribute('Reply-Message', "This device does not belong to {0}".format(r.pod))
            self.SendReplyPacket(pkt.fd, reply)
            return

        # Craft our Access-Accept response
        print "Authenticated as '{0}' (reservation {1})".format(u.username, r.id)
        reply.code = packet.AccessAccept
        attrs = {
            'Session-Timeout':      r.time_left.seconds,
            'Termination-Action':   0,
            'Reply-Message':        "Welcome to {0}! Reservartion ID: {1}\nYour reservation ends in {2}.".format(r.pod, r.id, str(r.time_left).split('.')[0]),
        }
        for k, v in attrs.items():
            reply.AddAttribute(k, v)

        self.SendReplyPacket(pkt.fd, reply)

    # TODO: Implement accounting functionality

class Command(NoArgsCommand):
    help = 'Starts the RADIUS daemon'

    def handle_noargs(self, **options):
        srv=RadiusServer(dict=dictionary.Dictionary('/home/stretch/myradiusd/dictionary'))
        srv.BindToAddress('')
        srv.Run()
