from app import app
from flask import render_template, request, redirect, url_for, jsonify
from app.utils.Utils import FileFolder, Persistence, os, Command, Hash

@app.route('/', methods=['GET'])
def index(messagem = None):
    
    p = Persistence()
    
    # nome, key
    systems = []
        
    key = "keyless system"
    
    keyPath = os.path.join(p.BaseSystem, p.NameKey)
    
    if os.path.exists(keyPath):
        keyHash = Hash.calculateHashFile(keyPath)
    
        storedKeys = Command.listdir(p.FolderKeys)

        key = "Key is not in the storage system"
        
        for storedKey in storedKeys:
            hashStorageKey = Hash.calculateHashFile(os.path.join(p.FolderKeys, storedKey))
            if keyHash == hashStorageKey:
                key = storedKey
    
    systemBase = ["Base System", key]
    
    for system in Command.listdir(p.LocateFolderSystems):
        
        key = "keyless system"
        
        keyPath = os.path.join(p.LocateFolderSystems, system, p.NameKey)
        
        if os.path.exists(keyPath):
            keyHash = Hash.calculateHashFile(keyPath)
        
            storedKeys = Command.listdir(p.FolderKeys)

            key = "Key is not in the storage system"
            
            for storedKey in storedKeys:
                hashStorageKey = Hash.calculateHashFile(os.path.join(p.FolderKeys, storedKey))
                if keyHash == hashStorageKey:
                    key = storedKey 
                    
        
        info = [system, key]
        systems.append(info)
        
    search = request.args.get('search')
    if search: 
        searchSystems = []
        for system in systems: 
            if str(search).lower() in str(system[0]).lower(): 
                searchSystems.append(system)
        
        return render_template('index.html', systems=searchSystems, systemBase=systemBase, messagem = messagem, search=search)
    
    return render_template('index.html', systems=systems, systemBase=systemBase, messagem = messagem, search="")

@app.route('/configure', methods=['GET', 'POST'])
def initConfigs(): 
    
    p = Persistence()
    
    if request.method == 'POST':    
        systemBase = request.form['systemBase']
        folderKeys = request.form['folderKeys']
        nameKey = request.form['nameKey']
        fileExecute = request.form['fileExecute']
        folderDebugs = request.form['folderDebugs']
        locateFolderSystems = request.form['locateFolderSystems']
        internalDebug = request.form['internalDebug']
        
    
        p.BaseSystem = systemBase
        p.FolderKeys = folderKeys
        p.NameKey = nameKey
        p.FileExecute = fileExecute
        p.FolderDebugs = folderDebugs
        p.LocateFolderSystems = locateFolderSystems
        p.InternalDebug = internalDebug
        
        
        return redirect('/')
    
    return render_template('initConfig.html', systemBase=p.BaseSystem, folderKeys=p.FolderKeys, nameKey=p.NameKey, fileExecute=p.FileExecute, folderDebugs=p.FolderDebugs, locateFolderSystems=p.LocateFolderSystems, internalDebug=p.InternalDebug)

@app.route('/path', methods=['GET'])
def path():
    return FileFolder().getPathFolder()

@app.route('/path-file', methods=['GET'])
def pathFile():
    return FileFolder().getPathFile()

@app.route('/new-system', methods=['GET'])
def newSystem():
    p = Persistence()
    nameFolder = request.args.get('systemName')
    pathNewSystem = os.path.join(p.LocateFolderSystems, nameFolder)

    if Command.mkdir(pathNewSystem):
        Command.copy(p.BaseSystem, pathNewSystem)
    
    return redirect('/')

@app.route('/remove-system', methods=['POST'])
def removeSystem():
    p = Persistence()
    systemName = request.form['systemName']
    pathDeleteSystem = os.path.join(p.LocateFolderSystems, systemName)

    print(systemName)
    print(p.LocateFolderSystems)
    print(pathDeleteSystem)

    Command.remove(pathDeleteSystem)
    
    return redirect('/')

@app.route('/edit-system', methods=['GET', 'POST'])
def editSystem():
    p = Persistence()
    
    if request.method == 'POST':
        
        EditSystemName = request.form["editSystemName"] 
        EditSystemNameOld = request.form["editSystemNameOld"] 
        debugSystem = request.form["debugSystem"] 
        debugSystemOld = request.form["debugSystemOld"] 
        keySelect = request.form["keySelect"] 
        keySystemOld = request.form["keySystemOld"]
        
        if EditSystemName != EditSystemNameOld:
            EditSystemNameOldPath = os.path.join(p.LocateFolderSystems, EditSystemNameOld)
            EditSystemNamePath = os.path.join(p.LocateFolderSystems, EditSystemName)
            Command.move(EditSystemNameOldPath, EditSystemNamePath)
        
        def changeKey():
            if keySelect != keySystemOld:
                keyPathSystemOld = os.path.join(p.LocateFolderSystems, EditSystemName, p.NameKey)
                Command.removeFile(keyPathSystemOld)
                
                keyPathSystemNew = os.path.join(p.FolderKeys, keySelect)
                system = os.path.join(p.LocateFolderSystems, EditSystemName)
                
                Command.copyFile(keyPathSystemNew, system)

                os.rename(os.path.join(system, keySelect), os.path.join(system, p.NameKey))
        
        changeKey()
        
        if debugSystem != debugSystemOld:
            print(debugSystem)
            Command.remove(os.path.join(p.LocateFolderSystems, EditSystemName))
            Command.mkdir(os.path.join(p.LocateFolderSystems, EditSystemName))
            Command.copy(p.BaseSystem, os.path.join(p.LocateFolderSystems, EditSystemName))
            Command.copy(os.path.join(p.FolderDebugs, debugSystem), os.path.join(p.LocateFolderSystems, EditSystemName))
            Command.mkdir(os.path.join(p.LocateFolderSystems, EditSystemName, debugSystem))
            changeKey()
        return redirect('/')
    
    systemName = request.args.get('systemName')
    systemKey = os.path.join(p.LocateFolderSystems, systemName, p.NameKey)
    
    listDebugs = Command.listdir(p.FolderDebugs)
    listKeys = Command.listdir(p.FolderKeys)
    
    debugSystem = ""
    keySelect = ""
    
    for debug in listDebugs: 
        if os.path.exists(os.path.join(p.LocateFolderSystems, systemName, debug)):
            debugSystem = debug
            break  
        
    print(listDebugs)  
    
    if os.path.exists(systemKey):
        if listKeys: 
            hashKeySystem = Hash.calculateHashFile(systemKey)
            
            for key in listKeys: 
                outerHash = Hash.calculateHashFile(os.path.join(p.FolderKeys, key))
                if hashKeySystem == outerHash:
                    keySelect = key
                    break
                
    return jsonify({
        'systemName': systemName,
        'keySelect': keySelect,
        'debugSystem': debugSystem,
        'listKeys': listKeys,
        'listDebugs': listDebugs
    })

