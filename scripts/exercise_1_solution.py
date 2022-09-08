# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 07:34:16 2022

@author: simonc
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 18:53:58 2022

@author: simonc
"""
from pathlib import Path
import os
import dlite
from dlite.triplestore import (
    en, Literal, Triplestore,
    EMMO, OWL, RDF, RDFS, SKOS, XSD,
)
from dlite.mappings import instantiate
from dlite.mappings import mapping_route

import pint
from scipy import integrate

import matplotlib.pyplot as plt

import ontopy


# set directory information
thisdir = Path(__file__).resolve().parent
entitydir = thisdir.parent / 'entities'
outputdir = thisdir / 'output'
ontodir = thisdir.parent / 'ontologies'
datadir = thisdir.parent / 'data'

# Add unit Ah to unit registry
ureg = pint.UnitRegistry()
ureg.define('Ah  = A * h')

ts = Triplestore("rdflib")
ts.parse(f"{ontodir}/battinfo-merged.ttl")

# BattINFO namespace
BATTINFO = ts.bind(
    'battinfo', 'https://big-map.github.io/BattINFO/ontology/BattINFO#')

# Dict mapping prefLabel to IRI
d = {o.value: s for s, o in ts.subject_objects(SKOS.prefLabel)}

# # Add ontological concept for time stamp
TimeStamp = BATTINFO['EMMO_d597d7b7-2d35-5d97-9cf1-622b8dfb7d24']
d['TimeStamp'] = TimeStamp
ts.add((TimeStamp, RDF.type, OWL.Class))
ts.add((TimeStamp, RDFS.subClassOf, OWL.Class))
ts.add((TimeStamp, SKOS.prefLabel, en('TimeStamp')))
ts.add((TimeStamp, d['elucidation'],
        en('The time of a data point in a time serie.')))

# Add timeFormat data property
timeFormat = BATTINFO['EMMO_eeef9cd8-9e15-54a7-93fe-a1c20c8372cb']
d['timeFormat'] = timeFormat
ts.add((timeFormat, RDF.type, OWL.DatatypeProperty))
ts.add((timeFormat, RDF.type, OWL.FunctionalProperty))
ts.add((timeFormat, RDFS.subPropertyOf, d['hasSymbolData']))
ts.add((timeFormat, RDFS.domain, TimeStamp))
ts.add((timeFormat, RDFS.range, XSD.string))
ts.add((timeFormat, SKOS.prefLabel, en('timeFormat')))
ts.add((timeFormat, d['elucidation'],
        en('A time format string according to strptime().')))

# Add TimeStamp subclass for times in seconds since start
TimeStamp_S = BATTINFO['EMMO_fb0da9cf-6b89-5072-bf5a-66e32c8cd6f6']
d['TimeStamp_S'] = TimeStamp_S
ts.add((TimeStamp_S, RDF.type, OWL.Class))
ts.add((TimeStamp_S, RDFS.subClassOf, TimeStamp))
ts.add((TimeStamp_S, SKOS.prefLabel, en('TimeStamp_S')))
ts.add((TimeStamp_S, timeFormat, Literal('%S')))
ts.add((TimeStamp_S, d['elucidation'],
        en('The time of a data point in seconds since start.')))

## Team A ##

raw_data_A = dlite.Instance.from_location(
    driver='csv',
    location=datadir / 'TeamA.csv',
)

datamodel = "SimpleTimeSeriesBatteryData.json"
datamodel_path = os.path.join(entitydir, datamodel)
SimpleTimeSeriesBatteryData = dlite.Instance.from_url(f'json://{datamodel_path}')

# # map raw data properties
# ts.add_mapsTo(d['TimeStamp_S'], raw_data_A, 'Zeit,_s')
# ts.add_mapsTo(d['CellVoltage'], raw_data_A, 'Spannung,_V')
# ts.add_mapsTo(d['InstantaneousCurrent'], raw_data_A, 'Strom,_A')

processed_data_A = SimpleTimeSeriesBatteryData(dims=[raw_data_A.rows])
processed_data_A.test_time = raw_data_A.get_property('Zeit,_s')
processed_data_A.battery_voltage = raw_data_A.get_property('Spannung,_V')
processed_data_A.battery_current = raw_data_A.get_property('Strom,_A')

ts.add_mapsTo(d['TimeStamp_S'], processed_data_A, 'test_time')
ts.add_mapsTo(d['CellVoltage'], processed_data_A, 'battery_voltage')
ts.add_mapsTo(d['InstantaneousCurrent'], processed_data_A, 'battery_current')

## Team B ##

raw_data_B = dlite.Instance.from_location(
    driver='csv',
    location=datadir / 'TeamB.csv',
)

# map raw data properties
# ts.add_mapsTo(d['TimeStamp_S'], raw_data_B, 'Time_/_s')
# ts.add_mapsTo(d['CellVoltage'], raw_data_B, 'Voltage_/_V')
# ts.add_mapsTo(d['InstantaneousCurrent'], raw_data_B, 'Current_/_A')

processed_data_B = SimpleTimeSeriesBatteryData(dims=[raw_data_A.rows])
processed_data_B.test_time = raw_data_B.get_property('Time_/_s')
processed_data_B.battery_voltage = raw_data_B.get_property('Voltage_/_V')
processed_data_B.battery_current = raw_data_B.get_property('Current_/_A')

ts.add_mapsTo(d['TimeStamp_S'], processed_data_B, 'test_time')
ts.add_mapsTo(d['CellVoltage'], processed_data_B, 'battery_voltage')
ts.add_mapsTo(d['InstantaneousCurrent'], processed_data_B, 'battery_current')

## Team C ##

raw_data_C = dlite.Instance.from_location(
    driver='csv',
    location=datadir / 'TeamC.csv',
)

# map raw data properties
# ts.add_mapsTo(d['TimeStamp_S'], raw_data_C, 'temps')
# ts.add_mapsTo(d['CellVoltage'], raw_data_C, 'tension')
# ts.add_mapsTo(d['InstantaneousCurrent'], raw_data_C, 'courant')

processed_data_C = SimpleTimeSeriesBatteryData(dims=[raw_data_A.rows])
processed_data_C.test_time = raw_data_C.get_property('temps')
processed_data_C.battery_voltage = raw_data_C.get_property('tension')
processed_data_C.battery_current = raw_data_C.get_property('courant')

ts.add_mapsTo(d['TimeStamp_S'], processed_data_C, 'test_time')
ts.add_mapsTo(d['CellVoltage'], processed_data_C, 'battery_voltage')
ts.add_mapsTo(d['InstantaneousCurrent'], processed_data_C, 'battery_current')

## Team D ##

raw_data_D = dlite.Instance.from_location(
    driver='csv',
    location=datadir / 'TeamD.csv',
)

# map raw data properties
# ts.add_mapsTo(d['TimeStamp_S'], raw_data_D, 'tiempo')
# ts.add_mapsTo(d['CellVoltage'], raw_data_D, 'Voltaje')
# ts.add_mapsTo(d['InstantaneousCurrent'], raw_data_D, 'corriente')

processed_data_D = SimpleTimeSeriesBatteryData(dims=[raw_data_A.rows])
processed_data_D.test_time = raw_data_D.get_property('tiempo')
processed_data_D.battery_voltage = raw_data_D.get_property('Voltaje')
processed_data_D.battery_current = raw_data_D.get_property('corriente')

ts.add_mapsTo(d['TimeStamp_S'], processed_data_D, 'test_time')
ts.add_mapsTo(d['CellVoltage'], processed_data_D, 'battery_voltage')
ts.add_mapsTo(d['InstantaneousCurrent'], processed_data_D, 'battery_current')


# query the triplestore
query_text = """
PREFIX map: <http://emmo.info/domain-mappings#>
PREFIX emmo: <http://emmo.info/emmo#>
PREFIX electrochemistry: <https://big-map.github.io/BattINFO/ontology/electrochemistry#>

