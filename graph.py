import spacy
from spacy.lang.ru import Russian
import networkx as nx
import matplotlib.pyplot as plt


def getSentences(text):
    nlp = Russian()
    nlp.add_pipe('sentencizer')
    document = nlp(text)
    return [sent.text for sent in document.sents]


def printToken(token):
    print(token.text, "->", token.dep_)


def appendChunk(original, chunk):
    return original + ' ' + chunk


def isRelationCandidate(token):
    deps = ["ROOT", "adj", "attr", "agent", "amod", "obl"]
    return any(subs in token.dep_ for subs in deps)


def isConstructionCandidate(token):
    deps = ["compound", "prep", "conj", "mod"]
    return any(subs in token.dep_ for subs in deps)


def processSubjectObjectPairs(tokens):
    subject = ''
    object = ''
    relation = ''
    subjectConstruction = ''
    objectConstruction = ''
    for token in tokens:
        printToken(token)
        if "punct" in token.dep_:
            continue
        if isRelationCandidate(token):
            relation = appendChunk(relation, token.lemma_)
        if isConstructionCandidate(token):
            if subjectConstruction:
                subjectConstruction = appendChunk(
                    subjectConstruction, token.text)
            if objectConstruction:
                objectConstruction = appendChunk(
                    objectConstruction, token.text)
        if "subj" in token.dep_:
            subject = appendChunk(subject, token.text)
            subject = appendChunk(subjectConstruction, subject)
            subjectConstruction = ''
        if "obl" in token.dep_:
            object = appendChunk(object, token.text)
            object = appendChunk(objectConstruction, object)
            objectConstruction = ''

    print(subject.strip(), ",", relation.strip(), ",", object.strip())
    return (subject.strip(), relation.strip(), object.strip())


def processSentence(sentence):
    tokens = nlp_model(sentence)
    return processSubjectObjectPairs(tokens)


def printGraph(triples):
    G = nx.Graph()
    for triple in triples:
        G.add_node(triple[0])
        G.add_node(triple[1])
        G.add_node(triple[2])
        G.add_edge(triple[0], triple[1])
        G.add_edge(triple[1], triple[2])

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()


if __name__ == "__main__":

    text = "Студент СГТУ - Мистер студенчество Саратовской области. Победители представят область на всероссийском конкурсе Студент технического университета стал I вице-мистером России. Студенты нашего вуза творческие, креативные, амбициозные молодые люди Студенты Политеха презентовали концепцию парковой зоны посёлка «Юбилейный». Команда студентов подробно рассказала о концепции проектной разработки Студенты СГТУ - Вице-мисс и Первый Вице-мистер студенчество Саратовской области. Студенты вуза выступили на региональном конкурсе интеллекта, творчества, спорта и красоты Студенты СГТУ впервые привезли в Саратов гран-при студвесны. Ребят встречали с фейерверками Студенты СГТУ поздравили ветеранов Великой отечественной войны. Вокалисты исполнили фронтовые песни Студенты СГТУ разработали проект для управления движением колонны беспилотных автомобилей. предложенное решение - возможная реализация беспилотных транспортных средств в будущем Студенты СГТУ стали победителями отборочного этапа Международного инженерного чемпионата «CASE-IN». Команды СГТУ заняли призовые места Студенты УРБАСа стали дипломантами международного конкурса. Серия проектов была создана в рамках интенсива Laboratorium"
    sentences = getSentences(text)
    # sentences = ["Мартин живет в Лондоне", "Мартин правит миром", "Лондон является столицей Великобритании", "В Москве растут цветы"]
    nlp_model = spacy.load('ru_core_news_sm')

    triples = []
    print(text)
    for sentence in sentences:
        triples.append(processSentence(sentence))

    printGraph(triples)
