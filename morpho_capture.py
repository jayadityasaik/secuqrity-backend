import subprocess
import re

def capture_fingerprint():

    cmd = [
        "curl.exe",
        "-k",
        "-X",
        "CAPTURE",
        "-H",
        "Content-Type: text/xml",
        "-d",
        "<PidOptions ver='1.0'><Opts fCount='1' fType='0' iCount='0' pCount='0' format='0' pidVer='2.0' timeout='10000' posh='UNKNOWN' env='P'/></PidOptions>",
        "https://127.0.0.1:11100/capture"
    ]

    response = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60
    )

    xml = response.stdout

    if 'errCode="0"' not in xml:
        raise Exception("Fingerprint capture failed")

    match = re.search(
        r"<Data type=\"X\">(.*?)</Data>",
        xml,
        re.DOTALL
    )

    if not match:
        raise Exception("Fingerprint data not found")

    return match.group(1)