@app.route('/edit-system-base', methods=['GET', 'POST'])
def editSystemBase():
    p = Persistence()
    
    if request.method == 'POST':
        
        keySelect = request.form["keySelectBase"] 
        keySystemOld = request.form["keySystemOldBase"]
        
        def changeKey():
            if keySelect != keySystemOld:
                keyPathSystemOld = os.path.join(p.BaseSystem, p.NameKey)
                Command.removeFile(keyPathSystemOld)
                
                keyPathSystemNew = os.path.join(p.FolderKeys, keySelect)
                system = os.path.join(p.BaseSystem)
                
                Command.copyFile(keyPathSystemNew, system)

                os.rename(os.path.join(system, keySelect), os.path.join(system, p.NameKey))
        
        changeKey() 
        return redirect('/')
    
    systemName = request.args.get('systemName')
    systemKey = os.path.join(p.BaseSystem, p.NameKey)
    
    listDebugs = Command.listdir(p.FolderDebugs)
    listKeys = Command.listdir(p.FolderKeys)
    
    keySelect = ""
            
    print(listDebugs)  
    
    if os.path.exists(systemKey):
        if listKeys: 
            hashKeySystem = Hash.calculateHashFile(systemKey)
            
            for key in listKeys: 
                outerHash = Hash.calculateHashFile(os.path.join(p.FolderKeys, key))
                if hashKeySystem == outerHash:
                    keySelect = key
                    break
                
    return jsonify({
        'systemName': "System Base",
        'keySelect': keySelect,
        'listKeys': listKeys,
    })


@app.route('/add-key', methods=['POST'])
def addKey():
    p = Persistence()
    nameKey = request.form['nameKey']
    keyFile = request.form['keyFile']
    
    hashKeyFile = Hash.calculateHashFile(keyFile)
    
    storedKeys = Command.listdir(p.FolderKeys)
    
    for storedKey in storedKeys:
        hashStorageKey = Hash.calculateHashFile(os.path.join(p.FolderKeys, storedKey))
        if hashKeyFile == hashStorageKey:
            return index(messagem="Key already exists")
    
    keyFileName = keyFile.split("/")[-1]
    
    if Command.copyFile(keyFile, p.FolderKeys): 
        Command.removeFile(keyFile)
        if nameKey == "":
            nameKey = keyFileName
            
        os.rename(os.path.join(p.FolderKeys, keyFileName), os.path.join(p.FolderKeys, nameKey))
    
    return redirect('/')


# debugFolder debugName add-debug
@app.route('/add-debug', methods=['POST'])
def AddDebug():
    p = Persistence()
    
    debugName = request.form['debugName']
    debugFolder = request.form['debugFolder']
    
    if p.InternalDebug: 
        if not os.path.exists(os.path.join(p.FolderDebugs, p.InternalDebug)):
            return index(messagem="Internal Debug not found")
        Command.descompact(debugFolder, p.FolderDebugs)
        Command.copy(os.path.join(p.FolderDebugs, p.InternalDebug), os.path.join(p.FolderDebugs, debugName))
        Command.remove(os.path.join(p.FolderDebugs, p.InternalDebug))
        Command.removeFile(debugFolder)
        return redirect('/')
    
    Command.mkdir(os.path.join(p.FolderDebugs, debugName))
    Command.descompact(debugFolder, os.path.join(p.FolderDebugs, debugName))
    Command.removeFile(debugFolder)
    
    return redirect('/')

@app.route('/start', methods=['POST'])
def start():
    p = Persistence()
    executeSystem = request.form['executeSystem']
    
    os.system("start " + os.path.join(p.LocateFolderSystems, executeSystem, p.FileExecute))
    
    pass

@app.route('/start-base', methods=['POST'])
def startBase():
    p = Persistence()
        
    os.system("start " + os.path.join(p.BaseSystem, p.FileExecute))
    
    pass


@app.route("/debug", methods=['GET'])
def Debug():
    p = Persistence()
    
    listdebugs = Command.listdir(p.FolderDebugs)
    
    search = request.args.get('search')
    
    if search:
        listdebugsNew = [debug for debug in listdebugs if search.lower() in str(debug).lower()]
        return render_template('debugs.html', debugs=listdebugsNew, search=search)
    
    return render_template('debugs.html', debugs=listdebugs, search="")

@app.route("/remove-debug", methods=['POST'])
def RemoveDebug():
    p = Persistence()
    debug = request.form['debug']
    Command.remove(os.path.join(p.FolderDebugs, debug))
    return redirect('/debug')