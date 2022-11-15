#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spacy
import json
nlp = spacy.load('pl_spacy_model') 

print('start')

class TokenInfo():
    def __init__(self, token, startIndex, tag = "o", selectedMeshPolTags = list(), isLastInSentence = False):
        self.token = token
        self.startIndex = startIndex
        self.tag = tag
        self.meshPolTags = list()
        self.selectedMeshPolTags = selectedMeshPolTags
        self.medicineTags = list()
        self.isLastInSentence = isLastInSentence
    def __str__(self):
        token = self.token
        return f"TokenInfo[{token.text}, {token.lemma_}, {token.tag_}, {self.meshTag}, {self.tag}]"
    def setLastInSentence(self, isLast):
        self.isLastInSentence = isLast
    def addMeshPolTag(self, meshPolTag):
        self.meshPolTags.append(meshPolTag)
    def removeMeshPolTag(self, meshPolTagToRemove):
        print(f"removing: {meshPolTagToRemove} idx: {self.startIndex}")
        self.meshPolTags = list(filter(lambda meshPolTag: meshPolTag.name != meshPolTagToRemove.name, self.meshPolTags))
    def addMedicineTag(self, medicineTag):
        self.medicineTags.append(medicineTag)
    def meshPolTagsLen(self):
        return len(self.meshPolTags)
    def getFirstMeshPolTagStr(self):
        if len(self.meshPolTags) > 0:
            meshPolTag = self.meshPolTags[0]
            return f"{meshPolTag.getIdx()}"
        else:
            return "o"
    def getMeshPolTagsCells(self, selectedMeshPolTags):
        tags = list(map(lambda tag: self.getTagIdxByName(tag.name), selectedMeshPolTags))
        return "\t".join(tags)
    def getMedicineTagCell(self):
        if len(self.medicineTags) > 0:
            return self.medicineTags[0].place
        else:
            return "o"
    
    def getTagIdxByName(self, tagName):
        tags = self.getMeshPolTagsByName(tagName)
        if len(tags) > 0:
            tag = tags[0]
            return f"{tag.getIdx()}"
        else:
            return "o"
    
    def getMeshPolTagsByName(self, name):
        return list(filter(lambda tag: tag.name == name, self.meshPolTags))
    
        
class TagInfo():
    def __init__(self, start, end, tag):
        self.start = int(start)
        self.end = int(end)
        self.tag = tag
    def __str__(self):
        return f"TagInfo[{self.start}, {self.end}, {self.tag}]"
    
class MeshPol():
    def __init__(self, name, tag, normalized = list()):
        print(f"init start {name} {tag}")
        self.name = name.strip()
        self.tag = tag.strip()
        self.tokens = list()
        self.normalized = list(map(lambda n: n.strip(), normalized))
        self.importanceIndex = -1
        print(f"init finish {self}")
        
    def __str__(self):
        tokensStr = ','.join([str(x) for x in self.normalized])
        return f"MeshPol[{self.name},{self.tag}, [{tokensStr}] ]"
    
    def isFirstNormalized(self, normalizedNamePart):
        return len(self.normalized) > 0 and self.normalized[0] == normalizedNamePart
    
    def normalize(self):
        self.tokens = nlp(self.name)
        self.normalized = list(map(lambda token: token.lemma_, self.tokens))
        
    def toDict(self):
        return dict(name=self.name, tag=self.tag, normalized=self.normalized)
    def getImportanceIndex(self, selectedMeshPolTagsNames):
        if self.importanceIndex == -1:
            self.importanceIndex = selectedMeshPolTagsNames.index(self.tag)
        return self.importanceIndex
    
def meshPolFromDict(dic):
    name = dic['name']
    tag = dic['tag']
    normalized = dic['normalized']
    return MeshPol(name, tag, normalized)
#    normalized = dic[]
    
    
        
class Medicine():
    def __init__(self, idx, name, nameDod, substance, normalized = list()):
        self.idx = idx
        self.name = name
        self.nameDod = nameDod
        self.substance = substance
        if len(normalized) > 0:
            self.tokens = list()
            self.normalized = normalized
        else:
            self.tokens = nlp(self.name)
            self.normalized = list(map(lambda token: token.lemma_, self.tokens))
        print(f"medicine created: {self.idx}, {self.name}")
    def __str__(self):
        return f"Medicine[{self.idx}, {self.name}, {self.nameDod}, {self.substance}]"
    def isFirstNormalized(self, normalizedNamePart):
        return len(self.normalized) > 0 and self.normalized[0] == normalizedNamePart
    def toDict(self):
        return dict(idx=self.idx, name=self.name, nameDod=self.nameDod, substance=self.substance, normalized=self.normalized)
    
