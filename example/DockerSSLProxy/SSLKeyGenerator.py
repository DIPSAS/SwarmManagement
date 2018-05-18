from OpenSSL import crypto, SSL
from time import gmtime
from pprint import pprint
from os.path import exists, join
import os

CERT_FILE = "site.crt"
KEY_FILE = "site.key"

# See: https://www.linux.org/threads/creating-a-self-signed-certificate-with-python.9038/
def create_self_signed_cert(cert_dir):
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    if not exists(join(cert_dir, CERT_FILE)) \
        or not exists(join(cert_dir, KEY_FILE)):

        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "NO"
        cert.get_subject().ST = "Norway"
        cert.get_subject().L = "Norway"
        cert.get_subject().O = "DIPS AS"
        cert.get_subject().OU = "DIPS"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        open(join(cert_dir, CERT_FILE), "wb").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), "wb").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

if __name__ == "__main__":
    cwd = os.getcwd()
    create_self_signed_cert(cwd)
