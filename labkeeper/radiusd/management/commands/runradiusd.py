import socket
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
            print "Received non-authentication packet on authentication port"
            raise server.ServerPacketError()

        print "Authentication request received from {0}:".format(pkt.source[0])
        for attr in pkt.keys():
            print "  {0:20} {1}".format(attr, pkt[attr])

        # TODO: Input sanitization

        # Check for a domain in username
        try:
            username, userdomain = pkt['User-Name'][0].split('@', 1)
        except ValueError:
            username = pkt['User-Name'][0]
            userdomain = None

        # If domain is specified, use it to identify ConsoleServer
        if userdomain:
            print "Identifying console server by domain ({0})".format(userdomain)
            try:
                c = ConsoleServer.objects.get(fqdn=userdomain)
            except ConsoleServer.DoesNotExist:
                print "Unrecognized console server ({0})".format(userdomain)
                raise server.ServerPacketError()
            # Enforce IP address if one has been set for the ConsoleServer
            if c.ip4_address and c.ip4_address != pkt.source[0]:
                print "Requester IP ({0}) does not match console server IP ({1})".format(c.ip4_address, pkt.source[0])
                raise server.ServerPacketError()
            # Verify that the domain specified resolves to the requester's IP
            if not socket.gethostbyname(userdomain) == pkt.source[0]:
                print "Domain authentication failure from {0} for {1} (actual IP {2})".format(pkt.source[0], userdomain, c.ip4_address)
                raise server.ServerPacketError()
        else:
            print "Identifying console server by IP address ({0})".format(pkt.source[0])
            try:
                c = ConsoleServer.objects.get(ip4_address=pkt.source[0])
            except ConsoleServer.DoesNotExist:
                print "Unrecognized console server ({0})".format(pkt.source[0])
                raise server.ServerPacketError()
        print "Found console server: {0}".format(c)

        # Record shared secret stored by ConsoleServer
        pkt.secret = str(c.secret)

        # Initialize a reply packet
        reply = self.CreateReplyPacket(pkt)

        # Attempt to find a Reservation matching the supplied credentials
        try:
            u = User.objects.get(username=username)
            r = Reservation.objects.get(user=u, password=pkt.PwDecrypt(pkt['User-Password'][0]), start_time__lte=timezone.now(), end_time__gt=timezone.now())
        except (User.DoesNotExist, Reservation.DoesNotExist):
            print "No reservation found for user '{0}'".format(username)
            reply.AddAttribute('Reply-Message', 'No reservation found')
            reply.code = packet.AccessReject
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
        srv=RadiusServer(dict=dictionary.Dictionary('radiusd/dictionary'))
        srv.BindToAddress('')
        srv.Run()