def medicineFromDict(dic):
    idx = dic['idx']
    name = dic['name']
    nameDod = dic['nameDod']
    substance = dic['substance']
    normalized = dic['normalized']
    return Medicine(idx, name, nameDod, substance, normalized)


def tagId(name):
    name = name.replace(',','').lower()
    splitted = name.split()
    splitted = map(lambda s: s[0:4], splitted)
    return "_".join(splitted)
    
class MeshPolTag():
    def __init__(self, name, place = "b"):
        self.name = name.strip()
        self.id = tagId(name).strip()
        self.place = place.strip()
    def __str__(self):
        return f"MeshPolTag[{self.name}, {self.id}, {self.place}]"
    def getImportanceIndex(self, selectedMeshPolTagsNames):
        return selectedMeshPolTagsNames.index(self.name)
    def getIdx(self):
        return f"{self.place}-{self.id}"
    
class MedicineTag():
    def __init__(self, place = "b"):
        self.place = place

def textFromFile(filename):
    file = open(filename)
    toReturn = file.read()
    file.close()
    return toReturn

def linesFromFile(filename):
    lines = []
    f = open(filename, "r")
    for x in f:
        lines.append(x)
    f.close()
    return lines

def sentencesFrom(text):
    return text.split("\n")
    
def writeToFile(lines, filename):
    outF = open(filename, "w")
    outF.writelines(lines)
    outF.close()
    

def tokenToLine(tokenInfo):
    token = tokenInfo.token
    cells = []
    cells.append(token.text.strip())
    cells.append(token.lemma_.strip())
    cells.append(token.tag_)
#    cells.append(str(token.idx))
#    cells.append(str(token.idx + len(token.text)))
    cells.append(tokenInfo.tag)
    cells.append(tokenInfo.getFirstMeshPolTagStr())
    cells.append(tokenInfo.getMedicineTagCell())
    emptyLine = ""
    if tokenInfo.isLastInSentence:
        emptyLine = "\n"
    return "\t".join(cells) + "\n" + emptyLine
    
def writeToCsv(filename, tokens = []):
    lines = map(tokenToLine, tokens)
    writeToFile(lines, f"{filename}.csv")
    
def lineToTag(line):
    splitted = line.split()
    tagInfo = TagInfo(splitted[2], splitted[3], splitted[1])
    return tagInfo

def lineToMeshPol(line):
    splitted = line.split("\t")
    return MeshPol(splitted[0], splitted[2])
    
def tagsFromFile(filename):
    lines = filter(lambda line: line.startswith('T'), linesFromFile(filename))
    return list(map(lineToTag, lines))

def meshPolsFromFile(filename, selectedMeshPolTags = list()):
    lines = list(linesFromFile(filename))
    allMeshPols = list(map(lineToMeshPol, lines))
    selectedMeshPolTagsNames = list(map(lambda selectedMeshPolTag: selectedMeshPolTag.name, selectedMeshPolTags))
    selectedMeshPols = list(filter(lambda meshPol: meshPol.tag in selectedMeshPolTagsNames, allMeshPols))
    selectedMeshPolsLen = len(selectedMeshPols)
    for idx,selectedMeshPol in enumerate(selectedMeshPols, start = 0):
        selectedMeshPol.normalize()
        print(f"MeshPols normalized: {idx+1}/{selectedMeshPolsLen}")
    return selectedMeshPols

def writeMeshPolsToCache(meshPols, meshpolFileCache):
    listToSave = list(map(lambda meshPol: meshPol.toDict(), meshPols))
    fileObject = open(meshpolFileCache, 'w')
    json.dump(listToSave, fileObject)
    fileObject.close()
    
def writeMedicinesToCache(medicines, medicinesFileCache):
    listToSave = list(map(lambda medicine: medicine.toDict(), medicines))
    fileObject = open(medicinesFileCache, 'w')
    json.dump(listToSave, fileObject)
    fileObject.close()
    

def meshPolsFromCache(meshpolFileCache):
    print("reading meshPols from cache")
    fileObject = open(meshpolFileCache, 'r')
    dictObjects = json.load(fileObject)
    meshPols = list(map(lambda dic: meshPolFromDict(dic), dictObjects))
    return meshPols

def medicinesFromCache(medicinesFileCache):
    print("reading medicines from cache")
    fileObject = open(medicinesFileCache, 'r')
    dictObjects = json.load(fileObject)
    medicines = list(map(lambda dic: medicineFromDict(dic), dictObjects))
    return medicines

