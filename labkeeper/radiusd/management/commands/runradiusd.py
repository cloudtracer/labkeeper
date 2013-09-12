import socket
from pyrad import dictionary, packet, server
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from scheduler.models import Reservation
from labs.models import ConsoleServer, ConsoleServerPort
from radiusd.models import RadiusLogin

# Resolve a domain name to one or more IPv4 and/or IPv6 addresses
def domain_to_ip(domain):
    try:
        return [r[4][0] for r in socket.getaddrinfo(domain, 0)]
    except socket.gaierror:
        return []


class RadiusServer(server.Server):

    auth_counter = 0

    # Bail on processing a request any further
    def bail(self, message=None):
        if message:
            print "[{0}] {1}".format(self.auth_counter, message)
        raise server.ServerPacketError()

    # Debugging
    def debug(self, message):
        print "[{0}] {1}".format(self.auth_counter, message)

    # Send an Access-Reject reply
    def access_reject(self, pkt, message=None):

        reply = self.CreateReplyPacket(pkt)
        reply.code = packet.AccessReject
        if message:
            print "[{0}] Access rejected: {1}".format(self.auth_counter, message)
            reply.AddAttribute('Reply-Message', message)
        self.SendReplyPacket(pkt.fd, reply)

    # Overriding Server's internal auth method because we need to handle NAS authentication dynamically
    def _HandleAuthPacket(self, pkt):

        self.auth_counter += 1

        # Sanity-checking
        if pkt.code != packet.AccessRequest:
            self.bail("Received non-authentication packet on authentication port")

        # Debugging
        self.debug("Authentication request received from {0}:".format(pkt.source[0]))
        for attr in pkt.keys():
            if not attr == 'User-Password':
                self.debug("  {0:20} {1}".format(attr, pkt[attr][0]))

        # Step 1: Is a domain specified in User-Name?
        #  - If yes, identify the ConsoleServer by domain name
        #  - If no, identify the ConsoleServer by source IPv4 or IPv6 address
        try:
            username, userdomain = pkt['User-Name'][0].split('@', 1)
        except ValueError:
            username = pkt['User-Name'][0]
            userdomain = None
        if userdomain:
            self.debug("Identifying console server by domain ({0})".format(userdomain))
            try:
                cs = ConsoleServer.objects.get(fqdn=userdomain)
            except ConsoleServer.DoesNotExist:
                self.bail("Unrecognized console server ({0})".format(userdomain))
            # Enforce IP address if one has been set for the ConsoleServer
            # TODO: IPv6 support (Yes, I'm a bad networker)
            if cs.ip4_address and cs.ip4_address != pkt.source[0]:
                self.bail("Requester IP ({0}) does not match console server IP ({1})".format(pkt.source[0], cs.ip4_address))
            # Verify that the domain specified resolves to the requester's IP
            elif pkt.source[0] not in domain_to_ip(userdomain):
                self.bail("Domain authentication failure from {0} for {1}".format(pkt.source[0], userdomain))
        else:
            self.debug("Identifying console server by IP address ({0})".format(pkt.source[0]))
            try:
                cs = ConsoleServer.objects.get(ip4_address=pkt.source[0])
            except ConsoleServer.DoesNotExist:
                self.bail("Unrecognized console server ({0})".format(pkt.source[0]))
        self.debug("Found console server: {0}".format(self.auth_counter, cs))

        # Step 2: Shared secret validation
        try:
            pkt.secret = str(cs.secret)
            pkt.PwDecrypt(pkt['User-Password'][0])
        except:
            self.bail("Invalid shared secret!")

        # Step 3: Attempt to retrieve the User based on the given User-Name
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            self.access_reject(pkt, "Invalid username")
            return

        # Step 4: Attempt to locate a Reservation for this User
        try:
            r = Reservation.objects.get(lab=cs.lab, end_time__gt=timezone.now(), user=u, password=pkt.PwDecrypt(pkt['User-Password'][0]))
        except Reservation.DoesNotExist:
            self.access_reject(pkt, "Sorry, no reservation found for {0}".format(username))
            return

        # Step 5: Validate that the Reservation is current
        if r.start_time > timezone.now():
            self.access_reject(pkt, "Your reservation has not started yet (scheduled for {0})".format(r.start_time))
            return

        # Step 6: Match the given NAS-Port to a ConsoleServerPort
        try:
            d = cs.ports.get(number=pkt['NAS-Port'][0]).device
        except ConsoleServerPort.DoesNotExist:
            self.access_reject(pkt, "Console server port {0} is not recognized".format(pkt['NAS-Port'][0]))
            return

        # Step 7: Validate that this Device belongs to one of the reserved Pods
        if d.pod not in r.pods.all():
            self.access_reject(pkt, "This device does not belong to one of the reserved pods")
            return

        # Step 8: Success! Reward the user with an Access-Accept response
        self.debug("Authenticated as '{0}' (reservation {1})".format(u.username, r.id))
        reply = self.CreateReplyPacket(pkt)
        reply.code = packet.AccessAccept
        attrs = {
            'Session-Timeout':      r.time_left.seconds,
            'Termination-Action':   0,
            #'Framed-Filter-Id':     ':group_name=admin:', # Needed for Opengear?
            'Reply-Message':        "Welcome to {0} - Pod {1}! Reservation ID: {2}\n"
                                    "Your reservation ends in {3}.".format(d.pod.lab, d.pod, r.id, str(r.time_left).split('.')[0]),
        }
        for k, v in attrs.items():
            reply.AddAttribute(k, v)
        self.SendReplyPacket(pkt.fd, reply)

        # Logging
        login = RadiusLogin(lab=cs.lab, device=d, user=u)
        try:
            login.user_ip = pkt['Calling-Station-Id'][0]
        except KeyError:
            pass
        login.save()

    # TODO: Implement accounting functionality?
    #def _HandleAcctPacket(self, pkt):
    #    #server.Server._HandleAcctPacket(self, pkt)
    #
    #    print "Received an accounting request"
    #    print "Attributes: "
    #    for attr in pkt.keys():
    #        print "%s: %s" % (attr, pkt[attr])
    #
    #    pkt.secret = 'secret1234'
    #
    #    reply=self.CreateReplyPacket(pkt)
    #    self.SendReplyPacket(pkt.fd, reply)

class Command(BaseCommand):
    help = "Start the RADIUS daemon"

    # Not used yet
    option_list = BaseCommand.option_list + (
        make_option('--debug',
                    action='store_true',
                    dest='debug',
                    default=False,
                    help='Enable debugging'),
    )

    def handle(self, *args, **options):
        srv = RadiusServer(dict=dictionary.Dictionary('radiusd/dictionary'))
        srv.BindToAddress('')
        srv.Run()
