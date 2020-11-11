from django.shortcuts import render
from django.http import HttpResponse
from SPARQLWrapper import SPARQLWrapper, JSON
import json

# Create your views here.
def index(request):
#     print(request.GET['test'])
    return HttpResponse("<b>Hello Django<b>")

def test1(request):
#     price_lte = request.GET['price_lte']

    return render(request,"test1.html",{"gets":"get1s"})


#http://127.0.0.1:8000/nlp/query1/?type=Ambassador&birth=192&death=200
def query1(request):

    try:
        url = request.get_full_path()
        splitedUrl = url.split('?')
        params = splitedUrl[1].split('&')
        dictParams = {}

        for i in params:
            para = i.split('=')
            print(para)
            dictParams[para[0]] = para[1]

        print(dictParams['type'])
        print(dictParams['birth'])
        print(dictParams['death'])
    except ValueError:
        print('valueError')

    sql =        """
                 SELECT ?name ?birth ?death ?person
                 WHERE {
                  ?person a dbo:"""+dictParams['type']+""" .
                  ?person dbo:birthDate ?birth .
                  filter (contains(str(?birth),\""""+dictParams['birth']+"""\"))
                  ?person dbo:deathDate ?death .
                  filter (contains(str(?death),\""""+dictParams['death']+"""\"))
                  ?person foaf:name ?name .
             }
             limit 100
                 """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sql)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

#     SELECT ?name ?birth ?death ?person
#     WHERE {
#       ?person a dbo:Ambassador .
#       ?person dbo:birthDate ?birth .
#       filter (contains(str(?birth),"190"))
#       ?person dbo:deathDate ?death .
#       filter (contains(str(?death),"199"))
#       ?person foaf:name ?name .
#     }


    return HttpResponse(json.dumps(results), content_type="application/json")
#     return render(request,"query.html",{"gets":results})

#http://127.0.0.1:8000/nlp/query2/?type=Ambassador&country=G
def query2(request):

    try:
        url = request.get_full_path()
        splitedUrl = url.split('?')
        params = splitedUrl[1].split('&')
        dictParams = {}

        for i in params:
            para = i.split('=')
            print(para)
            dictParams[para[0]] = para[1]

        print(dictParams['type'])
        print(dictParams['country'])


    except ValueError:
        print('valueError')

    sql =        """
    SELECT ?name ?birth ?person ?country
    WHERE {
      ?person a dbo:"""+dictParams['type']+""" .
      ?person dbo:birthDate ?birth .
      ?person foaf:name ?name .
      ?person dbo:country ?country.
      filter (contains(lcase(str(?country)),lcase(\""""+dictParams['country']+"""\")))

    }
    limit 100

                 """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sql)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

#     SELECT ?name ?person ?country ?birth
#     WHERE {
#       ?person a dbo:MusicalArtist .
#       ?person foaf:name ?name .
#       ?person dbo:country ?country.
#       ?person dbo:birthPlace ?birth
# filter(contains(str(?birth),"H"))
#     }


    return HttpResponse(json.dumps(results), content_type="application/json")

#http://127.0.0.1:8000/nlp/query3/?country=Taiwan&type=Town
def query3(request):

    try:
        url = request.get_full_path()
        splitedUrl = url.split('?')
        params = splitedUrl[1].split('&')
        dictParams = {}

        for i in params:
            para = i.split('=')
            print(para)
            dictParams[para[0]] = para[1]

        print(dictParams['country'])
        print(dictParams['type'])


    except ValueError:
        print('valueError')

    sql =        """
    SELECT  ?name ?country ?pop
    WHERE {
      ?pop a dbo:"""+dictParams['type']+""" .
      ?pop foaf:name ?name .
      ?pop dbo:country ?country .
      filter(contains(lcase(str(?country)),lcase(\""""+dictParams['country']+"""\")))
    }
                 """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sql)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

#     SELECT ?pop  ?name ?country
#     WHERE {
#       ?pop a dbo:Town .
#       ?pop foaf:name ?name .
#       ?pop dbo:country ?country .
#       filter(contains(str(?country),"Taiwan"))
#     }


    return HttpResponse(json.dumps(results), content_type="application/json")


#http://127.0.0.1:8000/nlp/query4/?number=5117&type=City&country=Taiwan (or type=Town)
def query4(request):

    try:
        url = request.get_full_path()
        splitedUrl = url.split('?')
        params = splitedUrl[1].split('&')
        dictParams = {}

        for i in params:
            para = i.split('=')
            print(para)
            dictParams[para[0]] = para[1]

        print(dictParams['number'])


    except ValueError:
        print('valueError')

    sql =        """
    SELECT  ?name ?country (xsd:integer(?population) as ?population) ?pop
    WHERE {
      ?pop a dbo:"""+dictParams['type']+""" .
      ?pop foaf:name ?name .
      ?pop dbo:country ?country .
      filter(contains(lcase(str(?country)),lcase(\""""+dictParams['country']+"""\")))
      ?pop dbo:populationTotal ?population
      filter(?population > """+dictParams['number']+""")
    }
                 """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sql)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

# dbo:Town or dbo:City
#     SELECT ?pop  ?name ?country (xsd:integer(?population) as ?population)
#     WHERE {
#       ?pop a dbo:Town .
#       ?pop foaf:name ?name .
#       ?pop dbo:country ?country .
#       filter(contains(str(?country),"Taiwan"))
#       ?pop dbo:populationTotal ?population
#       filter(?population > 5117)
#     }


    return HttpResponse(json.dumps(results), content_type="application/json")


#http://127.0.0.1:8000/nlp/query5/?type=Private&country=Taiwan
def query5(request):

    try:
        url = request.get_full_path()
        splitedUrl = url.split('?')
        params = splitedUrl[1].split('&')
        dictParams = {}

        for i in params:
            para = i.split('=')
            print(para)
            dictParams[para[0]] = para[1]

        print(dictParams['country'])
        print(dictParams['type'])


    except ValueError:
        print('valueError')

#     sql =        """
#      SELECT ?pop  ?name ?country ?type
#      WHERE {
#        ?pop a dbo:School .
#        ?pop foaf:name ?name .
#        ?pop dbp:country	 ?country.
#        filter(contains(str(?country),\""""+dictParams['country']+"""\"))
#        ?pop dbo:type ?type
#        filter(contains(str(?type),\""""+dictParams['type']+"""\"))
#      }
#                  """

    sql = """
         SELECT ?name ?country ?type ?pop
         WHERE {
           ?pop a dbo:School .
           ?pop foaf:name ?name .
           ?pop dbp:country	 ?country.
           filter(contains(lcase(str(?country)),lcase(\""""+dictParams['country']+"""\")))
           ?pop dbo:type ?type
           filter(contains(lcase(str(?type)),lcase(\""""+dictParams['type']+"""\")))
         }
    """
    print(sql)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sql)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


#       SELECT ?pop  ?name ?country ?type
#       WHERE {
#         ?pop a dbo:School .
#         ?pop foaf:name ?name .
#         ?pop dbp:country	 ?country.
#         filter(contains(str(?country),"Taiwan"))
#         ?pop dbo:type ?type
#         filter(contains(str(?type),"Public"))
#       }
    return HttpResponse(json.dumps(results), content_type="application/json")
