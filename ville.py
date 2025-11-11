import math as m
class ville:
    def __init__(self,city,lat,lon,x_km,y_km):
        self.city=city
        self.lat= lat
        self.lon = lon
        self.x_km = x_km
        self.y_km = y_km
    def print_ville(self):
        print(self.city,end=" |")

def distance_ville(ville1,ville2):
    dx=ville1.x_km-ville2.x_km
    dy=ville1.y_km-ville2.y_km
    return m.sqrt(dx**2+dy**2)
def haversine(ville1,ville2):
    R=6371
    lon1=m.radians(ville1.lon)
    lon2=m.radians(ville2.lon)
    lat1=m.radians(ville1.lat)
    lat2=m.radians(ville2.lat)
    dlat=lat1-lat2
    dlon=lon1-lon2
    return 2*R*m.asin(m.sqrt(m.sin(dlat/2)**2+m.cos(lat1)*m.cos(lat2)*m.sin(dlon/2)**2))
def print_citys(villes):
    for ville in villes:
        ville.print_ville()





ville_list=[ville("Algiers",36.7538,3.0588,275.165320849382,4086.8360949087823),
            ville("Oran",35.6971,-0.6417,-57.726424215067475,3969.336415923478),
            ville("Constantine",36.365,6.6147,595.0490544731289,4043.6035074293786),
            ville("Annaba",36.902,7.7639,698.4294607501363,4103.315183037506),
            ville("Blida",36.4736,2.8298,254.5648048056692,4055.6792764629777),
            ville("Batna",35.5559,6.1744,555.4402893462875,3953.6356922812665),
            ville("Sétif",36.1911,5.4137,487.00879347531685,4024.2667096858895),
            ville("Béjaïa",36.75,5.0736,456.4138785999164,4086.413554187533),
            ville("Tlemcen",34.8936,-1.3169,-118.46646103914969,3879.9912923645743),
            ville("Sidi Bel Abbès",35.2,-0.6333,-56.97077209818019,3914.061417888468),
            ville("Jijel",36.82,5.7666,518.7551782431169,4094.1971990526526),
            ville("Skikda",36.8769,6.9,620.7142388716933,4100.524190378728),
            ville("Tizi Ouzou",36.7167,4.0497,364.30528306647767,4082.71076313027),
            ville("Biskra",34.8519,5.7331,515.7415656341022,3875.3544639234965),
            ville("Mostaganem",35.9372,0.0906,8.150247832141364,3996.034317810836),
            ville("Chlef",36.1654,1.3345,120.04973214119921,4021.4090000711244),
            ville("Bordj Bou Arréridj",36.0756,4.7578,428.0049573483684,4011.4236956584430),
            ville("Mascara",35.3964,0.1403,12.621189523724432,3935.900101481459),
            ville("El Oued",33.3698,6.8677,617.808576565091,3710.5524631435956),
            ville("Médéa",36.2644,2.7535,247.7009647439431,4032.417297808936)
            ]
