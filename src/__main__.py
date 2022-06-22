import sys
import json
import argparse


def reverseCoordinates(coords):
    if isinstance(coords, (list, tuple)) and isinstance(coords[0], float):
        coords = list(coords[::-1])

    elif isinstance(coords, (list, tuple)):
        for i in range(0, len(coords)):
            if isinstance(coords[i], (list, tuple)):
                coords[i] = reverseCoordinates(coords[i])
    return coords


def main():
    parser = argparse.ArgumentParser(
        description="Reverse coordinate pairs within GeoJSON file",
        usage="reversecoords [<filename>]",
    )
    parser.add_argument("filename", help="Path to file or - for stdin")
    args = parser.parse_args()
    filename = args.filename

    if filename == "-":
        filehandle = sys.stdin
    else:
        filehandle = open(filename, "rb")

    geojson = json.load(filehandle)

    if filehandle is not sys.stdin:
        filehandle.close()

    if "type" in geojson and geojson["type"] == "FeatureCollection":
        for feature in geojson["features"]:
            feature["geometry"]["coordinates"] = reverseCoordinates(
                feature["geometry"]["coordinates"]
            )
    elif "type" in geojson and geojson["type"] == "Feature":
        geojson["geometry"]["coordinates"] = reverseCoordinates(
            geojson["geometry"]["coordinates"]
        )

    sys.stdout.write(json.dumps(geojson))