def getMeshPols(isMeshPolFromCache, meshpolFile, selectedMeshPolTags, meshpolFileCache):
    if isMeshPolFromCache:
        return meshPolsFromCache(meshpolFileCache)
    else:
        meshPols = meshPolsFromFile(meshpolFile, selectedMeshPolTags)
        writeMeshPolsToCache(meshPols, meshpolFileCache)
        return meshPols

def getMedicines(isMedicinesFromCache, medicinesFile, medicinesFileCache):
    if isMedicinesFromCache:
        return medicinesFromCache(medicinesFileCache)
    else:
        medicines = medicinesFromFile(medicinesFile)
        writeMedicinesToCache(medicines, medicinesFileCache)
        return medicines

def findTag(idx, tags):
    tagsWithIdx = list(filter(lambda tag: tag.start <= idx < tag.end, tags))
    if len(tagsWithIdx) > 0:
        tagInfo = tagsWithIdx[0]
        tagBase = tagInfo.tag
        if tagInfo.start == idx:
            return f"b-{tagBase}"
        else:
            return f"i-{tagBase}"
    else:
        return 'o'
    
def findSuspectMeshPols(tokenInfo, meshPols):
    normalizedNamePart = tokenInfo.token.lemma_
    return list(filter(lambda meshPol: meshPol.isFirstNormalized(normalizedNamePart), meshPols))

def isMeshPolForTokenInfos(meshPol, tokens, startIdx):
    meshPolNormalizedPartNames = meshPol.normalized
    meshPolNormalizedPartNamesLen = len(meshPolNormalizedPartNames)
    tokensLen = len(tokens)
    if startIdx + meshPolNormalizedPartNamesLen <= tokensLen:
        for normalizedIdx,meshPolNormalizedPartName in enumerate(meshPolNormalizedPartNames, start = 0):
            normalizedToken = tokens[startIdx + normalizedIdx].token.lemma_
            if meshPolNormalizedPartName != normalizedToken:
                return False
        return True
    else:
        return False

def getMeshPolTag(meshPolTag, idx):
    if (idx == 0):
        return MeshPolTag(meshPolTag.tag, "b")
    else:
        return MeshPolTag(meshPolTag.tag, "i")
    
def sortAndFilterBySelectedMeshPolTags(meshPolsForTokenInfos, selectedMeshPolTagsNames):
    filteredMeshPolsForTokenInfos =  list(filter(lambda mp: mp.tag in selectedMeshPolTagsNames, meshPolsForTokenInfos))
    def index(meshPol):
        return meshPol.getImportanceIndex(selectedMeshPolTagsNames)
    def negativeSize(meshPol):
        return -len(meshPol.normalized)
    sortedBySelectedMeshPolTagsNamesMeshPols = sorted(filteredMeshPolsForTokenInfos, key=index)
    if len(sortedBySelectedMeshPolTagsNamesMeshPols) > 0:
        mostImportantIndex = sortedBySelectedMeshPolTagsNamesMeshPols[0].getImportanceIndex(selectedMeshPolTagsNames)
        sortedBySelectedMeshPolTagsNamesMeshPols = list(filter(lambda meshPol: meshPol.getImportanceIndex(selectedMeshPolTagsNames) == mostImportantIndex, sortedBySelectedMeshPolTagsNamesMeshPols))
        sortedBySelectedMeshPolTagsNamesMeshPols = sorted(filteredMeshPolsForTokenInfos, key=negativeSize)
    return sortedBySelectedMeshPolTagsNamesMeshPols

def isRelatedToTag(tagForToken, tokenIdx, tokens, tagIdx):
    if len(tokens) > tokenIdx:
        token = tokens[tokenIdx]
        meshTags = token.getMeshPolTagsByName(tagForToken.name)
        if len(meshTags) == 0:
            return False
        else:
            meshTag = meshTags[0]
            if meshTag.place == "b" and tagIdx > 0:
                return False
            else:
                return True
    else:
        return False
    
def getRelatedIndexesForMeshTag(tagForToken, tokenIdx, tokens):
    def getRelatedIndexes(tagForToken, tokenIdx, tokens, relatedIndexes, tagIdx):
        if isRelatedToTag(tagForToken, tokenIdx, tokens, tagIdx):
            relatedIndexes.append(tokenIdx)
            return getRelatedIndexes(tagForToken, tokenIdx + 1, tokens, relatedIndexes, tagIdx + 1)
        else:
            return relatedIndexes
    return getRelatedIndexes(tagForToken, tokenIdx, tokens, list(), 0)

