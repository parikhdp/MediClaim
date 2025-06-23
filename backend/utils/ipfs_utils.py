import ipfshttpclient

client = ipfshttpclient.connect()

def upload_to_ipfs(data: bytes) -> str:
    try:
        res = client.add_bytes(data)
        return res
    except Exception as e:
        print(f"IPFS upload error: {e}")
        return ""
def download_from_ipfs(ipfs_hash: str) -> bytes:
    try:
        data = client.cat(ipfs_hash)
        print("Downloaded size:", len(data))
        return data
    except Exception as e:
        print(f"IPFS download error: {e}")
        return b""
