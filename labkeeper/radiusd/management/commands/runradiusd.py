from pyrad import dictionary, packet, server

from django.core.management.base import NoArgsCommand, CommandError

from freeradius.models import Radcheck

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
            Radcheck.objects.get(username=pkt['User-Name'][0], attribute='Cleartext-Password', value=pkt.PwDecrypt(pkt['User-Password'][0]))
            print "Password matches!"
            reply.code=packet.AccessAccept
        except Radcheck.DoesNotExist:
            print "Invalid password :("
            reply.code=packet.AccessReject

        self.SendReplyPacket(pkt.fd, reply)

class Command(NoArgsCommand):
    help = 'Starts the RADIUS daemon'

    def handle_noargs(self, **options):
        srv=RadiusServer(dict=dictionary.Dictionary('/home/stretch/myradiusd/dictionary'))
        srv.hosts["127.0.0.1"]=server.RemoteHost("127.0.0.1", "testing123", "localhost")
        srv.hosts["192.168.0.118"]=server.RemoteHost("192.168.0.118", "testing123", "testrouter")
        srv.BindToAddress("")
        srv.Run()