SELECT *
WHERE {
   ?subject map:mapsTo electrochemistry:EMMO_4ebe2ef1_eea8_4b10_822d_7a68215bd24d .
}
"""

query_text2 = """
PREFIX map: <http://emmo.info/domain-mappings#>
PREFIX emmo: <http://emmo.info/emmo#>
PREFIX electrochemistry: <https://big-map.github.io/BattINFO/ontology/electrochemistry#>
PREFIX custom: <https://big-map.github.io/BattINFO/ontology/BattINFO#>

SELECT *
WHERE {
   ?subject map:mapsTo custom:EMMO_fb0da9cf-6b89-5072-bf5a-66e32c8cd6f6 .
}
"""

query_text3 = """
PREFIX map: <http://emmo.info/domain-mappings#>
PREFIX emmo: <http://emmo.info/emmo#>
PREFIX electrochemistry: <https://big-map.github.io/BattINFO/ontology/electrochemistry#>
PREFIX custom: <https://big-map.github.io/BattINFO/ontology/BattINFO#>

SELECT *
WHERE {
   ?subject map:mapsTo ?object .
}
"""

query_result = ts.query(query_text)
query_result2 = ts.query(query_text2)
query_result3 = ts.query(query_text3)

for row in query_result3:
    print(f"{row.subject}" "     mapsTo     " f"{row.object}")

# for row in query_result:
#     print(f"{row.subject}")
    
# for row in query_result2:
#     print(f"{row.subject}")
    
for row1 in query_result:
    for row2 in query_result2:
        txt1 = row1.subject
        split_text_1 = txt1.split('#')
        inst_name_1 = split_text_1[0]
        txt2 = row2.subject
        split_text_2 = txt2.split('#')
        inst_name_2 = split_text_2[0]
        if inst_name_2 == inst_name_1:
            inst = dlite.get_instance(inst_name_1)
            voltage = inst.get_property(split_text_1[1])
            time = inst.get_property(split_text_2[1])
            plt.plot(time, voltage, label = split_text_1[0])
            plt.ylabel('battery voltage')
            plt.xlabel('test time')
            
        
    
plt.legend()
plt.show()

onto = ontopy.get_ontology("C:\\Users\\simonc\\Documents\\GitHub\\BattINFO\\battinfo.ttl")
onto.load()


print()
print("Battery Voltage is elucidated as:")
print(onto.CellVoltage.EMMO_967080e5_2f42_4eb2_a3a9_c58143e835f9)
print("it is a")
print(onto.CellVoltage.is_a)

print()
print("Battery Current is elucidated as:")
print(onto.InstantaneousCurrent.EMMO_967080e5_2f42_4eb2_a3a9_c58143e835f9)
print("it is a")
print(onto.InstantaneousCurrent.is_a)



collection = dlite.Collection()
collection.add(label='TeamA', inst=processed_data_A)
collection.add(label='TeamB', inst=processed_data_B)
collection.add(label='TeamC', inst=processed_data_C)
collection.add(label='TeamD', inst=processed_data_D)

# save the collection
collection.save('json', f'{thisdir}/output/team_data_collection.json', 'mode=w')
#raw_data.save('json', f'{thisdir}/output/data_extended.json', 'mode=w')
