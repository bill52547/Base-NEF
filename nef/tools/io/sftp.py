import paramiko
from contextlib import contextmanager
import os

home_path = os.environ['HOME']
pub_key_path = home_path + '/.ssh/nef_rsa.pub'
private_key_path = home_path + '/.ssh/nef_rsa'


def ssh_gen():
    import rsa
    if os.path.isfile(pub_key_path):
        return pub_key_path
    (pubkey, prvkey) = rsa.newkeys(1024)

    pub = pubkey.save_pkcs1()
    with open(pub_key_path, 'w') as pubfile:
        pubfile.write(pub)

    prv = prvkey.save_pkcs1()
    with open(private_key_path, 'w') as prvfile:
        prvfile.write(prv)
    return pub_key_path


if not os.path.isfile(pub_key_path):
    ssh_gen()

pkey = paramiko.RSAKey.from_private_key_file(pub_key_path)


@contextmanager
def ssh_connect(hostname = '127.0.0.1', port = 22, pkey = None):
    if pkey is None:
        pkey = pkey
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = hostname, port = port, pkey = pkey)
        yield ssh
    except ValueError(f'Connect to {hostname}:{port} failed'):
        pass
    finally:
        ssh.close()


@contextmanager
def build_transport(hostname = '127.0.0.1', port = 22, pkey = None):
    if pkey is None:
        pkey = pkey
    transport = paramiko.Transport((hostname, port))
    try:
        transport.connect(pkey = pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        yield sftp
    except ValueError(f'Build transport to {hostname}:{port} failed'):
        pass
    finally:
        transport.close()


def sftp_upload(local_path, remote_path, *, hostname = '127.0.0.1', port = 22, pkey = None):
    if pkey is None:
        pkey = pkey
    with build_transport(hostname, port, pkey) as sftp:
        sftp.put(local_path, remote_path)
    return remote_path


def sftp_download(remote_path, local_path, *, hostname = '127.0.0.1', port = 22, pkey = None):
    if pkey is None:
        pkey = pkey
    with build_transport(hostname, port, pkey) as sftp:
        sftp.get(remote_path, local_path)
    return local_path
