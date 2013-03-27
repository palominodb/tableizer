import itertools

import yaml

from utilities.utils import flatten

def truth(string):
    trues  = [ "y", "t", "true", "yes" ]
    falses = [ "n", "f", "false", "no" ]
    if string == True or string.lower() in trues:
        return True
    elif string == False or string.lower() in falses:
        return False
     
class SemanticsError(Exception): 
    pass
class Unknown(SemanticsError):
    pass
class UnknownCluster(SemanticsError):
    pass
class ClusterMismatch(SemanticsError):
    pass
class EmptyDSN(SemanticsError):
    pass
class PrimaryMismatch(SemanticsError):
    pass
class FailoverMismatch(SemanticsError):
    pass

class DSN:
    
    def __init__(self, uri=None):
        self.uri = uri
        if uri is None:
            self.raw = None
        else:
            self.raw = yaml.load(open(uri, 'r'))
    
    # Open a uri as a dsn.
    def open(self, uri):
        self.uri = uri
        self.raw = yaml.load(open(uri, 'r'))
        
    # Initialize a DSN from a hash.
    # It's __HIGHLY__ recommended to run validate after calling this.
    def from_dict(self, dic):
        if not isinstance(dic, dict):
            raise Exception, "Provided argument must be a dictionary."
        self.raw = dic
        
    # Reloads the dsn from the source uri.
    # This is fundamentally a distructive operation.
    def reload(self):
        self.open(self.uri)
        
    # Validates a DSN as being 'syntatically' and semantically correct.
    # Syntax errors are thrown if required keys are missing from the dsn.
    # A SemanticsError is thrown if there is disagreement in the DSN.
    # Presently, that means missing clusters, or disagreement between servers and clusters.
    def validate(self):
        if not self.raw or self.raw is None:
            raise EmptyDSN, "Can not validate and empty dsn."
        host_keys = ['version', 'active', 'readfor', 'writefor']
        cluster_keys = ['active', 'servers', 'schemas', 'primary', 'failover']
        
        for srv, d in self.raw.get('servers', {}).items():
            for k in host_keys:
                if not k in d.keys():
                    raise SyntaxError, "Server '%s' missing required key '%s'" % (srv, k)
        
        
        for clu, d in self.raw.get('clusters', {}).items():
            for k in cluster_keys:
                if not k in d.keys():
                    raise SyntaxError, "Cluster '%s' missing required key '%s'" % (clu, k)
                    
            if d.get('primary') is not None or d.get('failover') is not None:
                if self.raw.get('servers', {}).get(d.get('primary')) is None or \
                        clu not in self.raw.get('servers', {}).get(d.get('primary'), {}).get('writefor', ''):
                    raise PrimaryMismatch, "Cluster (%s) list %s as the primary, but the server doesn't agree." % (clu, d.get('primary'))
                    
                if d.get('failover') is not None and \
                        clu not in self.raw.get('servers', {}).get(d.get('failover'), {}).get('readfor', ''):
                    raise FailoverMismatch, "Cluster (%s) lists %s as the failover, but the server doesn't agree." % (clu, d.get('failover'))
                    
        for srv, d in self.raw.get('servers', {}).items():
            l = [d.get('writefor'), d.get('readfor')]
            l = flatten(l)
            l = set(l)
            l = filter(None, l)
            
            for clu in l:
                if not clu in self.raw.get('clusters').keys():
                    raise UnknownCluster, "Server '%s' mentions unknown cluster '%s'" %  (srv, clu)
                if not srv in self.raw.get('clusters', {}).get(clu, {}).get('servers', ''):
                    raise ClusterMismatch, "Server '%s' claims to participate in '%s', but the cluster doesn't agree." % (srv, clu)
                    
    # Retrieve destinations for writes for a cluster.
    # How writes are load-balaned is application dependent.
    # This method will only return active hosts.
    def get_write_hosts(self, cluster):
        write_hosts = []
        
        for srv, d in self.raw.get('servers', {}).items():
            if isinstance(d.get('writefor'), list):
                if srv in d.get('writefor', '') and self.host_active(srv):
                    write_hosts.append(srv)
            elif isinstance(d.get('writefor'), str):
                if d.get('writefor') == cluster and self.host_active(srv):
                    write_hosts.append(srv)
        return write_hosts
        
    # Retrieve read hosts for a cluster.
    # Read load-balancing is application specific, but in general,
    # round-robin, or random selection is better than hammering the
    # first one in the list.
    def get_read_hosts(self, cluster):
        read_hosts = []
        
        for srv, d in self.raw.get('servers', {}).items():
            if isinstance(d.get('readfor'), list):
                if srv in d.get('readfor', '') and self.host_active(srv):
                    read_hosts.append(srv)
            elif isinstance(d.get('readfor'), str):
                if d.get('readfor') == cluster and self.host_active(srv):
                    read_hosts.append(srv)
        return read_hosts
        
    # Returns names of all the hosts defined.
    def get_all_hosts(self):
        return self.raw.get('servers', {}).keys()
        
    # Returns names of all defined clusters.
    def get_all_clusters(self):
        return self.raw.get('clusters', {}).keys()
        
    # Returns true or false depending on whether or not the
    # host is active. If there is no such host, 'None' is returned.
    def host_active(self, server):
        if server in self.raw.get('servers', {}).keys():
            return truth(self.raw.get('servers', {}).get(server, {}).get('active'))
        else:
            return None
            
    # Same as above, but with a cluster.
    def cluster_active(self, cluster):
        if cluster in self.raw.get('clusters', {}).keys():
            return truth(self.raw.get('clusters', {}).get(cluster, {}).get('active'))
        else:
            return None
            
    def server_ttt(self, server):
        if server in self.raw.get('servers', {}).keys():
            return truth(self.raw.get('servers', {}).get(server, {}).get('ttt'))
        else:
            return None
