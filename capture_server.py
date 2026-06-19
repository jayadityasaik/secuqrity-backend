from flask import Flask, jsonify
from flask_cors import CORS
import re
import subprocess

app = Flask(__name__)

CORS(app)

@app.route("/capture", methods=["GET"])
def capture():

    xml_request = "<PidOptions ver='1.0'><Opts fCount='1' fType='0' iCount='0' pCount='0' format='0' pidVer='2.0' timeout='10000' posh='UNKNOWN' env='P'/></PidOptions>"

    cmd = [
        "curl.exe",
        "-k",
        "-X",
        "CAPTURE",
        "-H",
        "Content-Type: text/xml",
        "-d",
        xml_request,
        "https://127.0.0.1:11100/capture"
    ]

    response = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60
    )

    xml = response.stdout

    match = re.search(
        r"<Data[^>]*>(.*?)</Data>",
        xml,
        re.DOTALL
    )

    if (
        'errCode="0"' not in xml
        or not match
        or len(match.group(1).strip()) < 100
    ):

        return jsonify({
            "success": False,
            "xml": xml
        })

    return jsonify({
        "success": True,
        "fingerprint": match.group(1),
        "xml": xml
    })

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )