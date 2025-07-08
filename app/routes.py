from app import app
from flask import render_template, request, redirect, url_for, jsonify
from app.utils.Utils import FileFolder, Persistence, os, Command, Hash

@app.route('/', methods=['GET'])
def index():
    p = Persistence()
    
    messagem = request.args.get('error') if request.args.get('error') is not None or request.args.get('error') != "" else ""    
    sucess = request.args.get('sucess') if request.args.get('sucess') is not None or request.args.get('sucess') != "" else ""    
    
    
    if not p.validate():
        return redirect('/configure')
        
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
    searchValue = ""
    if search:
        searchValue = search
        searchSystems = []
        for system in systems: 
            if str(search).lower() in str(system[0]).lower(): 
                searchSystems.append(system)
    
        
        systems = searchSystems    
    
    
    return render_template('index.html', systems=systems, systemBase=systemBase, messagem = messagem, sucess = sucess, search=searchValue)

@app.route('/configure', methods=['GET', 'POST'])
def initConfigs(): 
    try: 
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
            
            
            return redirect(url_for('index', sucess="Configurações salvas com sucesso!"))
        
        return render_template('initConfig.html', systemBase=p.BaseSystem, folderKeys=p.FolderKeys, nameKey=p.NameKey, fileExecute=p.FileExecute, folderDebugs=p.FolderDebugs, locateFolderSystems=p.LocateFolderSystems, internalDebug=p.InternalDebug)

    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/path', methods=['GET'])
def path():
    try:
        return FileFolder.getPathFolder()
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/path-file', methods=['GET'])
def pathFile():
    try:
        return FileFolder.getPathFile()
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/new-system', methods=['GET'])
def newSystem():
    try: 
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        nameFolder = request.args.get('systemName')
        pathNewSystem = os.path.join(p.LocateFolderSystems, nameFolder)

        if os.path.exists(pathNewSystem):
            raise Exception("Ja existe um sistema com esse nome.")

        if Command.mkdir(pathNewSystem):
            Command.copy(p.BaseSystem, pathNewSystem)
        
        return redirect(url_for('index', sucess="Sistema criado com sucesso!"))
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/remove-system', methods=['POST'])
def removeSystem():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        systemName = request.form['systemName']
        pathDeleteSystem = os.path.join(p.LocateFolderSystems, systemName)


        Command.remove(pathDeleteSystem)
        
        return redirect(url_for('index', sucess="Sistema removido com sucesso!"))
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/edit-system', methods=['GET', 'POST'])
def editSystem():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        if request.method == 'POST':
            
            EditSystemName = request.form["editSystemName"] 
            EditSystemNameOld = request.form["editSystemNameOld"] 
            debugSystem = request.form["debugSystem"] 
            debugSystemOld = request.form["debugSystemOld"] 
            keySelect = request.form["keySelect"] 
            keySystemOld = request.form["keySystemOld"]

            EditSystemNameOldPath = os.path.join(p.LocateFolderSystems, EditSystemName)

            
            if EditSystemName != EditSystemNameOld:
                if os.path.exists(EditSystemNameOldPath):
                    raise Exception("Ja existe um sistema com esse nome.")
                EditSystemNameOldPath = os.path.join(p.LocateFolderSystems, EditSystemNameOld)
                EditSystemNamePath = os.path.join(p.LocateFolderSystems, EditSystemName)
                os.rename(EditSystemNameOldPath, EditSystemNamePath)
            
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
                Command.remove(os.path.join(p.LocateFolderSystems, EditSystemName))
                Command.mkdir(os.path.join(p.LocateFolderSystems, EditSystemName))
                Command.copy(p.BaseSystem, os.path.join(p.LocateFolderSystems, EditSystemName))
                if debugSystem != "":
                    Command.copy(os.path.join(p.FolderDebugs, debugSystem), os.path.join(p.LocateFolderSystems, EditSystemName))
                    Command.mkdir(os.path.join(p.LocateFolderSystems, EditSystemName, debugSystem))
                changeKey()
            return redirect(url_for('index', sucess="Sistema editado com sucesso!"))
        
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
        
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/edit-system-base', methods=['GET', 'POST'])
def editSystemBase():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
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
            return redirect(url_for('index', sucess="Sistema editado com sucesso!"))
        
        systemName = request.args.get('systemName')
        systemKey = os.path.join(p.BaseSystem, p.NameKey)
        
        listDebugs = Command.listdir(p.FolderDebugs)
        listKeys = Command.listdir(p.FolderKeys)
        
        keySelect = ""
                
        
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
        
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/add-key', methods=['POST'])
def addKey():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        nameKey = request.form['nameKey']
        keyFile = request.form['keyFile']

        temp = os.path.join(p.FolderKeys, nameKey)
        if os.path.exists(temp):
            raise Exception("Já existe uma chave com esse nome.")
        
        if not os.path.isfile(keyFile):
            raise Exception("A chave que passou deve ser um arquivo.")
        
        hashKeyFile = Hash.calculateHashFile(keyFile)
        
        storedKeys = Command.listdir(p.FolderKeys)
        
        for storedKey in storedKeys:
            hashStorageKey = Hash.calculateHashFile(os.path.join(p.FolderKeys, storedKey))
            if hashKeyFile == hashStorageKey:
                return redirect(url_for('index', error="Key already exists"))
        
        keyFileName = keyFile.split("/")[-1]
        
        if Command.copyFile(keyFile, p.FolderKeys): 
            Command.removeFile(keyFile)
            if nameKey == "":
                nameKey = keyFileName
                
            os.rename(os.path.join(p.FolderKeys, keyFileName), os.path.join(p.FolderKeys, nameKey))
        
        return redirect(url_for('index', sucess="Chave adicionada com sucesso!"))
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))
    
