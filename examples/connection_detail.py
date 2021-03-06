"""
Display detailed information about currently active connections.
"""
import NetworkManager
import socket
import struct

c = NetworkManager.const

for conn in NetworkManager.NetworkManager.ActiveConnections:
    settings = conn.Connection.GetSettings()
    for s in settings.keys():
        if 'data' in settings[s]:
            settings[s + '-data'] = settings[s].pop('data')

    devices = ""
    if conn.Devices:
        devices = " (on %s)" % ", ".join([x.Interface for x in conn.Devices])
    print "Active connection: %s%s" % (settings['connection']['id'], devices)
    size = max([max([len(y) for y in x.iterkeys()]) for x in settings.itervalues()])
    format = "      %%-%ds %%s" % (size + 5)
    for key, val in sorted(settings.iteritems()):
        print "   %s" % key
        for name, value in val.iteritems():
            if name == 'ssid':
                value = "".join([str(x) for x in value])
            print format % (name, value)
    for dev in conn.Devices:
        print "Device: %s" % dev.Interface
        print "   Type             %s" % c('device_type', dev.DeviceType)
        # print "   IPv4 address     %s" % socket.inet_ntoa(struct.pack('L', dev.Ip4Address))
        devicedetail = dev.SpecificDevice()
        if not callable(devicedetail.HwAddress):
            print "   MAC address      %s" % devicedetail.HwAddress
        print "   IPv4 config"
        print "      Addresses"
        for addr in dev.Ip4Config.Addresses:
            print "         %s/%d -> %s" % (socket.inet_ntoa(struct.pack('L', addr[0])), addr[1], 
                                            socket.inet_ntoa(struct.pack('L', addr[2])))
        print "      Routes"
        for addr in dev.Ip4Config.Routes:
            print "         %s/%d -> %s (%d)" % (socket.inet_ntoa(struct.pack('L', route[0])), route[1], 
                                                 socket.inet_ntoa(struct.pack('L', route[2])), socket.ntohl(route[3]))
        print "      Nameservers"
        for ns in dev.Ip4Config.Nameservers:
            print "         %s" % socket.inet_ntoa(struct.pack('L', ns))
