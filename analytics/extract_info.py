# -*- coding: utf-8 -*-
import json
import re
import unicodedata
import optparse
from engine import utils, db_interface
from pymongo import MongoClient
from bson.code import Code


db = db_interface.DBInterface('192.168.1.144')
db.connect()




neighbourhoods = [u'pueblo de el hatillo', u'el calvario', u'la lagunita', u'alto hatillo', \
                u'la boyera', u'las marias', u'oripoto', u'los pomelos', \
                u'lomas del sol', u'el solar del hatillo', u'los naranjos', \
                u'los geranios', u'la cabana', u'cerro verde', u'llano verde', \
                u'hacienda el encantado', u'colinas', u'vista el valle', u'los olivitos', \
                u'el cigarral', u'los pinos', u'lomas de la lagunita', u'bosques de la lagunita', \
                u'villanueva', u'loma linda', u'el manantial', u'cantarrana', u'el arroyo', \
                u'La Unión', u'El Otro Lado',u'Corralito', u'Turgua', u'La Hoyadita',\
                u'Plan de la Madera', u'Sabaneta', u'La Mata', u'Caicaguana', u'La Tiama',\
                u'El Peñón de Gavilán', u'Gavilán', u'El Hatillo, Altos del Halcón', u'Caserío Los Naranjos Rural'\
                u'Petare', u'Leoncio Martínez', u'La Dolorita', u'Filas de Mariches', u'Cuacaguita',\
                u'Leoncio Martinez', u'Santa Eduvigis', u'Sebucan', u'La Carlota', u'Campo Claro', \
                u'Santa Cecilia', u'Agua de Maiz', u'Los Chorros', u'Dos Caminos', u'Barrio La Lucha', \
                u'Los Ruices', u'Montecristo', u'Boleita', u'Los Cortijos', u'Petare', u'La California Norte', \
                u'El Marques', u'Horizonte', u'La California Sur', u'Colinas de los Ruices', u'Macaracuay', \
                u'El Llanito', u'Colinas de la California', u'Palo Verde', u'Lomas del Avila', u'La Urbina', \
                u'Terrazas del Avila', u'Urb. Miranda', u'Petare Casco Colonial', u'Buena Vista', \
                u'Barrio Dorado', u'Lebrun', u'Campo Rico', u'Barrio San Miguel', u'Pablo VI', \
                u'Primero de Noviembre', u'El Esfuerzo', u'19 de Abril', u'El Sucre', u'12 de octubre', \
                u'24 de Julio', u'El Torre', u'Barrio Buenos Aires', u'Callejon Torres', u'La Alcabala', \
                u'Antonio Jose de Sucre', u'Este del Avila', u'Barrio Bolivar', u'Julian Blanco', \
                u'Vista Hermosa', u'La Parrilla', u'24 de Marzo', u'La Bombilla', u'Colinas de La Bombilla', \
                u'5 de Julio', u'Jose Felix Ribas I', u'Jose Felix Ribas', u'Jose Felix Ribas III', \
                u'Jose Felix Ribas IV', u'Las Vegas de Petare', u'El Progreso', u'Guaicaipuro', \
                u'Maca I Mirador', u'Nazareno', u'Brisas del Zulia', u'El Morro', u'El Obelisco', \
                u'Maca Este', u'Altos del Naranjal', u'Colinas del 12 de Febrero', u'Maca II', \
                u'Las Praderas', u'Amapola', u'El Mosquito', u'Ali Primera', u'Casa de Tablas', \
                u'Calle Camacaro', u'Calle La Fila', u'Maca III San Blas', u'La Invasion', \
                u'La Machaca', u'Barrio El Encantado', u'Las Pomarrosas', u'Republicas Unidas', \
                u'Petare Barrio Union I Las Casitas', u'Carpintero', u'Valle Alto', u'Cuatricentenario', \
                u'Calle Lara', u'Barrio Nuevo', u'La Cueva del Humo', u'Barrio Union II El Tanque', \
                u'La Virgen', u'El Cerrito', u'Mesuca', u'Primero de Mayo', u'El Carmen', u'La 37', \
                u'San Pascual',u'Los Aguacaticos',u'Padre Jesus Misias Petare Barrio Union III Vuelta El Beso',u'Vuelta Los Manolos',u'Vuelta Los Granares',u'Vuelta El Fiscal',u'Tinaquillo',u'La planada',u'El Copon',u'Caruto',u'La Gruta',u'Callejon guanare',u'Vuelta Enrique',u'Sector La Ceiba',u'Caucaguita Urb. Turumo',u'Urb. Maturin',u'Parque Caiza',u'Brisas del Avila',u'Barrio Negro Primero',u'Los Guacamayos. Barrio Turumo',u'Los Aguacaticos',u'Barrio Ramon Brazon',u'Barrio 19 de marzo',u'Barrio El Placer',u'El Carmen',u'Chimborazo',u'Barrio Quintana', \
                u'Barrio El Cuji',u'Plan de la I',u'La Cuesta',u'Los Sapitos',u'Barrio El Progreso',u'Barrio El Tanque',u'Barrio Cubo Negro',u'Barrio Sandokan',u'Barrio Luis Herrera Campins',u'Barrio 28 de Junio',u'Barrio San Benito',u'Barrio Los Gochos',u'La Pipotera',u'Cuarta Terraza',u'Urb. Manuel Carvajal',u'La Dolorita',u'Terrazas de Guaicoco',u'El Limoncito',u'La Lira',u'Barrio 17 de Diciembre',u'La Invasion',u'Juan XXIII',u'La Frontera',u'Las Tapias',u'Los Chorritos',u'La Ensenada',u'El Tanque',u'Terminal',u'Sector Las Barracas', \
                u'San Isidro',u'Fila de Mariches',u'Monsenor Arias',u'Guayabitos',u'Altos de Capitolio',u'Ciudad Mariches',u'Hacienda Caballo Mocho',u'Brisas de Valle Fresco',u'Apolo 8',u'Brisas del Tamanaco',u'12 de Enero',u'La Veguita',u'Mirador del Este',u'La Oscurana',u'Altos de Tomas',u'Las Flores',u'Brisas Bolivarianas',u'Loma Larga',u'Los Unidos',u'Plan de la avioneta',u'El Rincon',u'Santa Isabel',u'Arboleda',u'Aurora',u'El Morichal',u'Barrio El Winche',u'Chaguarama']