@app.route('/add-debug', methods=['POST'])
def AddDebug():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        debugName = request.form['debugName']
        debugFolder = request.form['debugFolder']
        
        temp = "_"
        while True:
            if os.path.exists(temp): 
                temp += "_"
                continue
            break

        folderDebug = os.path.join(p.FolderDebugs, temp)
        folderName = os.path.join(p.FolderDebugs, debugName)

        if os.path.exists(folderName): 
            raise Exception("Nome do Debug já fornecido anteriormente. Tente outro nome.")
        
        if not os.path.exists(debugFolder):
            raise Exception("O caminho para o debug nao existe.")
        Command.mkdir(folderDebug)
        Command.descompact(debugFolder, folderDebug)
        Command.mkdir(folderName)
        Command.move(os.path.join(folderDebug, p.InternalDebug), os.path.join(folderName))
        Command.remove(folderDebug)
        Command.removeFile(debugFolder)

        return redirect(url_for('index', sucess="Debug adicionado com sucesso!"))
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/start', methods=['POST'])
def start():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        executeSystem = request.form['executeSystem']
        
        os.system("start " + os.path.join(p.LocateFolderSystems, executeSystem, p.FileExecute))
        
        return redirect(url_for('index', sucess="Sistema iniciado com sucesso!"))
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/start-base', methods=['POST'])
def startBase():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
            
        os.system("start " + os.path.join(p.BaseSystem, p.FileExecute))
        
        return redirect(url_for('index', sucess="Sistema iniciado com sucesso!"))
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route("/debug", methods=['GET'])
def Debug():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        listdebugs = Command.listdir(p.FolderDebugs)
        
        search = request.args.get('search')
        
        if search:
            listdebugsNew = [debug for debug in listdebugs if search.lower() in str(debug).lower()]
            return render_template('debugs.html', debugs=listdebugsNew, search=search)
        
        return render_template('debugs.html', debugs=listdebugs, search="")
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route("/remove-debug", methods=['POST'])
def RemoveDebug():
    try:
        p = Persistence()
        
        if not p.validate(): 
            return redirect('/configure')
        
        debug = request.form['debug']
        Command.remove(os.path.join(p.FolderDebugs, debug))
        return redirect('/debug')
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))