import googlemaps


def geocode_address(address):
    gmaps = googlemaps.Client(key="AIzaSyCs6iNDVPjAcoGLDpKhivAJ6R9VRqCfIUs")
    geocode_result = gmaps.geocode(address)
    return geocode_result