parser = optparse.OptionParser()
parser.add_option('-f', '--filename', help='stopword file', type='string', dest='filename' )
parser.add_option('-p', '--processsing', help='processing type: location or category', type='string', dest='processing' )
(opts, args) = parser.parse_args()

mandatories = ['filename', 'processing']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)

# preprocess
if opts.processing == 'location':
    loc_count = 0
    prep_count = 0
    regexes = map(lambda x: "(" + x.lower() +")", neighbourhoods)

    tweets, ids = db.get_tweets()
    tweets = utils.preprocess(tweets)

    for (text, id) in zip(tweets, ids):
        for reg in regexes:
            out = re.search(reg, text)
            if out:
                location = out.group(1)
                if db.set_neighbourhood(id, location):
                    loc_count += 1
        utils.remove_stopwords(text,opts.filename)
        if db.set_preprocessed_text(id, text):
            prep_count += 1
    print "Locations inserted:", loc_count
    print "Preprocessed tweets inserted:", prep_count

if opts.processing == 'category':
    key_count = 0
    regexes = [r'(basura|aseo|reciclaje|recliclar|limpieza|desechos)', \
               r'(calle|hueco|semaforo|trafico|cola|congestion|vias|via|avenida|remolque|remolcar|ciclovia)', \
               r'(secuestro|robo|secuestraron|robaron|asaltaron|asalto|policia|inseguridad|inseguro)']

    categories = [0, 1, 2]

    tweets, ids = db.get_tweets()
    print len(tweets)
    tweets = utils.preprocess(tweets)

    for (text, id) in zip(tweets, ids):
        for (reg, cat) in zip(regexes, categories):
            if re.search(reg, text):
                if db.set_category(id, cat):
                    key_count += 1

    print "Found", key_count, "in-category tweets"