def isNotMoreImportant(importance, meshPolTag, selectedMeshPolTagsNames):
    return meshPolTag.getImportanceIndex(selectedMeshPolTagsNames) >= importance

def meshPolTagsAreNotMoreImportant(importance, tokens, tokenIdx, selectedMeshPolTagsNames):
    return all(isNotMoreImportant(importance, meshPolTag, selectedMeshPolTagsNames) for meshPolTag in tokens[tokenIdx].meshPolTags)

def isEqual(elem1, elem2):
    return elem1 == elem2

def isTagImportant(tagForToken, tokenIdx, tokens, selectedMeshPolTagsNames, relatedIndexes = list()):
    if len(relatedIndexes) == 0:
        relatedIndexes = getRelatedIndexesForMeshTag(tagForToken, tokenIdx, tokens)
    importance = tagForToken.getImportanceIndex(selectedMeshPolTagsNames)
    resultList = list(map(lambda idx: meshPolTagsAreNotMoreImportant(importance, tokens, idx, selectedMeshPolTagsNames), relatedIndexes))
    result =  all(isEqual(elem, True) for elem in resultList)
    return result
    
def removeMeshPolTag(tokens, tagForToken, idx):
    tokens[idx].removeMeshPolTag(tagForToken)
    
def removeMeshTag(tagForToken, tokenIdx, tokens, relatedIndexes = list()):
    if len(relatedIndexes) == 0:
        relatedIndexes = getRelatedIndexesForMeshTag(tagForToken, tokenIdx, tokens)
    print(f"removeTag({tagForToken}, {tokenIdx}, tokens)")
    [removeMeshPolTag(tokens, tagForToken, idx) for idx in relatedIndexes]
    
def removeNotImportantMeshTags(tokens, selectedMeshPolTagsNames):
    print("removeNotImportantMeshTags")
    for tokenIdx, token in enumerate(tokens, start = 0):
        tagsForToken = token.meshPolTags
        for tagForToken in tagsForToken:
            indexesForTag = getRelatedIndexesForMeshTag(tagForToken, tokenIdx, tokens)
            if not isTagImportant(tagForToken, tokenIdx, tokens, selectedMeshPolTagsNames, indexesForTag):
                removeMeshTag(tagForToken, tokenIdx, tokens)
        
    
def updateWithMeshTags(tokens, meshPols, selectedMeshPolTagsNames):
    tokensLen = len(tokens)
    for tokenIdx,tokenInfo in enumerate(tokens, start = 0):
        suspectMeshPols = findSuspectMeshPols(tokenInfo, meshPols)
#        trzeba posortować suspectMeshPols po tym jak zostały wybrane tagi w pliku distinctMeshPolTags
        meshPolsForTokenInfos = list(filter(lambda meshPol: isMeshPolForTokenInfos(meshPol, tokens, tokenIdx), suspectMeshPols))
        meshPolsForTokenInfos = sortAndFilterBySelectedMeshPolTags(meshPolsForTokenInfos, selectedMeshPolTagsNames)
        if len(meshPolsForTokenInfos) > 0:
            print(f"found meshPols: {len(meshPolsForTokenInfos)}")
            mostImportantMeshPol = meshPolsForTokenInfos[0]
            meshPolNormalizedPartNames = mostImportantMeshPol.normalized
            for normalizedIdx,meshPolNormalizedPartName in enumerate(meshPolNormalizedPartNames, start = 0):
                meshPolTag = getMeshPolTag(mostImportantMeshPol, normalizedIdx)
                print(meshPolTag)
                tokenInfoToUpdate = tokens[tokenIdx+normalizedIdx]
                tokenInfoToUpdate.addMeshPolTag(meshPolTag)
        print(f"Tokens updated with mesh tags: {tokenIdx+1}/{tokensLen}") 
    print("updateWithMeshTags                FINISHED")
    removeNotImportantMeshTags(tokens, selectedMeshPolTagsNames)
    return tokens

def tokensFromAnnotations1(text, tags):
    doc = nlp(text)
    tokens = []
    for idx, sentence in enumerate(doc.sents, start = 0):
        for wordIdx,token in enumerate(sentence, start = 0):
            tag = findTag(token.idx, tags)
            tokens.append(TokenInfo(token, token.idx, tag, selectedMeshPolTags))
        tokens[len(tokens) - 1].setLastInSentence(True)
        print(f"Sentences normalized and with tags: {idx+1}")
    return tokens
    

