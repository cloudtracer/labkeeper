from pyrad import dictionary, packet, server
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand

from scheduler.models import Reservation

class RadiusServer(server.Server):

    def _HandleAuthPacket(self, pkt):
        server.Server._HandleAuthPacket(self, pkt)

        print "Received an authentication request"
        print "Attributes: "
        for attr in pkt.keys():
            print "%s: %s" % (attr, pkt[attr])

        reply=self.CreateReplyPacket(pkt)

        # Authenticate supplied credentials
        try:
            user = User.objects.get(username=pkt['User-Name'][0])
            r = Reservation.objects.get(user=user, password=pkt.PwDecrypt(pkt['User-Password'][0]), start_time__lte=datetime.now())
            print "Authenticated as {0} (reservation {1})".format(user.username, r.id)
            reply.code=packet.AccessAccept
            reply.AddAttribute('Session-Timeout', r.duration * 3600)
        except (User.DoesNotExist, Reservation.DoesNotExist):
            print "Authentication failed"
            reply.code=packet.AccessReject

        self.SendReplyPacket(pkt.fd, reply)

class Command(NoArgsCommand):
    help = 'Starts the RADIUS daemon'

    def handle_noargs(self, **options):
        srv=RadiusServer(dict=dictionary.Dictionary('/home/stretch/myradiusd/dictionary'))
        srv.hosts["127.0.0.1"]=server.RemoteHost("127.0.0.1", "testing123", "localhost")
        #srv.hosts["192.168.0.118"]=server.RemoteHost("192.168.0.118", "testing123", "testrouter")
        srv.BindToAddress("")
        srv.Run()