def tokensFromAnnotations0(sentences, tags):
    tokens = []
    textLen = 0
    sentencesLen = len(sentences)
    for idx,sentence in enumerate(sentences, start = 0):
        
        doc = nlp(sentence)
        for wordIdx,token in enumerate(doc, start = 0):
            tag = findTag(textLen+token.idx, tags)
            tokens.append(TokenInfo(token, textLen, tag, selectedMeshPolTags))
        textLen += len(sentence) + 1
        print(f"Sentences normalized and with tags: {idx+1}/{sentencesLen}")
        
    return tokens

def lineToMedicine(line):
    splitted = line.split("\t")
    subst = ""
    if len(splitted) > 3:
        subst = splitted[3]
    return Medicine(splitted[0], splitted[1], splitted[2], subst)

def medicinesFromFile(filename):
    lines = list(linesFromFile(filename))
    lines = lines[1:]
    return list(map(lineToMedicine, lines))

def findSuspectMedicines(tokenInfo, medicines):
    normalizedNamePart = tokenInfo.token.lemma_
    return list(filter(lambda medicine: medicine.isFirstNormalized(normalizedNamePart), medicines))

def isMedicineForTokenInfos(medicine, tokens, startIdx):
    medicineNormalizedPartNames = medicine.normalized
    medicineNormalizedPartNamesLen = len(medicineNormalizedPartNames)
    tokensLen = len(tokens)
    if startIdx + medicineNormalizedPartNamesLen <= tokensLen:
        for normalizedIdx,medicineNormalizedPartName in enumerate(medicineNormalizedPartNames, start = 0):
            normalizedToken = tokens[startIdx + normalizedIdx].token.lemma_
            if medicineNormalizedPartName != normalizedToken:
                return False
        return True
    else:
        return False
    
def getMedicineTag(medicine, idx):
    if (idx == 0):
        return MedicineTag("b-medicine")
    else:
        return MedicineTag("i-medicine")

def updateWithMedicines(tokens, medicines):
    tokensLen = len(tokens)
    for tokenIdx,tokenInfo in enumerate(tokens, start = 0):
        suspectMedicines = findSuspectMedicines(tokenInfo, medicines)
        medicinesForTokenInfos = list(filter(lambda medicine: isMedicineForTokenInfos(medicine, tokens, tokenIdx), suspectMedicines))
        if (len(medicinesForTokenInfos) > 0):
            print(f"found medicines: {len(medicinesForTokenInfos)}")
        for medicine in medicinesForTokenInfos:
            medicineNormalizedPartNames = medicine.normalized
            for normalizedIdx,medicineNormalizedPartName in enumerate(medicineNormalizedPartNames, start = 0):
                medicineTag = getMedicineTag(medicine, normalizedIdx)
                tokenInfoToUpdate = tokens[tokenIdx+normalizedIdx]
                tokenInfoToUpdate.addMedicineTag(medicineTag)
        print(f"Tokens updated with medicine tags: {tokenIdx+1}/{tokensLen}")
    print("updateWithMedicineTags                FINISHED")
    return tokens
                
        
    
# PARAMS
isMeshPolsFromCache = True
isMedicinesFromCache = True

# INPUT FILES
distinctMeshPolTags = "distinctMeshPolTags.txt"
meshpolFile = "meshpol.tsv"
meshpolFileCache = "meshpol_cache.json"
annotations = "patient_36002.ann"
full_text = "patient_36002.txt"
medicinesFile = "rpo.tsv"
medicinesFileCache = "medicines_cache.json"

# OUTPUT FILE
tokensFile = "tokens_20200320e"


selectedMeshPolTags = list(map(lambda line: MeshPolTag(line), linesFromFile(distinctMeshPolTags)))
print(len(selectedMeshPolTags))


meshPols = getMeshPols(isMeshPolsFromCache, meshpolFile, selectedMeshPolTags, meshpolFileCache)
medicines = getMedicines(isMedicinesFromCache, medicinesFile, medicinesFileCache)

tags = tagsFromFile(annotations)
text = textFromFile(full_text)
#sentences = sentencesFrom(text)

tokens = tokensFromAnnotations1(text, tags)
#tokens = tokensFromAnnotations0(sentences, tags)
tokens = updateWithMeshTags(tokens, meshPols, list(map(lambda meshTag: meshTag.name, selectedMeshPolTags)))
tokens = updateWithMedicines(tokens, medicines)

writeToCsv(tokensFile, tokens)
        




    